#!/bin/sh -x
set -e
BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD%/package})}
BUILD_DIR=${BUILDROOT}/build
DOWNLOAD_DIR=${BUILDROOT}/download
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}
MDSPLUS_VERSION=${MDSPLUS_VERSION:-stable_release-7-7-8}
LIBXML2_VERSION=${LIBXML2_VERSION:-2.9.1}
MDSPLUS_INSTALL_DIR=${STAGING_DIR}/mdsplus/${MDSPLUS_VERSION}
LIBXML2_INSTALL_DIR=${STAGING_DIR}/libxml2/${LIBXML2_VERSION}

MAKE_JOBS=${MAKE_JOBS:-$(nproc)}

install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}
install -d ${MDSPLUS_INSTALL_DIR}

MDSPLUS_SOURCE="mdsplus-${MDSPLUS_VERSION}.tar.gz"
MDSPLUS_DOWNLOAD="https://github.com/MDSplus/mdsplus/archive/${MDSPLUS_VERSION}.tar.gz"

if [ ! -f ${DOWNLOAD_DIR}/${MDSPLUS_SOURCE} ]; then
    wget -O ${DOWNLOAD_DIR}/${MDSPLUS_SOURCE} ${MDSPLUS_DOWNLOAD}
fi

MDSPLUS_SRC_DIR="${BUILD_DIR}/mdsplus-${MDSPLUS_VERSION}"
if [ ! -e ${MDSPLUS_SRC_DIR}/.built ]; then
    rm -rf ${MDSPLUS_SRC_DIR}
    cd ${BUILD_DIR}
    tar xzf ${DOWNLOAD_DIR}/${MDSPLUS_SOURCE}
    cd ${MDSPLUS_SRC_DIR}
    LD_LIBRARY_PATH=${LIBXML2_INSTALL_DIR}/lib \
    CFLAGS=-I${MDSPLUS_INSTALL_DIR}/include/libxml2 \
    LDFLAGS=-lpthread \
    ./configure --prefix=${MDSPLUS_INSTALL_DIR} \
                --enable-shared --disable-doxygen-doc \
                --disable-xmltest --with-xml-prefix=${LIBXML2_INSTALL_DIR} \
                --without-labview
    make all # Errors with jobs > 1
    make install
    touch ${MDSPLUS_SRC_DIR}/.built
fi

# Generate Modulefile
MODULE_DIR=${MODULE_DIR:-${BUILDROOT}/modules}
if [ ! -d ${MODULE_DIR}/MDSplus ]; then
	install -d ${MODULE_DIR}/MDSplus
fi

cat << EOF > ${MODULE_DIR}/MDSplus/${MDSPLUS_VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
    puts stderr {

Description
===========
MDSplus is a set of software tools for data acquisition and storage and a methodology
 for management of complex scientific data.


More information
================
 - Homepage: http://mdsplus.org/
    }
}

module-whatis {Description: MDSplus is a set of software tools for data acquisition and storage and a methodology
 for management of complex scientific data.}
module-whatis {Homepage: http://mdsplus.org/}

conflict MDSplus

if { ![ is-loaded libxml2/${LIBXML2_VERSION} ] } {
    module load libxml2/${LIBXML2_VERSION}
}

prepend-path CPATH              ${MDSPLUS_INSTALL_DIR}/include
prepend-path LD_LIBRARY_PATH    ${MDSPLUS_INSTALL_DIR}/lib
prepend-path LIBRARY_DIR        ${MDSPLUS_INSTALL_DIR}/lib
prepend-path PATH               ${MDSPLUS_INSTALL_DIR}/bin
EOF