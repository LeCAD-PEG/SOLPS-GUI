.. _setup:

.. highlight:: sh

**************************
Setting up the environment
**************************

The SOLPS GUI can run locally on a laptop or can be installed on a cluster.
The SOLPS GUI can handle multiple SOLPS trees and detached runs. Setting up the
environment is needed depending on the "machine" in use. GUI is developed
on ITER and EUROFusion-IM clusters as well as on local machines running *Linux*
or *OSX* for "personal use".

Running and building the SOLPS GUI can be done under BASH or TCSH shells.
SOLPS GUI runs multiple SOLPS trees by embeding TCSH that is used exclusively
for running SOLPS-ITER.

.. note::
   The SOLPS GUI is included inside SOLPS-ITER ``setup.csh`` on supported
   clusters. From there :command:`solps` command that starts the GUI is
   available directly.

ITER setup
==========

The latest version of the GUI is available on ITER HPC login nodes by::

   $ module load solps-gui
   $ solps #  and "solps -h" should work
   $ solps_doc # for the lastest HTML documentation in a browser

EUROFusion-IM setup
===================

The latest version of the GUI is available on all *Gateway* login nodes by::

   $ module load solps-gui
   $ solps #  and "solps -h" should work
   $ solps_doc # for the lastest HTML documentation in a browser

For using ParaView Catalyst and IMAS plugins the following modules are
available::

   $ module load itm-paraview
   $ module load imas
   $ module load imas-paraview-plugins
   $ imasdb solps-iter

Personal use
============

Users may build their own copies of SOLPS GUI by following instructions
in :file:`README.md` after ``git clone``. Short instructions for building::

    $ git clone ssh://git@git.iter.org/bnd/solps-gui.git
    $ cd solps-gui
    $ make solps-gui # It may take several hours to compile!

.. note::

    You will need at least GCC version 4.7 with many development packages
    to compile PyQt and Python 3+.
    Please read :file:`solps-gui/README.md` for further info on some systems.

Starting the GUI::

    $ source setupenv.sh
    $ solps

you may also compile paraview for using ParaView ReadUALEdge plugin::

    $ cd solps-gui
    $ make paraview-plugin # It may take several hours to compile!

This will compile imas, paraview and the plugin.

Further instructions (optional)::

    $ less README.md
    $ cd doc
    $ make html
    $ module load texlive # if you don't have system pdflatex
    $ make latexpdf
    $ evince build/latex/SOLPS-GUI.pdf

Updating to the latest version of GUI::

    $ cd solps-gui
    $ git pull

Submission scripts
------------------

Submission scripts were tested on ITER and EUROFusion-IM (ITM) clusters and
are part of SOLPS-ITER code. Local submission script :file:`localsubmit`
is also part of the SOLPS-ITER code. If submission scripts are not yet
available or adapted for running on target cluster one may revise already
available scripts. Please revise
:file:`solps-gui/src/examples/submit-scripts/localsubmit` and see
:ref:`submission-howto` for instructions how to setup "batch" processing
on a local machine and :ref:`submission_on_a_cluster` for more details on
cluster submission.