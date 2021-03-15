#!/bin/sh
set -e
BUILDROOT=${BUILDROOT:-$( cd "$( dirname "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && echo ${PWD%/package} )}
PACKAGE="llvm"
VERSION=${VERSION:-11.1.0}
MAJOR_VERSION=${VERSION%.*}
DOWNLOAD_LINK="https://github.com/llvm/llvm-project/releases/download/llvmorg-${VERSION}/llvm-project-${VERSION}.src.tar.xz"
FILENAME="${PACKAGE}-${VERSION}.tar.xz"

if  [ -e ${BUILDROOT}/package/solps_gui_utils.sh ]; then
    source ${BUILDROOT}/package/solps_gui_utils.sh
fi
if  [ -e ${BUILDROOT}/package/setup.sh ]; then
    source ${BUILDROOT}/package/setup.sh
fi

_downloadFileAndUnpack ${DOWNLOAD_LINK} ${FILENAME}

cd ${PACKAGE_SOURCE_DIR}
CMAKE_FLAG="-DCMAKE_BUILD_TYPE=Release -DLLVM_TARGETS_TO_BUILD=\"X86\""
CMAKE_FLAG="${CMAKE_FLAG} -DLLVM_ENABLE_PROJECTS=clang"

_cmake ${CMAKE_FLAG}
_make "-j${MAKE_JOBS}"
_install