SOLPS-ITER GUI
==============

## Build environment

Prepare Python 3, PyQt and ParaView with 

    MAKE_JOBS=4 ./build-pyqt.sh 
    MAKE_JOBS=4 ./build-paraview.sh

Source the setupenv.[c]sh for locally built PyQt with

    source setupenv.sh 

or 

    source setupenv.csh
 

## ITER specifics
### CentOS 5.x and xcb
Qt5.x requires XCB library for X11 rendering instead of Xlib.
On RHEL5 XCB is built from sources and put into staging/lib. 
Newer distros (e.g. RHEL6 on hpc-app1.iter.org) provide XCB.

### Documentation building with sphinx
Due to the problems with the installed OpenSSL libraries the following
preloads arerequired to install sphinx (or other PyPI packages):

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

##Install on OSX with homebrew

    brew install qt5
    brew linkapps qt5
    brew install PyQt5 --with-python3
