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
VERSION=${VERSION:-0.0.94}
GIT="ssh://git@git.iter.org/lib/gr-software.git"
SRC_DIR="${BUILD_DIR}/gr-${VERSION}"
INSTALL_DIR=${STAGING_DIR}/GR/${VERSION}


# Environment dependencies
case $(hostname -f) in
    *)
esac

# Prepare directories for download and building
install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}

# Download source

# Unpack sources
if [ ! -d ${SRC_DIR} ]; then
    git clone --branch ${VERSION} --single-branch ${GIT} ${SRC_DIR}
fi

cd ${SRC_DIR}

# Configure

# Build
if [ ! -e ${SRC_DIR}/.built ]; then
    SOLPS_LIB=${INSTALL_DIR}/lib BLDFLAG="ar cr" RANLIB=echo CFLAGS="-fPIC" \
    F77=gfortran \
    make libgr.a
    touch ${SRC_DIR}/.built
fi

# Install
if [ ! -d ${INSTALL_DIR} ]; then
    install -d ${INSTALL_DIR}/lib
    SOLPS_LIB=${INSTALL_DIR}/lib BLDFLAG="ar cr" RANLIB=echo CFLAGS="-fPIC" \
    F77=gfortran \
    make install
fi

# Generate Modulefile
if [ ! -d ${MODULE_DIR}/gr ]; then
	install -d ${MODULE_DIR}/GR
fi

cat << EOF > ${MODULE_DIR}/GR/${VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
    puts stderr {

Description
===========
GR is a universal framework for cross-platform visualization applications.
 It offers developers a compact, portable and consistent graphics library for their programs.
 Applications range from publication quality 2D graphs to the representation of complex 3D scenes.


More information
================
 - Homepage: https://gr-framework.org/index.html
    }
}

module-whatis {Description:
 GR is a universal framework for cross-platform visualization applications.
 It offers developers a compact, portable and consistent graphics library for their programs.
 Applications range from publication quality 2D graphs to the representation of complex 3D scenes.
}
module-whatis {Homepage: https://gr-framework.org/index.html}

conflict GR
prepend-path LD_LIBRARY_PATH    ${INSTALL_DIR}/lib
prepend-path LIBRARY_DIR        ${INSTALL_DIR}/lib
EOF