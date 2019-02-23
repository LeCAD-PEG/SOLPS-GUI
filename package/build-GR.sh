#!/bin/sh -x
set -e


case $(hostname -f) in
    *)
esac

MAKE_JOBS=${MAKE_JOBS:-$(nproc)} # Should use all threads of a system


BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD%/package})}
BUILD_DIR=${BUILDROOT}/build
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}
GR_VERSION=${GR_VERSION:-0.0.94}
GR_INSTALL_DIR=${STAGING_DIR}/GR/${GR_VERSION}
GR_GIT="ssh://git@git.iter.org/lib/gr-software.git"


install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${GR_INSTALL_DIR}
install -d ${GR_INSTALL_DIR}/lib

GR_SRC_DIR="${BUILD_DIR}/gr-software-${GR_VERSION}"
if [ ! -e ${GR_SRC_DIR}/.built ]; then
    rm -rf ${GR_SRC_DIR}
    cd ${BUILD_DIR}
    git clone --branch ${GR_VERSION} ${GR_GIT} ${GR_SRC_DIR}
    cd ${GR_SRC_DIR}
    make SOLPS_LIB=${GR_INSTALL_DIR}/lib BLDFLAG="ar cr" RANLIB=echo allf CFLAGS="-fPIC" F77=gfortran
    make install BLDFLAG="ar cr" RANLIB=echo SOLPS_LIB=${GR_INSTALL_DIR}/lib CFLAGS="-FPIC" F77=gfortran
    touch .built
fi

# Generate Modulefile
MODULE_DIR=${MODULE_DIR:-${BUILDROOT}/modules}
if [ ! -d ${MODULE_DIR}/gr ]; then
	install -d ${MODULE_DIR}/GR
fi

cat << EOF > ${MODULE_DIR}/GR/${GR_VERSION}
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
prepend-path LD_LIBRARY_PATH    ${GR_INSTALL_DIR}/lib
prepend-path LIBRARY_DIR        ${GR_INSTALL_DIR}/lib
EOF