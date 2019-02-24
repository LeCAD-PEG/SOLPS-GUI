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
VERSION=${VERSION:-3.8.4}
GIT="ssh://git@git.iter.org/imas/access-layer.git"
SRC_DIR="${BUILD_DIR}/access-layer-${VERSION}"
INSTALL_DIR=${STAGING_DIR}/imas/${VERSION}/solps

# Environment dependencies
case $(hostname -f) in
    *)
        PYTHON_VERSION=${PYTHON_VERSION:-3.6.8}
        PYTHON_MAINVERSION=${PYTHON_VERSION%.*}
        OPENBLAS_VERSION=${OPENBLAS_VERSION:-0.3.5}
        NUMPY_VERSION=${NUMPY_VERSION:-1.16.1}
        SCIPY_VERSION=${SCIPY_VERSION:-1.2.1}
        MDSPLUS_VERSION=${MDSPLUS_VERSION:-stable_release-7-7-8}
        BLITZ_VERSION=${BLITZ_VERSION:-1.0.0}
        LIBXML2_VERSION=${LIBXML2_VERSION:-2.9.1}
        SAXON_VERSION=${SAXON_VERSION:-HE9-8-0-12J}
        IMAS_VERSION=${IMAS_VERSION:-3.21.0}  # Data dictionary

        export IMAS_VERSION=${IMASDD_VERSION}
        INSTALL_DIR=${STAGING_DIR}/imas/${IMAS_VERSION}/solps
        export UAL_VERSION=${VERSION}


        export PATH=${STAGING_DIR}/Python/${PYTHON_VERSION}/bin:${PATH}
        export PYTHONPATH=${STAGING_DIR}/Python/${PYTHON_VERSION}/lib/python${PYTHON_MAINVERSION}/site-packages
        export LD_LIBRARY_PATH=${STAGING_DIR}/Python/${PYTHON_VERSION}/lib:${LD_LIBRARY_PATH}

        export CLASSPATH=${STAGING_DIR}/saxon/${SAXON_VERSION}/saxon9he.jar

        export MDSPLUS_DIR=${STAGING_DIR}/mdsplus/${MDSPLUS_VERSION}
        export MDS_PATH=${MDSPLUS_DIR}/tdi
        export LD_LIBRARY_PATH=${MDSPLUS_DIR}/lib:${LD_LIBRARY_PATH}
        export PATH=${MDSPLUS_DIR}/bin:${PATH}

        export PKG_CONFIG_PATH=${STAGING_DIR}/Python/${PYTHON_VERSION}/lib/pkgconfig:${PKG_CONFIG_PATH}
        export PKG_CONFIG_PATH=${STAGING_DIR}/blitz/${BLITZ_VERSION}/lib/pkgconfig:${PKG_CONFIG_PATH}
        export PKG_CONFIG_PATH=${STAGING_DIR}/mdsplus/${MDSPLUS_VERSION}/lib/pkgconfig:${PKG_CONFIG_PATH}

        # A way to find JAVA_HOME
        # And without /jre part.
        # java -XshowSettings:properties -version 2>&1 > /dev/null | grep 'java.home'
        # Print java properties and grep the line with java.home
        #
        # tr -d ' ' | sed -e 's|java.home=||' -e 's|/jre||'
        # Remove spaces and remove the "java.home=" and "/jre" parts.
        export JAVA_HOME=$(java -XshowSettings:properties -version 2>&1 > /dev/null | grep 'java.home' | tr -d ' ' | sed -e 's|java.home=||' -e 's|/jre||')

        A=$(echo "imas_${IMAS_VERSION}_ual_${VERSION}"|tr . _)
        B=$(uname -m) # Get system bitness
        ;;
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
    if [ ! -L ${SRC_DIR}/xml ]; then
        # Link IMASDD build directory
        ln -sf ${BUILD_DIR}/data-dictionary-${IMASDD_VERSION} xml
    fi

    IMAS_IFORT='no' IMAS_PYTHON3='yes' IMAS_PYTHON2='no' IMAS_CPP='yes' IMAS_FORTRAN='yes' \
    IMAS_PYTHON='yes' IMAS_JAVA='yes' IMAS_MATLAB='no' IMAS_MDSPLUS='yes' \
    IMAS_PREFIX=${INSTALL_DIR} \
    make #-j ${MAKE_JOBS}
    touch ${SRC_DIR}/.built
fi

# Install
if [ ! -d ${INSTALL_DIR} ]; then
    install -d ${INSTALL_DIR}
    IMAS_IFORT='no' IMAS_PYTHON3='yes' IMAS_PYTHON2='no' IMAS_CPP='yes' IMAS_FORTRAN='yes' \
    IMAS_PYTHON='yes' IMAS_JAVA='yes' IMAS_MATLAB='no' IMAS_MDSPLUS='yes' \
    IMAS_PREFIX=${INSTALL_DIR} \
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

if { ![ is-loaded mdsplus/${MDSPLUS_VERSION} ] } {
    module load mdsplus/${MDSPLUS_VERSION}
}

if { ![ is-loaded blitz/${BLITZ_VERSION} ] } {
    module load blitz/${BLITZ_VERSION}
}

if { ![ is-loaded OpenBLAS/${OPENBLAS_VERSION} ] } {
    module load OpenBLAS/${OPENBLAS_VERSION}
}

if { ![ is-loaded saxon/${SAXON_VERSION} ] } {
    module load saxon/${SAXON_VERSION}
}

if { ![ is-loaded libxml2/${LIBXML2_VERSION} ] } {
    module load libxml2/${LIBXML2_VERSION}
}

if { ![ is-loaded Python/${PYTHON_VERSION} ] } {
    module load Python/${PYTHON_VERSION}
}

setenv       IMAS_VERSION       ${IMAS_VERSION}
setenv       UAL_VERSION        ${VERSION}
setenv 		 IMAS_PREFIX		${INSTALL_DIR}
prepend-path LD_LIBRARY_PATH    ${INSTALL_DIR}/lib
prepend-path PKG_CONFIG_PATH    ${INSTALL_DIR}/lib/pkgconfig
prepend-path PYTHONPATH         ${INSTALL_DIR}/python/lib.linux-${B}-${PYTHON_MAINVERSION}
setenv       ids_path 			${INSTALL_DIR}/models/mdsplus

EOF