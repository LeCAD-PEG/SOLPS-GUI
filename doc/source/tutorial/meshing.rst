.. highlight:: csh

.. _meshing:


=======================
Meshing toolchain C-mod
=======================

.. note::   A short video tutorial on the **Meshing toolchain** is
            available `here <https://youtu.be/MtwH4vPCVic>`_.

DivGeo
======


In this tutorial we will use *DivGeo* and *Carre* to prepare the C-Mod tokamak
geometry. The model will be later used for creating a mesh. Each input file
used for creating the DivGeo model should be located in the ``baserun`` run
directory. The following commands repare the ``baserun`` input data needed for
this tutorial::

     $ stop
     $ cd runs/examples
     $ cmake . && make # Fetches all examples from external repository
     $ tar xvzf tutorial-DivGeo_C-Mod.tar.gz
     $ cd tutorial-DivGeo_C-Mod/baserun

The EFIT equilibrium file  ``baserun/g.990429019.00940`` in this example
describes a C-Mod tokamak lower single-null shot number 990429029 at 940 ms
of the the discharge.
Since DivGeo cannot read the EFIT format equilibrium file directly the EFIT
format is needed to be transformed to DivGeo equilibrium format with::

    $ e2d g990429019.00940 g990429019.00940.equ

To have smoother contouring in the grid generator, we should increase the
resolution of the equilibrium data. Using higher resolution equilibrium avoids
us some problems when the fluid grid is generated::

    $ d2d g990429019.00940.equ g990429019.00940.x2.equ

The the wall geometry file ``baserun/wall_geometry_990429019.ogr`` lists the
R, Z points in the machine coordinates and describes the layout of the plasma
facing components. The points are in `mm` and must form a closed polygon,
i.e. the first and last points must be the same.

*DivGeo* can be started inside SOLPS GUI. The procedure is as follows. First
start SOLPS GUI. SOLPS GUI will open with the **runs** tab.

.. image:: divgeo_1a.png
   :align: center

The ``baserun`` directory must be located under the
``${SOLPSTOP}/runs/examples/tutorial-DivGeo_C-Mod/`` directory for SOLPS-ITER
to work correctly. Moreover, the top directory ``${SOLPSTOP}/runs`` needs to
be listed in the :menuselection:`&Settings --> &Runs`, such as shown in the
following image:

.. image:: divgeo_1b.png
   :align: center

Next select the correct device for environment variable ``DEVICE``. To do this
click on :menuselection:`&Settings --> Preferences`. You will see a group
called **Environment variables** and in it *DEVICE*. There is a dropdown widget
in which you can either select or add the device variable. In this case either
select *cmod* or write *cmod* inside the edit area.

.. image:: divgeo_1c.png
   :align: center

Now select your ``baserun`` folder in :menuselection:`&Runs` tab and click
ont the :guilabel:`&Populate Baserun` tab. Click inside the DivGeo area to
start DivGeo. If you wish to dock it into SOLPS GUI, click once again inside
DivGeo area after DivGeo appears in standalone window.

.. image:: divgeo_1d.png
   :align: center

Additionally the ``tutorial-DivGeo_C-Mod/`` contains DivGeo files for different
stages in the tutorial in preparing the DivGeo model for the C-mod tokamak.
This way you can either start from beginning or from any point of the steps.

Make sure that when you either load a DivGeo file or start a new, to then save
it to the ``baserun`` directory, alongside the equilibrium file.

Import the vessel wall description
----------------------------------

The wall geometry file is located in the ``baserun`` directory.
Import the vessel wall description by opening
:menuselection:`&File --> &Import --> &Template` and load the
``wall_geometry_990429019.ogr`` file, which should be listed in the
Template dialog box.

Press :kbd:`CTRL+P` to fit the wall data to the workspace. If you cannot see
the wall, then use the :menuselection:`&View --> &Display` and make sure that
the :guilabel:`Template` radio button is pressed.

.. image:: divgeo_2.png
   :align: center

Import magnetic equilibrium data
--------------------------------

The magnetic equilibrium file is located in the ``baserun`` directory. Import
the magnetic equilibrium data by opening
:menuselection:`&File --> &Import --> &Equilibrium` and load the
``g990429019.00940.x2.equ`` file, which should be listed in the Equilibrium
dialog box.

If you cannot see the equilibrium displayed as blue (SOL) and red (core and PFR)
rectangles after it is loaded, then use :menuselection:`&View --> &Display`
and make sure that the :guilabel:`Equilibrium` radio button is pressed.

.. image:: divgeo_3.png
   :align: center

.. note::
   This step is available in ``step_1_import_wall_equi_topology.dg``

Converting the wall segments to geometry elements
-------------------------------------------------

To set the surface normals click
:menuselection:`&Command --> &Convert --> Template to elements`. The short pink
lines, which indicate the normal surfaces, will appear.

.. image:: divgeo_4.png
   :align: center

It is very important that all surface normals are pointing away from the
plasma. This convention is required by later steps in the grid triangulation
and input build-up process. To reverse them can set the middle mouse button to
`"Reverse normals”`. Then click :kbd:`Shift + Reverse normals` (middle
button) somewhere on the vessel wall and all of the normals should flip.

.. image:: divgeo_5.png
   :align: center

.. note::
   This step is available in ``step_2_reverse_normals.dg``

Setting the magnetic topology
-----------------------------

In DivGeo is very easy to choose which kind of magnetic topology the
modelling grid should have. You can choose it by opening
:menuselection:`&File --> &Import --> To&pology` and choose one of:

   1. SN lower single-null
   2. SN-up upper single-null
   3. DDN disconnected double-null, lower primary x-point
   4. CDN connected double-null
   5. DDN-up disconnected double-null, upper primary x-point

.. image:: divgeo_6.png
   :align: center

For C-Mod case select SN. The separatrix will be marked in a red line if the
topology is applied correctly.


Defining the extent of the targets
----------------------------------

The target definitions need to satisfy the following rules:

    1. Each target segment needs to have a short wall element at each end,
       which will not be part of the target, but will be used to separate the
       target from the main wall in a subsequent setup step;
    2. the targets must be closed polygons;
    3. the surfaces normals of the closed polygon must all point inward;
    4. the plasma-wetted part of the target must consist of at least two (2)
       wall elements.

In the C-Mod case first condition is not satisfied, therefore, a short segment
needs to be added. To add the short segments change the assignment of the
middle mouse button to `"Split element"`, and then click on the vertical
segment just above the target, which adds a point on the wall and creates a
new segment.
Avoid making very short segments, which can cause problems for the triangle
grid generator.

.. image:: divgeo_7.png
   :align: center

The second condition requires a closed polygon, therefore it is necessary to
add a point behind the target and then connect it to the existing points at the
ends of the target. To create a point, click
:menuselection:`&Edit --> &Create --> &Point` and create a point with the
coordinates: ``(400, -500)``.

.. image:: divgeo_8.png
   :align: center

Then, change the middle mouse button to `"Connect points”`,
:kbd:`middle-click` on the new point and drag the cursor to one end of the
target and release the mouse button. Connect the new point to the second end
as well.

The same thing is done for the outer target. The first and the second
conditions should be satisfied as was done for the inner target.

.. image:: divgeo_9.png
   :align: center

.. note::
   This step is available in ``step_3_defining_targets.dg``

Setting the "Structure" variable for "Structure"
------------------------------------------------

The structure variable is the primary definition for the vessel wall. You can
define the vessel wall by opening :menuselection:`V&ariables --> Structure`

Use the right mouse button (assigned to Mark) to select all segments except the
short segments that are just outside the targets. Using SHIFT+right click will
help a lot. Right clicking on a selected segment will un-select it.

.. image:: divgeo_10.png
   :align: center

Use the right mouse button (assigned to Mark) to select all segments. Using
:kbd:`SHIFT+Right Click` will help a lot. Right clicking on a selected
segment will un-select it. When the highlighting is complete, left-click on
`"Set"` in the `"Structure"` dialogue box, at the end of the line marked
`"Structure"`.

:kbd:`CTRL+U` to unmark everything.

As the same like the structure you can set the targets. Mark all of the
segments for the inner target and then click on `"Set”`. Do not include the
segments that are behind the target.

.. image:: divgeo_11.png
   :align: center

The same steps are used for setting the outer target.

.. image:: divgeo_12.png
   :align: center

.. note::
   This step is available in ``step_4_structure.dg``

Setting elements that are to be ignored by EIRENE
-------------------------------------------------

You can select which parts should EIRENE ignored, by opening
:menuselection:`V&ariables --> &Add --> &Elements not for Eirene`. Mark
the elements behind the targets and click `"Set”`.

.. image:: divgeo_13.png
   :align: center

Setting the elements that are used by B2plot
--------------------------------------------

Defining the wall surfaces that will be written to the mesh.extra file, that
defines the wall specification in B2plot, can be done opening the
:menuselection:`&Variables --> &Add --> &Input to b2plot`

Mark everything except the segments behind the targets.

.. image:: divgeo_14.png
   :align: center

