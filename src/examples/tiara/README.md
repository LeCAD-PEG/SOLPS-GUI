# TIARA example code

To run GGD example code load the following module load before any make.

   module use /opt/pkg/ITER/modules/all # HPC-FS only
   module load IMAS/3.38.1-4.11.4-foss-2022b-lite UDA/2.6.0

## Directory structure

- Makefile - Prepare local examples into $HOME/Downloads and local environment. make help for more info
- plot_traduit_out_b2us_or_b2fgmtry_examples.tar.gz - Examples of unstructured and structured SOLPS-ITER geometry
- plot_traduit_out_b2us_or_b2fgmtry.ipynb - Notebook for showing geometry examples that should TIARA produce
- plot_traduit_out_b2us_or_b2fgmtry.py - Same as above using PySide6
- ggdtest.ipynb - Plot edge profiles in GGD from TIARA