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
VERSION=${VERSION:-3.6.8}
MAINVERSION=${VERSION%.*}
SOURCE="Python-${VERSION}.tgz"
DOWNLOAD="https://www.python.org/ftp/python/${VERSION}/${SOURCE}"
SRC_DIR="${BUILD_DIR}/Python-${VERSION}"
INSTALL_DIR="${STAGING_DIR}/Python/${VERSION}"

# Environment dependencies
case $(hostname -f) in
  *)
        export LD_LIBRARY_PATH=${INSTALL_DIR}/lib:${LD_LIBRARY_PATH}
        export PYTHONPATH=${INSTALL_DIR}/lib/python${MAINVERSION}
        export PATH=${INSTALL_DIR}/bin:${PATH}
        ;;
esac


# Prepare directories for download and building
install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}
## Install Python3

# Download source
if [ ! -f ${DOWNLOAD_DIR}/${SOURCE} ]; then
    wget -O ${DOWNLOAD_DIR}/${SOURCE} ${DOWNLOAD}
fi

cd ${BUILD_DIR}

# Unpack sources
if [ ! -d ${SRC_DIR} ]; then
    tar xzf ${DOWNLOAD_DIR}/${SOURCE}
fi

cd ${SRC_DIR}

# Configure
if [ ! -e ${SRC_DIR}/.configured ]; then
    ./configure --prefix=${INSTALL_DIR} --enable-shared
    touch ${SRC_DIR}/.configured
fi

# Build
if [ ! -e ${SRC_DIR}/.built ]; then
    make -j${MAKE_JOBS}
    touch ${SRC_DIR}/.built
fi

# Install
if [ ! -d ${INSTALL_DIR} ]; then
    install -d ${INSTALL_DIR}
    make install

    ln -sf python3 ${INSTALL_DIR}/bin/python
    pip3 --trusted-host pypi.python.org install --upgrade \
        pip sphinx sphinx_rtd_theme mock nose

    # The following Python modules are preferred by IMAS

    pip3 --trusted-host pypi.python.org install --upgrade \
        Cython luigi tornado deap decorator liac-arff ecdsa \
        netaddr paramiko virtualenv setuptools \
        wheel pyvtk
fi


MODULE_DIR=${MODULE_DIR:-${BUILDROOT}/modules}
if [ ! -d ${MODULE_DIR}/Python ]; then
	install -d ${MODULE_DIR}/Python
fi

cat << EOF > ${MODULE_DIR}/Python/${VERSION}
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
prepend-path CPATH              ${INSTALL_DIR}/include
prepend-path LD_LIBRARY_PATH    ${INSTALL_DIR}/lib
prepend-path LD_LIBRARY_PATH    ${INSTALL_DIR}/lib/python${MAINVERSION}/site-packages
prepend-path LIBRARY_DIR        ${INSTALL_DIR}/lib
prepend-path PKG_CONFIG_PATH    ${INSTALL_DIR}/lib/pkgconfig
prepend-path PATH               ${INSTALL_DIR}/bin
EOF
