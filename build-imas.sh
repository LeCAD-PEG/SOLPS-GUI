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

BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD})}
BUILD_DIR=${BUILDROOT}/build
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}
DOWNLOAD_DIR=${BUILDROOT}/download

MAKE_JOBS=${MAKE_JOBS:-$(nproc)}

install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}

## Install Python3
PYTHON_SRC="Python-${PYTHON_VERSION}.tgz"
PYTHON_SITE="https://www.python.org/ftp/python"
PYTHON_DOWNLOAD="${PYTHON_SITE}/${PYTHON_VERSION}/${PYTHON_SRC}"

if [ ! -f ${DOWNLOAD_DIR}/${PYTHON_SRC} ]; then
    wget  -O ${DOWNLOAD_DIR}/${PYTHON_SRC} ${PYTHON_DOWNLOAD}
fi

PYTHON_SRC_DIR="${BUILD_DIR}/Python-${PYTHON_VERSION}"
PYTHON_INSTALL_DIR="${STAGING_DIR}"

if [ ! -e   ${PYTHON_SRC_DIR}/.built ]; then
  rm -rf ${PYTHON_SRC_DIR}
  cd ${BUILD_DIR}
  tar xzf ${DOWNLOAD_DIR}/${PYTHON_SRC}
  cd ${PYTHON_SRC_DIR}
  if pkg-config --exists libssl; then
    ssl=$(pkg-config --variable=prefix libssl)
    sed -i -e "s,#SSL=.*,SSL=${ssl}," -e "/^#.*ssl/s/#//" \
    -e '/ssl/s|-lcrypto|-lcrypto -Wl,-rpath,$(SSL)/lib|' Modules/Setup.dist
  fi
  ./configure --prefix=${STAGING_DIR} --enable-shared
  make -j ${MAKE_JOBS}
  make install
  ln -sf python3 ${STAGING_DIR}/bin/python
  LD_LIBRARY_PATH=${STAGING_DIR}/lib:${LD_LIBRARY_PATH} \
  PYTHONPATH=${STAGING_DIR}/lib/python${PYTHON_MAINVERSION} \
  PATH=${STAGING_DIR}/bin \
  ${STAGING_DIR}/bin/pip3 --trusted-host pypi.python.org install --upgrade \
      pip sphinx sphinx_rtd_theme mock nose
  # The following Python modules are preferred by IMAS
  LD_LIBRARY_PATH=${STAGING_DIR}/lib:${LD_LIBRARY_PATH} \
  PYTHONPATH=${STAGING_DIR}/lib/python${PYTHON_MAINVERSION} \
  PATH=${STAGING_DIR}/bin \
    ${STAGING_DIR}/bin/pip3 --trusted-host pypi.python.org install --upgrade \
      Cython luigi tornado deap decorator liac-arff ecdsa \
      netaddr paramiko virtualenv setuptools \
      wheel pyvtk
  touch ${PYTHON_SRC_DIR}/.built
fi


# Install numpy with OpenBLAS linking.
NUMPY_SRC="numpy-${NUMPY_VERSION}.tar.gz"
NUMPY_SITE="https://github.com/numpy/numpy/releases/download/"
NUMPY_DOWNLOAD="${NUMPY_SITE}/v${NUMPY_VERSION}/numpy-${NUMPY_VERSION}.tar.gz"

if [ ! -f ${DOWNLOAD_DIR}/${NUMPY_SRC} ]; then
    wget  -O ${DOWNLOAD_DIR}/${NUMPY_SRC} ${NUMPY_DOWNLOAD}
fi

NUMPY_SRC_DIR=${BUILD_DIR}/numpy-${NUMPY_VERSION}

if [ ! -e ${NUMPY_SRC_DIR}/.built ]; then
    rm -rf ${NUMPY_SRC_DIR}
    cd ${BUILD_DIR}
    tar xzf ${DOWNLOAD_DIR}/${NUMPY_SRC}
    cd ${NUMPY_SRC_DIR}
    # Set site.cfg to use OpenBLAS
cat <<EOF > site.cfg
[openblas]
libraries = openblas
library_dirs = ${STAGING_DIR}/lib
include_dirs = ${STAGING_DIR}/include
runtime_library_dirs = ${STAGING_DIR}/lib
EOF
    PATH=${STAGING_DIR}/bin:${PATH} \
    PYTHONPATH=${STAGING_DIR}/lib/python${PYTHON_MAINVERSION}/site-packages \
    LD_LIBRARY_PATH=${STAGING_DIR}/lib:${LD_LIBRARY_PATH} \
    ${STAGING_DIR}/bin/python3 setup.py build install --prefix=${STAGING_DIR}
    touch ${NUMPY_SRC_DIR}/.built
fi

# Install scipy with OpenBLAS linking.
SCIPY_SRC="scipy-${SCIPY_VERSION}.tar.gz"
SCIPY_SITE="https://github.com/scipy/scipy/releases/download/"
SCIPY_DOWNLOAD="${SCIPY_SITE}/v${SCIPY_VERSION}/scipy-${SCIPY_VERSION}.tar.gz"

if [ ! -f ${DOWNLOAD_DIR}/${SCIPY_SRC} ]; then
    wget  -O ${DOWNLOAD_DIR}/${SCIPY_SRC} ${SCIPY_DOWNLOAD}
fi

SCIPY_SRC_DIR=${BUILD_DIR}/scipy-${SCIPY_VERSION}
if [ ! -e ${SCIPY_SRC_DIR}/.built ]; then
    rm -rf ${SCIPY_SRC_DIR}
    cd ${BUILD_DIR}
    tar xzf ${DOWNLOAD_DIR}/${SCIPY_SRC}
    cd ${SCIPY_SRC_DIR}
    # Set site.cfg to use OpenBLAS
