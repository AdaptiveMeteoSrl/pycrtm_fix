
# -*- makefile -*
#
#  Trying to run make manually? You'll need to set the following environment variables.
#  FORT -- Compiler you want (ifort, gfortran, etc)
#  F2PY_COMPILER -- what f2py calls the compiler (gfortran = gnu95, intel = intelem)
#  FCFLAGS -- flags taken for the appropriate compiler (see CRTM "config-setup" directory)
#  ILOC -- path to the CRTM install directory. 
#          The install directory where you find  "lib" (where the libcrtm.a lives) and "include" (where all the *.mod files live)
  ILOC    = CRTM_PATH/crtm
  FCFLAGS = -fimplicit-none -ffree-form -fopenmp -fno-second-underscore -frecord-marker=4 -std=f2008 -fcheck=all
  F2PY = f2py --fcompiler=gnu95 --f90flags='${FCFLAGS}'
  LIB = ${ILOC}/lib
  INC = ${ILOC}/include

MODULE=pycrtm

all: ${MODULE}.so

#Only really need first bit, if you change interface, but do it anyway so you don't forget.
${MODULE}.so: pycrtm.f90
	f2py -m ${MODULE} -h sgnFile.pyf pycrtm.f90 --overwrite-signature
	${F2PY}  -c -L/usr/lib/x86_64-linux-gnu -lnetcdff -lnetcdf -lnetcdf -I/usr/include  -L/usr/lib/x86_64-linux-gnu  -I/usr/include  -L${LIB} -L/usr/lib/x86_64-linux-gnu/hdf5/serial -I/usr/lib/x86_64-linux-gnu/hdf5/serial -lcrtm -lnetcdf -lnetcdff -lhdf5 -lgomp -I${INC} -m ${MODULE} $<  only: wrap_forward wrap_k_matrix
clean:
	${RM} ${MODULE}*.so