.. note::
   This step is available in ``step_5_notforEirene_b2plotinput.dg``

Setting the target specifications
---------------------------------

Target specification #1
~~~~~~~~~~~~~~~~~~~~~~~

Click on :menuselection:`V&ariables --> Target specification --> #1`

#1 is the inner target for this case. The target index as a function of
magnetic topology is as follows:

+------------+------------+-----------+-----------+-----------+
| Topology   | Target #1  | Target #2 | Target #3 | Target #4 |
+------------+------------+-----------+-----------+-----------+
| SN-down    | HFS        | LFS       |           |           |
+------------+------------+-----------+-----------+-----------+
| SN-up      | LFS        | HFS       |           |           |
+------------+------------+-----------+-----------+-----------+
| DN         | HFS-down   | HFS-up    | LFS-up    | LFS-down  |
+------------+------------+-----------+-----------+-----------+

The target numbering must follow the order of the B2.5 grid indices, which
increase as one goes around the core plasma in a clockwise direction.

Mark the upper-most segment on the inner target, which is in the Scrape-Off
Layer, and click "Set" for "SOL edge" as shown in the following figure.

.. image:: divgeo_15.png
   :align: center

Mark the segment that defines the lower extent of the target , and click
"Set" for "PFR edge".

.. image:: divgeo_16.png
   :align: center

Change "Target material" to Mo for this case, to match the C-Mod target
material, and click "Set". Assign "Chem. sput." (chemical sputtering) to 0,
and click "Set".

Target specification #2
~~~~~~~~~~~~~~~~~~~~~~~

Click on :menuselection:`V&ariables --> Target specification --> #2`

The outer target is less straightforward and then inner target for this case.
The "edge" settings for the targets have to intersect the outer radial boundary
of the grid, but it’s not obvious where the SOL radial boundary edge will be at
this stage.

.. tip::

   Set the middle button to "Add surface".

   The outer radial extent of the SOL is set by the first intersection between
   a flux surface and the main chamber wall ("tangency point"), which will be
   near the inner midplane for this case.

   Hold the middle button down at the inner midplane and the flux coutour will
   appear, and you can see where it maps to at the outer target; see the figure
   on the right. Set "SOL edge" to this segment. (Note: You can accidentally
   add a surface in the core if you’re not careful with your clicking. Press
   :kbd:`Ctrl + Z` for undo if this happens.)

.. image:: divgeo_17.png
   :align: center

For "PFR edge", the segment indicated in the right-most figure is not the same
as the lower-, outer-most segment included when the Structure variable was set
for the outer target – this is OK. The "PFR edge" is only set based on where
the radial boundary of the grid will be, as determined by intersection with the
divertor knee.

.. image:: divgeo_18.png
   :align: center

Assign the *Mo* as the material and turn off *chemical sputtering*.

.. note::
   This step is available in ``step_6_target_specification.dg``

Poloidal grid points
--------------------

The poloidal distribution of cells on the Carre grid are set by the
`"poloidal grid points”` in DG. These are defined separately for the
divertor legs and the SOL.

Click :menuselection:`&Edit --> &Create --> &Grid points`.

Set the Zone to Inner divertor and Cells to 18. The distribution of the cells
can be adjusted by left-clicking and dragging the black line on the plot.
Then click Create to update the workspace. Repeat for the outer divertor. Set
48 points in the SOL, with a roughly uniform distribution of points. The
spacing of the grid points around the x-point should be symmetric.

.. image:: divgeo_19.png
   :align: center

Repeat for the outer divertor.

Set 48 points in the SOL, with a roughly uniform distribution of points
(a straight line on the grid point distribution plot).

The spacing of the grid points around the x-point should be symmetric. Meaning
that set the grid points for SOL, click the :guilabel:`Reset` button and assign
48 cells.

.. image:: divgeo_20.png
   :align: center

.. note::
   This step is available in ``step_7_grid_points.dg``

Radial surfaces
---------------

The radial surfaces in DG define the boundaries between rings on the Carre
grid.
Click :menuselection:`&Edit --> &Create --> &Surfaces...`

Set 18 surfaces in the SOL.

Adjust the radial distribution to give higher spatial resolution near the
separatrix.

.. image:: divgeo_21.png
   :align: center

.. note::
   This step is available in ``step_8_radial_surfaces_a.dg``

There is an issue in the PFR for this particular case: the flux surface which
is tangent to the "knee" will miss the bottom of the outer target and cross the
entrance to the "plenum" in the sub-divertor.

.. tip::

   Create a virtual structure in the PFR volume, which will cause DG to reduce
   the radial extent of the grid.

   Set the middle mouse button to "Add surface" and identify the flux surface
   which intersect the bottom of the outer target.

.. image:: divgeo_22.png
   :align: center

For this C-Mod case, add three points: ``(550,-450)``, ``(550,-460)``, and
``(525,-460)``. (:menuselection:`&Edit --> &Create --> &Point...`)

Make sure the surface normals point inward, using "Reverse normals" with the
middle button, if required.

Add the new surfaces to the "Elements not for Eirene" variable – there should
now be 6 segments in the list (the PFR triangle and the three surfaces that
are behind the targets).

.. image:: divgeo_23.png
   :align: center

Add the new surfaces to the "Structure" variable – there should now be 87
segments in the list.

.. image:: divgeo_24.png
   :align: center

.. note::
   This step is available in step_8_radial_surfaces_b_virtual_structure.dg

Set 18 surfaces in the PFR.

.. image:: divgeo_25.png
   :align: center

.. note::
   This step is available in  ``step_8_radial_surfaces_c_pfr.dg``

For the core region it is necessary to add a surface which will define the
extent to which the grid penetrates into the core.

Assign "Add surface" to the middle mouse button.

Middle-click and hold somewhere in the core, and release the mouse button when
happy with the location of the inner radial boundary.

.. image:: divgeo_26.png
   :align: center

The number of radial surfaces in the core must be the same as for the PFR, i.e.
18 in this case, using :menuselection:`&Edit --> &Create --> &Surface(s)...`

.. image:: divgeo_27.png
   :align: center

.. note::
   This step is available in  ``step_8_radial_surfaces_d_core.dg``


Setting the shadowing structure
-------------------------------

The shadowing structure is the set of physical wall elements that can receive
light from the plasma (or its reflections). It is used to compute the radiative
contribution to the wall heat loads.

Click :menuselection:`V&ariables --> &Add --> Shadowing structure`

First unselect everything with :kbd:`Ctrl + U`

Mark all the segments likely to receive light from the plasma. The shadowing
structure must be continuous and closed.

.. image:: divgeo_28.png
   :align: center

.. note::
   This step is available in  ``step_9_shadowin_structure.dg``

Adding some core radiation
--------------------------

To include core radiation in the wall heat loads, one needs to specify the
amount of core radiation (in `MW`).

Click :menuselection:`Variables --> Add --> Radiation sources`

Enter in the "Radiated Power" field the amount of core
radiation (in "MW") then need to specify the location from where this core
radiation is emitted.

This is done by providing a set of point sources. The radiated power will be
spread evenly among these point sources. You create them by clicking
:menuselection:`&Edit --> &Create --> &Source` and specify the X and
Y coordinates (in `mm`) of the point source location. You may input as few
or as many point sources as you’d like. The point sources (if you choose to
display them) are shown as white asterisks in the DG model.

.. image:: divgeo_29.png
   :align: center

.. note::
   This step is available in  ``step_10_radiation_sources.dg``

Defining "plot zones"
---------------------

The "plot zones" are a set of walls on which the power load, including the
contrabutions from the plasma particles, Eirene neutrals and radiation can
be computed by b2plot. You add them by clicking
:menuselection:`&Variables --> &Add --> &Plot zone`

Unselect everythin with :kbd:`Ctrl + U`

and mark the set of elements that you want to include in the plot zone.

.. image:: divgeo_30.png
   :align: center

Mark the "Starting element", i.e. the first element of the plot zone set, such
that, as you travel along the plot zone set, the plasma is to your LEFT.

.. image:: divgeo_31.png
   :align: center

Give the zone a label (`Zone-label`) that will be used in
the files created by b2plot (8 characters maximum, no spaces, stars or
ellipses).


Configuring the plasma species to be included in the simulations
----------------------------------------------------------------

It is very important to definite plasma species which are included in the
simulations. You definite them by clicking
:menuselection:`Variables --> Plasma species D`.

.. image:: divgeo_32.png
   :align: center

.. note::
   This step is available in  ``step_11_plot_zone_and_plasma_species.dg``

Also you can add it the impurity species with clicking
:menuselection:`Variables --> Add --> Plasma species`.
DG recognizes a few "generic” species: H, D, T, He, Be, C, N, Ne, and Ar,
for which a full consistent default set of reactions will be provided by
Uinp. For all other elements, Uinp will look for the corresponding ADAS
ionization and recombination rates, and, if present in your database, will
include them as part of your model.

