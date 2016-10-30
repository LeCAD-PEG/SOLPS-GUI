SOLPS-ITER GUI
==============

## Build environment

Prepare Python 3, PyQt and ParaView with 

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

## Running UI

    $ src/gui/solps.py # or simply type "solps" alias

## Buiding documentation

    $ cd doc
    $ make html # for solps_doc alias within "modern" browser
    $ make qthelp # for solps_help alias with assistant
    $ qcollectiongenerator build/qthelp/SOLPSGUI.qhcp
    $ make latexpdf PAPER=a4 # for PDF with TexLive


## ITER cluster specifics
### CentOS 5.x and xcb
Qt5.x requires XCB library for X11 rendering instead of Xlib.
On RHEL5 XCB is built from sources and put into staging/lib. 

### Documentation building with sphinx
Due to the problems with the installed OpenSSL libraries the following
preloads are required to install sphinx (or other PyPI packages):

    LD_PRELOAD=/usr/lib64/libgssapi_krb5.so:/usr/lib64/libz.so \
    pip3 install sphinx

### IMAS build environment
IMAS is not required to build SOLPS-GUI

    module use /work/imas/etc/modulefiles
    module load imas

## Ubuntu 14+ and other distros
XCB development libraries are required for building Qt5.x

    apt-cache search libxcb
    sudo apt-get install libxcb.*-dev
    sudo apt-get install libudev-dev libxi-dev


## Component tracker
See https://jira.iter.org/projects/IMAS?selectedItem=com.atlassian.jira.jira-projects-plugin:components-page

## Install on OS X with homebrew

    brew install qt5
    brew linkapps qt5
    brew install PyQt5 --with-python3
    pip3 install sphinx

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
