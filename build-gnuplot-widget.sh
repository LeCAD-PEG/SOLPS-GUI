#!/bin/sh -x

BUILDROOT=${PWD}
GNUPLOT_WIDGET_DIR=${GNUPLOT_WIDGET_DIR:-$BUILDROOT/src/gnuplot-widget}
SOURCES_DIR=$GNUPLOT_WIDGET_DIR/src
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging/lib/site-packages}
QT_VERSION="5.9.1"
QTDIR="${BUILDROOT}/staging/qt/$QT_VERSION"
# SOurce files.
FILES="$SOURCES_DIR/Qt*.h $SOURCES_DIR/gnuplotWidget.h"

# Where to store generated sip file
SIPDIR=${SIPDIR:-$BUILDROOT/staging/share/sip/PyQt5}

# Where to store compiled objects
OBJECTS_DIR=${OBJECTS_DIR:-$BUILDROOT/build/gnuplotWidget}

QT_LIBS="${QTDIR}/lib"
export QT_LIBS
export PATH="${BUILDROOT}/staging/bin:${QTDIR}/bin:${PATH}"
export LD_LIBRARY_PATH="${BUILDROOT}/staging/lib:${QTDIR}/lib:${LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH="${BUILDROOT}/staging/qt/$QT_VERSION/lib:${LD_LIBRARY_PATH}"
export PKG_CONFIG_PATH="${BUILDROOT}/staging/lib/pkgconfig:${PKG_CONFIG_PATH}"


case $(hostname -f) in
    *.iter.org)
        module purge
        module load GCC
        MAKE_JOBS=${MAKE_JOBS:-4}
        ;;
    *)
        ;;
esac

# Old ITER CASE
# case $(hostname -f) in
#   *.iter.org)
#         module purge
#     #module load GCC
#         module load imas binutils
#         module unload Anaconda2
#         qmake --version && sip -V
#         QT_VERSION=5.6.2 PyQT_VERSION=5.6.2 SIP_VERSION=4.18
#         QTDIR="${EBROOTANACONDA3}/pkgs/qt-5.6.2-3"
#         MAKE_JOBS=${MAKE_JOBS:-4}
#         # Because qmake cannot find mkspecs file on its own
#         export QMAKESPEC=$QTDIR/mkspecs/linux-g++
#     ;;
#   *)
#     ;;
# esac

export QTDIR

set -e

cd $GNUPLOT_WIDGET_DIR

# mocing .h files
for file in $FILES
do
    moc $file -o $SOURCES_DIR/moc_$(basename $file .h).cpp
done

if [ ! -d "$SIPDIR" ]; then
  mkdir $SIPDIR
fi

if [ ! -d "$OBJECTS_DIR" ]; then
  echo "no objects directory, creating it"
  mkdir $OBJECTS_DIR
fi
python3 configure.py --verbose --sipdir="$SIPDIR" --outdir="$OBJECTS_DIR" --srcdir="$SOURCES_DIR" --incdir="$SOURCES_DIR" --destdir="$STAGING_DIR"



# TODO: Move all compiling and other generated files to build dir.
# TODO: Safely remove as to not accidentally remove non-generated files.

cd $SOURCES_DIR

make -j $MAKE_JOBS
make install
make clean
make distclean
echo "Cleaning up"
rm moc_* sippy* sipAPI* pyQtGnuplot.*
rm -r $OBJECTS_DIR
