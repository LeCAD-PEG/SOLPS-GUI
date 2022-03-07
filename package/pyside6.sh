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
eval $(${PACKAGE_DIR}/libclang.sh --env --pkg)
eval $(${PACKAGE_DIR}/qt6.sh --env --pkg)
eval $(${PACKAGE_DIR}/python.sh --env)
eval $(${PACKAGE_DIR}/ninja.sh --env)



# Build
if [ ! -e ${PACKAGE_INSTALL_DIR}/.built ]; then
    cd ${PACKAGE_SOURCE_DIR}
#    mkdir -p ${PACKAGE_INSTALL_DIR}
#    echo "Preparing Python buildenv. See ${PACKAGE_LOG_DIR}/buildenv"
#    python -m venv buildenv
#    buildenv/bin/pip install -r requirements.txt &> ${PACKAGE_LOG_DIR}/buildenv
    echo "Building PySide6. See ${PACKAGE_LOG_DIR}/build"
    python setup.py install --standalone --skip-docs --parallel=${MAKE_JOBS} \
    	--ignore-git --prefix=${PACKAGE_INSTALL_DIR} &> ${PACKAGE_LOG_DIR}/build
    touch ${PACKAGE_INSTALL_DIR}/.built
fi
#_python_install "--skip-docs --ignore-git --prefix=${PACKAGE_INSTALL_DIR}"


# set +e
# ${PIP} uninstall -y numpy
# ${PYTHON} setup.py build install --prefix=${PYTHON_INSTALL_DIR}

# # Now install matplotlib.
# ${PIP} show matplotlib
# if [ $? -ne 0 ]; then
#     ${PIP} --trusted-host pypi.python.org install --upgrade matplotlib
# fi

# set -e
