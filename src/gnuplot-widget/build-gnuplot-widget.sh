#!/bin/sh -x


FILES="Qt*.h gnuplotWidget.h"
SIPDIR=$HOME/solps-gui/staging/share/sip/PyQt5
OBJECTS_DIR=$HOME/solps-gui/build/gnuplotWidget

for file in $FILES
do
    moc $file -o moc_$(basename $file .h).cpp
done
if [ ! -d "$SIPDIR" ]; then
  mkdir $SIPDIR
fi

if [ ! -d "$OBJECTS_DIR" ]; then
  echo "no objects dir, craeting it"
  mkdir $OBJECTS_DIR
fi
python3 configure.py --verbose --sipdir="$SIPDIR" --outdir="$OBJECTS_DIR" 

case $(hostname -f) in
  *.iter.org)
	module purge
	module load GCC
	MAKE_JOBS=${MAKE_JOBS:-4}
	;;
  *)
	;;
esac

make -j $MAKE_JOBS
make install
make clean
make distclean
echo "Cleaning up"
rm moc_*
rm -r $HOME/solps-gui/build/gnuplotWidget

rm pyQtGnuplot.so
