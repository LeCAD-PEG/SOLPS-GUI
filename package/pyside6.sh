#!/bin/bash -e

# See https://doc.qt.io/qtforpython/gettingstarted-linux.html
# Requires ninja, pip install setuptools

PACKAGE=pyside6
VERSION=${VERSION:-6.2.3}
GIT_URL=https://code.qt.io/pyside/pyside-setup.git

source $(cd ${0%/*} && echo ${PWD})/functions.sh $*

_prerequisites cmake ninja python libclang qt6

_gitCloneSingleBranch ${GIT_URL} ${VERSION}

QT_DIR=$(${PACKAGE_DIR}/qt6.sh --prefix)

eval $(${PACKAGE_DIR}/cmake.sh --env)
eval $(${PACKAGE_DIR}/libclang.sh --env)
eval $(${PACKAGE_DIR}/qt6.sh --env)
eval $(${PACKAGE_DIR}/python.sh --env)
eval $(${PACKAGE_DIR}/ninja.sh --env)

cd ${PACKAGE_SOURCE_DIR}


# Build
if [ ! -e ${PACKAGE_INSTALL_DIR}/.built ]; then
    python3.9 setup.py install \
          --qmake=${QT_DIR}/bin/qmake --cmake=$(which cmake) --skip-docs \
          --ignore-git --parallel=${MAKE_JOBS}
    mkdir -p ${PACKAGE_INSTALL_DIR}
    touch ${PACKAGE_INSTALL_DIR}/.built
fi


# set +e
# ${PIP} uninstall -y numpy
# ${PYTHON} setup.py build install --prefix=${PYTHON_INSTALL_DIR}

# # Now install matplotlib.
# ${PIP} show matplotlib
# if [ $? -ne 0 ]; then
#     ${PIP} --trusted-host pypi.python.org install --upgrade matplotlib
# fi

# set -e
