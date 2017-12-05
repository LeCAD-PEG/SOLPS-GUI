.. _introduction:

..  topic:: Abstract

    by *Xavier Bonnin* and *Richard Pitts*

    The design of the ITER divertor and estimates of the required fueling
    throughput have relied for many years on simulations performed by use of
    the SOLPS plasma edge modeling tool, more specifically its versions 4.0,
    4.2 and 4.3. However, the SOLPS code base has been developed independently
    by other research groups among the ITER Members’ institutions, most notably
    in IPP-Garching (EU) and St. Petersburg (RF), leading ultimately to
    versions SOLPS5.0/5.1 and SOLPS5.2, respectively.

    While the developments at ITER on SOLPS4.x, in collaboration with FZ-Jülich
    (EU), have focused mainly on the physics of neutral transport, the work
    done in Garching has been devoted mostly to improving the physics
    capabilities of the plasma model and the St. Petersburg efforts have
    concentrated on improving the numerical solution of the drift terms and
    the electric potential equation. These various enhancements have now
    reached some maturity and it was decided at the IO in 2012 to devote
    resources to merging back these three code versions into a single package
    that would bring together all the advances from those branches of
    development. This began with a first Task Agreement between IO
    and F4E to couple the newest versions of the two main components of the
    SOLPS package (separate plasma fluid and neutral transport codes) to yield
    a new code version, named SOLPS-ITER. Subsequently, additional effort has
    been devoted to adding further refinements present in the various
    previous versions which were not all captured in the initial coupling
    exercise. The new code was released to the R&D community at a workshop
    organized at the ITER Headquarters on April 13th-17th, 2015.

    The ambition of the SOLPS-ITER effort is to make this last code version
    become the new standard used across the ITER Parties for modeling not
    only ITER, but any other tokamaks and linear plasma devices wherever
    applicable.
    In order to facilitate user adoption of SOLPS-ITER and migration from
    earlier versions, it has therefore been decided to include as part of
    the SOLPS- ITER package, a more user-friendly interface for some of the
    more tedious and error-prone tasks to ease the transition for users of
    older versions and provide additional added value and incentive for those
    switching to SOLPS-ITER. At the same time, SOLPS users, including those
    at the IO, have, over the years, expressed the desire for some
    run monitoring framework and more powerful graphical post-processing tools.
    The aim of Graphical User Interface (GUI) is to provide the software
    constituting this interface.

    The SOLPS GUI adds to the current SOLPS-ITER code suite a framework
    consisting of various tools aiming at improving the user’s experience,
    to accelerate and simplify run input set-up, and to increase the scientific
    usability of the *B2.5-Eirene* simulation results.

============
Introduction
============

The SOLPS GUI is a framework tailored specifically for SOLPS-ITER code
suite in a sense that code specifics are built-in the interface. Its design
allows users to extend functionality by coupling custom widgets prepared
for the SOLPS GUI. These custom widgets are in similar environments called
*actors* as they do act on some data depending on input received
and then they pass results further in a scientific workflow. Custom widgets
for SOLPS are operating in a similar fashion in a way that they receive and
send the signals to other widgets for further operation. In principle, no
programming is needed by users to create their own *Dashboard* for analyzing
and controlling the SOLPS simulations. Graphical workflow "design" is done
with `Qt designer <http://doc.qt.io/qt-5/qtdesigner-manual.html>`_.
In contrast to scientific workflow engines such as
`Kepler <https://kepler-project.org>`_ here we are more oriented to
look-and-feel experience than to create a general purpose workflow engine.
That's why the widgets in SOLPS GUI are concentrated to have "nice"
input and output presentation while we don't care how "nicely" wires are
placed. "Wiring" is usually taking significant space in other workflow
engines where *actors* are "small" or unified size with separated or neglected
display output. SOLPS GUI is having vice-versa approach with widgets filling
up available *Dashboard* completely. There can be many widgets that trigger
part of the workflow, whereas there is just *play* used in *Kepler*.
SOLPS GUI **signal/slot** philosophy provided by
`Qt framework <http://www.qt.io/qt-framework/>`_ is similar to
input/output ports in *Kepler*, while the triggering is more explicit than
implicit. This means that it is usually just one trigger needed to start the
action with the assumption that all needed signals describing the action
already arrived beforehand.

