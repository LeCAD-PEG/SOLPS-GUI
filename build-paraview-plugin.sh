#!/bin/sh -x

MAKE_JOBS=${MAKE_JOBS:-4}
BUILDROOT=$(cd ${0%/*} && echo ${PWD})
BUILD_DIR=${BUILDROOT}/build
PARAVIEW_VERSION=${PARAVIEW_VERSION:-5.4.1}
QT_VERSION=${QT_VERSION:-4.8.7}
DOWNLOAD_DIR=${DOWNLOAD_DIR:-${BUILDROOT}/download}
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}


case $(hostname -f) in
  *.iter.org)
        module purge
        module load imas/3.15.0/ual/3.6.4 blitz/0.10 binutils/2.25
        module load OpenSSL/1.0.2g-GCC-4.8.3
        module unload zlib
        module load Python/2.7.9-goolf-1.5.16 # overwrite Anaconda2
        module load paraview/5.4.1
        module load qt/4.8.7
	export CC=gcc
	export CXX=g++
	MAKE_JOBS=${MAKE_JOBS:-4}
	;;

  *.marconi.cineca.it) # EU-IM Gateway with CentOS7.2
	. /etc/profile.d.gw/modules.sh
	module purge
	module load cineca imasenv/3.12.1 cmake/3.5.2
	module switch itm-python/2.7
	module unload matlab
	QT_VERSION=4.8.7
	module load itm-qt/${QT_VERSION}
	MAKE_JOBS=${MAKE_JOBS:-36}
	;;

  *)
	;;
esac

if test -z "${IMAS_VERSION}" ; then
    echo "Required IMAS module not present"
    exit 2
fi

STAGING_PARAVIEW=${STAGING_PARAVIEW:-\
    ${STAGING_DIR}/paraview/${PARAVIEW_VERSION}}
STAGING_PLUGINS=${STAGING_PLUGINS:-\
    ${STAGING_DIR}/paraview-plugins/${PARAVIEW_VERSION}/${IMAS_VERSION}}


CMAKE_VERSION=${CMAKE_VERSION:-3.10.1}

#Initialize directories

install -d ${BUILD_DIR}
install -d ${DOWNLOAD_DIR}
install -d ${STAGING_DIR}

# We need recent CMAKE for building ParaView 5.x
CMAKE_TEST=$(hash cmake 2> /dev/null && cmake --version \
             | sed -e 's/[^0-9]//g;s/^\(.\{2\}\).*/\1/')
if [ "${CMAKE_TEST}0" -ge 350 ]
 then CMAKE=cmake
 else CMAKE=${STAGING_DIR}/cmake/${CMAKE_VERSION}/bin/cmake
 CMAKE_VERSION=${CMAKE_VERSION} MAKE_JOBS=${MAKE_JOBS} ./build-cmake.sh
fi

set -e

export PKG_CONFIG_PATH=${STAGING_DIR}/qt/${QT_VERSION}/lib/pkgconfig:${PKG_CONFIG_PATH}
export PATH=${STAGING_DIR}/qt/${QT_VERSION}/bin:${PATH}


name=Edge
[ -d ${BUILD_DIR}/Plugins-ReadUAL${name} ] && rm ${BUILD_DIR}/Plugins-ReadUAL${name}/CMakeCache.txt
install -d ${BUILD_DIR}/Plugins-ReadUAL${name}
install -d ${STAGING_PLUGINS}
cd ${BUILD_DIR}/Plugins-ReadUAL${name}
PATH=${STAGING_DIR}/bin:${PATH} \
 ${CMAKE} -DCMAKE_BUILD_TYPE:STRING=Debug \
    -DCMAKE_INSTALL_PREFIX:PATH=${STAGING_PARAVIEW} \
    -DParaView_DIR:PATH=${STAGING_PARAVIEW} \
    ${BUILDROOT}/src/plugins/paraview
make -j ${MAKE_JOBS} VERBOSE=1 all
install -d ${STAGING_PLUGINS}
install ${BUILD_DIR}/Plugins-ReadUAL${name}/libReadUAL${name}.so \
	${STAGING_PLUGINS}

