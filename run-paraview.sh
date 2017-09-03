#!/bin/bash

PARAVIEW_VERSION=${PARAVIEW_VERSION:-5.4.1}
QT_VERSION=${QT_VERSION:-4.8.7}

case $(hostname -f) in
  *.iter.org) 
	module purge
	# The following modules are needed for IMAS plugins
        module load imas/3.10.1/ual/3.6.0 blitz/0.10 binutils/2.25
        module load OpenSSL/1.0.2g-GCC-4.8.3
        module load Python/2.7.9-goolf-1.5.16 # overwrite Anaconda
	imasdb solps-iter
	imasdb
	;;

  *.marconi.cineca.it) # EU-IM Gateway with CentOS7.2
	. /etc/profile.d.gw/modules.sh
	module load imas/3.9.1/ual/3.5.3 blitz/0.10
	module switch itm-python/2.7.13.b7
	imasdb solps-iter
	imasdb	
	;;
  
  *)
	;;
esac

BUILDROOT=${PWD}
BUILD_DIR=${BUILDROOT}/build
DOWNLOAD_DIR=${DOWNLOAD_DIR:-${BUILDROOT}/download}
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}
#STAGING_DIR=/work/imas/project
STAGING_QT=${STAGING_QT:-${STAGING_DIR}/qt/${QT_VERSION}}
STAGING_PARAVIEW=${STAGING_PARAVIEW:-$STAGING_DIR/paraview/$PARAVIEW_VERSION}

#install -d /tmp/${USER}

LD_LIBRARY_PATH=${STAGING_QT}/lib:${LD_LIBRARY_PATH} ${STAGING_PARAVIEW}/bin/paraview $@