cat <<EOF > site.cfg
[openblas]
libraries = openblas
library_dirs = ${STAGING_DIR}/lib
include_dirs = ${STAGING_DIR}/include
runtime_library_dirs = ${STAGING_DIR}/lib
EOF
    PATH=${STAGING_DIR}/bin:${PATH} \
    PYTHONPATH=${STAGING_DIR}/lib/python${PYTHON_MAINVERSION}/site-packages \
    LD_LIBRARY_PATH=${STAGING_DIR}/lib:${LD_LIBRARY_PATH} \
    ${STAGING_DIR}/bin/python3 setup.py build install --prefix=${STAGING_DIR}
    touch ${SCIPY_SRC_DIR}/.built
fi

set +e
# Now install matplotlib if required.
LD_LIBRARY_PATH=${STAGING_DIR}/lib:${LD_LIBRARY_PATH} \
PYTHONPATH=${STAGING_DIR}/lib/python${PYTHON_MAINVERSION} \
PATH=${STAGING_DIR}/bin \
${STAGING_DIR}/bin/pip3 show matplotlib
if [ $? -ne 0 ]; then
    LD_LIBRARY_PATH=${STAGING_DIR}/lib:${LD_LIBRARY_PATH} \
    PYTHONPATH=${STAGING_DIR}/lib/python${PYTHON_MAINVERSION} \
    PATH=${STAGING_DIR}/bin \
    ${STAGING_DIR}/bin/pip3 --trusted-host pypi.python.org install --upgrade \
        matplotlib
fi
set -e

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
    PATH=${STAGING_DIR}/bin:${PATH} \
    PYTHONPATH=${STAGING_DIR}/lib/python${PYTHON_MAINVERSION}/site-packages \
    LD_LIBRARY_PATH=${STAGING_DIR}/lib:${LD_LIBRARY_PATH} \
    ./configure --with-python=${STAGING_DIR} \
      --prefix=${STAGING_DIR} LDFLAGS=-L${STAGING_DIR}/lib
    make -j${MAKE_JOBS}
    make install
    # Not sure if python bindings needed
    # cd python
    # CFLAGS=-I${LIBXML2_SRC_DIR}/include ${STAGING_DIR}/bin/python3 setup.py build
    # CFLAGS=-I${LIBXML2_SRC_DIR}/include ${STAGING_DIR}/bin/python3 setup.py install
    touch .built
fi

BLITZ_SOURCE="blitz-${BLITZ_VERSION}.tar.gz"
BLITZ_DOWNLOAD="https://github.com/blitzpp/blitz/archive/${BLITZ_VERSION}.tar.gz"

if [ ! -f ${DOWNLOAD_DIR}/${BLITZ_SOURCE} ]; then
    wget -O ${DOWNLOAD_DIR}/${BLITZ_SOURCE} ${BLITZ_DOWNLOAD}
fi

BLITZ_SRC_DIR="${BUILD_DIR}/blitz-${BLITZ_VERSION}"
if [ ! -e ${BLITZ_SRC_DIR}/.built ]; then
    rm -rf ${BLITZ_SRC_DIR}
    cd ${BUILD_DIR}
    tar xzf ${DOWNLOAD_DIR}/${BLITZ_SOURCE}
    cd ${BLITZ_SRC_DIR}
    CXX=g++ ./configure --prefix=${STAGING_DIR} --with-pic
    make #-j ${MAKE_JOBS}
    make install
    touch ${BLITZ_SRC_DIR}/.built
fi

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
    LD_LIBRARY_PATH=${STAGING_DIR}/lib \
    CFLAGS=-I${STAGING_DIR}/include/libxml2 \
    LDFLAGS=-lpthread \
    ./configure --prefix=${STAGING_DIR}/mdsplus/${MDSPLUS_VERSION} \
                --enable-shared --disable-doxygen-doc \
                --disable-xmltest --with-xml-prefix=${STAGING_DIR} \
                --without-labview
    make all # Errors with jobs > 1
    make install
    touch ${MDSPLUS_SRC_DIR}/.built
fi

# Download and extract SAXON
SAXON_SOURCE="Saxon${SAXON_VERSION}.zip"
SAXON_DOWNLOAD="https://sourceforge.net/projects/saxon/files/Saxon-HE/9.8/Saxon${SAXON_VERSION}.zip/download"

if [ ! -f ${DOWNLOAD_DIR}/${SAXON_SOURCE} ]; then
	wget -O ${DOWNLOAD_DIR}/${SAXON_SOURCE} ${SAXON_DOWNLOAD}
fi

if [ ! -e ${STAGING_DIR}/saxon/saxon9he.jar ]; then
	unzip ${DOWNLOAD_DIR}/${SAXON_SOURCE} -d ${STAGING_DIR}/saxon
fi


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
    	sed -i -e 's/Version: -/Version: - ${IMASDD_VERSION}-${IMASUAL_VERSION}/g' ${STAGING_DIR}/access-layer/${IMASUAL_VERSION}/lib/pkgconfig/imas-gfortran.pc
    fi
    # Enable the fail on error
    set -e

    # Link imas as imas, so you can simply say import imas in python!
    A=$(echo "imas_${IMASDD_VERSION}_ual_${IMASUAL_VERSION}"|tr . _)
    B=$(uname -m) # Get system bitness
    ln -sf $A ${STAGING_DIR}/access-layer/${IMASUAL_VERSION}/python/lib.linux-${B}-${PYTHON_MAINVERSION}/imas

    touch ${IMASUAL_SRC_DIR}/.built
fi
