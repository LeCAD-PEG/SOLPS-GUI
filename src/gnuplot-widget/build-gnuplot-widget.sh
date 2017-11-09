#!/bin/sh -x




SOURCES_DIR=$PWD/src
# SOurce files.
FILES="$SOURCES_DIR/Qt*.h $SOURCES_DIR/gnuplotWidget.h"

# Where to store generated sip file
SIPDIR=$HOME/solps-gui/staging/share/sip/PyQt5

# Where to store compiled objects
OBJECTS_DIR=$HOME/solps-gui/build/gnuplotWidget
STAGING_DIR=$HOME/solps-gui/staging/lib/site-packages

echo $FILES
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
rm -r $HOME/solps-gui/build/gnuplotWidget
