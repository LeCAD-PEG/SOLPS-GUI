.. highlight:: csh

.. ualedgeplugin_:


=================================
Using ParaView ReadUALEdge plugin
=================================

This tutorial covers the basic instructions about running and using
ParaView application [1]_ and how to run and use ReadUALEdge
ParaView plugin on g04.efda-itm.



Introduction to ParaView
-------------------------

ParaView is an open-source, multi-platform application used to visualize
data sets. Here we won't cover the installation process as the all needed
informations including setup guide, tutorials etc. can be found on ParaView
wiki page http://www.paraview.org/Wiki/ParaView and in ParaView Guide
found on http://www.paraview.org/paraview-guide/.

The use of some useful ParaView tools will be covered in ReadUALEdge
plugin chapter.


ParaView ReadUALEdge plugin
---------------------------

ParaView ReadUALEdge plugin is a tool used to visualize and analyze data,
obtained by fusion simulations (electron temperature/density, ion
temperature/density) stored in CPO and/or IDS database.

Here we'll demonstrate how to launch and use the ReadUALEdge plugin using
two different IDS databases, first being shot: ``16151; run: 1000`` [2]_
and  ``shot: 1; run: 1`` [3]_

.. [1] During the time of writing this  tutorial ParaView version 5.1.0
       was used.
.. [2] ``user: kosl; tokamak: aug; version: 4.10a``.
.. [3] ``user: kosl; tokamak: aug; version: 4.10a``. IDS database for
       now doesn't take in those three parameters as the CPO database does.

Note that because we are using IDS database, the following modules
must be loaded using terminal commands::

% module use -a ~dkaljun/imas/etc/modulefiles
% module load imas/develop/3/ual/develop

Additional commands to check available modules etc.::

% module avail imas
% module display imas/develop/3/ual/develop

Loading the plugin
^^^^^^^^^^^^^^^^^^
After launching the ParaView application the start window appears.


.. figure:: images/1_start_window_marked.png
   :scale: 80
   :align: center

   ParaView start window.

The main parts are:

 1. Menu bar
 2. Toolbar
 3. Pipeline Browser
 4. View Browser

Loading and running the ReadUALEdge plugin is done in the next few steps:

 1. Open the *Plugin Manager* by navigating from Menu Bar to
    :menuselection:`Tools --> Manage Plugins`

    .. figure:: images/2_manage_plugins.png
       :scale: 80
       :align: center
 2. In Plugin Manager press the :guilabel:`Load Now` button.