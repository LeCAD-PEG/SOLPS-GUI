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
VERSION=${VERSION:-1.0.0}
SRC_DIR=${BUILDROOT}/src/gnuplot-widget
INSTALL_DIR=${STAGING_DIR}/gnuplot-widget/python-${PYTHON_VERSION}-qt-${QT_VERSION}

# Environment dependencies
case $(hostname -f) in
    *.iter.org)
        module purge
        #module load GCC/4.8.3 binutils/2.25
        MAKE_JOBS=${MAKE_JOBS:-4}
        ;;
    *.marconi.cineca.it)
        module purge
        module load cineca imasenv
        module unload matlab
        QT_VERSION=5.8.0
        module load itm-qt/${QT_VERSION}
        ;;
    *)
        QT_VERSION=${QT_VERSION:-5.9.1}
        PyQT_VERSION=${PyQT_VERSION:-5.9.1}
        PYTHON_VERSION=${PYTHON_VERSION:-3.6.8}
        SIP_VERSION=${SIP_VERSION:-4.19.13}
        PYTHON_MAINVERSION=${PYTHON_VERSION%.*}
        GNUPLOT_VERSION=${GNUPLOT_VERSION:-5.2.2}

        QTDIR=${STAGING_DIR}/qt/${QT_VERSION}
        PYTHON_INSTALL_DIR=${STAGING_DIR}/Python/${PYTHON_VERSION}
        PyQt_INSTALL_DIR=${STAGING_DIR}/PyQt5/${PyQT_VERSION}
        SIP_INSTALL_DIR=${STAGING_DIR}/sip/${SIP_VERSION}

        export QTDIR
        export PATH="${PYTHON_INSTALL_DIR}/bin:${QTDIR}/bin:${SIP_INSTALL_DIR}/bin:${PATH}"
        export LD_LIBRARY_PATH="${PYTHON_INSTALL_DIR}/lib:${QTDIR}/lib:${LD_LIBRARY_PATH}"
        export PKG_CONFIG_PATH="${PYTHON_INSTALL_DIR}/lib/pkgconfig:${PKG_CONFIG_PATH}"
        export PYTHONPATH=${PyQt_INSTALL_DIR}/lib/python${PYTHON_MAINVERSION}/site-packages:${PYTHONPATH}
        export PYTHONPATH=${PYTHON_INSTALL_DIR}/lib/python${PYTHON_MAINVERSION}/site-packages:${PYTHONPATH}
        export PYTHONPATH=${SIP_INSTALL_DIR}/lib/python/site-packages:${PYTHONPATH}
        ;;
esac

# Prepare directories for download and building
install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}

# Download source

# Unpack sources

cd ${SRC_DIR}
# Configure
SOURCE_FILES="${SRC_DIR}/src/Qt*.h ${SRC_DIR}/src/gnuplotWidget.h"
for file in ${SOURCE_FILES} # MOCing .h files
do
  echo $file
  cpp_file="${SRC_DIR}/src/moc_$(basename ${file} .h).cpp"
  if [ ! -e ${cpp_file} ]; then
    moc ${file} -o ${SRC_DIR}/src/moc_$(basename ${file} .h).cpp
  fi
done

if [ ! -d ${INSTALL_DIR}/share/sip/PyQt5 ]; then
    install -d ${INSTALL_DIR}/share/sip/PyQt5
fi

if [ ! -d ${BUILD_DIR}/gnuplotWidget ]; then
    install -d ${BUILD_DIR}/gnuplotWidget
fi

python3 configure.py --verbose --sipdir=${INSTALL_DIR}/share/sip/PyQt5 \
        --outdir=${BUILD_DIR}/gnuplotWidget --srcdir=${SRC_DIR}/src \
        --incdir=${SRC_DIR}/src --destdir=${INSTALL_DIR}


# Build

cd ${SRC_DIR}/src
make -j${MAKE_JOBS}


# Install
make install

# After-build clean
make clean
make distclean
rm -f moc_* sippy* sipAPI* pyQtGnuplot.*
rm -rf ${OBJECTS_DIR}

if [ ! -d ${MODULE_DIR}/gnuplot-widget ]; then
	install -d ${MODULE_DIR}/gnuplot-widget
fi
cat << EOF > ${MODULE_DIR}/gnuplot-widget/python-${PYTHON_VERSION}-qt-${QT_VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
puts stderr "\tThis module sets the environment for gnuplot-widget"
}
module-whatis  "Gnuplot-widget is a python PyQt5 widget with embedded Gnuplot."

conflict gnuplot-widget

if { ![ is-loaded gnuplot/${GNUPLOT_VERSION}-qt-${QT_VERSION}] } {
    module load gnuplot/${GNUPLOT_VERSION}-qt-${QT_VERSION}
}

if { ![ is-loaded Python/${PYTHON_VERSION} ] } {
    module load Python/${PYTHON_VERSION}
}

if { ![ is-loaded PyQt5/${QT_VERSION} ] } {
    module load PyQt5/${QT_VERSION}
}

prepend-path PYTHON_PATH        ${INSTALL_DIR}/lib/python${PYTHON_MAINVERSION}/site-packages
EOF