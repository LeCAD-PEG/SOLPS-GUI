.. highlight:: csh

.. catalyst_:

.. _catalyst-tutorial:

=======================
Using ParaView Catalyst
=======================

With this tutorial we'll show how to instrument the SOLPS-ITER code with
*in situ* visualization using ParaView Catalyst. SOLPS-ITER code needs to be
compiled and linked with ParaView Catalyst libraries.

.. note::   A short video tutorial on the use of the **Catalyst** is
            available `here <https://youtu.be/PQwG3V4f2-U>`_.

Building SOLPS-ITER with Catalyst
---------------------------------
For the *Catalyst demo* we will clone and build a new SOLPS-ITER tree with::

  $ git clone --recursive ssh://git@git.iter.org/bnd/solps-iter.git \
    solps-iter-catalyst
  $ cd solps-iter-catalyst
  $ git checkout feature/IDS
  $ git submodule update
  $ git config --global user.name "John Doe" # Your GIT identity is needed
  $ git config --global user.email johndoe@example.com # to be set only once.
  $ tcsh # if running under bash
  $ source setup.csh
  $ make b25

Basic Catalyst simulation
-------------------------
We will start the default Insitu *live visualization* on
``hpc-app1.iter.org`` login node using only *B2.5 standalone* that is not
built by default.

The following commands copy the case that contains the usual
AUG_16151_D demo with additional ``coproc.py`` file that has hardcoded
``hpc-app1.iter.org`` and port ``22222`` for connecting to ParaView
Catalyst::

  $ stop
  $ cd runs
  $ mkdir catalyst-demo
  $ cd catalyst-demo
  $ cp -av ~kosl/solps-iter-catalyst/runs/AUG_16151_D .
  $ cd AUG_16151_D
  $ correct_baserun_timestamps
  $ cd run_for_GUI_demo

or enter similar run therein, such as::

  $ cd AUG_16151_D/16151_1.6MW_2.0e19_D=0.4_chi=1.6_standalone

Before starting the simulation it is recommended that ParaView Catalyst is
started with :menuselection:`Catalyst --> Connect` and select free port.
This is especially true if several users are running this tutorial at the
same time. One can list already occupied ports on the login node by
issuing::

  $ netstat -ln --tcp | grep -v :: | grep -v 127.0.0 | less

and then selecting a free port in the range from 1025 to 65535
(inclusive). In rare (standalone) cases where a cluster is empty, one
can select the default *Catalyst Server Port* on ``22222``. Otherwise,
one may try another free port.

.. image:: catalyst_1.png
   :align: center

Immediately after starting the Catalyst server the  ``catalyst:`` icon appears
under the ``builtin:`` icon. We will pause the simulation at the first time
step to demonstrate initial conditions by selecting
:menuselection:`Catalyst --> Pause Simulation` that will change the
:guilabel:`catalyst:` icon to

Immediately after starting the Catalyst server the ``catalyst:`` icon
appears under the ``builtin:`` icon. We will pause the simulation at the
first time step to demonstrate initial conditions by selecting
:menuselection:`Catalyst --> Pause Simulation` that will change the
:guilabel:`catalyst:` icon to
 
.. image:: catalyst_2.png
   :align: center

inside the :guilabel:`Pipeline browser`. Before starting the B2.5 simulation
on *remote* compute node(s) we need to adjust the last line of the ``coproc.py``
from ``localhost`` to whatever our :command:`hostname` is. Similarly we should
change *Catalyst Server Port* if default one is already occupied. For example:

.. code-block:: python

   # Live Visualization, if enabled.
   coprocessor.DoLiveVisualization(datadescription, "hpc-app1.iter.org" , 22222)

and then start the simulation with the usual::

  $ rm -f *.prt
  $ itersubmit
  $ qstat -u ${USER} # should show running case for next 5 minutes

EUROFusion-IM users on the Gateway login node *g03* need to setup
``g03.efda-itm.eu`` in :file:`coproc.py` and use :command:`itmsubmit` instead.

.. note::

   The default ``coproc.py`` file can always be copied into run directory from
   ``${SOLPSTOP}/modules/B2.5/src/catalyst/coproc.py`` and placed inside
   run directory to enable Catalyst coprocessing.
   If the ``coproc.py`` file is not provided inside run directory then B2
   will simply run without Catalyst's capabilities.

