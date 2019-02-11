#!/bin/sh -x

CMAKE_VERSION=${CMAKE_VERSION:-3.10.1}

case $(hostname -f) in
  *.iter.org)
	module purge
	module load GCC/4.8.3 binutils/2.25
	module load OpenSSL/1.0.2g-GCC-4.8.3
	export CC=gcc
	export CXX=g++
        CMAKE_EXTRA_FLAGS=${CMAKE_EXTRA_FLAGS:-\
          -DCMAKE_EXE_LINKER_FLAGS:STRING=-L${EBROOTOPENSSL}/lib}
	MAKE_JOBS=${MAKE_JOBS:-8}
	;;
  *)
	;;
esac

MAKE_JOBS=${MAKE_JOBS:-4}

BUILDROOT=$(cd ${0%/*} && echo ${PWD})
BUILD_DIR=${BUILDROOT}/build
DOWNLOAD_DIR=${DOWNLOAD_DIR:-${BUILDROOT}/download}
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}
CMAKE_INSTALL_DIR=${CMAKE_INSTALL_DIR:-${STAGING_DIR}/cmake/${CMAKE_VERSION}}

#Initialize directories

install -d ${BUILD_DIR}
install -d ${DOWNLOAD_DIR}
install -d ${STAGING_DIR}

set -e

# Install cmake as needed
CMAKE_SRC_DIR="${BUILD_DIR}/cmake-${CMAKE_VERSION}"
if ! test -e  ${CMAKE_SRC_DIR}/.built ; then
  CMAKE_SRC="cmake-${CMAKE_VERSION}.tar.gz"
  CMAKE_MAIN_VERSION=${CMAKE_VERSION%.*}
  CMAKE_SITE="https://cmake.org/files/v${CMAKE_MAIN_VERSION}"
  CMAKE_DOWNLOAD="${CMAKE_SITE}/cmake-${CMAKE_VERSION}.tar.gz"
  if [ ! -f ${DOWNLOAD_DIR}/${CMAKE_SRC} ]; then
     wget  -O ${DOWNLOAD_DIR}/${CMAKE_SRC} --no-check-certificate \
	 ${CMAKE_DOWNLOAD}
  fi
  rm -rf ${CMAKE_SRC_DIR}
  cd ${BUILD_DIR}
  tar xzf ${DOWNLOAD_DIR}/${CMAKE_SRC}
  cd ${CMAKE_SRC_DIR}
  ./bootstrap --prefix=${CMAKE_INSTALL_DIR} -- ${CMAKE_EXTRA_FLAGS}
  make -j ${MAKE_JOBS} VERBOSE=1
  make install
  touch ${CMAKE_SRC_DIR}/.built
fi




