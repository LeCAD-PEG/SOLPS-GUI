# TIARA example code

To run GGD Notebook example code load the following module load before any make.

   module use /opt/pkg/ITER/modules/all # HPC-FS only
   module load IMAS/3.38.1-4.11.4-foss-2022b-lite UDA/2.6.0


To run interactive Python from command line
   
   source local/bin/activate
   module load PySide6/6.5.2-GCCcore-12.2.0
   module load matplotlib/3.7.0-gfbf-2022b


## Directory structure

- Makefile - Prepare local examples into $HOME/Downloads and local environment. make help for more info
- plot_traduit_out_b2us_examples.tar.gz - Examples of unstructured and structured SOLPS-ITER geometry
- plot_traduit_out_b2us.ipynb - Notebook for showing geometry examples that should TIARA produce
- plot_traduit_out_b2us.py - Same as above using PySide6
- tiara_ggd_to_b2us.py - Reads GGD and saves it into TRADUID.B2US format
- ggdtest.ipynb - Plot edge profiles in GGD from TIARA
