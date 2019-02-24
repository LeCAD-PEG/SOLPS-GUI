#!/bin/sh -x
set -e

# For Qt5.x build problems on RHEL5 see
# https://forum.qt.io/topic/37757/howto-building-qt-5-2-1-including-webkit-on-rhel5-linux-centos-5-7
# See http://kate-editor.org/2014/12/22/qt-5-4-on-red-hat-enterprise-5/

# Variables
BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD%/package})}
MAKE_JOBS=${MAKE_JOBS:-$(nproc)}

# Buildroot directories
MODULE_DIR=${MODULE_DIR:-${BUILDROOT}/modules}
BUILD_DIR=${BUILDROOT}/build
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}
DOWNLOAD_DIR=${BUILDROOT}/download
PATCH_DIR=${BUILDROOT}/src/patches

# Package variables
VERSION=${VERSION:-5.9.1} # should be the same as Qt
SOURCE="PyQt5_gpl-${VERSION}.tar.gz"
DOWNLOAD="http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-${VERSION}/${SOURCE}/download"
SRC_DIR="${BUILD_DIR}/PyQt5_gpl-${VERSION}"
INSTALL_DIR="${STAGING_DIR}/PyQt5/${VERSION}"

# Site specific defaults
case $(hostname -f) in
     *.iter.org) # RHEL7
        module purge
        # module load GCC/4.8.3 binutils/2.25 python/2.7/11 #gperf
        # module load imas/3.7.2/ual/3.3.14
            MAKE_JOBS ?= 14
        unset CXX CC # Remove ICC to be selected by chance
            QT_EXTRA_FLAGS=${QT_EXTRA_FLAGS:-\
                            -D GLX_GLXEXT_LEGACY \
                            -D _X_INLINE=inline \
                            -D FC_WEIGHT_EXTRABLACK=215 \
                            -D FC_WEIGHT_ULTRABLACK=FC_WEIGHT_EXTRABLACK}
        ;;
    # SLES 11.4 WPCD Gateway (incompatible XCB, Xlib and GL libraries)
    tok*.bc.rzg.mpg.de) # IPP MPG
        MAKE_JOBS=${MAKE_JOBS:-16}
        QT_EXTRA_FLAGS=${QT_EXTRA_FLAGS:--no-sql-mysql -no-opengl \
            -skip qtcanvas3d  -skip qtpurchasing -skip qtvirtualkeyboard}
        ;;

    *.marconi.cineca.it) # EU-IM Gateway CentOS 7 with GCC 6.1
        MAKE_JOBS=${MAKE_JOBS:-16}
        #. /etc/profile.d.gw/modules.sh
        # module unload itm-gcc/6.1.0 itm-python/2.7
        #module switch itm-python/2.7.13.b1
        #module unload itm-gcc/6.1.0 gcc/6.1.0
        module unload matlab
        module unload paraview
        export CXXFLAGS="-fpermissive"
        QT_EXTRA_FLAGS=${QT_EXTRA_FLAGS:--no-sql-sqlite}
        ;;
    *)
        PYTHON_VERSION=${PYTHON_VERSION:-3.6.8}
        PYTHON_MAINVERSION=${PYTHON_VERSION%.*}
        QT_VERSION=${QT_VERSION:-5.9.1}
        SIP_VERSION=${SIP_VERSION:-4.19.13}
        STAGING_QT=${STAGING_QT:-${STAGING_DIR}/qt/${QT_VERSION}}
        SIP_INSTALL_DIR="${STAGING_DIR}/sip/${SIP_VERSION}"
        PYTHON_INSTALL_DIR=${STAGING_DIR}/Python/${PYTHON_VERSION}

        export PATH=${PYTHON_INSTALL_DIR}/bin:${PATH}
        export LD_LIBRARY_PATH=${PYTHON_INSTALL_DIR}/lib:${LD_LIBRARY_PATH}
        export LD_LIBRARY_PATH=${SIP_INSTALL_DIR}/lib/python${PYTHON_MAINVERSION}:${LD_LIBRARY_PATH}
        export PYTHONPATH=

        ;;
esac

# Prepare directories for download and building
install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}

# Download source
if [ ! -f ${DOWNLOAD_DIR}/${SOURCE} ]; then
    wget -O ${DOWNLOAD_DIR}/${SOURCE} --no-check-certificate ${DOWNLOAD}
fi

cd ${BUILD_DIR}

# Unpack sources
if [ ! -d ${SRC_DIR} ]; then
    tar xzf ${DOWNLOAD_DIR}/${SOURCE}
fi

cd ${SRC_DIR}

# Configure
if [ ! -e ${SRC_DIR}/.configured ]; then
    python3 configure.py --confirm-license --verbose \
        --qmake=${STAGING_DIR}/qt/${QT_VERSION}/bin/qmake \
        --sip=${SIP_INSTALL_DIR}/bin/sip \
        --destdir=${INSTALL_DIR}/lib/python${PYTHON_MAINVERSION}/site-packages
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
fi

# Generate Modulefile
if [ ! -d ${MODULE_DIR}/PyQt5 ]; then
    install -d ${MODULE_DIR}/PyQt5
fi

cat << EOF > ${MODULE_DIR}/PyQt5/${VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
    puts stderr {

Description
===========
PyQt5 is a set of Python bindings for v5 of the Qt application framework from The Qt Company.


More information
================
 - Homepage: http://www.riverbankcomputing.co.uk/software/pyqt
    }
}

if { ![ is-loaded Python/${PYTHON_VERSION} ] } {
    module load Python/${PYTHON_VERSION}
}

if { ![ is-loaded SIP/${SIP_VERSION} ] } {
    module load SIP/${SIP_VERSION}
}

if { ![ is-loaded Qt5/${QT_VERSION} ] } {
    module load Qt5/${QT_VERSION}
}

module-whatis {Description: PyQt5 is a set of Python bindings for v5 of the Qt application framework from The Qt Company.}
module-whatis {Homepage: http://www.riverbankcomputing.co.uk/software/pyqt}

conflict PyQt5
prepend-path PYTHONPATH         ${INSTALL_DIR}/lib/python${PYTHON_MAINVERSION}/site-packages
EOF