Immediately after the job starts running from the batch, the code Catalyst
*co-processor* connects back to the *Catalyst server*, which pauses the
code and new :guilabel:`input` icon appears below the :guilabel:`catalyst:`
icon.


.. image:: catalyst_3.png
   :align: center

If you click on the the grayed-out icon nearby the :guilabel:`input` icon
the :guilabel:`Extract: input` extract should appear as

.. image:: catalyst_4.png
   :align: center

and once we click on grayed-out :guilabel:`eye` icon the mesh is shown in
a new :guilabel:`RenderWindow2` as a surface.
If we close :guilabel:`RenderWindow2` and change :guilabel:`Representation`
to *Surface With Edges* with some zooming we see

.. image:: catalyst_5.png
   :align: center

Instead of a :guilabel:`Solid Color` one may select any other B2.5 field
available under the :guilabel:`Coloring` combo box.

Once the simulation is running you may pause it or set the breakpoint time
step. Set the breakpoint with :menuselection:`Catalyst --> Set Breakpoint`
to 5

.. image:: catalyst_6.png
   :align: center

and :menuselection:`Catalyst --> Continue` the simulation that will stop
shortly at time step 5. After some additional inspection of the fields press
:menuselection:`Catalyst --> Continue` to run the simulation to the last
timestep at 1018 timesteps. While running, a live simulation is shown.
If we open :menuselection:`Catalyst --> Set Breakpoint` while simulation is
running, then the time will keep increasing while editing and this can be used
to follow the current state of the simulation and at the end of live
visualisation the following message will occur:

.. image:: catalyst_7.png
   :align: center

The same message occurs if the simulation is killed by the user and
ParaView is ready to accept a connection from the new simulations. If one
needs to change the *Catalyst Server Port* when the simulation is running
then ParaView needs to be restarted!

It is quite fine if one :menuselection:`File --> Exit` the ParaView while
the simulation is running. One can always reconnect by starting ParaView
and :menuselection:`Catalyst --> Connect` back at any time to see the
current state. The graphics pipeline that was created during is preserved
within the *co-processor* state and can be saved for future use while the
simulation is running.

Co-Processing pipeline
----------------------

We will extend default co-processing script to include saving each time
step for later analysis and creation of animation. For that, the
``coproc.py`` pipeline needs to be changed. The easiest way to do that is
by creating and exporting visualisation pipeline shown in the
:guilabel:`Pipeline Browser`.

