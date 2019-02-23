#!/bin/sh -x
set -e
BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD%/package})}
BUILD_DIR=${BUILDROOT}/build
DOWNLOAD_DIR=${BUILDROOT}/download
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}
LIBXML2_VERSION=${LIBXML2_VERSION:-2.9.1}
PYTHON_VERSION=${PYTHON_VERSION:-3.6.8}
LIBXML2_INSTALL_DIR=${STAGING_DIR}/libxml2/${LIBXML2_VERSION}
PYTHON_INSTALL_DIR=${STAGING_DIR}/Python/${PYTHON_VERSION}

MAKE_JOBS=${MAKE_JOBS:-$(nproc)}

install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}
install -d ${LIBXML2_INSTALL_DIR}

LIBXML2_SRC="libxml2-${LIBXML2_VERSION}.tar.gz"
LIBXML2_SITE="ftp://xmlsoft.org/libxml2" # Using FTP site, to avoid using
                                         # autoconf tools on the github release
LIBXML2_DOWNLOAD="${LIBXML2_SITE}/libxml2-${LIBXML2_VERSION}.tar.gz"

if [ ! -f ${DOWNLOAD_DIR}/${LIBXML2_SRC} ]; then
    wget  -O ${DOWNLOAD_DIR}/${LIBXML2_SRC} ${LIBXML2_DOWNLOAD}
fi

LIBXML2_SRC_DIR="${BUILD_DIR}/libxml2-${LIBXML2_VERSION}"
if [ ! -e ${LIBXML2_SRC_DIR}/.built ]; then
    rm -rf ${LIBXML2_SRC_DIR}
    cd ${BUILD_DIR}
    tar xzf ${DOWNLOAD_DIR}/${LIBXML2_SRC}
    cd ${LIBXML2_SRC_DIR}
    PATH=${STAGING_DIR}/Python/bin:${PATH} \
    PYTHONPATH=${PYTHON_INSTALL_DIR}/lib/python${PYTHON_MAINVERSION}/site-packages \
    LD_LIBRARY_PATH=${STAGING_DIR}/Python/lib:${LD_LIBRARY_PATH} \
    ./configure --with-python=${PYTHON_INSTALL_DIR} \
      --prefix=${LIBXML2_INSTALL_DIR} LDFLAGS=-L${STAGING_DIR}/lib
    make -j${MAKE_JOBS}
    make install
    # Not sure if python bindings needed
    # cd python
    # CFLAGS=-I${LIBXML2_SRC_DIR}/include ${STAGING_DIR}/bin/python3 setup.py build
    # CFLAGS=-I${LIBXML2_SRC_DIR}/include ${STAGING_DIR}/bin/python3 setup.py install
    touch .built
fi

# Generate Modulefile
MODULE_DIR=${MODULE_DIR:-${BUILDROOT}/modules}
if [ ! -d ${MODULE_DIR}/libxml2 ]; then
	install -d ${MODULE_DIR}/libxml2
fi

cat << EOF > ${MODULE_DIR}/libxml2/${LIBXML2_VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
puts stderr "\tThis module sets the environment for libxml2 v${LIBXML2_VERSION}"
}

module-whatis "Libxml2 is the XML C parser and toolkit developed for the Gnome project (but usable outside of the Gnome platform). (v${LIBXML2_VERSION}"

conflict libxml2

if { ![ is-loaded Python/${PYTHON_VERSION} ] } {
    module load Python/${PYTHON_VERSION}
}

prepend-path PATH  					${LIBXML2_INSTALL_DIR}/bin
prepend-path CPATH 					${LIBXML2_INSTALL_DIR}/include
prepend-path LD_LIBRARY_PATH		${LIBXML2_INSTALL_DIR}/lib
prepend-path PKG_CONFIG_PATH		${LIBXML2_INSTALL_DIR}/lib/pkgconfig
EOF