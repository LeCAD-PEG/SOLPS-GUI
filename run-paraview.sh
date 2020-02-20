#!/bin/bash

QT_VERSION=${QT_VERSION:-4.8.7}
BUILDROOT=${PWD}
BUILD_DIR=${BUILDROOT}/build
DOWNLOAD_DIR=${DOWNLOAD_DIR:-${BUILDROOT}/download}
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}

case $(hostname -f) in
  *.iter.org)
    PARAVIEW_VERSION=${PARAVIEW_VERSION:-5.5.2}
    PARAVIEW_MAINVERSION=${PARAVIEW_VERSION%.*}
	module purge
	# The following modules are needed for IMAS plugins
    module load IMAS/3.26.0-4.5.0
    module load ParaView/5.5.2-intel-2018a-Python-3.6.4-mpi
	imasdb solps-iter
	imasdb
    paraview
	;;

  *.marconi.cineca.it) # EU-IM Gateway with CentOS7.2

    PARAVIEW_VERSION=${PARAVIEW_VERSION:-5.4.1}
    PARAVIEW_MAINVERSION=${PARAVIEW_VERSION%.*}
	. /etc/profile.d.gw/modules.sh
	module load cineca imasenv cmake/3.5.2 blitz/0.10
	module unload matlab
	module switch itm-python/2.7
	imasdb solps-iter
	imasdb
	;;

  *)
    PARAVIEW_VERSION=${PARAVIEW_VERSION:-5.6.2}
    PARAVIEW_MAINVERSION=${PARAVIEW_VERSION%.*}
    module load imas/3.26.0/solps
    module load ParaView/5.6.2
    module load paraview-plugin-edge/1.5
    paraview
	;;
esac