Users are therefore encouraged to design their own *Dashboard* by redesigning
it to suit their needs. As the *Dashboard* is intended to be configured with
*Qt designer* this means that all action needs to be provided within the
widgets connected by signals. "Wiring" can be graphical too. GUI
is then saved in XML files and compiled on-the-fly at the GUI startup. Even
if providing limited set of "custom" widgets there can exist many different
*Dashboards* for running SOLPS simulations. The may differ on the analysis,
user's preference and maybe exchanged for reuse by others. Nice thing with
such *graphical programming* is not just adding functionality easily
but one can simply remove the unwanted custom widgets too.

SOLPS Structure
---------------

SOLPS  consists of a suite of codes comprising a grid generator, CARRE,
a tool for specifying the material structures and providing inputs to
the other codes, DG, the plasma fluid code, B2, the kinetic neutrals
Monte Carlo code, EIRENE, and in addition to that a bundle of plotting
tools and scripts used for post-processing. Up to now there were a
number of different versions of SOLPS . SOLPS 4.0 is an old version
which is complete and not being updated anymore. Currently SOLPS 5.0 is
used by the majority of regular users. Versions 5.1 and 5.2 are
currently being developed, improving the performance of EIRENE and B2
part of the code, respectively. The most recent version is 6.0, which
brings improved mesh adaptation in B2 codes.

.. _fig-solps-sub-workflow:
.. figure:: howto/catalyst/images/workflow.*
   :alt: SOLPS code workflow.

   SOLPS code workflow.

Since SOLPS is a large scale software with a few hundred thousand lines of
code it has a complex workflow, depicted in
:numref:`fig-solps-sub-workflow`, with many input and output files at
different parts of the program. The complete workflow can be separated into
three parts — (i) pre-processing, (ii) processing, and (iii)
post-processing. In the following subsections these parts will be briefly
explained.

Pre-Processing
~~~~~~~~~~~~~~

Pre-Processing part of SOLPS is concerned with mesh preparation,
processing, and preparing input data of the initial physics states.
Pre-Processing can be divided into two parts, case build-up and grid
generation chain. Build-up consists of a graphical user interface called
DG, as well as programs that convert user file input and produce input
for B2 solver, ``b2ag``, ``b2ah``, ``b2ai`` and ``b2ar``. Grid
generation chain, on the other hand, is made of the mesh generators
CARRE, TRIA, and Triageom.

Case Build-Up
^^^^^^^^^^^^^

DG  is the interactive graphical interface software that allows to users
to visualize, inspect, and modify SOLPS mesh geometry. As input, it
takes geometry data from CAD drawing or other sources, values of the
poloidal magnetic flux on a regular grid, and a computational grid used
by B2-EIRENE and produces output files to be used by the interface
routines the input files for B2-EIRENE and grid generator CARRE. Case
output file is handed over to UINP module which translates it to output
suitable for input to standalone version of EIRENE.

Furthermore, four additional programs are necessary to prepare SOLPS,
more precisely B2, for running, which process user input about geometry
and initial states. The programs are the following.

-  ``b2ag`` - Prepares input file for B2 which contains information
   about geometry and magnetic field.

-  ``b2ah`` - Prepares input file for B2 which contains information
   about default physics parameters.

-  ``b2ai`` - Prepares input file for B2 which contains information
   about initial plasma state.

-  ``b2ar`` - Prepares input file for B2 which contains information
   about default atomic physics rates.

Grid Generation Chain
^^^^^^^^^^^^^^^^^^^^^

DG works on top of a computer code which generates a structured
curvilinear quasi-orthogonal mesh, called CARRE. CARRE  takes in data in
the form of three files which parametrize the equilibrium and the
structures within the vacuum vessel, and specify the various
distributions of flux surfaces and grid points. Output files serve as a
feed to ``b2ag`` and Triageom, and contains the graphic presentation of
the mesh and all necessary information to do the computation with the
mesh.

In order to run the EIRENE Monte Carlo simulations there needs to be a
triangular mesh generator. TRIA  provides a locally refined triangular
mesh outside of the regular B2 grid. After running TRIA, the Triageom 
program has to be run to produce the combined triangular mesh covering
the whole computational domain.

Processing
~~~~~~~~~~

The heart of the SOLPS code is the solvers B2 and EIRENE. Each of them
can run in a standalone mode or in a coupled mode, which means that each
solver computes its own part and passes data to the other. If running in
a coupled mode, the two codes talk to each other through files that
contain geometry and plasma states.

