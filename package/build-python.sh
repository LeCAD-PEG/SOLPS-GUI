#!/bin/sh -x
set -e
BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD%/package})}
BUILD_DIR=${BUILDROOT}/build
DOWNLOAD_DIR=${BUILDROOT}/download
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}
PYTHON_VERSION=${PYTHON_VERSION:-3.6.8}
PYTHON_MAINVERSION=${PYTHON_VERSION%.*}
NUMPY_VERSION=${NUMPY_VERSION:-1.16.1}
SCIPY_VERSION=${SCIPY_VERSION:-1.2.1}
OPENBLAS_VERSION=${OPENBLAS_VERSION:-0.3.5}

PYTHON_INSTALL_DIR="${STAGING_DIR}/Python/${PYTHON_VERSION}"
OPENBLAS_INSTALL_DIR=${STAGING_DIR}/OpenBLAS/${OPENBLAS_VERSION}

MAKE_JOBS=${MAKE_JOBS:-$(nproc)}

install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}
install -d ${PYTHON_INSTALL_DIR}

## Install Python3
PYTHON_SRC="Python-${PYTHON_VERSION}.tgz"
PYTHON_SITE="https://www.python.org/ftp/python"
PYTHON_DOWNLOAD="${PYTHON_SITE}/${PYTHON_VERSION}/${PYTHON_SRC}"

if [ ! -f ${DOWNLOAD_DIR}/${PYTHON_SRC} ]; then
    wget  -O ${DOWNLOAD_DIR}/${PYTHON_SRC} ${PYTHON_DOWNLOAD}
fi

PYTHON_SRC_DIR="${BUILD_DIR}/Python-${PYTHON_VERSION}"

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
  ./configure --prefix=${PYTHON_INSTALL_DIR} --enable-shared
  make -j ${MAKE_JOBS}
  make install
  ln -sf python3 ${PYTHON_INSTALL_DIR}/bin/python
  LD_LIBRARY_PATH=${PYTHON_INSTALL_DIR}/lib:${LD_LIBRARY_PATH} \
  PYTHONPATH=${PYTHON_INSTALL_DIR}/lib/python${PYTHON_MAINVERSION} \
  PATH=${PYTHON_INSTALL_DIR}/bin \
  ${PYTHON_INSTALL_DIR}/bin/pip3 --trusted-host pypi.python.org install --upgrade \
      pip sphinx sphinx_rtd_theme mock nose
  # The following Python modules are preferred by IMAS
  LD_LIBRARY_PATH=${PYTHON_INSTALL_DIR}/lib:${LD_LIBRARY_PATH} \
  PYTHONPATH=${PYTHON_INSTALL_DIR}/lib/python${PYTHON_MAINVERSION} \
  PATH=${PYTHON_INSTALL_DIR}/bin \
    ${PYTHON_INSTALL_DIR}/bin/pip3 --trusted-host pypi.python.org install --upgrade \
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
library_dirs = ${OPENBLAS_INSTALL_DIR}/lib
include_dirs = ${OPENBLAS_INSTALL_DIR}/include
runtime_library_dirs = ${OPENBLAS_INSTALL_DIR}/lib
EOF
    PATH=${PYTHON_INSTALL_DIR}/bin:${PATH} \
    PYTHONPATH=${PYTHON_INSTALL_DIR}/lib/python${PYTHON_MAINVERSION}/site-packages \
    LD_LIBRARY_PATH=${OPENBLAS_INSTALL_DIR}/lib:${LD_LIBRARY_PATH} \
    LD_LIBRARY_PATH=${PYTHON_INSTALL_DIR}/lib:${LD_LIBRARY_PATH} \
    ${PYTHON_INSTALL_DIR}/bin/python3 setup.py build install --prefix=${PYTHON_INSTALL_DIR}
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
library_dirs = ${OPENBLAS_INSTALL_DIR}/lib
include_dirs = ${OPENBLAS_INSTALL_DIR}/include
runtime_library_dirs = ${OPENBLAS_INSTALL_DIR}/lib
EOF
    PATH=${PYTHON_INSTALL_DIR}/bin:${PATH} \
    PYTHONPATH=${PYTHON_INSTALL_DIR}/lib/python${PYTHON_MAINVERSION}/site-packages \
    LD_LIBRARY_PATH=${OPENBLAS_INSTALL_DIR}/lib:${LD_LIBRARY_PATH} \
    LD_LIBRARY_PATH=${PYTHON_INSTALL_DIR}/lib:${LD_LIBRARY_PATH} \
    ${PYTHON_INSTALL_DIR}/bin/python3 setup.py build install --prefix=${PYTHON_INSTALL_DIR}
    touch ${SCIPY_SRC_DIR}/.built
