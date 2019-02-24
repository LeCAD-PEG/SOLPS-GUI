#!/bin/sh -x
set -e


# Variables
BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD%/package})}
MAKE_JOBS=${MAKE_JOBS:-$(nproc)}

# Buildroot directories
MODULE_DIR=${MODULE_DIR:-${BUILDROOT}/modules}
BUILD_DIR=${BUILDROOT}/build
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}
PATCH_DIR=${BUILDROOT}/src/patches
DOWNLOAD_DIR=${BUILDROOT}/download

# Package variables
VERSION=${VERSION:-5.9.1}
MAJOR_VERSION=${VERSION%.*}
SOURCE="qt-everywhere-opensource-src-${VERSION}.tar.xz"
DOWNLOAD="http://download.qt.io/official_releases/qt/${MAJOR_VERSION}/${VERSION}/single/${SOURCE}"
SRC_DIR="${BUILD_DIR}/qt-everywhere-opensource-src-${VERSION}"
INSTALL_DIR=${STAGING_DIR}/qt/${VERSION}

# Environment dependencies

# Prepare directories for download and building
install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}

# Download source
if [ ! -f ${DOWNLOAD_DIR}/${SOURCE} ]; then
    wget -O ${DOWNLOAD_DIR}/${SOURCE} ${DOWNLOAD}
fi

cd ${BUILD_DIR}

# Unpack sources
if [ ! -d ${SRC_DIR} ]; then
    xzcat ${DOWNLOAD_DIR}/${SOURCE} | tar -xf -
fi

cd ${SRC_DIR}

# Configure
if [ ! -e ${SRC_DIR}/.configured ]; then
    # sed -i.orig -e 's/-Wno-error=return-type//' \
    #     qtlocation/src/3rdparty/poly2tri/poly2tri.pro
    #patch -p 1 -d ${SRC_DIR} < ${PATCH_DIR}/qt5-openssl.patch
    # patch -p 1 -d ${SRC_DIR} < ${PATCH_DIR}/qt5-no-offscreen.patch
    # #patch -p 1 -d ${SRC_DIR} < ${PATCH_DIR}/qt5-qfbvthandler.patch
    # patch -p 1 -d ${SRC_DIR}<${PATCH_DIR}/qglxintegration-glx-context.patch
    # #patch -p 1 -d ${SRC_DIR} < ${PATCH_DIR}/qt5-qxcbconnection.patch
    # patch -p 1 -d ${SRC_DIR} < ${PATCH_DIR}/qt5-qbenchmarkperfevents.patch
    # #patch -p 1 -d ${SRC_DIR} < ${PATCH_DIR}/qsimd.cpp-gcc4.2.patch
    # patch -p 1 -d ${SRC_DIR} < ${PATCH_DIR}/qt5-qdbusinternalfilters.patch
    # patch -p 1 -d ${SRC_DIR} < ${PATCH_DIR}/qt5-invoke-static.patch
    # #patch -p 1 -d ${SRC_DIR} < ${PATCH_DIR}/qt5-qtbase-platformsupport-fbconveniance-qfbvthandler.patch
    # sed -i -e '/auto/d' qtdeclarative/tests/tests.pro \
    #                   qtmultimedia/tests/tests.pro \
    #                   qtgraphicaleffects/tests/tests.pro
    ./configure -v --prefix=${INSTALL_DIR} -opensource -confirm-license \
      -shared \
      -skip qtmultimedia \
      -skip qtwayland \
      -skip qtgamepad \
      -skip qtwebchannel \
      -skip qtwebengine \
      -skip qtwebsockets \
      -skip qtwebview \
      -skip qt3d ${XCB_FLAGS} ${QT_EXTRA_FLAGS} \
      -qt-xkbcommon -xkb-config-root /usr/share/X11/xkb \
      -nomake tests
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
    # Install documentation
    export PATH=${INSTALL_DIR}/bin:${PATH}
    make -C qttools/src sub-qdoc
    make -C qtbase/src html_docs
    make qmake_all
    make -j ${MAKE_JOBS} docs install_docs
fi

# Generate Modulefile
if [ ! -d ${MODULE_DIR}/Qt5 ]; then
    install -d ${MODULE_DIR}/Qt5
fi

cat << EOF > ${MODULE_DIR}/Qt5/${VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
    puts stderr { Qt is a comprehensive cross-platform C++ application framework. - Homepage: http://qt.io/
    }
}

module-whatis {Description: Qt is a comprehensive cross-platform C++ application framework. - Homepage: http://qt.io/}
conflict Qt5
prepend-path CPATH              ${INSTALL_DIR}/include
prepend-path LD_LIBRARY_PATH    ${INSTALL_DIR}/lib
prepend-path LIBRARY_DIR        ${INSTALL_DIR}/lib
prepend-path PKG_CONFIG_PATH    ${INSTALL_DIR}/lib/pkgconfig
prepend-path PATH               ${INSTALL_DIR}/bin
EOF