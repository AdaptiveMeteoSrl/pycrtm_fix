#!/usr/bin/env python3
import configparser
import os, h5py, sys
import numpy as np
from matplotlib import pyplot as plt

thisDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(thisDir)
sys.path.insert(0,parentDir)
from pyCRTM import pyCRTM, profilesCreate

def main(coefficientPath, sensor_id):
    thisDir = os.path.dirname(os.path.abspath(__file__))
    cases = os.listdir( os.path.join(thisDir,'data') )
    cases.sort()
    # create 4 profiles for each of the 4 cases
    profiles = profilesCreate( 4, 92 )
    storedTb = []
    storedEmis = []
    # populate the cases, and previously calculated Tb from crtm test program.    
    for i,c in enumerate(cases):
        h5 = h5py.File(os.path.join(thisDir,'data',c) , 'r')
        profiles.Angles[i,0] = h5['zenithAngle'][()]
        profiles.Angles[i,1] = 999.9 
        profiles.Angles[i,2] = 100.0  # 100 degrees zenith below horizon.
        profiles.Angles[i,3] = 0.0 # zero solar azimuth 
        profiles.Angles[i,4] = h5['scanAngle'][()]
        profiles.DateTimes[i,0] = 2001
        profiles.DateTimes[i,1] = 1
        profiles.DateTimes[i,2] = 1
        profiles.Pi[i,:] = np.asarray(h5['pressureLevels'] )
        profiles.P[i,:] = np.asarray(h5['pressureLayers'][()])
        profiles.T[i,:] = np.asarray(h5['temperatureLayers'])
        profiles.Q[i,:] = np.asarray(h5['humidityLayers'])
        profiles.O3[i,:] = np.asarray(h5['ozoneConcLayers'])
        profiles.clouds[i,:,0,0] = np.asarray(h5['cloudConcentration'])
        profiles.clouds[i,:,0,1] = np.asarray(h5['cloudEffectiveRadius'])
        profiles.aerosols[i,:,0,0] = np.asarray(h5['aerosolConcentration'])
        profiles.aerosols[i,:,0,1] = np.asarray(h5['aerosolEffectiveRadius'])
        profiles.aerosolType[i] = h5['aerosolType'][()]
        profiles.cloudType[i] = h5['cloudType'][()]
        profiles.cloudFraction[i,:] = h5['cloudFraction'][()]
        profiles.climatology[i] = h5['climatology'][()]
        profiles.surfaceFractions[i,:] = h5['surfaceFractions']
        profiles.surfaceTemperatures[i,:] = h5['surfaceTemperatures']
        profiles.S2m[i,1] = 33.0 # just use salinity out of S2m for the moment.
        profiles.windSpeed10m[i] = 5.0
        profiles.LAI[i] = h5['LAI'][()]
        profiles.windDirection10m[i] = h5['windDirection10m'][()]
        # land, soil, veg, water, snow, ice
        profiles.surfaceTypes[i,0] = h5['landType'][()]
        profiles.surfaceTypes[i,1] = h5['soilType'][()]
        profiles.surfaceTypes[i,2] = h5['vegType'][()]
        profiles.surfaceTypes[i,3] = h5['waterType'][()]
        profiles.surfaceTypes[i,4] = h5['snowType'][()]
        profiles.surfaceTypes[i,5] = h5['iceType'][()]
        storedTb.append(np.asarray(h5['Tb']))
        storedEmis.append(np.asarray(h5['emissivity_atms']))
        h5.close()

    crtmOb = pyCRTM()
    crtmOb.profiles = profiles
    crtmOb.coefficientPath = pathInfo['CRTM']['coeffs_dir']
    crtmOb.sensor_id = sensor_id
    crtmOb.nThreads = 4
    crtmOb.output_tb_flag = False # Radiance in output
    crtmOb.loadInst()

    crtmOb.runDirect()
    forwardTb = crtmOb.Bt
    forwardEmissivity = crtmOb.surfEmisRefl[0,:]
    crtmOb.surfEmisRefl = []

    crtmOb.runK()
    kTb = crtmOb.Bt
    kEmissivity = crtmOb.SurfEmisK

    try:
      if ( all( np.abs( forwardTb.flatten() - np.asarray(storedTb).flatten() ) <= 1e-5)  and all( np.abs( kTb.flatten() - np.asarray(storedTb).flatten() ) <= 1e-5) ):
          print("Yay! all values are close enough to what CRTM test program produced!")
      else: 
          print("Boo! something failed. Look at cris plots")
    except:
        pass

    #wavenumbers[0:4,:] = np.linspace(1,1306,1305)
    wavenumbers        = np.zeros((4,crtmOb.Wavenumbers.size))
    wavenumbers[0:4,:] = np.array(crtmOb.Wavenumbers)
	
    plt.figure()
    plt.plot(wavenumbers.T,forwardTb.T ) 
    plt.legend(['1','2','3','4'])
    plt.xlabel('Wavenumber $[cm^{-1}]$',weight='bold',size=13)
    plt.legend(['1','2','3','4'], title = 'Test')
    plt.ylabel('Radiance $[mW/ster/m^2/cm^{-1}]$',weight='bold',size=13)

    plt.savefig(os.path.join(thisDir,sensor_id+'_spectrum_forward.png'))
    print("Saved "+os.path.join(thisDir,sensor_id+'_spectrum_forward.png'))

    plt.figure()
    plt.plot(wavenumbers.T,forwardEmissivity.T)
    plt.xlabel('Wavenumber $[cm^{-1}]$',weight='bold',size=13)
    plt.ylabel('Surface Emissivity',weight='bold',size=13)
    plt.legend(['1','2','3','4'], title = 'Test')

    plt.savefig(os.path.join(thisDir,sensor_id+'_emissivity_forward.png'))
    print("Saved "+os.path.join(thisDir,sensor_id+'_emissivity_forward.png')) 
    
    plt.figure()
    plt.plot(wavenumbers.T,kEmissivity.T)
    plt.xlabel('Wavenumber $[cm^{-1}]$',weight='bold',size=13)
    plt.ylabel('Surface Emissivity K',weight='bold',size=13)
    plt.legend(['1','2','3','4'], title = 'Test')
    plt.savefig(os.path.join(thisDir,sensor_id+'_emissivity_k.png')) 
    print("Saved "+os.path.join(thisDir,sensor_id+'_emissivity_k.png')) 

    fig, axs = plt.subplots(nrows=4,figsize=(12,5),sharex=False)
    for i in range(4):
       axs[i].imshow(crtmOb.TK[i,:,:].T, cmap = 'viridis',extent=[wavenumbers.min(),wavenumbers.max(),0,crtmOb.TK[i,:,:].T.shape[0] - 1])
       axs[i].set_ylabel('Level',weight='bold')
       axs[i].set_title('T Jacobian | Test: '+repr(i+1))
    plt.xlabel('Wavenumber $[cm^{-1}]$',weight='bold',size=13)
    plt.savefig(os.path.join(thisDir,sensor_id+'_T_k.png'),bbox_inches='tight',dpi=300)
    print("Saved "+os.path.join(thisDir,sensor_id+'_T_k.png'))

    return


def parser():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--sensor_id', type=str,required=True,
                    help='Sensor ID')
    return parser.parse_args()

if __name__ == "__main__":
    
    args = parser()
    pathInfo = configparser.ConfigParser()
    pathInfo.read( os.path.join(parentDir,'crtm.cfg') ) 
    coefficientPath = pathInfo['CRTM']['coeffs_dir']
    sensor_id = args.sensor_id
    main(coefficientPath, sensor_id)