If one wishes to use a different reaction set than the default, one can
instead choose to load the reactions from an AMDS file, using:
:menuselection:`&Variables --> &Add --> &Reference to AMDS`
and giving the name of the AMDS file requested. The number of AMDS files to
be loaded is not limited. These files are to be found in the::

    $SOLPSTOP/modules/AMDS directory.


One can also specify a simple boundary condition of either flux or value for
the density of the highest ionization charge state of that species along the
core boundaries.

EIRENE setup of the "void" regions outside the Carre grid
---------------------------------------------------------

EIRENE will use a triangle grid in regions that are outside the fluid grid,
and this variable defines the zones for the triangle mesh generator.

Mark all of the main chamber elements, including the "SOL edge” segments for
the targets. :menuselection:`&Variables --> &Add --> &TRIA-EIRENE parameters`

Set index to -1 in the dialogue box, and :kbd:`"General Triangle size”`
to 10.0, which will generate large triangles. The negative index indicates
that a mesh should be generated inside the marked region, and a positive
value means the opposite.

.. image:: divgeo_33.png
   :align: center

Press kbd:`Ctrl + U` to unmark everything.

Mark the the wall segments in the PFR, including the "PFR edge" elements. Set
index to -2 in the dialogue box, and "General Triangle size" to 10.0.

.. image:: divgeo_34.png
   :align: center

.. note::
   This step is available in  ``step_12_tria-eirene-parameters.dg``

Local refinement of the EIRENE triangle grid
--------------------------------------------
With DG it’s possible to increase the spatial resolution on sub-regions of the
triangle mesh, i.e. the PFR. You can add it by clicking
:menuselection:`&Variables --> &Add --> &Mesh Refinement Zones`

Select wall elements that bound the region of interest (left-right,
top-bottom), as shown on the right, and click "Set" for "Region
identification". Set "Desired side length" to the desired characteristic
scale size of the triangles in this region.

.. image:: divgeo_35.png
   :align: center

.. note::
   This step is available in  ``step_13_mesh_refinement_zone.dg``

Choose the toroidal approximation
---------------------------------

To set the toroidal approximation you need to set the `"Major Radius"` to a
negative (real) number, such as -1.0, if you want to use the toroidal
approximation instead of the cylindrical approximation.

:menuselection:`Variables --> Global Eirene Data`

.. note::
   This step is available in  ``step_14_prepared_for_carre_and_triang.dg``

Write the output data files that are needed by later steps
----------------------------------------------------------

With the :menuselection:`Commands --> Check variables` you can check if all
variables have valid values.

Hopefully you see this at the bottom of the screen:

  All variables have valid values

Then click on:

  1. :menuselection:`Commands --> Rebuild Carre objects`
  2. :menuselection:`File --> Save`
  3. :menuselection:`File --> Output`

The last command will create three files:

  - **<DG_model_name>.dgo**, the DG "output" file
  - **<DG_model_name>.str**, the "structure" file (used by Carre)
  - **<DG_model_name>.trg**, the "targets" file (used by Carre)

And you are set to go to the next part of tutorial.

Carre
=====

Now that we have prepared our DivGeo model, the next step is creating the
plasma grid using Carre.

Switch to Carre tab in SOLPS-GUI.

.. image:: carre_1.png
   :align: center

This tab is grouped into two sections, upper and lower half. The upper half
is self assessment of Carre for the current baserun. Checkboxes, which are
clickable tells the user which steps were already run and the *DG model* drop
down button tells us which DivGeo model has been used to create the plasma
grid.

.. note::

  If the list does not contain a DG model, you have to rescan the baserun dir
  with clicking the :guilabel:`Update DG list`.

The lower half is the interface to the Carre. On the left side are control
buttons and on the right we have a log window which shows us the output of
Carre. Underneath the log window we have the response widgets for Carre. The
manual input button spawns an **input dialog** in which we will write the
parameters value when needed and the *Yes* and *No* button are used for yes/no
(y/n) questions, given by Carre.

Starting Carre
--------------

Before starting carre we must first select our *DivGeo model*, we created
previously. Simply click on the drop down button under ``DG model`` and there
should be the name of our *DivGeo model*, ``C-mod_g990429019_00940.dg``.
Click on it so it is selected.

The reason why this must be done is that for the first time a linking
has to be made against the *DivGeo model*, so that the proper files and their
formats are copied to the correct locations.

For more information search the ``solps-iter/scripts`` folder and run the
``lns`` script.

Now we can click the button :guilabel:`Start Carre` to start Carre. This will
take a while since the environemnt of *SOLPS-ITER* has to be loaded to a TCSH
shell before Carre can be started.

Notice that the ``lns`` check box was ticked. Whenever you will want to redo
the linking with ``lns`` just untick it before clicking
:guilabel:`Start Carre`.

After a while the following output should be shown in the log window.

.. image:: carre_2.png
   :align: center

Prepare
-------

This step reads the DG files and translates them into the format needed by
Carre.

Click on widget :guilabel:`Prepare`. If there is no error the output should be
as in the following figure

.. image:: carre_3.png
   :align: center

Now we click on the checkbox :guilabel:`Prepare`.

.. image:: carre_4.png
   :align: center

Gridding step
-------------

Click the :guilabel:`Grid`. Soon a first question will appear, whether the *X-*
and *O-* points identified by Carre are correct (they usually are). If they are
not, then, you refuse the selection and indicate yourself which of the extrema
are *X-* and *O-* points.

.. image:: carre_5.png
   :align: center

To accept click on the :guilabel:`Yes` widget.

Grid parameter selection step
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Carre then provides a table of parameters. Please refer to Chapter 8 of the
SOLPS-ITER manual for a full description. Carre attempts to provide a grid
that must satisfy three criteria simultaneously:

1. The grid cells must be as locally orthogonal as possible
2. The grid cells must align with the targets in their vicinity
3. The size of neighboring grid cells must not vary too quickly.

The specific definitions of these criteria and their respective weights can be
found in the original Carre paper, which you will find at:
``$SOLPSTOP/modules/Carre/doc/Carre_Paper.pdf``. In some instances, it is
relatively easy to find a satisfactory solution meeting these three criteria,
but this is not always the case, especially in geometries where the targets
are almost parallel to the flux surfaces, putting criteria 1 and 2 at odds with
one another.

Quickly, the data provided in the Carre table indicates the poloidal spacing of
the grid points along the separatrix segments (check the Carre paper for their
numbering convention), the radial spacing of the successive flux surfaces as
one steps away from the separatrix (again, the numbering convention is given in
the Carre paper), the penetration depth of the grid (*pntrat*), the guard
lengths (i.e. the vicinity over which criterion 2 above is applied, in meters),
and some numerical parameters used for the optimization algorithm that attempts
to build the mesh.

The poloidal spacings are deduced from the distribution of grid points chosen
in DG. The guard lengths are given by the "*CARRE guard length*"" parameters in
the DG "*Target specifications*". The *pntrat* value is obtained from the
innermost DG surface chosen in the core.

Carre criterion checks
~~~~~~~~~~~~~~~~~~~~~~

Often, the first pass at the Carre grid parameters will not pass internal
muster. Carre checks for a few minimal requirements:

 - The poloidal grid spacing must be above a minimal threshold, defined by the
   pasmin parameter. This is not enforced by DG and is the most common
   correction you’ll have to make.

 - The radial and poloidal grid spacings in each region must have the same sign.
   The spacings are constrained by the first and last values of the region to
   grid and the total interval length.

Modifying the Carre parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From the log window the following output should be seen

.. image:: carre_6.png
   :align: center

The are more parameters printed if you scroll up, but no errors were reported.
If you would accept them by pressing :guilabel:`Yes`, the following text would
be displayed in the log window

.. image:: carre_7.png
   :align: center

As the error message says the grid parameters describing the grid are too fine
in the radial direction. If you pressed :guilabel:`Yes`, then you would have to
click on the :guilabel:`Grid` again to start the process again; that is saying
yes to the *X-* and *O-* points.

Now instead of pressing :guilabel:`Yes`, press :guilabel:`No`, then Carre will
ask us for input, to change the grid parameters.

.. image:: carre_8.png
   :align: center

Now if you scroll up to the part that says
``RADIAL DISTRIBUTIONS FOR EACH REGION``, you will see that the parameters
``deltr1(1)`` for region 1, ``deltr1(2)`` for reagion 2 and ``deltr1(3)`` for
region 3 are too small.

.. image:: carre_9.png
   :align: center

So now we click on :guilabel:'Terminal input', which shows a dialog in which
we will write:

   deltr1(1)=0.001
   deltr1(2)=-0.001
   deltr1(3)=-0.001
   end

.. image:: carre_10.png
   :align: center

And click on ``Ok``. Then Carre again asks us if we wish to accept the values.
We Click on the widget :guilabel:`Yes`.

Now we will get no error message but instead the following output

.. image:: carre_11.png
   :align: center

Now we check the check box for *Grid*, as we have completed this step.

.. image:: carre_12.png
   :align: center

Producing the grid
~~~~~~~~~~~~~~~~~~

