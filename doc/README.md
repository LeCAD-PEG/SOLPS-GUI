## Compiling documentation under BASH

Installing local packages at HPC-FS cluster
~~~ bash
echo $0 # should print /bin/bash
module use /opt/pkg/ITER/modules/all/
module load PySide6/6.2.3-GCCcore-10.2.0
module load double-conversion/3.1.5-GCCcore-10.2.0
python3 -m venv local
local/bin/pip3 install sphinx_rtd_theme
~~~

Subsequent runs under BASH
~~~ bash
module use /opt/pkg/ITER/modules/all/
module load PySide6/6.2.3-GCCcore-10.2.0
module load double-conversion/3.1.5-GCCcore-10.2.0
python3 -m venv local
source local/bin/activate
make html
firefox build/html/index.html
~~~

LATeX documentation in addition needs

~~~ bash
module load texlive/20210216-GCCcore-10.2.0
make latexpdf
firefox build/latex/SOLPS-GUI.pdf
env --unset LD_LIBRARY_PATH okular build/latex/SOLPS-GUI.pdf
~~~


## Compiling under tcsh

Under TCSH some infinite loop consuming memory happens when
compiling `python_code.rst` with PySide6/6.2.3 if class 
`Property()` does not contain `doc="Description of the property"`

Using Sphinx module

	module load Sphinx/3.5.2-GCCcore-10.2.0
	module unload SimDB
	make html 

Installing packages
~~~ csh
echo $0 # should print tcsh
python3 -m venv local
local/bin/pip3 install sphinx_rtd_theme
~~~

Subsequent runs under tcsh
~~~ csh
module unload ToFu # and possibly other modules
source local/bin/activate.csh
make html
~~~
