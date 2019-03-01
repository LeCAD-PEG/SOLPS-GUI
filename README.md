SOLPS-ITER GUI
==============

## Build environment

Prepare Python 3, PyQt and ParaView with GCC 4.8+

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
On the ITER cluster the following modules and commands are needed
for building documentation (and running SOLPS GUI):

    $ module load Perl/5.20.3-goolf-1.5.16 imas texlive python/3.6/3
    $ cd doc
    $ make install-iter # or use one of
    $ make latexpdf PAPER=a4 # for PDF with TexLive
    $ make html # for solps_doc alias within "modern" browser
    $ make qthelp # for solps_help alias with assistant
    $ qcollectiongenerator build/qthelp/SOLPSGUI.qhcp

One should always build latexpdf before html as HTML includes
generated SOLPS-GUI.pdf

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

Building PyQt based Gnuplot widget with build-gnuplot-widget.sh has been
unsucessful so far.

## Importing IMAS Python modules into local Python
For situations where IMAS library is provided system wide but Python3
is used from local build using setupenv.sh then one can install IMAS
package by

    pip3 install --user --compile ${IMAS_PREFIX}/python/dist/imas*.tar.gz

## Compiling SOLPS-ITER

Scripts have been added for compiling SOLPS-ITER and it's prerequisites into
the same build environment as SOLPS-GUI. Some packages can be installed with
the use of package managers:

Ubuntu 9.6 (stretch):
    apt-get install libncarg-dev libcairo2-dev libfontconfig1-dev \
    libxrender-dev libx11-dev libfreetype6-dev ksh libxslt1-dev openjdk-8-jdk \
    libreadline-dev xsltproc libopenmpi-dev libmotif-dev libnetcdf-dev \
    texlive texlive-latex-recommended texlive-binaries emacs25-bin-common

    apt-get install build-essential

CentOS7:

    yum install epel-release

    yum install ncl-devel cairo-devel fontconfig-devel libXrender-devel \
    libX11-devel freetype-devel ksh libxslt java-1.8.0-openjdk-devel \
    readline-devel libxslt openmpi-devel motif-devel netcdf-devel \
    netcdf-fortran-devel ctags-etags texlive texlive-latex \
    texlive-latex-bin-bin texlive-collection-latexrecommended \
    environment-modules openssl-devel

    yum groupinstall "Development tools"

The configuration of SOLPS-ITER used GNU gcc/gfortran compiler toolchain. Along
SOLPS-ITER other packages are compiled, such as IMAS, OpenBLAS.

To start building the packages, run the following command:

    cd solps-gui
    make solps-iter