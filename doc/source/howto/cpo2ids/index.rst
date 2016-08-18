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
~~~~~~~~~~~~~~~~~~

Briefly, grid consists of subgrids [2]_ which represents all data
regarding the Tokamak: geometry and values. The subgrids are the
pieces that give us the whole form and/or split bigger subgrids into
smaller ones. For example, subgrid *Cells* is a whole of subgrids
*Core*, *SOL*, *Inner* divertor* and *Outer divertor*. So, if we are
interested only in tokamak core data, we can choose *Core* subgrid
instead of the *Cells* subgrid, as seen in :num:`Fig. #ids-cells-te`
and :num:`Fig. #ids-core-te`.  

Subgrids are of different classes. Class 1 is for *nodes*, class 2 for
*edges* and class 3 for 2D *cells/faces*.

.. [2] In CPO *subgrid* term is used, while in IDS it's used term *subset*.

.. _ids-cells-te:

.. figure:: IDS_ReadUALEdge_Cells_Subgrid.png
   :alt: Cells subgrid showing electron temperature values (using IDS database)

   Cells subgrid showing electron temperature values (using IDS database).


.. _ids-core-te:

.. figure:: IDS_ReadUALEdge_Core_Subgrid.png
   :alt: Core subgrid showing electron temperature values (using IDS database)

   Core subgrid showing electron temperature values (using IDS database).

Subgrids structure in CPO database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In CPO database, subgrid base parameters and indices regarding nodes,
edges and cells are stored in ``edge.grid.subgrid(i)``, as seen in
:num:`Fig. #cpo-grid`, where ``i`` is **subgrid base index** going
from *1..n*, where *n* is sum of all subgrids.

The ``.subgrids`` subdata holds subgrid name in ``.id`` and
**list of indices**, as seen in :num:`Fig. #cpo-subgrids`, either in
**range** form found in ``.list(1).indset(1).range`` or **list**
form found in ``.list(1).ind(j)`` together with **subgrid class**
located in ``.list(1).cls`` (1 for nodes, 2 for edges and 3 for
cells) as seen in :num:`Fig. #cpo-list`, where *j* is number of all
indices for given subgrid.

The found indices correspond to the “main” subgrid of the same class.
For example, *Core* of subgrid class 3 corresponds to the main subgrid
of the same class *Cells*. Other “main” subgrids are *Nodes* for class
1 subgrids and *Edges* for class 2 subgrids.

.. _cpo-grid:

.. figure:: images/edge_xsd_Element_grid.png
   :alt: CPO *grid* structure

   CPO *grid* structure

.. _cpo-subgrids:

.. figure:: images/utilities_xsd_Element_subgrids.png
   :alt: CPO *subgrids* structure

   CPO *subgrids* structure

.. _cpo-list:

.. figure:: images/utilities_xsd_Element_list.png
   :alt: CPO *list* structure

   CPO *list* structure

Subgrids structure in IDS database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

IDS subgrid base parameters, used to determine geometry data of
subgrids, are stored in location
``edge-profiles.ggd(1).grid.grid-subset(i)``, where ``i`` is **subgrid
base index** going from, the same as in CPO, ``1...n``, where ``n`` is
sum of all subgrids, as seen in :num:`Fig. #ids-grid`.

.. _ids-grid:
.. figure:: images/dd_edge_profiles_edge_profiles_time_slice0.png

   IDS *grid* structure

It holds **subgrid name** in ``.identifier.name`` and additional info
**subgrid base index** in ``.identifier.index``, as seen in
:num:`Fig. #ids-subset` and :num:`Fig. #ids-identifier`.

.. _ids-subset:
.. figure:: images/dd_edge_profiles_generic_grid_dynamic_grid_subset.png

   IDS *subset* structure

.. _ids-identifier:
.. figure:: images/dd_edge_profiles_generic_grid_dynamic_grid_subset2.png

   IDS *identifier* structure


Furthermore, as seen in :num:`Fig. #ids-element` and
:num:`Fig. #ids-dimension` in ``.element(1).object(1).dimension`` it
holds **subgrid class** and in ``.element(1).object(1).index`` it
holds **subgrid object index**, used to navigate to subgrids geometry
data, which will be covered later.

.. _ids-element:
.. figure:: images/dd_edge_profiles_generic_grid_dynamic_grid_subset_element.png

   IDS *element* structure   

.. _ids-dimension:
.. figure:: images/dd_edge_profiles_generic_grid_dynamic_grid_subset3.png

   IDS *dimension* structure

In IDS we have one new important parameter found in
``.element(1).object(1).index``. It holds **subgrid class object
index**, which is ``1...n``, where ``n`` is sum of all subgrids of
certain class, and it’s one of important parameters used to determine
location of geometry data on IDS database for each subgrid.

Another difference is, while CPO database in ``subgrid(i). ...``, as
previously explained, holds also list of indices for given subgrid,
the indices in IDS database are instead stored “close” to geometry
data, which we’ll cover later.

Converting subgrid subdata set from CPO to IDS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Regarding the previously explained CPO and IDS database structure,
transferring subgrid data from CPO to IDS database is done by
transferring data from

-  | CPO: ``edge.grid.subgrid(i).id`` to
   | IDS: ``edge-profiles.ggd(1).grid-subset(i).identifier.name``

-  | CPO: ``edge.grid.subgrid(i).list(1).cls`` to
   | IDS:
     ``edge-profiles.ggd(1).grid-subset(i).element(1).object(1).dimension``

in addition, while converting we add

-  | IDS: ``edge-profiles.ggd(1).grid-subset(i).identifier.index``
   | = ``subgrid-base-index``

-  | IDS:
     ``edge-profiles.ggd(1).grid-subset(i).element(1).object(1).index``
   | = ``subgrid-class-object-index``

where ``i`` is **subgrid base index**.

Geometry and nodes
------------------

Main data of our geometry represent the ``nodes/points``. Edges and
faces/cells are constructed using nodes.
