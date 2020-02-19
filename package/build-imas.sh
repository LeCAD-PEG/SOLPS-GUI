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
VERSION=${VERSION:-4.5.0}
GIT="ssh://git@git.iter.org/imas/access-layer.git"
SRC_DIR="${BUILD_DIR}/access-layer-${VERSION}"
INSTALL_DIR=${STAGING_DIR}/imas/${IMASDD_VERSION}/solps # Use IMASDD version later.

# Environment dependencies
if [ -e ${BUILDROOT}/package/setup.sh ]; then
    . ${BUILDROOT}/package/setup.sh
fi

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
if [ ! -e ${SRC_DIR}/.configured ]; then
    rm -rf ${INSTALL_DIR}
    touch ${SRC_DIR}/.configured
fi

# Build
if [ ! -e ${SRC_DIR}/.built ]; then
    if [ ! -L ${SRC_DIR}/xml ]; then
        # Link IMASDD build directory
        ln -sf ${BUILD_DIR}/data-dictionary-${IMASDD_VERSION} xml
    fi

    IMAS_IFORT='no' IMAS_PYTHON3='yes' IMAS_PYTHON2='no' IMAS_CPP='yes' IMAS_FORTRAN='yes' \
    IMAS_PYTHON='yes' IMAS_JAVA='no' IMAS_MATLAB='no' IMAS_MDSPLUS='yes' IMAS_UDA='no' \
    IMAS_MEX='no' \
    IMAS_PREFIX=${INSTALL_DIR} \
    make -j ${MAKE_JOBS}
    touch ${SRC_DIR}/.built
fi

# Install
if [ ! -d ${INSTALL_DIR} ]; then
    install -d ${INSTALL_DIR}
    IMAS_IFORT='no' IMAS_PYTHON3='yes' IMAS_PYTHON2='no' IMAS_CPP='yes' IMAS_FORTRAN='yes' \
    IMAS_PYTHON='yes' IMAS_JAVA='no' IMAS_MATLAB='no' IMAS_MDSPLUS='yes' \
    IMAS_PREFIX=${INSTALL_DIR} IMAS_UDA='no' IMAS_MEX='no' \
    make install IMAS_INSTALL_DIR=${INSTALL_DIR}

    # Post installation
    # For some reason the version of IMAS is not written into the pkg-config
    # file. Fixing that if the version is not in the *.pc file

    # Disable the fail on error
    set +e
    if ! grep -Fxq "Version: - ${IMAS_VERSION}-${VERSION}" ${INSTALL_DIR}/lib/pkgconfig/imas-gfortran.pc
    then
        sed -i -e "s/Version: -/Version: - ${IMAS_VERSION}-${VERSION}/g" ${INSTALL_DIR}/lib/pkgconfig/imas-gfortran.pc
    fi
    # Enable the fail on error
    set -e
    A=$(echo "imas_${IMAS_VERSION}_ual_${VERSION}"|tr . _)
    B=$(uname -m) # Get system bitness
    # Link imas as imas, so you can simply say import imas in python!
    ln -sf $A ${INSTALL_DIR}/python/lib.linux-${B}-${PYTHON_MAINVERSION}/imas

    # Create binary directory, even if it's empty
    install -d ${INSTALL_DIR}/bin
fi

# Generate Modulefile
if [ ! -d ${MODULE_DIR}/imas/${IMAS_VERSION} ]; then
    install -d ${MODULE_DIR}/imas/${IMAS_VERSION}
fi

cat << EOF > ${MODULE_DIR}/imas/${IMAS_VERSION}/solps
#%Module1.0#####################################################################
##
## \$name modulefile
##
module-whatis "Integrated Modelling and Analysis Suite (IMAS). (imas:${IMAS_VERSION} ual:${VERSION}})"

proc ModulesHelp { } {
  puts stderr "\tThis module sets the environment for IMAS version ${IMAS_VERSION}"
}

conflict imas

if { ![ is-loaded MDSplus/${MDSPLUS_VERSION} ] } {
    module load MDSplus/${MDSPLUS_VERSION}
}

if { ![ is-loaded blitz/${BLITZ_VERSION} ] } {
    module load blitz/${BLITZ_VERSION}
}

if { ![ is-loaded OpenBLAS/${OPENBLAS_VERSION} ] } {
    module load OpenBLAS/${OPENBLAS_VERSION}
}

if { ![ is-loaded libxml2/${LIBXML2_VERSION} ] } {
    module load libxml2/${LIBXML2_VERSION}
}

if { ![ is-loaded Python/${PYTHON_VERSION} ] } {
    module load Python/${PYTHON_VERSION}
}

setenv       IMAS_VERSION       ${IMAS_VERSION}
setenv       UAL_VERSION        ${VERSION}
setenv       IMAS_PREFIX        ${INSTALL_DIR}
prepend-path PATH               ${INSTALL_DIR}/bin
prepend-path LD_LIBRARY_PATH    ${INSTALL_DIR}/lib
prepend-path PKG_CONFIG_PATH    ${INSTALL_DIR}/lib/pkgconfig
prepend-path PYTHONPATH         ${INSTALL_DIR}/python/lib.linux-${B}-${PYTHON_MAINVERSION}
setenv       ids_path           ${INSTALL_DIR}/models/mdsplus

EOF