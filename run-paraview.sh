#!/bin/bash

PARAVIEW_VERSION=${PARAVIEW_VERSION:-5.3.0}
QT_VERSION=${QT_VERSION:-4.8.7}

case $(hostname -f) in
  *.iter.org) 
	module purge
	# module load MVAPICH2/2.2b-GCC-4.9.3-2.25 python/2.7/11
	# module load GCC/4.8.3
	# The following modules are needed for IMAS plugins
	module load imas/3.9.1/ual/3.5.3 blitz/0.10
  module load python/2.7/11
	imasdb solps-iter
	imasdb
	;;

  *.marconi.cineca.it) # EU-IM Gateway with CentOS7.2
	. /etc/profile.d.gw/modules.sh
	module load imas/3.7.4/ual/3.4.0 blitz/0.10
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

install -d /tmp/${USER}

LD_LIBRARY_PATH=${STAGING_QT}/lib:${LD_LIBRARY_PATH} ${STAGING_PARAVIEW}/bin/paraview $@

