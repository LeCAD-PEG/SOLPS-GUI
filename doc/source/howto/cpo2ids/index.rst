.. _cpo2ids-howto:

.. highlight:: csh

=============
CPO2IDS HOWTO
=============

:Author: Dejan Penko and Leon Kos

Our goal was to create a converter which will serve us for data
transfer between the *Edge* CPO and the *Edge_profiles* IDS
database. Test data transfer was done on ``gateway.efda-itm.org`` using two
different CPO databases:

 1. The first being *Shot: 16151; Run: 1000; User: kosl; Tokamak: aug;* 
    converting to IDS database *Shot: 16151; Run: 1000*.
 2. The second CPO database *Shot: 1; Run: 1; User: kosl; Tokamak: iter;* 
    converting to IDS database *Shot: 1; Run: 1*.

This HOWTO is split in two main parts. In the first part
we'll talk about using converter (needed modules, run command etc.)
and in the second chapter about the CPO and IDS data structure and
converting process, where first we will cover subgrids base
information, then geometry regarding the subgrids and lastly values
(as in electron density, electron temperature, ion density and ion
temperature) regarding the subgrids. In each section we'll talk about
data structure and converting the data from CPO to IDS database.

To avoid any confusion with index counting (python, C++ index counting
starts with 0, while in Fortran starts with 1) we'll be using Fortran
counting for the purposes of this working paper, which is also used in
CPO database description.

Using the cpo2ids converter
===========================

In order for the converter to work the following modules must be loaded 
(using terminal on the Gateway cluster where both CPO and IDS UAL modules are installed)::

 $ module use -a ~dkaljun/imas/etc/modulefiles
 $ module load imas/develop/3/ual/develop

Additional commands to check available modules etc.::

 $ module avail imas
 $ module display imas/develop/3/ual/develop

Then to run the cpo2ids converter [1]_  using the command::

 $ python cpo2ids.py --shot=16151 --run=1000 --user=kosl --tokamak=aug --version=4.10a

The *shot*, *run*, *user*, *tokamak* and *verison* variable has to be
correctly defined in order to get access to desired database. The
order of the variables can be random, only the ``python cpo2ids.py``
has to be in the start of the command.  For now for writing to IDS the
*shot* and *run* parameters are the same as of the CPO's. If needed
that can be changed in the future.

When the converter is done the resulting files are stored in
``$HOME/public/imasdb/solps-iter/3/0`` as ``ids_161511000``
(ids_shotNumber_runNumber).

.. [1] cpo2ids.py can be found under SOLPS-ITER/feature/IDS GIT repository
       in directory ``modules/B2.5/src/ids``.

CPO and IDS data structure and converting process explained
===========================================================

Subgrids
--------

What is a subgrid?
^^^^^^^^^^^^^^^^^^

Briefly, grid consists of subgrids[2]_ which represents all data
regarding the Tokamak: geometry and values. The subgrids are the
pieces that give us the whole form and/or split bigger subgrids into
smaller ones. For example, subgrid *Cells* is a whole of subgrids
*Core*, *SOL*, *Inner* divertor* and *Outer divertor*. So, if we are
interested only in tokamak core data, we can choose *Core* subgrid
instead of the *Cells* subgrid, as seen in Fig. \ref{fig:ids_Cells_te}
and \ref{fig:ids_Core_te}.  Subgrids are of different classes. Class 1
is for *nodes*, class 2 for *edges* and class 3 for 2D *cells/faces*.

.. [2] In CPO *subgrid* term is used, while in IDS it's used term *subset*.
