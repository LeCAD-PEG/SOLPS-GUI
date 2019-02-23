#!/bin/sh -x
set -e
GLI_VERSION=${GLI_VERSION:-4.5.30}


case $(hostname -f) in
    *)
esac

MAKE_JOBS=${MAKE_JOBS:-$(nproc)} # Should use all threads of a system


BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD%/package})}
BUILD_DIR=${BUILDROOT}/build
DOWNLOAD_DIR=${BUILDROOT}/download
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}
GLI_INSTALL_DIR=${STAGING_DIR}/GLI/${GLI_VERSION}

GLI_SOURCE="gli-${GLI_VERSION}.tar.gz"
GLI_DOWNLOAD="http://iffwww.iff.kfa-juelich.de/gli/gli-${GLI_VERSION}.tar.gz"


install -d ${BUILD_DIR}
install -d ${DOWNLOAD_DIR}
install -d ${STAGING_DIR}
install -d ${GLI_INSTALL_DIR}


if [ ! -f ${DOWNLOAD_DIR}/${GLI_SOURCE} ]; then
    wget -O ${DOWNLOAD_DIR}/${GLI_SOURCE} ${GLI_DOWNLOAD}
fi

GLI_SRC_DIR="${BUILD_DIR}/gli"
if [ ! -e ${GLI_SRC_DIR}/.built ]; then
    rm -rf ${GLI_SRC_DIR}
    cd ${BUILD_DIR}
    tar xzf ${DOWNLOAD_DIR}/${GLI_SOURCE}
    cd gli/src
    ./configure CFLAGS="-DUSE_INTERP_RESULT"
    make # Fails if j > 1
    make install DESTDIR=${GLI_INSTALL_DIR}
    touch ${GLI_SRC_DIR}/.built
fi

# Generate Modulefile
MODULE_DIR=${MODULE_DIR:-${BUILDROOT}/modules}
if [ ! -d ${MODULE_DIR}/GLI ]; then
	install -d ${MODULE_DIR}/GLI
fi

cat << EOF > ${MODULE_DIR}/GLI/${GLI_VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
    puts stderr {

Description
===========
Graphics Language Interpreter


More information
================
 - Homepage: http://iffwww.iff.kfa-juelich.de/gli/
    }
}
module-whatis {Description: Graphics Language Interpreter}
module-whatis {Homepage: http://iffwww.iff.kfa-juelich.de/gli/}

conflict GLI
prepend-path PATH               ${GLI_INSTALL_DIR}
prepend-path LD_LIBRARY_PATH    ${GLI_INSTALL_DIR}/lib
setenv       GLI_HOME ${GLI_INSTALL_DIR}
EOF