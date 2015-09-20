SOLPS-ITER GUI
==============

## Build environment

Prepare Python 3, PyQt and ParaView with 

    nice MAKE_JOBS=4 ./build-pyqt.sh 
    nice MAKE_JOBS=4 ./build-paraview.sh

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

## Component tracker
See https://jira.iter.org/projects/IMAS?selectedItem=com.atlassian.jira.jira-projects-plugin:components-page
