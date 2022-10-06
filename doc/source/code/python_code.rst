
.. _python-code:

=======================
Python code description
=======================

Main program solps.py
=====================

.. automodule:: solps
   :members:
   :noindex:

Custom widgets and plugins for the Dashboard
============================================

Pairs of custom widgets and plugins for Qt Designer to ease configuration
of the Dashboard by graphical programming by users.

-------
Gnuplot
-------

This widget is an embedded gnuplot inside PySide6, written in Python. With the help of
a simple python wrapper has been made so we can use the embedded gnuplot
inside GUI.

.. automodule:: gnuplot
   :members:
   :undoc-members:

-----------
SOLPS Plots
-----------

.. automodule:: solpsplots
   :members:
   :undoc-members:
   :private-members:

----------
Line input
----------

.. automodule:: lineinput
   :members:
   :undoc-members:
   :private-members:

------------
Tcsh scripts
------------

.. automodule:: tcsh
   :members:
   :undoc-members:
   :private-members:

--------
Director
--------

.. automodule:: director
   :members:
   :undoc-members:
   :private-members:

------
Script
------

.. automodule:: script
   :members:
   :undoc-members:
   :private-members:


------
B2plot
------

.. automodule:: b2plot
   :members:
   :undoc-members:
   :private-members:

----------------------------
Input file editor and viewer
----------------------------

.. automodule:: solpsinput
   :members:
   :undoc-members:
   :private-members:

-------------------
Eirene input editor
-------------------

.. automodule:: eirene
   :members:
   :undoc-members:
   :private-members:

---------------
B2 input editor
---------------

.. automodule:: b2
   :members:
   :undoc-members:
   :private-members:

--------
Add menu
--------

.. automodule:: addmenu
   :members:
   :undoc-members:
   :private-members:

------------
Put edge IDS
------------
This widget reads the geometry and plasma state and creates IDS.
It can be used as a standalone tool too.

.. automodule:: put_edge_ids
   :members:
   :undoc-members:
   :private-members:

------------
Get edge IDS
------------

This widget reads the geometry and plasma state from an IDS and creates a
run directory.

.. automodule:: get_edge_ids
   :members:
   :undoc-members:
   :private-members:

------------
TCSH process
------------

This is a base class for all the widget that requires a TCSH terminal with a
SOLPS-ITER environment. Also for the sake of consistency this widget also
contains signal/slot functions for easier integration inside Qt Designer

.. automodule:: tcsh_process
   :members:
   :undoc-members:
   :private-members:

------
Divgeo
------

This widget starts DivGeo from a SOLPS-ITER project and also docks the widget
inside the GUI.

.. automodule:: divgeo
   :members:
   :undoc-members:
   :private-members:


-----
Carre
-----

This widget runs the carre script in a baserun directory and provides an
interface for communicating with the script

.. automodule:: carre
   :members:

------
Triang
------

This widget runs the Triang script for the user in the baserun directory.
It runs the script triang from ``SOLPSTOP/scripts`` folder.

.. automodule:: triang
   :members:

--------------
Initialize run
--------------

This widget is used to initialize a run from a baserun directory.

.. automodule:: initialize_run
   :members:
   :undoc-members:
   :private-members: