SOLPS-ITER GUI
==============

## Build environment

Prepare Python 3, PyQt and ParaView with 

    MAKE_JOBS=4 ./build-pyqt.sh 
    MAKE_JOBS=4 ./build-paraview.sh

Source the setupenv.sh with

    source setupenv.sh
 

## ITER specifics
### CentOS 5.x and xcb
Qt5.x on RHEL5 requires xcb library for X11 rendering instead 
of Xlib and is built from sources and put into staging/lib. 
Newer distros (e.g. RHEL6 on hpc-app1.iter.org) provide xcb.

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

##Install on OSX with homebrew

    brew install qt5
    brew linkapps qt5
    brew install PyQt5 --with-python3
