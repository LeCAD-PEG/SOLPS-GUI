#!/bin/sh -x
set -e
PYTHON_VERSION=${PYTHON_VERSION:-3.6.8}
PYTHON_MAINVERSION=${PYTHON_VERSION%.*}
OPENBLAS_VERSION=${OPENBLAS_VERSION:-0.3.5}
NUMPY_VERSION=${NUMPY_VERSION:-1.16.1}
SCIPY_VERSION=${SCIPY_VERSION:-1.2.1}
MDSPLUS_VERSION=${MDSPLUS_VERSION:-stable_release-7-7-8}
BLITZ_VERSION=${BLITZ_VERSION:-1.0.0} # Apparently this is the same as 0.10.0
LIBXML2_VERSION=${LIBXML2_VERSION:-2.9.1}
SAXON_VERSION=${SAXON_VERSION:-HE9-8-0-12J}
IMASDD_VERSION=${IMASDD_VERSION:-3.21.0}  # Data dictionary
IMASUAL_VERSION=${IMASUAL_VERSION:-3.8.4}  # Access layer

# A way to find JAVA_HOME
# And without /jre part.
# java -XshowSettings:properties -version 2>&1 > /dev/null | grep 'java.home'
# Print java properties and grep the line with java.home
#
# tr -d ' ' | sed -e 's|java.home=||' -e 's|/jre||'
# Remove spaces and remove the "java.home=" and "/jre" parts.
JAVA_HOME=$(java -XshowSettings:properties -version 2>&1 > /dev/null | grep 'java.home' | tr -d ' ' | sed -e 's|java.home=||' -e 's|/jre||')

BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD%/package})}
BUILD_DIR=${BUILDROOT}/build
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}
DOWNLOAD_DIR=${BUILDROOT}/download

# Only for Access-Layer. No need to install data-dictionary. Only build
# directory required
IMAS_INSTALL_DIR=${STAGING_DIR}/imas/${IMASDD_VERSION}/solps
PYTHON_INSTALL_DIR=${STAGING_DIR}/Python/${PYTHON_VERSION}

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
    PATH=${PYTHON_INSTALL_DIR}/bin:${PATH} \
    PYTHONPATH=${PYTHON_INSTALL_DIR}/lib/python${PYTHON_MAINVERSION}/site-packages \
    LD_LIBRARY_PATH=${PYTHON_INSTALL_DIR}/lib:${LD_LIBRARY_PATH} \
    CLASSPATH=${STAGING_DIR}/saxon/${SAXON_VERSION}/saxon9he.jar \
    make DD_BUILD=${STAGING_DIR}/data-dictionary/${IMASDD_VERSION}
    touch ${IMASDD_SRC_DIR}/.built
fi

IMASUAL_GIT="ssh://git@git.iter.org/imas/access-layer.git"
IMASUAL_SRC_DIR="${BUILD_DIR}/access-layer-${IMASUAL_VERSION}"

A=$(echo "imas_${IMASDD_VERSION}_ual_${IMASUAL_VERSION}"|tr . _)
B=$(uname -m) # Get system bitness

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
    PATH=${PYTHON_INSTALL_DIR}/bin:${STAGING_DIR}/mdsplus/${MDSPLUS_VERSION}/bin:${PATH} \
    PYTHONPATH=${PYTHON_INSTALL_DIR}/lib/python${PYTHON_MAINVERSION}/site-packages \
    LD_LIBRARY_PATH=${PYTHON_INSTALL_DIR}/lib:/${STAGING_DIR}/mdsplus/${MDSPLUS_VERSION}/lib:${LD_LIBRARY_PATH} \
    PKG_CONFIG_PATH=${PYTHON_INSTALL_DIR}/lib/pkgconfig:${PKG_CONFIG_PATH} \
    PKG_CONFIG_PATH=${STAGING_DIR}/blitz/${BLITZ_VERSION}/lib/pkgconfig:${PKG_CONFIG_PATH} \
    JAVA_HOME=${JAVA_HOME} \
    CLASSPATH=${STAGING_DIR}/saxon/${SAXON_VERSION}/saxon9he.jar \
    IMAS_IFORT='no' IMAS_PYTHON3='yes' IMAS_PYTHON2='no' IMAS_CPP='yes' IMAS_FORTRAN='yes' \
    IMAS_PYTHON='yes' IMAS_JAVA='yes' IMAS_MATLAB='no' IMAS_MDSPLUS='yes' \
    IMAS_PREFIX=${IMAS_INSTALL_DIR} \
    make install IMAS_INSTALL_DIR=${IMAS_INSTALL_DIR}

    # For some reason the version of IMAS is not written into the pkg-config
    # file. Fixing that if the version is not in the *.pc file

    # Disable the fail on error
    set +e
    if ! grep -Fxq "Version: - ${IMASDD_VERSION}-${IMASUAL_VERSION}" ${IMAS_INSTALL_DIR}/lib/pkgconfig/imas-gfortran.pc
    then
    	sed -i -e "s/Version: -/Version: - ${IMASDD_VERSION}-${IMASUAL_VERSION}/g" ${IMAS_INSTALL_DIR}/lib/pkgconfig/imas-gfortran.pc
    fi
    # Enable the fail on error
    set -e

    # Link imas as imas, so you can simply say import imas in python!
    ln -sf $A ${IMAS_INSTALL_DIR}/python/lib.linux-${B}-${PYTHON_MAINVERSION}/imas

    # Create binary directory, even if empty
    install -d ${IMAS_INSTALL_DIR}/bin

    touch ${IMASUAL_SRC_DIR}/.built
fi

# Generate Modulefile
MODULE_DIR=${MODULE_DIR:-${BUILDROOT}/modules}
if [ ! -d ${MODULE_DIR}/imas/${IMASDD_VERSION} ]; then
	install -d ${MODULE_DIR}/imas/${IMASDD_VERSION}
fi

cat << EOF > ${MODULE_DIR}/imas/${IMASDD_VERSION}/solps
#%Module1.0#####################################################################
##
## \$name modulefile
##
module-whatis "Integrated Modelling and Analysis Suite (IMAS). (imas:${IMASDD_VERSION} ual:${IMASUAL_VERSION}})"

proc ModulesHelp { } {
  puts stderr "\tThis module sets the environment for IMAS version ${IMASDD_VERSION}"
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

if { ![ is-loaded saxon/${SAXON_VERSION} ] } {
    module load saxon/${SAXON_VERSION}
}

if { ![ is-loaded libxml2/${LIBXML2_VERSION} ] } {
    module load libxml2/${LIBXML2_VERSION}
}

if { ![ is-loaded Python/${PYTHON_VERSION} ] } {
    module load Python/${PYTHON_VERSION}
}

setenv       IMAS_VERSION       ${IMASDD_VERSION}
setenv       UAL_VERSION        ${IMASUAL_VERSION}
setenv 		 IMAS_PREFIX		${IMAS_INSTALL_DIR}
prepend-path LD_LIBRARY_PATH    ${IMAS_INSTALL_DIR}/lib
prepend-path PKG_CONFIG_PATH    ${IMAS_INSTALL_DIR}/lib/pkgconfig
prepend-path PYTHONPATH         ${IMAS_INSTALL_DIR}/python/lib.linux-${B}-${PYTHON_MAINVERSION}
setenv       ids_path 			${IMAS_INSTALL_DIR}/models/mdsplus

EOF