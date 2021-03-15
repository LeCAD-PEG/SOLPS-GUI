#!/bin/sh
set -e
BUILDROOT=${BUILDROOT:-$( cd "$( dirname "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && echo ${PWD%/package} )}
PACKAGE="numpy"
VERSION=${VERSION:-1.20.1}
DOWNLOAD_LINK="https://github.com/numpy/numpy/releases/download/v${VERSION}/numpy-${VERSION}.tar.gz"
FILENAME="${PACKAGE}-${VERSION}.tar.gz"

if  [ -e ${BUILDROOT}/package/solps_gui_utils.sh ]; then
    source ${BUILDROOT}/package/solps_gui_utils.sh
fi
if  [ -e ${BUILDROOT}/package/setup.sh ]; then
    source ${BUILDROOT}/package/setup.sh
fi
_downloadFileAndUnpack ${DOWNLOAD_LINK} ${FILENAME}

cd ${PACKAGE_SOURCE_DIR}

# Before calling configure we have set the site.cfg
cat << EOF > site.cfg
[openblas]
libraries = openblas
library_dirs = ${OPENBLAS_INSTALL_DIR}/lib
include_dirs = ${OPENBLAS_INSTALL_DIR}/include
runtime_library_dirs = ${OPENBLAS_INSTALL_DIR}/lib
EOF

_python_configure
_python_make

pip uninstall -y numpy
_python_install "--prefix=${PYTHON_INSTALL_DIR}"

# Now install matplotlib.
set +e
pip show matplotlib
if [ $? -ne 0 ]; then
    pip --trusted-host pypi.python.org install --upgrade matplotlib
fi
set -e