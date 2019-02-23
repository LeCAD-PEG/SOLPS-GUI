#!/bin/sh -x
set -e
MSCL_VERSION=${MSCL_VERSION:-1.1.1}


case $(hostname -f) in
    *)
esac

MAKE_JOBS=${MAKE_JOBS:-$(nproc)} # Should use all threads of a system


BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD%/package})}
BUILD_DIR=${BUILDROOT}/build
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}
MSCL_INSTALL_DIR=${STAGING_DIR}/mscl/${MSCL_VERSION}

MSCL_GIT="ssh://git@git.iter.org/lib/mscl.git"


install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${MSCL_INSTALL_DIR}
install -d ${MSCL_INSTALL_DIR}/lib

MSCL_SRC_DIR="${BUILD_DIR}/mscl-${MSCL_VERSION}"
if [ ! -e ${MSCL_SRC_DIR}/.built ]; then
    rm -rf ${MSCL_SRC_DIR}
    cd ${BUILD_DIR}
    git clone --branch ${MSCL_VERSION} ${MSCL_GIT} ${MSCL_SRC_DIR}
    cd ${MSCL_SRC_DIR}
cat <<EOT >> config/compiler.UNKNOWN.gfortran
CC       = gcc
CFLAGS   = -O3 -fPIC -fsecond-underscore

FC   = gfortran
FFLAGS   = -O3 -fPIC -fsecond-underscore
NFLAGS   = -O0 -fPIC -fsecond-underscore

CPP  = cpp
CPPFLAGS = -traditional -P

AR       = ar
EOT

    OBJECTCODE=UNKNOWN.gfortran SOLPS_LIB=${MSCL_INSTALL_DIR}/lib make install -j${MAKE_JOBS}
    touch .built
fi
# Generate Modulefile
MODULE_DIR=${MODULE_DIR:-${BUILDROOT}/modules}
if [ ! -d ${MODULE_DIR}/mscl ]; then
	install -d ${MODULE_DIR}/mscl
fi

cat << EOF > ${MODULE_DIR}/mscl/${MSCL_VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
    puts stderr {

Description
===========
Standard library used within SOLPS distribution.


More information
================
 - Homepage: https://git.iter.org/projects/LIB/repos/mscl
    }
}

module-whatis {Description: Standard library used within SOLPS distribution.}
module-whatis {Homepage: https://git.iter.org/projects/LIB/repos/mscl}

conflict MSCL

prepend-path LD_LIBRARY_PATH    ${MSCL_INSTALL_DIR}/lib
prepend-path LIBRARY_DIR        ${MSCL_INSTALL_DIR}/lib
prepend-path PKG_CONFIG_PATH    ${MSCL_INSTALL_DIR}/lib/pkgconfig

EOF