EIRENE
^^^^^^

EIRENE  is a linear Monte-Carlo solver developed specifically for the
transport of neutral particles in plasma. The code works using 2D
toroidal geometry for divertor applications. There are two options of
code usage. The simplest is that the code uses the same quasi-orthogonal
grid as the B2 code. Because of many drawbacks in using EIRENE on such
grid, it can be run on a triangular grid which is provided by TRIA in
SOLPS code. It can fill the volume between the quasi-orthogonal grid and
the additional surfaces. The plasma grid is divided into triangles as
well and both of the grids are attached to each other, forming one
continuous triangular grid.

In order to run, SOLPS provides EIRENE with input geometric data. The form
of input depends on whether it runs in standalone or coupled mode. The
connections between modules are illustrated in
:numref:`fig-solps-sub-workflow`

B2
^^

The B2  code solves a set of fluid equations describing the
2-dimensional radial-poloidal transport of a multi-species plasma with
toroidal symmetry. The fluid equations for the plasma are solved on a
regular, quasi-orthogonal grid aligned with the magnetic field, provided
by CARRE grid generator. Original version of B2 has been replaced by
B2.5 that is currently being used. The most recent version proposed is
B2.6  and offers improvements to data structure and grid adaptation.

The main program for B2.5 code is called ``b2mn``. It calls the driver
routine ``b2mndr`` for the actual computation, which calls ``b2mnds``
for initialization of B2 calculation and in each time step ``b2mndt``
routine that performs one implicit time step for the B2 system of
equations.

Post-Processing
~~~~~~~~~~~~~~~

There are a number of scripts and routines available for
post-processing.

-  ``b2plot`` - Designed to take data from B2, B2.5 or B2.5-EIRENE and
   plot it under interactive control.

-  ``b2ts`` - An example post-processing program. it reads the basic
   output files produced by b2mn and prints some simple geometric
   quantities.

-  ``b2yg`` - It reads and displays the geometry and magnetic field.

-  ``b2yh`` - It reads and displays the table of physics parameters.

-  ``b2yi`` - It reads and displays the plasma state.

-  ``b2ym`` - It produces movie output.

-  ``b2yn`` - It displays the progress of the inner iterations.

-  ``b2yp`` - It displays the plasma state.

-  ``b2yq`` - It provides a quick display of the evolution data.

-  ``b2yr`` - It reads and displays a table of atomic rate coefficients.

-  ``MATLAB scripts`` - Various MATLAB routines for data analysis and
   post-processing.

Grid Description
----------------

The main program for B2.5 code is called ``b2mn``. It calls the driver
routine ``b2mndr`` for the actual computation, which calls ``b2mnds``
for initialization of B2 calculation and in each time step ``b2mndt``
routine that performs one implicit time step for the B2 system of
equations.

Coordinate Systems
~~~~~~~~~~~~~~~~~~

The B2 fluid model that is used to describe the plasma in the scrape-off
layer is solved in the poloidal field-aligned coordinate system. The
choice of the coordinate system is due to the alignment of transport of
plasma along the magnetic field lines, which is strong in parallel and
weak in radial direction. In addition to that the coordinate system also
takes advantage of tokamak’s shape. Its rotational symmetry allows
three-dimensional problem to be reduced into two dimensions. Poloidal
cut through the torus, in :numref:`coordinates`, shows the cells are
quadrilateral shaped and either aligned with or perpendicular to the
magnetic field lines.

Because of the reasons mentioned earlier, the following coordinate
systems are used for the B2 model (:numref:`coordinates`).

#. **Cylindrical system** (:math:`R,\phi,z`), where :math:`R` is the
   torus’s major radius, :math:`\phi` the toroidal direction and
   :math:`z` the height.

#. **Parallel system** (:math:`\parallel,\perp,r`), where
   :math:`\parallel` is the direction parallel and :math:`\perp`
   perpendicular (diamagnetic direction) to magnetic field B and
   :math:`r` the outward normal to the flux surface.

#. **Poloidal system** (:math:`\theta,r,\phi`), where :math:`\theta` is
   tangent to the magnetic surface in the poloidal plane, :math:`r` is
   normal to the flux surface in the poloidal plane and :math:`\phi` is
   the angle in the toroidal direction. Later, (:math:`\theta,r,\phi`)
   is denoted as (:math:`x,y,z`).

