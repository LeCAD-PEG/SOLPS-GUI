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
VERSION=${VERSION:-1.5.0}

# Environment dependencies
if [ -e ${BUILDROOT}/package/setup.sh ]; then
    . ${BUILDROOT}/package/setup.sh
fi

# Prepare directories for download and building
install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}

# Download source

# Unpack sources

# Configure

# Build

# Install

# Generate Modulefile
if [ ! -d ${MODULE_DIR}/solps-gui ]; then
    install -d ${MODULE_DIR}/solps-gui
fi

cat << EOF > ${MODULE_DIR}/solps-gui/${VERSION}
#%Module1.0###################################################################
##
## \$name modulefile
##
conflict solps-iter
if { ! [ is-loaded imas/${IMASDD_VERSION}/solps ] } {
    module load imas/${IMASDD_VERSION}/solps
}
if { ![ is-loaded Python/${PYTHON_VERSION} ] } {
    module load Python/${PYTHON_VERSION}
}

if { ![ is-loaded PyQt5/${PyQt_VERSION} ] } {
    module load PyQt5/${PyQt_VERSION}
}
if { ![ is-loaded gnuplot/${GNUPLOT_VERSION}-qt-${QT_VERSION} ] } {
    module load gnuplot/${GNUPLOT_VERSION}-qt-${QT_VERSION}
}

setenv SOLPSGUITOP ${BUILDROOT}
set SOLPSGUITOP ${BUILDROOT}

setenv QT_QPA_FONTDIR /usr/share/fonts/dejavu
prepend-path PYQTDESIGNERPATH \$SOLPSGUITOP/src/plugins/designer
prepend-path PYTHONPATH \$SOLPSGUITOP/src/widgets
prepend-path PYTHONPATH \$SOLPSGUITOP/src/gui

set-alias solps  "python3 \$SOLPSGUITOP/src/gui/solps.py"
set-alias solps_doc "xdg-open \$SOLPSGUITOP/doc/build/html/index.html"
set-alias solps_help "assistant -collectionFile \$SOLPSGUITOP/doc/build/qthelp/SOLPSGUI.qhc"
set-alias eirene "python3 \$SOLPSGUITOP/src/widgets/eirene.py"
set-alias b2 "python3 \$SOLPSGUITOP/src/widgets/b2.py"
EOF