A more indepth of what does the step ``Grid`` do.

After clicking :guilabel:`Yes` for grid parameters Carre then proceeds, one
region at a time (*ireg* index), to build the flux surfaces (*ir* index) in
order, stepping from the separatrix outward.

Normal output looks like:

| ireg= 1
| ir= 2
| ir= 3
| ir= 4
| ir= 5
| ir= 6
| ...
| ir= 7
| ir= 8
| ir= 9
| ir= 10
| ir= 11

However, this is not always the case. If the Carre algorithm fails to converge
while building the flux surfaces, you will get a (non-fatal) error message that
allows you to continue, but suggests some possible changes to the gridding
parameters that might improve convergence, although it may not improve the
"*quality*" of the final grid.

You may also get a fatal error message that indicates that Carre was not able
to build the next flux surface. This usually occurs because the radial spacings
required are too small compared to the resolution of the magnetic equilibrium
provided (fix this by refining the equilibrium a further step, using d2d, or
by increasing the minimal radial spacings by modifying the deltr1 and deltrn
parameters). Sometimes, this is because the limiting structures in the DG
structure are so small that they may stepped over as Carre moves from one flux
surface to the next, and can be fixed by going back to the DG model and
making this limiting structures bigger (a few cm is usually sufficient).

Saving the grid parameters
--------------------------

If you wish to remember the settings change you made, click the
:guilabel:`SaveChoice` button. The grid parameters are then written in the
**carre.dat** file. If you wish to re-use these parameters, skip the
``Prepare`` step in your next invocation of the carre script.

It is good to also check the :guilabel:`SaveChoice` check box, so it is noted
that the grid parameters were changed.

.. image:: carre_13.png
   :align: center

Converting the grid output from Carre
-------------------------------------

The conversion step takes the *carre.out* file containing the Carre grid and
converts it to the Sonnet and B2.5 formats, respectively a \*.sno and \*.geo
file.

Click on the :guilabel:`Convert`.

.. image:: carre_14.png
   :align: center

And check the checkbox for *Convert*.

.. image:: carre_15.png
   :align: center

Storing the grid files
----------------------

Click on :guilabel:`Store` to store the grid files.

.. image:: carre_16.png
   :align: center

Sometimes you will get an error message saying:

  No traduit.out. Convert the grid first.

Even though we did Convert the grid successfully. In this case sometimes
convert doesn't work, even though it produces a normal output. Run it again and
try to store the grid files again.

And check the checkbox for *Store*.

.. image:: carre_17.png
   :align: center

Inspecting the mesh
===================

Now we will check the generated mesh. Switch over to the DivGeo tab and if you
have closed ``C-mod_g990429019_00940.dg``, reopen it and if you wish dock it.

In DivGeo click on :menuselection:`File --> Import --> Mesh` and open
``C-mod_g990429019_00940.sno`` file. Note that DG can only read files in the
Sonnet format (\*.sno).

.. image:: carre_18.png
   :align: center

You may see some grid cells that are outlined in magenta. These are concave
cells that will yield errors when running Eirene and should be corrected before
proceeding. Two methods are available.

Changing grid parameters in Carre
---------------------------------

The first is to go back to Carre and chose a different set of gridding
parameters and try your luck or smarts against an ill-posed mathematical
problem. This is where the Save option comes in handy!

An easier way is the next method.

Manually change mesh points in DivGeo
-------------------------------------

The second is to modify the grid points by hand (if there are not too many of
them). This can be done as follows. Change one of the mouse button functions
to ``Move mesh point`` and select a corner of a magenta grid cell and move it
until the cell outline changes colour to lavender. You may need to propagate
such changes over a range of cells.

The result is that there are no more magenta grids.

.. image:: carre_19.png
   :align: center

Bear in mind however that you are only
modifying the \*.sno grid file. You will need to save your modifications by
exporting the mesh :menuselection:`File --> Export --> Mesh`.

Triang
======

Head over to *Triang* tab to start Triang. The functionality of this tab is
similar to the one with Carre, except there are other steps and there is no
DivGeo model selection.

.. note::
   Note that the mention of checking the check boxes will be omitted but
   nonetheless do not forget to check them as they are part of the
   self-assessment!


.. image:: triang_1.png
   :align: center

Start triang with :guilabel:`Start Triang`. The output will be as following:

.. image:: triang_2.png
   :align: center

Create the input files
----------------------

Uinp is a program that builds several input files for SOLPS-ITER programs
according to the data provided in the DG model:

  - Eirene input files input.eir, test.eir and triang.eir
  - Tria input file header triang.hed
  - B2.5 pre-processor input files b2ag.dat, b2ai.dat, b2ar.dat, and converter
    input file b2yt.dat.
  - B2.5 input file b2.user.parameters
  - b2plot input file mesh.extra
  - Stencil files b2ah.dat.stencil, b2.neutral.parameters.stencil and
    b2.boundary.parameters.stencil which are sample files containing a very
    rough default physics model for the boundary conditions and recycling
    parameters, but that have the right format for further modification to
    adapt to your physics problem at hand.

On the first call, it is best to use :guilabel:`Uinp(U)` as in uppercase U.
Uinp will display the list of particles being used, the reactions it will
include in the Eirene input file, the boundaries it will define, etc...

If Uinp is happy the following output at the end should be observed

.. image:: triang_3.png
   :align: center

Otherwise an error such as the following can occur:

| ==> Check the "Index" specification in
| "TRIA-EIRENE parameters" in DG variables
| The targets must be numbered according to the B2 convention:
| going clockwise and starting from the bottom left corner.
| nn -4
| ERROR in uichkchn, nn -4

In which case you should check the ``TRIA-EIRENE parameters`` section in the
making of the DivGeo model.

After that run Uinp(u) again until it succeeds.

Modifying the b2ag.dat file
---------------------------

If you have modified the grid file by hand in DG, you need to modify the
b2ag.dat (right) file created by Uinp to point to your modified file instead
of the file initially created by Carre.

Click on the button :guilabel:`Edit b2ag.dat`. An input dialog will show.

Change the value of the first parameter in the \*param list from ``-1.0`` to
``-2.0`` and the name of the file given to the b2agfs_geometry switch to your
modified \*.sno file.

*SOLPS-GUI* provides a little help and shows in the end it prints you the
latest \*.sno file created. The line should be similar to:

  !Latest SNO file in DivGeo/device/cmod: C-mod_g990429019_00940.v003.sno

.. image:: triang_4.png
   :align: center

No to avoid any problems, copy the name of the \*.sno file to the
b2agfs_geometry switch and delete the line.

.. image:: triang_5.png
   :align: center

Creating the fort.30 file
-------------------------

Once you are pointing to the correct mesh file, proceed with the triang by
clicking on :guilabel:`B2ag`.

This command runs the b2ag program to create a geometry file that provides the
mesh geometry used by Eirene.

.. image:: triang_6.png
   :align: center

This step will be skipped if a **fort.30** file is already present. If you are
re-running triang to obtain a new geometry in an already populated directory,
make sure you have removed the older b2ag.dat and fort.30 files beforehand.

Eirene triangulation preparation run
------------------------------------

Press :guilabel:`Eirene`. If this step is successful, the output will look like

.. image:: triang_7.png
   :align: center

If this step fails (i.e. the message “No valid fort.78 file created” appears),
you should look at the error messages from Eirene that you will find in the
eirtria.log file. Standard Eirene debugging applies.

This step uses Eirene to produce the full contours that will be used in the
triangulation step next. The contours deduced by Eirene are written in the
fort.78 file. The script then concatenates this file with the triang.hed file,
which contains the information about the desired triangle sizes and mesh
refinement zones from DG to form the tria.in file that will be the input for
the tria program.

Triangulation
-------------

Press :guilabel:`Tria`. If this step is successful, the output will look like

.. image:: triang_8.png
   :align: center

The triangulation results will be stored in three files:

  - *tria.nodes*
  - *tria.elemente*
  - *tria.neighbor*

which contain, respectively, the coordinates of the nodes, the vertices
assignment for the triangles, and the connectivity information between
triangles.

If this step fails, you should look at the error messages from tria that you
will find in the tria.log file generated in the baserun directory.

Triangulating the Carre grid and merging it with the outer triangles
--------------------------------------------------------------------

Press :guilabel:`triaGeom`. If this step is successful, the output will look
like

.. image:: triang_9.png
   :align: center

This steps takes the output from the triangulation step and adds nodes
corresponding to the Carre grid cells, each of which is split into at least two
triangles.

The connectivity information is also enriched to indicate in which Carre grid
cell, if any, each triangle is embedded.

This step also creates the links between the triageom.[cells,nodes,links]
files and the fort.3[3-5] files used later by SOLPS-ITER.

Storing the triangle files
--------------------------

Press :guilabel:`Store`. If this step is successful, the output will look like

.. image:: triang_10.png
   :align: center

The triangulation files will be stored in some standard directories. The script
may ask you to create these directories if those are not yet present. Simply
press :guilabel:`Yes` if you are asked.

