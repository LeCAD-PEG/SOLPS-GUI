#!/bin/bash

PARAVIEW_VERSION=${PARAVIEW_VERSION:-5.4.1}
QT_VERSION=${QT_VERSION:-4.8.7}

case $(hostname -f) in
  *.iter.org) 
	module purge
	# The following modules are needed for IMAS plugins
	module load IMAS/3.21.0-3.8.6 binutils/2.28-GCCcore-6.4.0 Blitz++/0.10-GCCcore-6.4.0
	imasdb solps-iter
	imasdb
	;;

  *.marconi.cineca.it) # EU-IM Gateway with CentOS7.2
	. /etc/profile.d.gw/modules.sh
	module load cineca imasenv cmake/3.5.2 blitz/0.10
	module unload matlab
	module switch itm-python/2.7
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

LD_LIBRARY_PATH=${STAGING_QT}/lib:${LD_LIBRARY_PATH} \
${STAGING_PARAVIEW}/bin/paraview $@

