#!/bin/sh -x


FILES="Qt*.h gnuplotWidget.h"
for file in $FILES
do
    moc $file -o moc_$(basename $file .h).cpp
done
if [ ! -d "$HOME/solps-gui/staging/share/sip/PyQt5" ]; then
  mkdir $HOME/solps-gui/staging/share/sip/PyQt5
fi
python3 configure.py --verbose --sipdir="$HOME/solps-gui/staging/share/sip/PyQt5"

make
make install