Links to the triangle files as fort.33, fort.34, and fort.35, as needed by
Eirene, are updated to their new location.

Converting the triangle files into an "outer" template
------------------------------------------------------

Press :guilabel:`Conv2Out`. If this step is successful, the output will look
like

.. image:: triang_11.png
   :align: center


template.aXXX.tria file contains the triangles created by the tria step, which
cover the area outside the Carre grid.

Converting the triangle files into a "grid" template
----------------------------------------------------

Press :guilabel:`Conv2Grid`. If this step is successful, the output will look
like

.. image:: triang_12.png
   :align: center


The template.gXXX.tria file contains the triangles created by the triageom
step, which covers the entire domain.

View the results in DivGeo
==========================

You can view the triangle grids by importing them as templates, using the
template file created during the two conversion steps above. If you are happy
with them, you are done! Otherwise, you may wish to modify the triangle size
and/or the mesh refinement regions. Also, you can move or create wall vertices,
since those vertices act as anchors for the triangulation.

Head back to DivGeo tab and import the resulting templates with
:menuselection:`File --> Import --> Template` and import
``template.gXXX.tria.ogr``. The index may be different at your case.


.. image:: triang_13.png
   :align: center




.. Prepare the links of the DG output files for later programs
.. -----------------------------------------------------------

.. Because the other SOLPS-GUI programs expect to find the DG output files in a
.. "standard" place, a set of symbolic links is produced to fulfill this
.. requirement, by means of the command: ``lns <DG_model_name>``
.. Note that you should not include the ``".dg"`` extension in the DG model name.

.. Launch the mesh building script
.. -------------------------------

.. In the following part we will proceed the creation of a plasma grid using the
.. Carre gird operator

.. ``carre -``.

.. Preparation step
.. ----------------

.. The preparation starts with:

.. :kbd:`p (or <Enter>)`

.. This steps reads the DG files and translates them into
.. the format needed by Carre

.. :kbd:`class = cmod`

.. :kbd:`grid_stem = g1070725014.00700.default.pnl`

..  :kbd:`rdeqdg: before rdeqlh`

..  :kbd:`rdeqdg: after rdeqlh. nr,nz,btf,rtf=          257         257`

..    :kbd:`5.40751075744629       0.660000026226044`

..  :kbd:`reading rgr...`

..  :kbd:`reading zgr...`

..  :kbd:`reading pfm...`

.. :kbd:`Help, Prepare, Grid, Save, Convert, sTore, Next, Remove, Input, Output,`

.. :kbd:`Quit`

.. Gridding step
.. -------------

.. The gridding step strats with:

.. :kbd:`g (or <Enter>)`

.. The first question you must answer is whether the `X-` and `O-` points
.. identified by Carre are correct (they usually are). If they are not, then,
.. you refuse the selection and indicate yourself which of the extrema are `X-`
.. and `O-` points.

.. :kbd:`Starting`

.. :kbd:`newpag OK`

.. :kbd:`cpsets ok`

.. :kbd:`cprect ok`

.. :kbd:`cpcldr ok`

.. :kbd:`Pre-selected points are identified.`

.. :kbd:`O-point:     6.8030E-01   -8.0087E-03`

.. :kbd:`X-point:     5.6218E-01   -3.8994E-01`

.. :kbd:`Do you accept the selection (y/n)?`

.. :kbd:`y`

.. Grid parameter selection step
.. -----------------------------

.. Carre then provides a table of parameters. Carre attempts to provide a grid
.. that must satisfy three criteria simulatenously:

..     1. The grid cells must be as locally orthogonal as possible
..     2. The grid cells must align with the targets in their vicinity
..     3. The size of neighbouring grid cells must not vary too quickly.

.. It is relatively easy to find a satisfactory solution meeting these three
.. criteria, but this is not always the case, especially in geometries where the
.. targets are almost parallel to the flux surfaces, putting criteria 1 and 2 at
.. odds with one another.

.. Quickly, the data provided in the Carre table indicates the poloidal spacing
.. of the grid points along the separatrix segments, the radial spacing of the
.. successive flux surfaces as one steps away from the separatrix, the
.. penetration depth of the grid (:kbd:`pntrat`), the guard lengths (i.e. the
.. vicinity
.. over which criterion 2 above is applied, in meters), and some numerical
.. parameters used for the optimization algorithm that attempts to build the mesh.

.. The poloidal spacings are deduced from the distribution of grid points chosen
.. in DG. The guard lengths are given by the `"CARRE guard length"` parameters in
.. the DG `"Target specifications"`. The pntrat value is obtained from the
.. innermost DG surface chosen in the core.

.. The radial extent of the grid (and therefore the radial grid spacings) is
.. determined by the first tangency points (in the PFR and main chamber vessel)
.. between the flux surfaces and the `"Structure"` defined in DG. However, the
.. algorithm is not identical to DG’s, so the values found may differ.

.. SEPARATRIX SEGMENTS:

.. === =========== ========== =========== =========== =========== =============
..  #   nptseg(i)   lg(i)      deltp1(i)    deltpn(i)     dpmin      dpmax
.. === =========== ========== =========== =========== =========== =============
..  1      21      1.1724E-01  9.1116E-03  1.8834E-04  1.8834E-04  9.1116E-03

..  2      21      1.1053E-01  8.8644E-03  1.8323E-04  1.8323E-04  8.8644E-03

..  3      41      1.7723E+00  1.1810E-02  1.5681E-02  1.1810E-02  6.0815E-02

.. === =========== ========== =========== =========== =========== =============

.. RADIAL DISTRIBUTIONS FOR EACH REGION:

.. Distribution in psi: repart=    2

.. ====== ======= ============ ============ ============ ============ ============
.. region  npr(i)     width      deltr1(i)   deltrn(i)     drmin      drmax
.. ====== ======= ============ ============ ============ ============ ============
..  1       21      2.7276E-02   9.6815E-05   2.4586E-03   9.6815E-05   2.4586E-03

..  2       11     -1.8005E-02  -2.1524E-04  -3.1739E-03  -3.1739E-03  -2.1524E-04

.. ====== ======= ============ ============ ============ ============ ============


.. CENTRAL REGION: region i=  3     pntrat max.= 0.39977943

.. ======= ======= ============ ============ ============= ============ ===========
..  pntrat  npr(i)    width      deltr1(i)     deltrn(i)      drmin         drmax
.. ======= ======= ============ ============ ============= ============ ===========
.. 0.161   11       -1.4957E-01  -1.7755E-03  -2.6181E-02  -2.6181E-02  -1.7755E-03

.. ======= ======= ============ ============ ============= ============ ===========

.. GUARD LENGTH FOR EACH DIVERTOR PLATE:

.. ============ ============
..  tgarde(1)     tgarde(2)
.. ============ ============
..   0.20000        0.20000
.. ============ ============

.. RELAXATION PARAMETERS USED TO CONSTRUCT THE MESH:

.. ========= ============= =============== ============
.. nrelax        relax          pasmin         rlcept
.. ========= ============= =============== ============
.. 5000         0.200          1.000E-03      1.000E-06
.. ========= ============= =============== ============


.. Carre criterion checks
.. ----------------------

.. Often, the first pass at the Carre grid parameters will not pass internal
.. muster. Carre checks for a few minimal requirements:

..     1. The poloidal grid spacing must be above a minimal threshold, defined
..        by the :kbd:`pasmin` parameter. This is not enforced by DG and is the
..        most common correction you’ll have to make.
..     2. The radial and poloidal grid spacings in each region must have the
..        same sign. The spacings are constrained by the first and last values
..        of the region to grid and the total interval length.

.. The code will not proceed until these requirements are met and will show
.. messages like this:

.. :kbd:`Invalid data for segment 1!`

.. The numbers :kbd:`dpmin` and :kbd:`dpmax` must be larger than :kbd:`pasmin` in
.. absolute value.

.. Modify :kbd:`deltp1`, :kbd:`deltpn` or :kbd:`pasmin` accordingly.

.. :kbd:`dpmin,dpmax,pasmin =  1.8834E-04  9.1116E-03  1.0000E-03`

.. :kbd:`Invalid data for segment 2!`

.. The numbers :kbd:`dpmin` and :kbd:`dpmax` must be larger than :kbd:`pasmin`
.. in absolute value. Modify :kbd:`deltp1`, :kbd:`deltpn` or :kbd:`pasmin`
.. accordingly.

.. :kbd:`dpmin,dpmax,pasmin =  1.8323E-04  8.8644E-03  1.0000E-03`

.. Type the name of the variable to be changed followed by `'='`, and its
.. numerical value. For example: :kbd:`nptseg(2)=32` (return). Type `"end"` to
.. stop.

.. Modifying the Carre parameters
.. ------------------------------

.. Usually changing the value of :kbd:`pasmin` is a good start.

.. :kbd:`pasmin = 0.99e-3`

.. :kbd:`end`

.. :kbd:`Invalid data for segment 1!`

