#!/bin/sh -x

QT_VERSION=${QT_VERSION:-5.9.1}
PyQT_VERSION=${PyQT_VERSION:-5.9.1}
PYTHON_VERSION=${PYTHON_VERSION:-3.6.4}
SIP_VERSION=${SIP_VERSION:-4.19.13}
PYTHON_MAINVERSION=${PYTHON_VERSION%.*}
GNUPLOT_VERSION=${GNUPLOT_VERSION:-5.2.2}

BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD%/package})}
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}
QTDIR=${STAGING_DIR}/qt/${QT_VERSION}
PYTHON_INSTALL_DIR=${STAGING_DIR}/Python/${PYTHON_VERSION}
PyQt_INSTALL_DIR=${STAGING_DIR}/PyQt5/${PyQT_VERSION}
GNUPLOT_WIDGET_INSTALL_DIR=${STAGING_DIR}/gnuplot-widget/python-${PYTHON_VERSION}-qt-${QT_VERSION}
SIP_INSTALL_DIR=${STAGING_DIR}/SIP/${SIP_VERSION}


# Where to store generated sip file
SIPDIR=${SIPDIR:-${GNUPLOT_WIDGET_INSTALL_DIR}/share/sip/PyQt5}

# Where to store compiled objects
OBJECTS_DIR=${OBJECTS_DIR:-${BUILDROOT}/build/gnuplotWidget}

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
	export PATH="${PYTHON_INSTALL_DIR}/bin:${QTDIR}/bin:${PATH}"
	export LD_LIBRARY_PATH="${PYTHON_INSTALL_DIR}/lib:${QTDIR}/lib:${LD_LIBRARY_PATH}"
	export PKG_CONFIG_PATH="${PYTHON_INSTALL_DIR}/lib/pkgconfig:${PKG_CONFIG_PATH}"
	export PYTHONPATH=${PyQt_INSTALL_DIR}/lib/python${PYTHON_MAINVERSION}/site-packages:${PYTHONPATH}
	export PYTHONPATH=${SIP_INSTALL_DIR}/lib/python${PYTHON_MAINVERSION}/site-packages:${PYTHONPATH}
    ;;
esac


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
    --destdir=${GNUPLOT_WIDGET_INSTALL_DIR}/lib/python${PYTHON_MAINVERSION}/site-packages

# TODO: Move all compiling and other generated files to build dir.
# TODO: Safely remove as to not accidentally remove non-generated files.

cd ${GNUPLOT_WIDGET_SRC_DIR}

make -j ${MAKE_JOBS}
make install
make clean
make distclean
rm -f moc_* sippy* sipAPI* pyQtGnuplot.*
rm -fr ${OBJECTS_DIR}
echo "Gnuplot widget has been installed in ${GNUPLOT_WIDGET_INSTALL_DIR}"

# Generate Modulefile
MODULE_DIR=${MODULE_DIR:-${BUILDROOT}/modules}
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

prepend-path PYTHON_PATH        ${GNUPLOT_WIDGET_INSTALL_DIR}/lib/python${PYTHON_MAINVERSION}/site-packages
EOF