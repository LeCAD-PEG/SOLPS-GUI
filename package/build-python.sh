#!/bin/sh -x
set -e
BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD%/package})}
BUILD_DIR=${BUILDROOT}/build
DOWNLOAD_DIR=${BUILDROOT}/download
STAGING_DIR=${BUILDROOT}/staging
PYTHON_VERSION=${PYTHON_VERSION:-3.6.8}
PYTHON_MAINVERSION=${PYTHON_VERSION%.*}
NUMPY_VERSION=${NUMPY_VERSION:-1.16.1}
SCIPY_VERSION=${SCIPY_VERSION:-1.2.1}

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