.. The numbers :kbd:`dpmin` and :kbd:`dpmax` must be larger than :kbd:`pasmin` in
.. absolute value. MModify :kbd:`deltp1`, :kbd:`deltpn` or :kbd:`pasmin`
.. accordingly.

.. :kbd:`dpmin,dpmax,pasmin =  1.8834E-04  9.1116E-03  9.9000E-04`

.. :kbd:`Invalid data for segment 2!`

.. The numbers :kbd:`dpmin` and :kbd:`dpmax` must be larger than :kbd:`pasmin`
.. in absolute value.
.. Modify :kbd:`deltp1`, :kbd:`deltpn` or :kbd:`pasmin` accordingly.

.. :kbd:`dpmin,dpmax,pasmin =  1.8323E-04  8.8644E-03  9.9000E-04`

.. We now modify the poloidal grid spacings. The first spacing is the one touching
.. the `X-point`, and the last spacing is at the targets.

.. :kbd:`deltpn(1)=1.0e-3`

.. :kbd:`deltpn(2)=1.0e-3`

.. :kbd:`end`

.. SEPARATRIX SEGMENTS:

.. === ========== ============ ============= ============ ============= ===========
..  #   nptseg(i)   lg(i)       deltp1(i)     deltpn(i)      dpmin         dpmax
.. === ========== ============ ============= ============ ============= ===========
.. 1      21      1.1724E-01   9.1116E-03    1.0000E-03   1.0000E-03    9.1116E-03

.. 2      21      1.1053E-01   8.8644E-03    1.0000E-03   1.0000E-03    8.8644E-03

.. 3      41      1.7723E+00   1.1810E-02    1.5681E-02   1.1810E-02    6.0815E-02

.. === ========== ============ ============= ============ ============= ===========

.. RELAXATION PARAMETERS USED TO CONSTRUCT THE MESH:

.. ====== ======== =========== ===========
.. nrelax  relax     pasmin       rlcept
.. ====== ======== =========== ===========
.. 5000    0.200    9.900E-04   1.000E-06

.. ====== ======== =========== ===========

.. :kbd:`Do you wish to accept these values (y/n)? y`

.. Producing the grid
.. ------------------

.. Carre then proceeds, one region at a time (:kbd:`ireg` index), to build the
.. flux surfaces (:kbd:`ir` index) in order, stepping from the separatrix outward.
.. If the Carre algorithm fails to converge while building the flux surfaces,
.. you will get a (non-fatal) error message that allows you to continue, but
.. suggests some possible changes to the gridding parameters that might improve
.. convergence, although it may not improve the “quality” of the final grid.

.. You may also get a fatal error message that indicates that Carre was not able
.. to build the next flux surface. This usually occurs because the radial
.. spacings required are too small compared to the resolution of the magnetic
.. equilibrium provided (fix this by refining the equilibrium a further step,
.. using :kbd:`d2d`, or by increasing the minimal radial spacings by modifying the
.. :kbd:`deltr1` and :kbd:`deltrn` parameters). Sometimes, this is because the
.. limiting  structures in the DG structure are so small that they may stepped
.. over as Carre moves from one flux surface to the next, and can be fixed by
.. going back to the DG model and making this limiting structures bigger.

.. You will get this kind of output:

.. :kbd:`ireg=           1`

.. :kbd:`ir=           2`

.. :kbd:`ir=           3`

.. :kbd:`ir=           4`

.. :kbd:`ir=           5`

.. :kbd:`ir=           6`

.. ….

.. :kbd:`ir=           7`

.. :kbd:`ir=           8`

.. :kbd:`ir=           9`

.. :kbd:`ir=          10`

.. :kbd:`ir=          11`


.. Saving the grid parameters
.. --------------------------

.. If you wish to remember the settings change you made, choose the :kbd:`Save`
.. option. The grid parameters are then written in the :kbd:`carre.dat` file. If
.. you wish to re-use these parameters, skip the :kbd:`Prepare` step in your next
.. invocation of the :kbd:`carre` script.

.. :kbd:`Help, Prepare, Grid, Save, Convert, sTore, Next, Remove, Input, Output,`
.. :kbd:`Quit ?`

.. :kbd:`s`

.. Saved grid settings in carre.dat file


.. Converting the grid output from Carre
.. -------------------------------------

.. To convert the grid output from Carre, you can do it by:

.. :kbd:`c (or <Enter>)`

.. :kbd:`Help, Prepare, Grid, Save, Convert, sTore, Next, Remove, Input, Output,`
.. :kbd:`Quit ?`

.. :kbd:`c`

.. Name of the file containing the carre grid

.. :kbd:`carre.out`


.. The conversion step takes the carre.out file containing the Carre grid and
.. converts it to the `Sonnet` and `B2.5` formats, respectively a :kbd:`*.sno`
.. and :kbd:`*.geo` file.

.. Select the output format

..     1. standard mailtri format
..     2. format `B2.5`
..     3. format `SONNET-DIVIMP`
..     4. format `DG-SONNET-B2-EIRENE`
..     5. revised `DIVIMP` with grid parameters and `PSI` values

..  :kbd:`The format chosen is :           4`

..  Name of the file containing the carre grid :kbd:`carre.out`

..  Select the output format

..     1. standard mailtri format
..     2. format `B2.5`
..     3. format `SONNET-DIVIMP`
..     4. format `DG-SONNET-B2-EIRENE`
..     5. revised `DIVIMP` with grid parameters and `PSI` values

..  :kbd:`The format chosen is :           2`

.. Storing the grid files
.. ----------------------

.. The sorting of the grid files can be made by:

.. :kbd:`Help, Prepare, Grid, Save, Convert, sTore, Next, Remove, Input, Output,`
.. :kbd:`Quit?`

.. :kbd:`t (or <Enter>)`

.. dir OK

.. The grid in DG format is stored as ``*.sno`` format. The ``dg.dgo``,
.. ``dg.equ``, ``dg.str`` and ``dg.trg``, you need to copied them into
.. the: :

..     $ /home/ITER/user_name/SOLPS-GUI/modules/DivGeo/device/cmod


.. The grid in B2.5 format is stored as ``*.geo`` format and the you can view
.. the grid in PostScript format as ``*.ps`` format.

.. Import the mesh into DG
.. -----------------------

.. After you stored the grid files, the ``*sno`` format file is the one that DG
.. can read it as a mesh. Note that DG can only read files in the Sonnet format
.. ``(*.sno)``. The mesh can be import as:

.. :menuselection:`File --> Import --> Mesh`

.. When you import the mesh you need to check if some grid cells are
.. outlined in magenta. If there are, these are concave cells that will yield
.. errors when running Eirene and should be corrected before proceeding. Two
.. methods are available for proceeding. The first is to go back to
.. Carre and chose a different set of gridding parameters. This is where the Save
.. option comes in. The second is to modify the grid points by hand (if there
.. are not too many of them). This can be done as follows. Change one of the
.. mouse button functions to ``Move mesh point`` and select a corner of a magenta
.. grid cell and move it until the cell outline changes colour to lavender. You
.. may need to propagate such changes over a range of cells. Bear in mind
.. however that you are only modifying the ``*.sno`` grid file. You will need to
.. save your modifications by exporting the mesh:

.. :menuselection:`File --> Export --> Mesh`

.. .. image:: divgeo_23.png
..    :align: center

.. Closing Carre or gridding again
.. -------------------------------

.. If you are satisfied with your grid, or modified it within DG, you can now quit
.. the carre script with

.. :kbd:`Help, Prepare, Grid, Save, Convert, sTore, Next, Remove, Input, Output,`
.. :kbd:`Quit ?`

.. :kbd:`q (or <Enter>)`

.. If you wish to obtain a new grid (and you have saved the previous set of
.. gridding parameters):

.. :kbd:`g (or <Enter>)`

.. Repeat until the grid will be done correct.

.. Start the triangulation script
.. ------------------------------
.. After the meshing part, is needed to be done the triangulation script. This
.. script can be start with:

.. :kbd:`triang-.`

.. Create the input files for triangulation script
.. -----------------------------------------------

.. On the first call, when you will get:

.. :kbd:`Help, Uinp, B2ag, Eirene, Tria, triaGeom, Plot, View, Store, Convert,`
.. :kbd:`List, Remove, reMap, Inquire, Quit ?`

.. is best to use:

.. :kbd:`U`

.. Using uppercase U instead of the (default) lowercase u ensures that the links
.. (from the ``lns`` command earlier) are correct. ``Uinp`` is a program that
.. builds several input files for SOLPS-GUI programs according to the data
.. provided in the DG model:

..    1. Eirene input files ``input.eir, test.eir and triang.eir``
..    2. Tria input file header ``triang.hed``
..    3. B2.5 pre-processor input files ``b2ag.dat, b2ai.dat, b2ar.dat``, and
..       converter input file ``b2yt.dat``.
..    4. B2.5 input file ``b2.user.parameters``
..    5. b2plot input file ``mesh.extra``
..    6. Stencil files ``b2.neutral.parameters.stencil`` and
..       ``b2.boundary.parameters.stencil`` which are sample files containing a
..       very rough default physics model for the boundary conditions and
..       recycling parameters, but that have the right format for further
..       modification to adapt to your physics  problem at hand.

