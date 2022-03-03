#!/bin/bash -e

PACKAGE=python
VERSION=${VERSION:-3.9.10}
DOWNLOAD_LINK=https://www.python.org/ftp/python/${VERSION}/Python-${VERSION}.tgz
FILENAME=${PACKAGE}-${VERSION}.tar.gz

source $(cd ${0%/*} && echo ${PWD})/functions.sh $*

_downloadFileAndUnpack ${DOWNLOAD_LINK} ${FILENAME}

cd ${PACKAGE_SOURCE_DIR}

# Before calling configure we have to fix the SSL linking
if pkg-config --exists libssl; then
    ssl=$(pkg-config --variable=prefix libssl)

    # Modules/Setup checkup.
    MODULES_FILE=Modules/Setup.dist
    [ ! -e "Modules/Setup.dist" ] && MODULES_FILE=Modules/Setup
    sed -i -e "s,#SSL=.*,SSL=${ssl}," -e "/^#.*ssl/s/#//" \
    -e '/ssl/s|-lcrypto |-lcrypto -Wl,-rpath,$(SSL)/lib|' ${MODULES_FILE}
fi

# FFI library is no longer bundled together so it is required to have
# development and runtime packages of FFI installed on the system.

_configure "--enable-shared --enable-optimizations --with-system-ffi"
_make "-j${MAKE_JOBS}"
_install

# Post install things
ln -sf python3 ${PACKAGE_INSTALL_DIR}/bin/python

# Pip packages to install

export PATH=${PACKAGE_INSTALL_DIR}/bin:${PATH}
export LD_LIBRARY_PATH=${PACKAGE_INSTALL_DIR}/lib:${LD_LIBRARY_PATH}
echo "Installing packages via pip. Check ${PACKAGE_LOG_DIR}/pip_installs"
pip3 --trusted-host pypi.python.org install --upgrade \
    pip Cython sphinx sphinx_rtd_theme mock nose wheel setuptools \
    pyside6 spyder pyqtgraph matplotlib scipy &> ${PACKAGE_LOG_DIR}/pip_installs
