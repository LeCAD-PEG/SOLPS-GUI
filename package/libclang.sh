#!/bin/bash -e
# https://github.com/llvm/llvm-project/releases

PACKAGE=libclang
VERSION=${VERSION:-13.0.0}
MAJOR_VERSION=${VERSION%.*}
DOWNLOAD_LINK=https://github.com/llvm/llvm-project/releases/download/llvmorg-${VERSION}
FILENAME=llvm-${VERSION}.src.tar.xz

source $(cd ${0%/*} && echo ${PWD})/functions.sh $*

_downloadFileAndUnpack ${DOWNLOAD_LINK}/${FILENAME} ${FILENAME}
LLVM_DIR=${PACKAGE_SOURCE_DIR}

(
    PACKAGE="clang"
    FILENAME=clang-${VERSION}.src.tar.xz
    source ${PACKAGE_DIR}/functions.sh
    _downloadFileAndUnpack ${DOWNLOAD_LINK}/${FILENAME} ${FILENAME}
    ln -sf ${PACKAGE_SOURCE_DIR} ${SOURCE_DIR}/clang
)

cd ${PACKAGE_SOURCE_DIR}
CMAKE_FLAG="-DCMAKE_BUILD_TYPE=Release"
CMAKE_FLAG="${CMAKE_FLAG} -DLLVM_ENABLE_PROJECTS=clang"

_cmake "${CMAKE_FLAG}"
_cmake_build  "--parallel ${MAKE_JOBS}"
_cmake_install
#_make "-j${MAKE_JOBS}"
#_install