.. ``Uinp`` will display the list of particles being used, the reactions it will
.. include in the Eirene input file, the boundaries it will define and so on.

.. The output of the list of the particles, all them reactions (ionization,
.. recombination) you can see it in the ``AMJUEL``. which is a Database of
.. Eirene.

.. Meshing ITER Baseline scenario
.. ==============================

.. The ITER baseline scenario case follows the same steps as for the C-Mod.
.. Every file which is used for running is located in one working directory
.. called ``baserun``. The basic setup of the run directory starts::

..      $ stop
..      $ cd runs/examples
..      $ cmake . && make # Fetches all examples
..      $ tar xvzf tutorial-DivGeo_ITER_baseline_scenario.tar.gz
..      $ cd tutorial-DivGeo_ITER_baseline_scenario/baserun

.. In this directory you will find the following files:

.. Baseline2008-li0.x4.equ
..     - Equilibrium file (Sonnet format)
.. F57-Be_W-Ne.dg
..     - DivGeo model
.. iterm.carre.105
..     - CARRE grid for SOLPS_ITER simulations
.. tt.tpl
..     - Vacuum vessel description

.. Then is needed to copy the EFIT equilibrium file ``Baseline2008-li0.70`` into
.. ``baserun`` directory. This example of the equilibrium file is for a
.. ITER case Ne plasma with beryllium wolfram impurities. Because the format of
.. the EFIT equilibrium file is not readable, so is needed to format it, into
.. the DG equilibrium::

..     $ e2d Baseline2008-li0.70 Baseline2008-li0.70.equ

.. To improved smoother contouring for the equilibrium of the ITER baseline
.. case should increase the resolution of the data. Using higher resolution
.. equilibrium can avoid some problems when the fluid grid is generated::

..     $ d2d Baseline2008-li0.70.equ Baseline2008-li0.70.x4.equ


.. The next step is to copy the wall geometry file into ``baserun``
.. directory.

.. To start DivGeo, as a SOLPS-GUI tool can be done with choosing first at the
.. Runs menu the directory baserun and after that to click on the Populate baserun
.. and just click on the Start DivGeo button on the left down corner of the
.. SOLPS-GUI window.


.. Import geometry file
.. --------------------

.. To start to use the DivGeo should make an import of the wall geometry file
.. which is already into ``baserun`` directory. That can be done with opening
.. the: :menuselection:`File --> Import --> Template` and load
.. ``F57-Be_W-Ne.ogr``, which should appear in the dialogue box. Then press
.. :kbd:`CTRL+P` to fit the wall data to the workspace. If you cannot
.. see the wall, then use the :menuselection:`View --> Display` and make sure
.. that the Template radio button is pressed.

.. .. image:: divgeo_ITER_1.png
..    :align: center

.. Import equilibrium file
.. -----------------------

.. After that need to be load the equilibrium file
.. :menuselection:`File --> Import --> Equilibrium` and select the
.. ``Baseline2008-li0.70.x4.equ`` from the dialogue box.If you cannot
.. see the equilibrium displayed as red (SOL) and blue (core and PFR)
.. rectangles after it is loaded, then use :menuselection:`View --> Display`
.. and make sure that the Equilibrium button is pressed.

.. .. image:: divgeo_ITER_2.png
..    :align: center

.. Setting the magnetic topology
.. -----------------------------

.. You can tell to DivGeo also which kind of magnetic topology you want the
.. modelling grid to have. As was said at the C-Mod case that can be done by
.. :menuselection:`File --> Import --> Topology` and choose one of topology in
.. the list. For the previous example of C-Mod case was selected SN. But for
.. this case none of the topologies fulfills the conditions. You can create a
.. magnetic topology by your own with :menuselection:`Commands --> Edit
.. topology`

.. .. image:: divgeo_ITER_4.png
..    :align: center

.. You choose that you want the topology to be through x-point and write which
.. level. You save the topology and after that you chose it from the list.

.. Setting the structure
.. ----------------------

.. This is the primary definition for the vessel wall. This can be done if you
.. choose :menuselection:`Variables --> Structure`

.. .. image:: divgeo_ITER_5.png
..    :align: center

.. Use the right mouse button (assigned to Mark) to select all segments. Using
.. :kbd:`SHIFT+Right Click` will help a lot. Right clicking on a selected
.. segment will un-select it. When the highlighting is complete, left-click on
.. `“Set”` in the `“Structure”` dialogue box, at the end of the line marked
.. `“Structure”`.

.. :kbd:`CTRL+U` to unmark everything.

.. Setting the structure for the targets
.. -------------------------------------

.. As the same like the structure you can set the targets. Mark all of the
.. segments for the inner target and then click on `“Set”`. Do not include the
.. segments that are behind the target.

.. .. image:: divgeo_ITER_6.png
..    :align: center

.. The same is for the outer target.

.. .. image:: divgeo_ITER_7.png
..    :align: center

.. Creating the radial surfaces
.. ----------------------------

.. The radial surfaces in DG define the boundaries between rings on the Carre
.. grid. To create the surfaces can be done by
.. :menuselection:`Edit --> Create --> Surfaces…` Set 18 surfaces in the SOL.
.. Adjust
.. the radial distribution to give higher spatial resolution near the
.. separatrix.

.. .. image:: divgeo_ITER_8.png
..    :align: center

.. Adding a radial surfaces
.. ------------------------

.. For the core region it is necessary to add a surface which will define the
.. extent to which the grid penetrates into the core. To do that assign `“Add
.. surface”` to the middle mouse button. :kbd:`Middle-click` and hold somewhere in
.. the core,

.. .. image:: divgeo_ITER_9.png
..    :align: center

.. Adding core radiation
.. ---------------------

.. To include core radiation in the wall heat loads, one needs to specify the
.. amount of core radiation (in `MW`):
.. :menuselection:`Variables --> Add --> Radiation sources`
.. Enter in the `“Radiated Power”` field the amount of core radiation (in `MW`) then
.. need to specify the location from where this core radiation is emitted.
.. This is done by providing a set of point sources. The radiated power will be
.. spread evenly among these point sources. You create them by:
.. :menuselection:`Edit --> Create --> Source`
.. And specify the X and Y coordinates (in `mm`) of the point source location.
.. You may input as few or as many point sources as you’d like. The point
.. sources (if you choose to display them) are shown as white asterisks  in the
.. DG model.

.. .. image:: divgeo_ITER_10.png
..    :align: center

.. Defining plot zones
.. -------------------

.. The plot zones are a set of walls on which the power load, including the
.. contrabutions from the plasma particles, Eirene neutrals and radiation can be
.. computed by b2plot. That can be done with
.. :menuselection:`Variables --> Add --> Plot zone`
.. :kbd:`CTRL+U` and mark the set of elements that you want to include in
.. the plot zone. :kbd:`CTRL+U` mark the `“Starting element”`. which is the
.. first element of the plot zone set.

.. Give the zone a label, because this zones will be used in the files created by
.. b2plot.

.. .. image:: divgeo_ITER_11.png
..    :align: center

.. Setting the structure that are used by B2plot
.. ---------------------------------------------

.. Defining the wall surfaces also defines the wall specification in B2plot, that
.. can be done by
.. :menuselection:`Variables --> Add --> Input to b2plot`
.. Mark all elements which are specifaing the b2plot and click `SET`.

.. .. image:: divgeo_ITER_12.png
..    :align: center

.. Setting the shadowing structure
.. -------------------------------

.. The shadowing structure is the set of physical wall elements that can receive
.. light from the plasma (or its reflections). It is used to compute the
.. radiative contribution to the wall heat loads.
.. :menuselection:`Variables --> Add --> Shadowing structure` :kbd:`CTRL+U`

.. Mark all the segments likely to receive light from the plasma. The shadowing
.. structure must be continuous and closed.

.. .. image:: divgeo_ITER_13.png
..    :align: center

.. Setting the gas puffing
.. -----------------------

.. It is very important to set the parameters of how much the gas is puffing
.. into the SOL. For this reason DG has a special option to do that. The gas
.. puffing parameters can be define by
.. :menuselection:`Variables --> Add --> Gas puff`

.. .. image:: divgeo_ITER_14.png
..    :align: center

.. First you need to mark an set the puffing slot from where the gas will enter
.. into the system. Then all other specifications. For gas specious you select
.. what kind of gas is puffing, in this case is D2. Then the puffing flux for
.. this case is 2.7e22.

.. PRF surface group pump
.. ----------------------

.. For PFR edge is only set based on where the radial boundary of the grid
.. will be, as determined by intersection with the divertor knee. You can
.. definite the PRF surface group pump with choosing the
.. :menuselection:`Variables --> Add --> PFR surface group` and then choosing
.. which part you will mark: the pump part

.. .. image:: divgeo_ITER_15.png
..    :align: center

.. The part of the inner divertor

