SOLPS-ITER GUI
==============

## Build environment

Prepare Python 3, PyQt and ParaView with GCC 4.7+

    ./build-pyqt.sh
    ./build-paraview.sh



One can modify the following environment variables to change
default build procedure:

 - MAKE_JOBS  number of parallel jobs to make
 - STAGING_PREFIX installation destination
 - USE_QT_XCB for newer distros lacking full XCB support

Source the setupenv.[c]sh for locally built PyQt with

    $ source setupenv.sh

or

    $ source setupenv.csh

Optionally after building  PyQt you can build gnuplot 5.2 and embedded gnuplot
in Qt with the following commands:

    source setupenv.sh
    ./build-gnuplot.sh
    cd /src/gnuplot-widget
    ./build-gnuplot-widget.sh

## Running UI

    $ src/gui/solps.py # or simply type "solps" alias

## Buiding documentation

    $ cd doc
    $ make latexpdf PAPER=a4 # for PDF with TexLive
    $ make html # for solps_doc alias within "modern" browser
    $ make qthelp # for solps_help alias with assistant
    $ qcollectiongenerator build/qthelp/SOLPSGUI.qhcp


## ITER cluster specifics
### CentOS 5.x and xcb
Qt5.x requires XCB library for X11 rendering instead of Xlib.
On RHEL5 XCB is built from sources and put into staging/lib.

### IMAS build environment
IMAS is not required to build the SOLPS GUI.

    module use /work/imas/etc/modulefiles
    module load imas
    imasdb solps-iter

## Ubuntu 14+ and other distros
XCB development libraries are required for building Qt5.x

    apt-cache search libxcb
    sudo apt-get install libxcb.*-dev
    sudo apt-get install libudev-dev libxi-dev

## PIP3 packages

   apt-get install libssl-dev liblzma-dev

are required to build pip3 and corresponding Python packages, themes.


## Component tracker
See https://jira.iter.org/projects/IMAS?selectedItem=com.atlassian.jira.jira-projects-plugin:components-page

## Install on OS X with homebrew

    brew install qt5
    brew linkapps qt5
    brew install PyQt5 --with-python3
    pip3 install sphinx sphinx_rtd_theme matplotlib

## User preferences
Preferences of some widgets and settings are stored to allow users
configure the GUI. Size and position of the Main window is saved
when user closes the GUI. At the same time columns position and widths
are stored too. In some cases one wants to start from scratch by
clearing the preferences.
### Clearing user preferences on Linux

    rm ${HOME}/.config/ITER/solps-gui.conf

### Clearing user preferences on OS X

    rm ${HOME}/Library/Preferences/com.iter.solps-gui.plist
    killall -u $USER cfprefsd

## Building on RHEL6 clusters
Some RHEL6 clusters lack full XCB devel support and for that we recommend the
following option to building pyqt:

    USE_QT_XCB=YES ./build-pyqt.sh

## Building Qt (using build-pyqt.sh or build-paraview.sh) on debian stretch (9)
Older versions of Qt ( < 5.9.0) do not support OpenSSL-1.1.0, which is the
only available package for debian stretch to get via command:

    apt-get install openssl

For this you have to install the development packages for older version of
openssl (1.0.x):

    apt-get install libssl1.0-dev

This installs the development files for openSSL version 1.0.2.

## Building interactive Gnuplot widget for Anaconda3
Anaconda3 lacks mkspecs and some other development Qt and PyQt build required
files. To build the Anaconda3 binary-compatible gnuplot and PyQt widget do:

    module load imas binutils
    module unload Anaconda2
    qmake --version && sip -V
    export QT_VERSION=5.6.2 PyQT_VERSION=5.6.2 SIP_VERSION=4.18
    export STAGING_QT=${EBROOTANACONDA3}/pkgs/qt-5.6.2-3
    QT_LIBS=$(pkg-config --libs Qt5Network Qt5Svg Qt5PrintSupport Qt5Widgets\
                Qt5Gui Qt5Core)
    QT_LIBS="-Wl,-rpath=${EBROOTANACONDA3}/lib ${QT_LIBS}"
    export QT_LIBS="-L${EBROOTANACONDA3}/lib -liconv ${QT_LIBS}"
    export GNUPLOT_INSTALL_DIR=/work/imas/opt/gnuplot/5.2.1
    MAKE_JOBS=16 ./build-gnuplot.sh
