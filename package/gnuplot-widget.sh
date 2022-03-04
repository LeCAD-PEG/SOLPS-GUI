#!/bin/bash -e

PACKAGE=gnuplot-widget
VERSION=python-$($(cd ${0%/*} && echo ${PWD})/python.sh --version)
VERSION+=-qt-$($(cd ${0%/*} && echo ${PWD})/qt5.sh --version)

source $(cd ${0%/*} && echo ${PWD})/functions.sh $*

_prerequisites python qt5 pyqt

eval $(${PACKAGE_DIR}/python.sh --env)
eval $(${PACKAGE_DIR}/qt5.sh --env --pkg)
eval $(${PACKAGE_DIR}/pyqt.sh --env)
eval $(${PACKAGE_DIR}/sip.sh --env)

PYTHON_VERSION=$(${PACKAGE_DIR}/python.sh --version)
PYTHON_MAINVERSION=${PYTHON_VERSION%.*}
QT_VERSION=$(${PACKAGE_DIR}/qt5.sh --version)

# Package variables
SRC_DIR=${BUILDROOT}/src/gnuplot-widget
INSTALL_DIR=${STAGING_DIR}/gnuplot-widget/python-${PYTHON_VERSION}-qt-${QT_VERSION}

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


export PYTHONPATH=$(${PACKAGE_DIR}/pyqt.sh --prefix)/lib/python${PYTHON_MAINVERSION}/site-packages:${PYTHONPATH}
export PYTHONPATH=$(${PACKAGE_DIR}/sip.sh --prefix)/lib:${PYTHONPATH}


echo $PYTHONPATH
python3 configure.py --verbose --sipdir=${INSTALL_DIR}/share/sip/PyQt5 \
        --outdir=${BUILD_DIR}/gnuplotWidget --srcdir=${SRC_DIR}/src \
        --incdir=${SRC_DIR}/src --destdir=${PACKAGE_INSTALL_DIR}


# Build

cd ${SRC_DIR}/src
make -j${MAKE_JOBS}


# Install
make install

# After-build clean
make clean
make distclean
rm -f ${SRC_DIR}/moc_* ${SRC_DIR}/sippy* ${SRC_DIR}/sipAPI* ${SRC_DIR}/pyQtGnuplot.*
rm -rf ${OBJECTS_DIR}
