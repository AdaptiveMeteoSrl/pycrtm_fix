# pycrtm_fix
- gfortran.setup - Configuration file for CRTM setup. The additional flag '-fPIC' has been added to FCFLAGS.
                   HDF5 and NetCDF4 libraries were installed through
  
                            sudo apt-get install libhdf5-dev
                            sudo apt-get install libnetcdf-dev
                            sudo apt-get install libnetcdff-dev


- test_sensor.py - Test pycrtm (default 4 cases) 
   usage test_sensor.py [-h] --sensor_id SENSOR_ID
        optional arguments:
          -h, --help            show this help message and exit
          --sensor_id SENSOR_ID
                                Sensor ID (i.e. cris_npp)
