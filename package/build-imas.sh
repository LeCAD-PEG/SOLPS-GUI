#!/bin/sh -x
set -e
PYTHON_VERSION=${PYTHON_VERSION:-3.6.8}
PYTHON_MAINVERSION=${PYTHON_VERSION%.*}
NUMPY_VERSION=${NUMPY_VERSION:-1.16.1}
SCIPY_VERSION=${SCIPY_VERSION:-1.2.1}
MDSPLUS_VERSION=${MDSPLUS_VERSION:-stable_release-7-7-8}
BLITZ_VERSION=${BLITZ_VERSION:-1.0.0} # Apparently this is the same as 0.10.0
LIBXML2_VERSION=${LIBXML2_VERSION:-2.9.1}
SAXON_VERSION=${SAXON_VERSION:-HE9-8-0-12J}
IMASDD_VERSION=${IMASDD_VERSION:-3.21.0}  # Data dictionary
IMASUAL_VERSION=${IMASUAL_VERSION:-3.8.4}  # Access layer

BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD%/package})}
BUILD_DIR=${BUILDROOT}/build
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}
DOWNLOAD_DIR=${BUILDROOT}/download

MAKE_JOBS=${MAKE_JOBS:-$(nproc)}

install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}



IMASDD_GIT="ssh://git@git.iter.org/imas/data-dictionary.git"

IMASDD_SRC_DIR="${BUILD_DIR}/data-dictionary-${IMASDD_VERSION}"
if [ ! -e ${IMASDD_SRC_DIR}/.built ]; then
    rm -rf ${IMASDD_SRC_DIR}
    cd ${BUILD_DIR}
    git clone --branch ${IMASDD_VERSION} --single-branch ${IMASDD_GIT} ${IMASDD_SRC_DIR}
    cd ${IMASDD_SRC_DIR}
    PATH=${STAGING_DIR}/bin:${PATH} \
    PYTHONPATH=${STAGING_DIR}/lib/python${PYTHON_MAINVERSION}/site-packages \
    LD_LIBRARY_PATH=${STAGING_DIR}/lib:${LD_LIBRARY_PATH} \
    CLASSPATH=${STAGING_DIR}/saxon/saxon9he.jar \
    make install DD_BUILD=${STAGING_DIR}/data-dictionary/${IMASDD_VERSION}
    touch ${IMASDD_SRC_DIR}/.built
fi

IMASUAL_GIT="ssh://git@git.iter.org/imas/access-layer.git"
IMASUAL_SRC_DIR="${BUILD_DIR}/access-layer/${IMASUAL_VERSION}"
if [ ! -e ${IMASUAL_SRC_DIR}/.built ]; then
    rm -rf ${IMASUAL_SRC_DIR}
    cd ${BUILD_DIR}
    git clone --branch ${IMASUAL_VERSION} --single-branch ${IMASUAL_GIT} ${IMASUAL_SRC_DIR}
    cd ${IMASUAL_SRC_DIR}

    # Link Data dictionary install/include dir
    ln -sf ${IMASDD_SRC_DIR} ${IMASUAL_SRC_DIR}/xml
    export IMAS_VERSION=${IMASDD_VERSION}
    export UAL_VERSION=${IMASUAL_VERSION}
    MDSPLUS_DIR=${STAGING_DIR}/mdsplus/${MDSPLUS_VERSION} \
    MDS_PATH=${STAGING_DIR}/mdsplus/${MDSPLUS_VERSION}/tdi \
    PATH=${STAGING_DIR}/bin:${STAGING_DIR}/mdsplus/${MDSPLUS_VERSION}/bin:${PATH} \
    PYTHONPATH=${STAGING_DIR}/lib/python${PYTHON_MAINVERSION}/site-packages \
    LD_LIBRARY_PATH=${STAGING_DIR}/lib:/${STAGING_DIR}/mdsplus/${MDSPLUS_VERSION}/lib:${LD_LIBRARY_PATH} \
    PKG_CONFIG_PATH=${STAGING_DIR}/lib/pkgconfig:${PKG_CONFIG_PATH} \
    CLASSPATH=${STAGING_DIR}/saxon/saxon9he.jar \
    IMAS_IFORT='no' IMAS_PYTHON3='yes' IMAS_PYTHON2='no' IMAS_CPP='yes' IMAS_FORTRAN='yes' \
    IMAS_PYTHON='yes' IMAS_JAVA='no' IMAS_MATLAB='no' IMAS_MDSPLUS='yes' \
    IMAS_PREFIX=${STAGING_DIR}/access-layer/${IMASUAL_VERSION} \
    make install IMAS_INSTALL_DIR=${STAGING_DIR}/access-layer/${IMASUAL_VERSION}

    # For some reason the version of IMAS is not written into the pkg-config
    # file. Fixing that if the version is not in the *.pc file

    # Disable the fail on error
    set +e
    if ! grep -Fxq "Version: - ${IMASDD_VERSION}-${IMASUAL_VERSION}" ${STAGING_DIR}/access-layer/${IMASUAL_VERSION}/lib/pkgconfig/imas-gfortran.pc
    then
    	sed -i -e "s/Version: -/Version: - ${IMASDD_VERSION}-${IMASUAL_VERSION}/g" ${STAGING_DIR}/access-layer/${IMASUAL_VERSION}/lib/pkgconfig/imas-gfortran.pc
    fi
    # Enable the fail on error
    set -e

    # Link imas as imas, so you can simply say import imas in python!
    A=$(echo "imas_${IMASDD_VERSION}_ual_${IMASUAL_VERSION}"|tr . _)
    B=$(uname -m) # Get system bitness
    ln -sf $A ${STAGING_DIR}/access-layer/${IMASUAL_VERSION}/python/lib.linux-${B}-${PYTHON_MAINVERSION}/imas

    touch ${IMASUAL_SRC_DIR}/.built
fi
