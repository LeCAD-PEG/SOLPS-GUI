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

# Package Variables
VERSION=${VERSION:-4.19.18}
SOURCE="sip-${VERSION}.tar.gz"
DOWNLOAD="https://www.riverbankcomputing.com/static/Downloads/sip/${VERSION}/${SOURCE}"
SRC_DIR=${BUILD_DIR}/sip-${VERSION}
INSTALL_DIR=${STAGING_DIR}/sip/${VERSION}

# Environment dependencies
if [ -e ${BUILDROOT}/package/setup.sh ]; then
    . ${BUILDROOT}/package/setup.sh
fi

# Prepare directories for download and building
install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}

# Download source
if [ ! -f ${DOWNLOAD_DIR}/${SOURCE} ]; then
    wget -O ${DOWNLOAD_DIR}/${SOURCE} --no-check-certificate ${DOWNLOAD}
fi

cd ${BUILD_DIR}

# Unpack sources
if [ ! -d ${SRC_DIR} ]; then
    tar xzf ${DOWNLOAD_DIR}/${SOURCE}
fi

cd ${SRC_DIR}

# Configure
if [ ! -e ${SRC_DIR}/.configured ]; then
    rm -rf ${INSTALL_DIR}
    python3 configure.py --bindir=${INSTALL_DIR}/bin \
        --sip-module=PyQt5.sip \
        --destdir=${INSTALL_DIR}/lib/
    touch ${SRC_DIR}/.configured
fi

# Build
if [ ! -e ${SRC_DIR}/.built ]; then
    make -j${MAKE_JOBS}
    touch ${SRC_DIR}/.built
fi

# Install
if [ ! -d ${INSTALL_DIR} ]; then
    install -d ${INSTALL_DIR}
    make install
fi

# Generate Modulefile
if [ ! -d ${MODULE_DIR}/SIP ]; then
    install -d ${MODULE_DIR}/SIP
fi
cat << EOF > ${MODULE_DIR}/SIP/${VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
    puts stderr { SIP is a tool that makes it very easy to create Python bindings for C and C++ libraries. - Homepage: http://www.riverbankcomputing.com/software/sip/
    }
}

module-whatis {Description: SIP is a tool that makes it very easy to create Python bindings for C and C++ libraries. - Homepage: http://www.riverbankcomputing.com/software/sip/}
if { ![ is-loaded Python/${PYTHON_VERSION} ] } {
    module load Python/${PYTHON_VERSION}
}

conflict SIP
prepend-path PATH               ${INSTALL_DIR}/bin
prepend-path CPATH              ${INSTALL_DIR}/include
prepend-path PYTHONPATH         ${INSTALL_DIR}/lib
EOF








