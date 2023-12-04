# FIX for using pyCRTM with CRTM v2.4.0

This repository contains a fix for using the pyCRTM wrapper (https://github.com/karpob/pycrtm) having CRTM version 2.4.0 installed (https://github.com/JCSDA/crtm). The fix consists of a configuration file to compile CRTM and a Makefile to compile the pyCRTM shared library. The software has been installed under several Ubuntu distributions.

<br/><br/>

## Tutorial

 1. Install CRTM following the tutorial and configuring the setup as in gfortran.setup;
 2. Link or rename CRTM installation path to a directory called crtm and then configure the Makefile in pycrtm as in the given example;
 3. Create pycrtm librarary with:
    
              make clean
              make
 4. Link CRTM coefficients inside the installation path in a directory called '*crtm_coef*';
 5. Copy test_sensor.py in testCases and run it to test pyCRTM.


## File description

<br/><br/>
- *gfortran.setup* - Configuration file for CRTM setup. The additional flag '-fPIC' has been added to FCFLAGS.
                   HDF5 and NetCDF4 libraries were installed through:
  
                            sudo apt-get install libhdf5-dev
                            sudo apt-get install libnetcdf-dev
                            sudo apt-get install libnetcdff-dev

<br/><br/>
- *Makefile* - Makefile for the creation of the pycrtm shared object. It must be in the pycrtm clone path.
               The variable CRTM_LIB contained this file should be replaced with the path to a directory containing your CRTM installation in a directory called crtm.
               As an example, the default installation procedure of CRTM v2.4.0 create the directory *MYPATH/src/Build/crtm_v2.4.0_alpha*. It should be renamed (or symbolically linked) *crtm*,
               so the Makefile will contain the line

                            ILOC = MYPATH/src/Build/crtm

<br/><br/>
- *test_sensor.py* - Test pycrtm (default 4 cases) 
   usage test_sensor.py [-h] --sensor_id SENSOR_ID
        optional arguments:
          -h, --help            show this help message and exit
          --sensor_id SENSOR_ID
                                Sensor ID (i.e. cris_npp)
