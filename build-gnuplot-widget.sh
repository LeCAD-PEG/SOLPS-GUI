#!/bin/sh -x

QT_VERSION=${QT_VERSION:-5.9.1}
PYTHON_VERSION=${PYTHON_VERSION:-3.6.4}

BUILDROOT=${PWD}
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}
QTDIR=${STAGING_DIR}/qt/${QT_VERSION}


# Where to store generated sip file
SIPDIR=${SIPDIR:-${STAGING_DIR}/share/sip/PyQt5}

# Where to store compiled objects
OBJECTS_DIR=${OBJECTS_DIR:-${BUILDROOT}/build/gnuplotWidget}

case $(hostname -f) in
    *.iter.org)
        module purge
        module load GCC
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
        ;;
esac



export PATH="${STAGING_DIR}/bin:${QTDIR}/bin:${PATH}"
export LD_LIBRARY_PATH="${STAGING_DIR}/lib:${QTDIR}/lib:${LD_LIBRARY_PATH}"
export PKG_CONFIG_PATH="${STAGING_DIR}/lib/pkgconfig:${PKG_CONFIG_PATH}"

PYVER=${PYTHON_VERSION%.*} # just major.minor version 
INSTALL_DIR=${INSTALL_DIR:-${STAGING_DIR}/lib/python${PYVER}/site-packages}
GNUPLOT_WIDGET_DIR=${GNUPLOT_WIDGET_DIR:-${BUILDROOT}/src/gnuplot-widget}
GNUPLOT_WIDGET_SRC_DIR=${GNUPLOT_WIDGET_DIR}/src

MAKE_JOBS=${MAKE_JOBS:-4}
export QTDIR

set -e

cd ${GNUPLOT_WIDGET_DIR}

which moc
which qmake

SOURCE_FILES="${GNUPLOT_WIDGET_SRC_DIR}/Qt*.h ${GNUPLOT_WIDGET_SRC_DIR}/gnuplotWidget.h"
for file in ${SOURCE_FILES} # MOCing .h files
  do moc ${file} -o ${GNUPLOT_WIDGET_SRC_DIR}/moc_$(basename ${file} .h).cpp
done

install -d ${SIPDIR}
install -d ${OBJECTS_DIR}

which python3
python3 configure.py --verbose --sipdir=${SIPDIR} --outdir=${OBJECTS_DIR} \
    --srcdir=${GNUPLOT_WIDGET_SRC_DIR} --incdir=${GNUPLOT_WIDGET_SRC_DIR} \
    --destdir=${INSTALL_DIR}

# TODO: Move all compiling and other generated files to build dir.
# TODO: Safely remove as to not accidentally remove non-generated files.

cd ${GNUPLOT_WIDGET_SRC_DIR}

make -j ${MAKE_JOBS}
make install
make clean
make distclean
rm -f moc_* sippy* sipAPI* pyQtGnuplot.*
rm -fr ${OBJECTS_DIR}
echo "Gnuplot widget has been installed in ${INSTALL_DIR}"
