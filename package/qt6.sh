#!/bin/bash -e

PACKAGE=qt6
VERSION=${VERSION:-6.2.3}
BUILD_TYPE=${BUILD_TYPE:-release}
MAJOR_VERSION=${VERSION%.*}
FILENAME=qt-everywhere-src-${VERSION}.tar.xz
DOWNLOAD_LINK=https://download.qt.io/official_releases/qt/${MAJOR_VERSION}/${VERSION}/single/${FILENAME}

source $(cd ${0%/*} && echo ${PWD})/functions.sh $*

_prerequisites cmake ninja

_downloadFileAndUnpack ${DOWNLOAD_LINK} ${FILENAME}

# Set compile version
if [ ${BUILD_TYPE} == release ]; then
	# Release version
	CONFIGURE_FLAG="-release -platform linux-g++"
else
	# Debug version
	CONFIGURE_FLAG="-debug -platform linux-g++"
	CONFIGURE_FLAG+=" -force-debug-info"
	CONFIGURE_FLAG+=" -no-separate-debug-info"
fi

CONFIGURE_FLAG+=" -nomake tests -nomake examples -bundled-xcb-xinput -xcb"

eval $(${PACKAGE_DIR}/ninja.sh --env)

_configure_cmake "${CONFIGURE_FLAG}"  
#_cmake_build --verbose
_cmake_build "--parallel ${MAKE_JOBS}"
_cmake_install

# TODO: also install documentation, but that requires LLVM...