.. _coordinates:
.. figure:: howto/catalyst/images/coordinates.*
   :alt: Global coordinate systems in three-dimensional simulation domain of B2 code: cylindrical (:math:`R,\phi,z`), parallel          (:math:`\parallel,\perp,r`), poloidal (:math:`x,y,z`).

   Global coordinate systems in three-dimensional simulation domain of B2 code: cylindrical (:math:`R,\phi,z`), parallel    (:math:`\parallel,\perp,r`), poloidal (:math:`x,y,z`).

Grid Generation Workflow
~~~~~~~~~~~~~~~~~~~~~~~~

SOLPS code provides a semi-automated grid generation workflow. A graphical
interface, DG, is used to set up input files for the grid generator.
Input data to DG contains information about the poloidal magnetic flux
on regular grid and divertor geometric data from CAD drawings or other
sources. After combining this information, the actual grid generation is
done by CARRE grid generator that constructs mesh in four following
steps .

#. Identification of the magnetic field configuration.

#. Parametrization of separatrices and outer boundaries, and partition
   of the simulation domain into regions.

#. Distribution of grid points on initial flux surfaces.

#. Mapping of grid points from one flux surface to the next.

These steps have to be repeated until a satisfactory grid is obtained.
It is then passed to ``b2ag`` code which converts the grid to input
format expected by the B2 code.

Due to the grid structure and magnetic field configuration, and the fact
that the grid generator needs to automatically apply field-alignment and
orthogonality constraints, grid generation is a demanding process. This
leads to improper mesh structure at the target plates . Usually, the
user needs to manually configure parameters that affect orthogonality in
that area.

.. _fig-grid-sub-workflow:
.. figure:: howto/catalyst/images/grid-workflow.*
   :alt: Grid generation workflow.

   Grid generation workflow.

Data Structure
~~~~~~~~~~~~~~

Quadrilateral cells in physical space are converted into unit squares on
a Cartesian coordinate system (:numref:`fig-phys-sub-comp`).
This is a computational space where each unit represents one cell in a
physical space.
Computational domain is further divided into regions, depending on the
magnetic field configuration. Line that divides them is called
separatrix. The regions are as follows.

#. Scrape-off layer (SOL)

#. Private flux region (PFR)

#. Core

Every region forms a rectangular block of cells in computational space.
Outline of the computational domain is shaped similarly to a
two-dimensional array. This allows efficient storage of cells and the
information each cell contains in three or more dimensional arrays.
Every cell :math:`\Omega_{i,j}` is identified with its position
(:math:`i,j`) and every information, e.g. position of each cell’s
vertexes, are stored in the same position. Convenient structure of
computational space itself defines each cell’s neighbors, which are the
same in computational and physical space. Neighbors are defined as
:math:`\Omega_{i{\pm}1,j{\pm}1}`. However, due to the complex geometry
between region boundaries each cell stores information about its
neighbors explicitly as well.

.. _fig-phys-sub-comp:
.. figure:: howto/catalyst/images/comp-space-and-grid.*
   :alt: B2.5 simulation domains in physical and computational space.

   B2.5 simulation domains in physical and computational space.
   (a) Mesh with :math:`98 \times 38` cells in physical space.
   (b) Grid separated into three regions in physical space.
   (c) The regions are scrape-off layer (SOL, colored in grey),
   private flux region (PFR, green), and core (blue).
   Separatrix is shown as a red line.


IMAS
----

The ITER Integrated Modelling & Analysis Suite (IMAS)  and the
EUROfusion integrated modelling (EU-IM)  effort orchestrate computation
of fusion codes with Kepler  scientfic workflow engine. Complex
integrated modelling (IM) workflows created by EU-IM task force  on top
of the Kepler framework include with several physics codes at different
time and space scales. The IMAS and EU-IM Physics Data Model (PDM) is
the main advantage in contrast to OMFIT  framework that provides physics
modules without the underlying data model that allows coupling of codes
with prescribed data structures named IDS (Interface Data Structures) or
CPO (Consistent Physical Objects). Data structures that are served
within personal or global databases are accessible with several
programming languages (Fortran, C++, Java, Python, and Matlab)
translated from XSD  schema. Kepler workflow engine, written in Java,
needs to encapsulate physics codes inside its components called
"actors". For that *component builders* were developed that helps
"classical" code developers to "wrap" their physics code written in
non-Java language by specifying communication *ports* and run-time
environment to get the *actor skeleton*. From there on developers are
required to adapt the code for PDM and any code-configurable
input-parameters into machine readable translation that is usually in
XML  language. Many IM workflows are quite straightforward to model in
Kepler and are hardly changed due to their complexity in code-coupling.