fi

set +e
# Now install matplotlib if required.
LD_LIBRARY_PATH=${STAGING_DIR}/lib:${LD_LIBRARY_PATH} \
PYTHONPATH=${PYTHON_INSTALL_DIR}/lib/python${PYTHON_MAINVERSION} \
PATH=${STAGING_DIR}/bin \
${STAGING_DIR}/bin/pip3 show matplotlib
if [ $? -ne 0 ]; then
    LD_LIBRARY_PATH=${PYTHON_INSTALL_DIR}/lib:${LD_LIBRARY_PATH} \
    PYTHONPATH=${PYTHON_INSTALL_DIR}/lib/python${PYTHON_MAINVERSION} \
    PATH=${PYTHON_INSTALL_DIR}/bin \
    ${PYTHON_INSTALL_DIR}/bin/pip3 --trusted-host pypi.python.org install --upgrade \
        matplotlib
fi
set -e
MODULE_DIR=${MODULE_DIR:-${BUILDROOT}/modules}
if [ ! -d ${MODULE_DIR}/Python ]; then
	install -d ${MODULE_DIR}/Python
fi

cat << EOF > ${MODULE_DIR}/Python/${PYTHON_VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
    puts stderr {

Description
===========
Python is a programming language that lets you work more quickly and integrate your systems
 more effectively.


More information
================
 - Homepage: http://python.org/


Included extensions
===================
asn1crypto-0.24.0, bcrypt-3.1.4, bitstring-3.1.5, blist-1.3.6,
certifi-2018.1.18, cffi-1.11.5, chardet-3.0.4, cryptography-2.1.4,
Cython-0.27.3, deap-1.2.2, decorator-4.1.2, docopt-0.6.2, ecdsa-0.13,
idna-2.6, joblib-0.11, liac-arff-2.1.1, mock-2.0.0, mpi4py-3.0.0,
netaddr-0.7.19, netifaces-0.10.6, nose-1.3.7, numpy-1.14.0, pandas-0.22.0,
paramiko-2.4.0, paycheck-1.0.2, pbr-3.1.1, pip-9.0.1,
py_expression_eval-0.3.4, pyasn1-0.4.2, pycparser-2.18, pycrypto-2.6.1,
PyNaCl-1.2.1, pyparsing-2.2.0, python-dateutil-2.6.1, pytz-2017.3,
requests-2.18.4, scipy-1.0.0, setuptools-38.4.0, six-1.11.0, urllib3-1.22,
virtualenv-15.1.0, xlrd-1.1.0
    }
}

module-whatis {Description: Python is a programming language that lets you work more quickly and integrate your systems
 more effectively.}
module-whatis {Homepage: http://python.org/}
module-whatis {Extensions: asn1crypto-0.24.0, bcrypt-3.1.4, bitstring-3.1.5, blist-1.3.6, certifi-2018.1.18, cffi-1.11.5, chardet-3.0.4, cryptography-2.1.4, Cython-0.27.3, deap-1.2.2, decorator-4.1.2, docopt-0.6.2, ecdsa-0.13, idna-2.6, joblib-0.11, liac-arff-2.1.1, mock-2.0.0, mpi4py-3.0.0, netaddr-0.7.19, netifaces-0.10.6, nose-1.3.7, numpy-1.14.0, pandas-0.22.0, paramiko-2.4.0, paycheck-1.0.2, pbr-3.1.1, pip-9.0.1, py_expression_eval-0.3.4, pyasn1-0.4.2, pycparser-2.18, pycrypto-2.6.1, PyNaCl-1.2.1, pyparsing-2.2.0, python-dateutil-2.6.1, pytz-2017.3, requests-2.18.4, scipy-1.0.0, setuptools-38.4.0, six-1.11.0, urllib3-1.22, virtualenv-15.1.0, xlrd-1.1.0}

conflict Python
prepend-path CPATH              ${PYTHON_INSTALL_DIR}/include
prepend-path LD_LIBRARY_PATH    ${PYTHON_INSTALL_DIR}/lib
prepend-path LD_LIBRARY_PATH    ${PYTHON_INSTALL_DIR}/lib/python${PYTHON_MAINVERSION}/site-packages
prepend-path LIBRARY_DIR        ${PYTHON_INSTALL_DIR}/lib
prepend-path PKG_CONFIG_PATH    ${PYTHON_INSTALL_DIR}/lib/pkgconfig
prepend-path PATH               ${PYTHON_INSTALL_DIR}/bin
EOF
