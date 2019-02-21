#!/bin/bash

PARAVIEW_VERSION=${PARAVIEW_VERSION:-5.4.1}
PARAVIEW_MAINVERSION=${PARAVIEW_VERSION%.*}

QT_VERSION=${QT_VERSION:-4.8.7}
BUILDROOT=${PWD}
BUILD_DIR=${BUILDROOT}/build
DOWNLOAD_DIR=${DOWNLOAD_DIR:-${BUILDROOT}/download}
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}




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
	export IMAS_VERSION=3.21.0
	export UAL_VERSION=3.8.4
	MDSPLUS_VERSION=stable_release-7-7-8
	export LD_LIBRARY_PATH=${STAGING_DIR}/qt/${QT_VERSION}/lib:${LD_LIBRARY_PATH}
	export LD_LIBRARY_PATH=${STAGING_DIR}/mdsplus/${MDSPLUS_VERSION}/lib:${LD_LIBRARY_PATH}
	export LD_LIBRARY_PATH=${STAGING_DIR}/access-layer/${UAL_VERSION}/lib:${LD_LIBRARY_PATH}
	export LD_LIBRARY_PATH=${STAGING_DIR}/lib:${LD_LIBRARY_PATH}
	export LD_LIBRARY_PATH=${STAGING_DIR}/paraview/${PARAVIEW_VERSION}/lib/paraview-${PARAVIEW_MAINVERSION}:${LD_LIBRARY_PATH}
	export ids_path=${STAGING_DIR}/access-layer/${UAL_VERSION}/models/mdsplus
	;;
esac

#STAGING_DIR=/work/imas/project
STAGING_PARAVIEW=${STAGING_PARAVIEW:-$STAGING_DIR/paraview/$PARAVIEW_VERSION}

#install -d /tmp/${USER}

${STAGING_PARAVIEW}/bin/paraview $@