It should be noted that the coupling of codes on PDM does not binds the
user to model workflow in *Kepler* and other workflow engines could be
used instead. Some of Kepler weak points in complex IM workflows are:
(i) no fault tolerance (recover / divert / restart) capabilities, (ii)
remote execution model is part of the workflow, (iii) remote HPC/GRID/cloud
submission/data transfer policy is usually incompatible with external
workflows, (iv) variations of actors and composite actors are bound to.
Scientific workflow systems foster *open and reproducible research* and
tend to abstract computational resources inside web interfaces .
*Reproducible science* should be enabled with *workflow exchange* though
web portals such as myExperiment , *provenance* and *open data*. However,
the technical details in running the workflows are hindering exchange for
reuse and are rarely changed once created. Kepler graphical user interface
(GUI) for editing and execution is an application that typically runs in a
virtual desktop provided by a compute-cluster login-node. While scientific
workflow engines cover "task" dependencies well by creating *direct acyclic
graphs* they provide little support for interactive tasks in preparing the
input data. Physics code monitoring and visualisation is another aspect
that is not covered sufficiently and extensions are required to provide
progress evidence to users. Visualization pipeline that is often neglected
in many workflow systems is primary point of VisTrails workflow system that
concentrates in data exploration where complex 3D visualizations are
needed. Building visualization pipeline on top of VTK toolkit is also
possible with interactive 3D visualization tools such as ParaView or VisIt
that are ubiquitously used among HPC community. Important aspect for
day-to-day users is tailoring GUI to preferences while using the physics
code(s) so that they can interactively explore compute progress. For that
purpose users usually create custom GUI for controlling and monitoring in a
*dashboard* that eases the control over their cases, called "Runs" in the
*Scrape-Off Layer Plasma Simulation* (SOLPS) code together with the
standalone ParaView application for *in situ* instrumentation.

SOLPS is a package of codes developed over many years and was started as
an evaluation tool for engineers but then developed into an essential
tool that allowed combining the design and modeling process of the
divertor, with synthesizing different pieces of information from the
theoretical analysis, experimental studies and engineering intuition.
Several versions of SOLPS code exist to date. The newly developed
SOLPS-ITER  suite of codes comprise a grid generator CARRE , a tool for
specifying the material structures and providing inputs to the other
codes, DivGeo, the plasma fluid code B2 , the kinetic neutrals Monte
Carlo code Eirene , and in addition to that a bundle of plotting tools
and scripts used for post-processing.

The ambition of the SOLPS-ITER effort is to become the new standard used
across the ITER Parties for modeling not only ITER, but any other
tokamaks and linear plasma devices wherever applicable. In order to
facilitate user adoption of SOLPS-ITER and migration from earlier
versions, it has therefore been decided to include as part of the
SOLPS-ITER package, a more user-friendly interface for some of the more
tedious and error-prone tasks to ease the transition for users of older
versions and provide additional added value and incentive for those
users switching to SOLPS-ITER. At the same time, SOLPS users have, over
the years, expressed the desire for some run monitoring framework and
more powerful graphical post-processing tools.


The possibility of designing the workflows and the dashboard by extending
existing Qt tools that are traditionally used only for GUI designs and have
programmed actions in the code. With the SOLPS-ITER GUI the workflow
creation is possible with Python-based workflow engine. The workflow
execution model is independent of clusters and provided by *Runs* view.
Within the GUI *Designer* the layout of the widgets is fully configurable
and in contrast to other scientific workflow engines, provides the
dashboard as the front end to users solving the workflow monitoring problem
in user friendly way. The sharing of a complex dashboard design is
possible among users and is more oriented towards monitoring and graphical
presentation, with full visualization support. Having all these features in
mind, we would like to highlight that the approach presented in
continuation is significantly advanced for users with similar physics codes
that need to be put inside a dashboard for easy handling, coupling,
monitoring and scientific discovery exploration.
