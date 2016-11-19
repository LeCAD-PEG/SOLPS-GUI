#!/bin/sh -x

MAKE_JOBS=${MAKE_JOBS:-4}
BUILDROOT="${PWD}"
BUILD_DIR="${BUILDROOT}/build"
PARAVIEW_VERSION=${PARAVIEW_VERSION:-5.1.2}
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}
STAGING_PARAVIEW="${STAGING_DIR}/paraview/${PARAVIEW_VERSION}"
STAGING_PLUGINS="${STAGING_DIR}/paraview-plugins/${PARAVIEW_VERSION}/${IMAS_VERSION}"


case $(hostname) in
  *.iter.org) 
	module purge
	module load imas/3.7.0/ual/3.3.13 blitz/0.10 binutils/2.25
	export CC=gcc
	export CXX=g++
	MAKE_JOBS=${MAKE_JOBS:-8}
	;;
  *)
	;;
esac

if test -z "${IMAS_VERSION}" ; then
    echo "Required IMAS module not present"
    exit 2
fi


set -e

name=Edge
install -d ${BUILD_DIR}/Plugins-ReadUAL${name}
install -d ${STAGING_PLUGINS}
cd ${BUILD_DIR}/Plugins-ReadUAL${name}
PATH=${STAGING_DIR}/bin:${PATH} \
 cmake -DCMAKE_BUILD_TYPE:STRING=Debug \
    -DCMAKE_INSTALL_PREFIX:PATH=${STAGING_PARAVIEW} \
    -DParaView_DIR:PATH=${STAGING_PARAVIEW} \
    ${BUILDROOT}/src/plugins/paraview 
make -j ${MAKE_JOBS} VERBOSE=1 all
install -d ${STAGING_PLUGINS}
install ${BUILD_DIR}/Plugins-ReadUAL${name}/libReadUAL${name}.so \
	${STAGING_PLUGINS}

