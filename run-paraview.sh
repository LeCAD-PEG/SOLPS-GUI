#!/bin/sh -x

PARAVIEW_VERSION=${PARAVIEW_VERSION:-5.1.2}
QT_VERSION=${QT_VERSION:-4.8.7}

case $(hostname) in
  *.iter.org) 
	module purge
	module load MVAPICH2/2.2b-GCC-4.9.3-2.25  python/2.7/11

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

