#!/bin/sh -x


FILES="Qt*.h gnuplotWidget.h"
for file in $FILES
do
    moc $file -o moc_$(basename $file .h).cpp
done
python3 configure.py --verbose --sipdir="/home/simicg/solps-gui/staging/share/sip/PyQt5"

make
make install