To create a new pipeline we need to:
 1. :menuselection:`Catalyst --> Connect`
 2. :menuselection:`Catalyst --> Pause Simulation`
 3. :menuselection:`Tools --> Manage Plugins ...` and :guilabel:`Load Selected`
    *CatalystScriptGeneratorPlugin* and  :guilabel:`Close`.
 4. Start the simulation again with::

    $ rm -f *.prt
    $ itersubmit

 5. Once we see the :guilabel:`input`  we click on the icon and select
    :menuselection:`Writers --> Paralel Polydata Writer` from the menu.
    Change default *Property* :guilabel:`File Name` from ``filename_%t.pvtp``
    to ``solps_%t.pvtp`` and :guilabel:`Write Frequency` to 5.

    .. image:: catalyst_8.png
       :align: center

 6. Select :menuselection:`CoProcessing --> Export State`
    and :guilabel:`Next >`.
 7. Check :guilabel:`Show All Sources` and add *input* to proceed with
    :guilabel:`Next >` and retain :guilabel:`Name Simulation Inputs` as input
    by continuing with :guilabel:`Next >`.
 8. Under  :guilabel:`Export State Configuration` check just
    :guilabel:`Live Visualization` and press :guilabel:`Finish` and then
    replace ``runs/catalyst-demo/AUG_16151_D/run_for_GUI_demo/coproc.py``.
 9. Edit last line from ``coproc.py`` and change ``"localhost"`` back to
    "hpc-app1.iter.org" or enter::

    $ sed -i -e s/localhost/hpc-app1.iter.org/ coproc.py

 10. Kill simulation with::

     $ qstat -u ${USER}
     $ qdel Job_ID

 11. We start the simulation once again with
     :menuselection:`Catalyst --> Connect` and issuing::

     $ rm -f *.prt
     $ itersubmit

     that will connect to Catalyst and show new a pipeline. Actually,
     there is no need to start ParaView unless a *live visualization* is
     needed. The files ``solps_%t.pvtp`` will be created anyway as part of
     the co-processor pipeline and will be preserved under
     ``b2mn.exe.dir/``. Those files can be opened at a later time with
     ParaView and played in time. Complete dumps of the code for each time
     step can occupy several GBytes of disk space even for a small
     example.
     
 12. Instead of dumping complete set of variables we create a new pipeline
     while running a live visualization by selecting :guilabel:`input` and
     :menuselection:`Filters --> Alphabetical --> Pass Arrays`.
 13. Select only ``te`` and ``ti`` in filter :guilabel:`Properties`.
 14. Add :menuselection:`Writers --> Paralel Polydata Writer` and
     rename output *File Name*  to ``teti_%t.pvtp`` to get

     .. image:: catalyst_9.png
        :align: center
 15. Repeating simulation once again with::

     $ rm -f *.prt
     $ itersubmit

     we get a new set of files under ``b2mn.exe.dir/`` with a smaller footprint.
 16. To open all ``.pvpt`` files at once created in ``b2mn.exe.dir/`` select 
     :menuselection:`File --> Open` and navigate to ``b2mn.exe.dir/`` in current
     run directory. Open the top ``.pvtp`` file
     (one with plus on the left of file name).
     This will load all time steps into ParaView.

     .. image:: catalyst_10.png
        :align: center

     .. note:: In some cases ParaView fails to load all time steps.
               If that happens close and reopen ParaView and repeat
               the steps above.
               
 17. Now select ``te`` from Active Menu Controls.

     .. image:: catalyst_11.png
        :align: center
 18. To move through time steps use Time Controls on the top of the window.
     We can either move from step to step or play it as an animation.

     .. image:: catalyst_12.png
        :align: center
 19. In order to plot variable ``te`` max  value over time we need to select 
     :menuselection:`Edit --> Find Data`. Select ``te`` and ``is max`` and 
     *Run Selection Query*. To show the plot select *Plot Selection Over Time*.

     .. image:: catalyst_13.png
        :align: center
 20. Select *Close* to close the window. New plot view should open next to the
     the default Render View. To select variables you would like to plot
     (e.g. ``te``) go to :guilabel:`Properties` and scroll down to section
     *Series Parameters* where we can select  variables to plot.
     We can also modify the number of other plot options here.
     Note that you can plot any other statistical parameter instead 
     of max showed in this example.
     
     .. image:: catalyst_14.png
        :align: center
 21. We should now see similar view on the right.

     .. image:: catalyst_15.png
        :align: center
 22. In addition to plotting we can also analyse data with respect to
     position on the grid. To do that select
     :menuselection:`Edit --> Find Data`. To specify
     your own query select :guilabel:`Query` and type ``te  >= mean(te)``.
     Then select :guilabel:`Run Selection Query`.

     .. image:: catalyst_16.png
        :align: center
 23. Now close the window. Cells that meet criteria we specified will 
     be colored pink. When we move through time steps, the selection area will
     change according to the variable values in each time step.
     Again, we can use more meaningful selection criteria and see how
     it changes with respect to time and positon on the grid.

     .. image:: catalyst_17.png
        :align: center
     .. note:: We don't need ParaView running if we already have the desired
               fields extracted with ``coproc.py`` for later analysis,
               visualization and debugging.
 24. In order to present results in standard *eV*, we multiply all
     ``te`` values that are in *Joules* by 6.242e18. To do that we use
     Calculator filter and create new cell data ``Te`` derived from
     ``te``, where ``Te=te*6.242e18`` by

       #. Setting :guilabel:`Expression` to ``te*6.242e18``
          and :guilabel:`Array Name` to ``Te[eV]``.
       #. Selecting :guilabel:`Array Association` to  ``Cell Data``.
       #. After pressing :guilabel:`Apply` coloring can be selected for a
          newly calculated ``Te[eV]``.

     .. note::

        A similar example, but for converting from electron temperature in
        *eV* to *Joules* is described in ReadUALEdge
        :ref:`paraview-python-filter` tutorial.
