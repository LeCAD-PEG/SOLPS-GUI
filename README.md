SOLPS-ITER GUI
==============

## Build environment

Prepare Python 3 and PyQt with 
    nice ./build-pyqt.sh

ParaView build with
    nice ./build-paraview.sh

Source the setupenv.sh with
    source serupenv.sh
 

## ITER specifics
### IMAS build environment
IMAS is not required to build SOLPS-GUI\s\s
    export MODULEPATH=/work/imas/etc/modulefiles:${MODULEFILES}\s\s
 or\s\s 
    module use /work/imas/etc/modulefiles\s\s
    module load imas\s\s

## Component tracker
See https://jira.iter.org/projects/IMAS?selectedItem=com.atlassian.jira.jira-projects-plugin:components-page
