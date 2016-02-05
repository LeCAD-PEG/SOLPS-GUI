.. _setup:

.. highlight:: sh

**************************
Setting up the environment
**************************

Creating SSH host keys
======================

The following commands are needed if you would like to use SOLPS-GUI
network run updates from compute nodes back to the login node via
SSH::

    $ ssh-keygen -t rsa
    $ sh -c 'SOLPS_GUI_IP=$(hostname -i) \
    && SSH_KEY=$(ssh-keygen -F ${SOLPS_GUI_IP}) \
    && test -z "${SSH_KEY}" \
    && ssh-keyscan -t rsa -H ${SOLPS_GUI_IP} >> ~/.ssh/known_hosts'

ITER setup
==========

Tha latest version of the GUI is available by::

   $ module use /work/imas/etc/modulefiles
   $ module load solps-gui
   $ solps #  and "solps -h" should work
   $ solps_doc # for the lastest HTML documentation in a browser

Personal use
============

Users may build their own version by following instructions in README.md
after ``git clone``. Short instructions for building::

    $ git clone ssh://git@git.iter.org/bnd/solps-gui.git
    $ cd solps-gui
    $ ./build-pyqt.sh # It may take several hours to compile!

Starting the GUI::

    $ source setupenv.sh
    $ src/gui/solps.py


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
==================

If submission scripts are not yet available or adapted for running on
target cluster one may revise already available scripts. Basic
``localsubmit`` may be copied from ``solps-gui/src/examples` to
``solps-iter/scripts`` from home directory with::

    $ cp solps-gui/src/examples/localsubmit solps-iter/scripts/
