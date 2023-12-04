# FIX for using pyCRTM with CRTM v2.4.0

## Tutorial


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
