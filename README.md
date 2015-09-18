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
IMAS is not required to build SOLPS-GUI  
    export MODULEPATH=/work/imas/etc/modulefiles:${MODULEFILES}  
 or  
    module use /work/imas/etc/modulefiles  
    module load imas  

## Component tracker
See https://jira.iter.org/projects/IMAS?selectedItem=com.atlassian.jira.jira-projects-plugin:components-page
