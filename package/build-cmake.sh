#!/bin/sh -x
set -e


# Variables
BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD%/package})}
MAKE_JOBS=${MAKE_JOBS:-$(nproc)}

# Buildroot directories
MODULE_DIR=${MODULE_DIR:-${BUILDROOT}/modules}
BUILD_DIR=${BUILDROOT}/build
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}
DOWNLOAD_DIR=${BUILDROOT}/download

# Package variables
VERSION=${VERSION:-3.10.1}
MAIN_VERSION=${VERSION%.*}
SOURCE="cmake-${VERSION}.tar.gz"
DOWNLOAD="https://cmake.org/files/v${CMAKE_MAIN_VERSION}/cmake-${VERSION}.tar.gz"
SRC_DIR="${BUILD_DIR}/cmake-${VERSION}"
INSTALL_DIR=${STAGING_DIR}/cmake/${VERSION}

# Environment dependencies
case $(hostname -f) in
    *.iter.org)
        module purge
        module load GCC/4.8.3 binutils/2.25
        module load OpenSSL/1.0.2g-GCC-4.8.3
        export CC=gcc
        export CXX=g++
        CMAKE_EXTRA_FLAGS=${CMAKE_EXTRA_FLAGS:-\
        -DCMAKE_EXE_LINKER_FLAGS:STRING=-L${EBROOTOPENSSL}/lib}
        MAKE_JOBS=8
        ;;
    *)
        ;;
esac

# Prepare directories for download and building
install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}

# Download source
if [ ! -f ${DOWNLOAD_DIR}/${SOURCE} ]; then
    wget -O ${DOWNLOAD_DIR}/${SOURCE} ${DOWNLOAD}
fi

cd ${BUILD_DIR}

# Unpack sources
if [ ! -d ${SRC_DIR} ]; then
    tar xzf ${DOWNLOAD_DIR}/${SOURCE}
fi

cd ${SRC_DIR}

# Configure
if [ ! -e ${SRC_DIR}/.configured ]; then
    ./bootstrap --prefix=${INSTALL_DIR} -- ${CMAKE_EXTRA_FLAGS}
    touch ${SRC_DIR}/.configured
fi

# Build
if [ ! -e ${SRC_DIR}/.built ]; then
    make -j${MAKE_JOBS} VERBOSE=1
    touch ${SRC_DIR}/.built
fi

# Install
if [ ! -d ${INSTALL_DIR} ]; then
    install -d ${INSTALL_DIR}
    make install
fi


# Generate Modulefile
if [ ! -d ${MODULE_DIR}/cmake ]; then
    install -d ${MODULE_DIR}/cmake
fi

cat << EOF > ${MODULE_DIR}/cmake/${VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
puts stderr "\tThis module sets the environment for cmake v${VERSION}"
}
module-whatis "CMake is an open-source, cross-platform family of tools designed to build, test and package software. (v${VERSION}"

conflict cmake
prepend-path PATH               ${INSTALL_DIR}/bin
EOF