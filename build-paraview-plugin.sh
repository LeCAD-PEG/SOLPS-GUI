#!/bin/sh -x

MAKE_JOBS=${MAKE_JOBS:-4}
BUILDROOT="${PWD}"
BUILD_DIR="${BUILDROOT}/build"
PARAVIEW_VERSION=${PARAVIEW_VERSION:-5.4.1}
QT_VERSION=${QT_VERSION:-4.8.7}
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}
STAGING_PARAVIEW="${STAGING_DIR}/paraview/${PARAVIEW_VERSION}"
STAGING_PLUGINS="${STAGING_DIR}/paraview-plugins/${PARAVIEW_VERSION}/${IMAS_VERSION}"


case $(hostname -f) in
  *.iter.org) 
	module purge
        module load imas/3.10.1/ual/3.6.0 blitz/0.10 binutils/2.25
        module load OpenSSL/1.0.2g-GCC-4.8.3
        module load Python/2.7.9-goolf-1.5.16 # overwrite Anaconda
	export CC=gcc
	export CXX=g++
	MAKE_JOBS=${MAKE_JOBS:-4}
	;;

  *.marconi.cineca.it) # EU-IM Gateway with CentOS7.2
	. /etc/profile.d.gw/modules.sh
	module load imas/3.9.1/ual/3.5.3
	MAKE_JOBS=${MAKE_JOBS:-36}
	export CXXFLAGS=-fpermissive
	;;
  
  *)
	;;
esac

if test -z "${IMAS_VERSION}" ; then
    echo "Required IMAS module not present"
    exit 2
fi

export PKG_CONFIG_PATH=${STAGING_DIR}/qt/${QT_VERSION}/lib/pkgconfig:${PKG_CONFIG_PATH}
export PATH=${STAGING_DIR}/qt/${QT_VERSION}/bin:${PATH}

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

