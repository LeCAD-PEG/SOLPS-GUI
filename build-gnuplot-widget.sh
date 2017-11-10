#!/bin/sh -x

BUILDROOT=${PWD}
GNUPLOT_WIDGET_DIR=${GNUPLOT_WIDGET_DIR:-$BUILDROOT/src/gnuplot-widget}
SOURCES_DIR=$GNUPLOT_WIDGET_DIR/src
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging/lib/site-packages}
# SOurce files.
FILES="$SOURCES_DIR/Qt*.h $SOURCES_DIR/gnuplotWidget.h"

# Where to store generated sip file
SIPDIR=${SIPDIR:-$BUILDROOT/staging/share/sip/PyQt5}

# Where to store compiled objects
OBJECTS_DIR=${OBJECTS_DIR:-$BUILDROOT/build/gnuplotWidget}

cd $GNUPLOT_WIDGET_DIR

for file in $FILES
do
    moc $file -o $SOURCES_DIR/moc_$(basename $file .h).cpp
done

if [ ! -d "$SIPDIR" ]; then
  mkdir $SIPDIR
fi

if [ ! -d "$OBJECTS_DIR" ]; then
  echo "no objects dir, craeting it"
  mkdir $OBJECTS_DIR
fi
python3 configure.py --verbose --sipdir="$SIPDIR" --outdir="$OBJECTS_DIR" --srcdir="$SOURCES_DIR" --incdir="$SOURCES_DIR" --destdir="$STAGING_DIR"

case $(hostname -f) in
  *.iter.org)
	module purge
	module load GCC
	MAKE_JOBS=${MAKE_JOBS:-4}
	;;
  *)
	;;
esac

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