.. .. image:: divgeo_ITER_16.png
..    :align: center

.. The part of the outer divertor

.. .. image:: divgeo_ITER_17.png
..    :align: center

.. EIRENE setup of the "void” regions outside the Carre grid
.. ---------------------------------------------------------

.. EIRENE will use a triangle grid in regions that are outside the fluid grid,
.. and this variable defines the zones for the triangle mesh generator.

.. Mark all of the main chamber elements, including the "SOL edge” segments for
.. the targets. :menuselection:`Variables --> Add --> TRIA-EIRENE parameters`

.. Set index to -1 in the dialogue box, and :kbd:`"General Triangle size”`
.. to 10.0, which will generate large triangles. The negative index indicates
.. that a mesh should be generated inside the marked region, and a positive
.. value means the opposite.

.. .. image:: divgeo_ITER_18.png
..    :align: center

.. With :kbd:`CTRL+U` mark the the wall segments in the PFR, including the `"PFR
.. edge”` elements. Set index to -2 in the dialogue box, and `"General Triangle
.. size”` to 10.0.

.. Global B2 data
.. --------------

.. In the global B2 data you can set some power parameters as the electron and
.. ion power, and also the power fraction inboard and the time dependent strtum.
.. :menuselection:`Variables --> Add --> Global B2 data`
.. For the electron and ion power for this case you need to set it on 50. For
.. the power fraction inboard 0.25

.. .. image:: divgeo_ITER_19.png
..    :align: center

.. Configuring the plasma species to be included in the simulations
.. ----------------------------------------------------------------

.. It is very important to definite plasma species which are included in the
.. simulations. That you do it by: :menuselection:`Variables --> Plasma
.. species D` . Also you can add it the impurity species
.. :menuselection:`Variables --> Add --> Plasma species`

.. DG recognizes a few "generic” species: H, D, T, He, Be, C, N, Ne, and Ar,
.. for which a full consistent default set of reactions will be provided by
.. Uinp. For all other elements, Uinp will look for the corresponding ADAS
.. ionization and recombination rates, and, if present in your database, will
.. include them as part of your model.

.. .. image:: divgeo_ITER_20.png
..    :align: center

.. Local refinement of the EIRENE triangle grid
.. --------------------------------------------
.. With DG it’s possible to increase the spatial resolution on sub-regions of the
.. triangle mesh, i.e. the PFR. This can be done by
.. :menuselection:`Variables --> Add --> Mesh Refinement Zones`

.. .. image:: divgeo_ITER_21.png
..    :align: center

.. Select wall elements that bound the region of interest (left-right,
.. top-bottom), as shown on the right, and click `"Set”` for `"Region
.. identification”`. Set `"Desired side length”` to the desired characteristic
.. scale size of the triangles in this region.

.. Creating the grid points
.. ------------------------

.. The poloidal distribution of cells on the Carre grid are set by the
.. `"poloidal grid points”` in DG.  These are defined separately for the
.. divertor legs and the SOL. :menuselection:`Edit --> Create --> Grid points`.
.. Set the Zone to Inner divertor and Cells to 18. The distribution of the cells
.. can be adjusted by left-clicking and dragging the black line on the plot.
.. Then click Create to update the workspace. Repeat for the outer divertor. Set
.. 48 points in the SOL, with a roughly uniform distribution of points. The
.. spacing of the grid points around the x-point should be symmetric.

.. .. image:: divgeo_ITER_22.png
..    :align: center

.. Write the output data files that are needed by later steps
.. ----------------------------------------------------------

.. With the :menuselection:`Commands --> Check variables` you can check if all
.. variables have valid values. If the check is it ok with:
.. :menuselection:`Commands --> Rebuild Carre objects`
.. :menuselection:`File --> Save`
.. :menuselection:`File --> Output`
.. can be create three files:
.. :kbd:`<DG_model_name>.dgo`, `the DG “output” file`
.. :kbd:`<DG_model_name>.str`, `the “structure” file (used by Carre)`
.. :kbd:`<DG_model_name>.trg`, `the “targets” file (used by Carre)`
.. which are leater used for Carre meshing building script.

.. .. image:: carre_gui_1.png
..    :align: center


.. Prepare the links of the DG output files for later programs
.. -----------------------------------------------------------

.. Because the other SOLPS-GUI programs expect to find the DG output files in a
.. "standard" place, a set of symbolic links is produced to fulfill this
.. requirement, by means of the command: ``lns <DG_model_name>``
.. Note that you should not include the ``".dg"`` extension in the DG model name.

.. Launch the mesh building script
.. -------------------------------

.. In the following part we will proceed the creation of a plasma grid using the
.. Carre grid operator. First is necessary to check if the saved ``".dg"``
.. files are in ``home`` directory at ``baserun``. You can check it by clicking
.. ``&Runs``.

.. .. image:: carre_gui_2.png
..    :align: center

.. Carre grid operator is opening by choosing the ``&Populate Baserun`` and then
.. on the down left corner of the window there is a ``Carre`` button.

.. .. image:: carre_gui_3.png
..    :align: center

.. After that you should choose the  ``".dg"`` model on which you want to make
.. the mesh. And than ``Start Carre``.

.. .. image:: carre_gui_4.png
..    :align: center

.. Preparation step
.. ----------------

.. This step reads the ``DG`` files and translates them into the format needed
.. by Carre. In SOLPS-GUI this step is done by clicking on the ``Prepare`` button.

.. .. image:: carre_gui_5.png
..    :align: center

.. Gridding step
.. -------------

.. The gridding step strats with clicking on ``Grid``
.. The first question you must answer is whether the `X-` and `O-` points
.. identified by Carre are correct (they usually are) click `Yes`. If they are
.. not, then, you refuse the selection and indicate yourself which of the extrema
.. are `X-` and `O-` points.

.. .. image:: carre_gui_6.png
..    :align: center

.. Grid parameter selection step
.. -----------------------------

.. Carre then provides a table of parameters. Carre attempts to provide a grid
.. that must satisfy three criteria simulatenously:

..     1. The grid cells must be as locally orthogonal as possible
..     2. The grid cells must align with the targets in their vicinity
..     3. The size of neighbouring grid cells must not vary too quickly.

.. It is relatively easy to find a satisfactory solution meeting these three
.. criteria, but this is not always the case, especially in geometries where the
.. targets are almost parallel to the flux surfaces, putting criteria 1 and 2 at
.. odds with one another.

.. In SOLPS-GUI this is done by choosing ``Save Choice``

.. .. image:: carre_gui_7.png
..    :align: center

.. Carre criterion checks
.. ----------------------

.. Often, the first pass at the Carre grid parameters will not pass internal
.. muster. Carre checks for a few minimal requirements:

..     1. The poloidal grid spacing must be above a minimal threshol.
..     2. The radial and poloidal grid spacings in each region must have the
..        same sign. The spacings are constrained by the first and last values
..        of the region to grid and the total interval length.

.. The code will not proceed until these requirements are met and will show
.. messages like this `Try to increase the` ``deltr[1n]`` `values, or to reduce`
.. `the number of the radial grid points, or to use equilibrium data with higher`
.. `resolution`

.. Modifying the Carre parameters
.. ------------------------------

.. Carre parameters can be modified by opening ``Terminal input`` and writing
.. the correct values of the parameteres:

.. .. image:: carre_gui_8.png
..    :align: center


.. Producing the grid
.. ------------------

.. If the set parmeters are correct next Carre starts to produce the grid. As
.. an output you can see it on the window the following:

.. .. image:: carre_gui_9.png
..    :align: center

.. and ``Yes`` if the paramteres are correct.

.. Saving the grid parameters
.. --------------------------

.. During the``Save Choice`` the grid parameters are then written in the
.. :kbd:`carre.dat` file.


.. Converting the grid output from Carre
.. -------------------------------------

.. To convert the grid output from Carre, you can do it by clicking on ``Convert``.

.. .. image:: carre_gui_10.png
..    :align: center


.. Name of the file containing the carre grid

.. :kbd:`carre.out`

.. The conversion step takes the carre.out file containing the Carre grid and
.. converts it to the `Sonnet` and `B2.5` formats, respectively a :kbd:`*.sno`
.. and :kbd:`*.geo` file.

.. Storing the grid files
.. ----------------------

.. The sorting of the grid files can be made by clicking on ``Store``:

.. .. image:: carre_gui_11.png
..    :align: center

.. The grid in DG format is stored as ``*.sno`` format. The ``dg.dgo``,
.. ``dg.equ``, ``dg.str`` and ``dg.trg``.

.. The grid in B2.5 format is stored as ``*.geo`` format and the you can view
.. the grid in PostScript format as ``*.ps`` format.

.. Import the mesh into DG
.. -----------------------

.. After you stored the grid files, the ``*sno`` format file is the one that DG
.. can read it as a mesh. Note that DG can only read files in the Sonnet format
.. ``(*.sno)``. The mesh can be import as:

.. :menuselection:`File --> Import --> Mesh`

.. .. image:: carre_gui_12.png
..    :align: center
