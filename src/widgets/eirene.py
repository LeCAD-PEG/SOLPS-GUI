#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Eirene editor

Copyright (c) 2017, ITER Organization
Route de Vinon-sur-Verdon, CS 90 046, 13067 St. Paul Lez Durance Cedex, France

EIRENE editor structures input.dat in a readable tree-view with a help that
shows us a short description of input cards from Eirene manual.

The editor reads the file line by line. If format of the card is known then
help description as well as a validation is performed.

The pattern and help description are derived from the manual.

The editor widget has two main windows, one with the text in a tree-style
view and the second window contains the help description for the variables.

To start editing a line either push "F2" key or double-click. If the line
has help description, it also has a validation for editing.
"""

from PyQt5.QtCore import Qt, QSize, pyqtSignal, pyqtSlot, QEvent
from PyQt5.QtGui import QFont, QValidator
from PyQt5.QtWidgets import (QWidget, QSplitter, QTreeWidget, QTextBrowser,
                             QTreeWidgetItem, QAbstractItemView,
                             QStyledItemDelegate, QLineEdit,
                             QAbstractItemView)
import logging
import re

no_description_in_manual = """No description in manual."""

point_example = """Coordinate for corner of a triangle.
<p>Example:</p>
<p>plane triangle defined by the corners P<sub>1</sub> , P<sub>2</sub> ,
P<sub>3</sub></p>
<p>P 1 =(P1(1),P1(2),P1(3))</p>
<p>P 2 =(P2(1),P2(2),P2(3))</p>
<p>P 3 =(P3(1),P3(2),P3(3))</p>"""

eirene_params = {

'*** 1. Data for operating mode' : """The variables in this
block control some of the more general options in EIRENE such as over- all
running time, usage of dump files but also a few parameters depending on the
simulation model (drifts included or not, etc.).""",

'NOD' : """<p>No description available.</p>""",

'NMACH' : """<b>Code-number</b> for the computer used
<dl>
  <dt>= 1</dt><dd>CRAY</dd>
  <dt>= 2</dt><dd>IBM</dd>
  <dt>= 3</dt><dd>FACOM</dd>
  <dt>= 4</dt><dd>VAX</dd>
</dl>
<p>
This flag is not in use any more. In the past (eighties of last
century) it only affected the round-off error margin used for
geometrical computations. In case NMACH=1, the error tolerated in the
geometry routines is EPSGEO=1.D-10, and EPSGEO=1.D-6 for all other
values of NMACH.</p>""",

'NMODE' : """<b>Operating mode</b> <dl> <dt>= 0</dt><dd>EIRENE run as stand-
alone-code. Code coupling segment couple_Dummy.f may be used. Input block 14
has a fixed format, see section 2.14.</dd> <dt> &ne; 0</dt><dd> EIRENE calls
the code coupling subroutine INFCOP in the code coupling segment couple_Name.f
where 'Name' is a character string identifying the particular external code, to
which EIRENE is to be coupled (e.g.: Name=B2, Name=DIVIMP, Name=U-file,
Name=FIDAP, Name=EMC3, Name=OSM, etc.).  Hence: the routine INFCOP is called by
EIRENE for communication with external data sources, e.g., external data
structures for iterative mode by coupling to other codes. The calling program
for the first 3 entries of INFCOP is subroutine INPUT, and the call to
subroutine INFCOP is after reading 13 blocks from the formatted input file
(READ (IUNIN,...)). A 14th block of the input file is read from subroutine
INFCOP with the format (if any) specified there. At entry IF0COP geometrical
data are provided (overruling corresponding data in input block 2).  At entry
IF1COP plasma profiles (more generally: background medium data) are defined
(overruling the background data specified in block 5).  Any other data (e.g.,
surface- or volume source distributions overruling the data in input block 7)
are expected from entry IF2COP.</dd> <dt>&gt; 0</dt> <dd>0 If NMODE &gt; 0,
subroutine INFCOP is called once again after each completed stratum (at the
entry IF3COP(ISTRAA,ISTRAE)) to return data to another code (post-processing).
The call to IF3COP is from subroutine MCARLO, at the end of the DO 1000 -loop
over the strata. One final call to the interfacing routine (entry IF4COP) is
implemented after the calls to the EIRENE printout- and plot routines, e.g. to
perform global balances etc. after summation of the contributions from the
individual strata.</dd> </dl> """,

'NTCPU' : """<p>Maximum number of CPU seconds allowed for this run. NTCPU must
be less than or equal to the time parameter in the job-card (if any).</p> <p>If
more than one iteration is carried out (NITER, see below, this section) or more
than one time cycle (NTIME, see below, this section), then each iteration or
cycle can take up to NTCPU seconds.</p> <p>In 2008 the definition of NTCPU was
slightly changed: the initialisation overhead is not any longer included in
NTCPU. I.e., this variable NTCPU now is close to the true Monte Carlo sampling
time. The total cpu-time, including initialisation overhead as well as post-
processing is printed at the end of an EIRENE run (see: "total cpu-time of this
run" in printout file).</p>""",

'NFILE' : """<b>Flag for the use of dump files FT10, FT11, FT12, FT13,
FT14 and FT15.</b>
<dl>
  <dt>= 0</dt><dd>Neither reading nor saving of data is done.</dd>
  <dt>= JKLMN:</dt>
  <dt>N = 1</dt><dd>EIRENE writes output data from this run into files
FT10 and FT11 to save them for plot or printout options in this or in
later 'read only' runs with the same input file.</dd>
<dt>N = 6</dt><dd>same as N=1, but only the data for the sum over all
strata are written (sufficient, e.g., for BGK-iterations, or for post
processing, (subroutine DIAGNO, see input block 12) as long as this
post processing only is to be done on total results (not on
contributions from individual strata).</dd>
<dt>N = 2</dt><dd> EIRENE reads output data from an earlier run from
files FT10 and FT11. No new particle histories are computed, only the
requested output is printed and plots are produced. Iteration cycles
or time cycles (if any) are abandoned.</dd>
<dt>N = 7</dt><dd>same as N=2, but only the data for the sum over
strata are read. See N=6 option described above.</dd>
<dt>M = 1</dt><dd>EIRENE writes geometry data into file FT12. These
data are the output from subroutines GRID and VOLUME in the
initialization phase.</dd>
<dt>M = 2</dt><dd>EIRENE reads geometry data from file FT12. The
geometry subroutines GRID and VOLUME are not called. This option
should be used if the geometry has not changed as compared to an
earlier run. It reduces the CPU costs for the overhead.</dd>
<dt>L = 1</dt><dd>EIRENE writes plasma data and atomic and molecular
data ("A&amp;M data") into file FT13. These data are output from
subroutines PLASMA, XSECTA, XSECTM, XSECTI, XSECTP in the
initialization phase. At the end of a run, some background medium data
may have been modified in subroutine MODUSR, (iterative mode) see
NITER flag below. In this case FT13 may be re-written to prepare for
next iterations.</dd>  Also the primary source parameters (input block
7) are saved, for later iterations or time-steps.</dd>
<dt>L = 2</dt><dd>EIRENE reads plasma data, A&M data from file
FT13. It also reads the entire input block 7 from FT13, and overwrites
the input read from this block 7 by those data. Routines PLASMA,
XSECTA, XSECTM, XSECTI, XSECTP are not called. This option should be
used if neither the plasma background nor the selection of atomic
processes to be used, nor the primary source model (block 7) has
changed as compared to an earlier run. It then reduces the CPU costs
for the overhead.</dd>
<dt>L = 3</dt><dd>Acts as if both NFILE-L=1 and
NFILE-L=2. I.e. reading background data from file, and writing new
background data onto file at the end of the run, the time-step or the
iteration. For continuation of iterative calculations, for
example.</dd>
<dt>L = 4</dt><dd>Same as NFILE-L=3, except: primary source data
(input block 7) are not read from fort.13, but are taken as specified
in input block 7. This allows to modify these primary sources
parameters during iterations or time-steps not only via module MODUSR,
but directly via input file.</dd>
<dt>L = 6,7,8,9</dt><dd>Same as L=1,2,3,4, respectively, but XDR file
format is used.</dd>
<dt>K = 1</dt><dd>EIRENE saves some data for optimizing non-analog
sampling and stratified source sampling on file FT14.</dd>
<dt>K = 2</dt><dd>EIRENE reads from file FT14 and tries to optimize
operation for the next run, time-step or iteration. Currently only
allocation of CPU time in stratified source sampling is
optimized. More details: see paragraph 2.1.1 below.</dd>
<dt>K = 3</dt><dd>Acts as if both NFILE-K=1 and NFILE-K=2.</dd>
<dt>J = 1</dt><dd>Only for time-dependent option (see block
13). EIRENE writes "census data" at the end of last time-step onto
file FT15.</dd>
<dt>J = 2</dt><dd>EIRENE reads "census data" from file FT15, and uses
it as initial distribution for the coming next time-step.</dd>
<dt>J = 3</dt><dd>Acts as if both NFILE-J=1 and NFILE-J=2.</dd>
</dl>""",

'NITER0' : """<p>Initial iteration number: (Default: NITER0=1) Irrelevant
parameter. Only needed for book keeping and printout. EIRENE labels the
iterations from NITER0 to NITER.</p>""",

'NITER' : """<p>Number of iterations, if EIRENE runs in "iterative
mode".</p>
<dl>
<dt>&gt; 0</dt><dd>EIRENE calls user supplied subroutine MODUSR after
completing the run; some model parameters may be modified here for the
next iteration step, and some results from the previous step may be
saved on a file.</dd>
<dt>&gt;1</dt><dd>EIRENE recalls itself but does not read from the
formatted input file again. This recalling is repeated NITER times
(including the first iteration). The CPU time NTCPU is used for each
iteration. Hence the true CPU time then is NTCPU NITER.</dd>
</dl>""",

'NTIME0': """<p>Initial time-cycle number: (default: NTIME0=1). Irrelevant.
Only needed for book keeping and printout. EIRENE labels the time steps from
NTIME0 to NTIME.</p>""",

'NTIME' : """<p>Total number of iterations ("cycles") in time carried out in
one single run. The total time per cycle is defined as NTMSTP * DTIMV (see
below, input block 13).</p> <p>After each time-cycle the subroutine TMSTEP is
called. In this routine the "census arrays", which store the test particle
population at time ti: ti = ti1 + t = t0 + it = TIME0 + ITIME [NTMSTP * DTIMV
] are filled and prepared for the next time-cycle. The census arrays from the
previous time cycle (if any), i.e., at t = ti1, are overwritten here. <p>After
the last time-cycle, the census arrays are written on file fort.15, in order
to permit continuation in time in a next run.  The background conditions (and
source distributions or any other input parameters) for the next time cycle
can be modified in subroutine TMSUSR(ti), which is called from subroutine
TMSTEP.</p> <p>If the population on the census array is not empty or known
from a previous run (NFILE-J flag, see above), then this census population
defines one additional stratum for the current cycle. I.e., the census
population then determines the initial condition for the distribution function
f(r; v; i; t = t0). The source strength FLUX is computed from that initial
condition.</p>""",

'NOPTIM' : """<p>Default: NRAD, = total number of grid cells (verify this
default in case of older versions: there it may have been NOPTIM=1) NOPTIM is
the first dimension of the arrays IGJUM3(ICELL,ISURF), which may be used for
optimizing code performance by reducing unnecessary geometrical calcula-
tions.</p>""",

'NOPTM1': """<p>Default: 1</p>""",

'NGEOM_USR' : """<p>for value =1: user defined (external) geometry package
(LEVGEO=10), then no grid storage is provided in EIRENE. Default: 0</p>""",

'NCOUP_INPUT' : """<p> =1: Storage for data transfer via coupling routines, =0:
no such storage.  Default: 1</p>""",

'NSMSTRA' : """<p>"Sum over strata" disabled for value 0, enabled for value 1.
Default: 1</p>""",

'NSTORAM' : """<p>Storage vs.  speed in atomic data evaluation. Maximum
storage, fastest com- putation: =9. Minimum storage, maximum work (slowest
option) =0. Default: 9</p>""",

'NGSTAL' : """<p>Storage for spatial distribution of surface tallies on non-
default standard surfaces for value =1. For value =0: only total (spatially
integrated) surfaces fluxes. Default: 0</p>""",

'NRTAL' : """<p>Condensing mesh cells into fewer larger cells, for output
volume tallies. The under- lying fine mesh has NRAD cells (see input block 2).
The coarser mesh, obtained from condensing cells into one larger cell, has
NRTAL cells.  Default: 0: Then internally: NRTAL=NRAD, and no condensation is
carried out.</p> <p>NCLTAL(IRAD) = IRTAL: grid cell IRAD is condensed into the
larger cell IRTAL.  I.e.: output is average over a larger cell IRTAL, which is
comprised of all cells IRAD such that NCLTAL(IRAD) = IRTAL, IRAD=1, NRAD</p>
<p>The input data in input block 5 (background medium) are always given on the
fine mesh (size: NRAD)</p> <p>For output tallies (cell averaging) several
cells IRAD1, IRAD2,... can be condensed into one larger cell IRTAL. Cell
volumes, scoring, statistics are automatically done on the coarser grid (size:
NRTAL).</p> <p>The index array NCLTAL(NRAD) can be defined in the problem
specific "user" rou- tines (see section 3), e.g.: INIUSR, GEOUSR, etc..</p>
<p>Default: NCLTAL(IRAD)=IRAD for IRAD=1,NRAD</p>""",

'NREAC_ADD' : """<p> Storage for additional reaction decks read onto EIRENE
arrays in USR- routines, post-processing, etc. Default: 0</p>""",

'NLSCL' : """<p>Some volume averaged tallies are re-scaled in order to exactly
preserve the total number of particles, which otherwise would be the case only
up to statistical precision (due to the use of track-length estimators).
EIRENE computes three factors FATM, FMOL and FION such that particle balances
for atoms, molecules and test ions, respectively, are accurately observed,
if NLSCL = TRUE.</p>""",

'NLTEST' : """<p>Tests for consistency between cell numbers and geometrical
data along the particle tracks are carried out at each point of collision. If
inconsistencies are detected, the history is stopped and an error message is
printed. The contribution of these particles to the particle- and energy
balances is stored in the bins "PTRASH" and "ETRASH" respectively.""",

'NLANA' : """<p>De-activates (NLANA=.TRUE.) all non-analog sampling
distributions, such as biased source sampling, splitting, etc.. Select
NLANA=.TRUE., if particle trajectory plots are used to get an intuitive
picture of what is going on physically.</p>""",

'NLDRFT' : """<p>Drift component in the bulk ions velocity distribution is
included, i.e. the assumed underlying distribution in velocity space is a
drifting Maxwellian for volumetric background tallies of bulk particles. (see
input block 5, input tallies VXIN, VYIN, VZIN)). Otherwise (if NLDRFT = FALSE)
an isotropic Maxwellian distribution is assumed for the background particles
and the input for VXIN,...VZIN is ignored.  This flag also affects the output
tallies for energy exchange, momentum exchange between test particles and
background particles, as well as sampling from linear collision
kernels.</p>""",

'NLCRR' : """<p>Correlated sampling is used. See discussion at end of section
1.8.""",

'NLERG' : """<p>The case is automatically reduced to a case for estimating cell
volumes by utilizing an "ergodic property". More details: see paragraph 2.1.2
below.</p>""",

'NLIDENT' : """<p>In multi-processor calculation mode NLIDENT forces all
processors working on the same stratum to use the same sequence of random
numbers and hence to carry out exactly identical work. This flag can be used
to test the parallelized code version.</p>""",

'NLONE' : """<p>The case is automatically reduced to a single species and "one
speed transport" problem (to simplify setting up cases for comparison with
analytic results). (not ready, don't use)</p>""",

'NLMOVIE' : """<p>reset a number of model parameters to enable a series of
geometry plots for making particle trajectory movies. This option only works
in connection with time dependent mode, see NTIME flag described above, and
input block 2.13. More details: see paragraph 2.1.3 below.</p>""",

'NLDFST' : no_description_in_manual,
'NLOLDRAN' : no_description_in_manual,
'NLCASCAD' : no_description_in_manual,
'NLOCTREE' : no_description_in_manual,
'NLWRMSH' : no_description_in_manual,
'NEXVS' : no_description_in_manual,
'NLTRIMESH' : no_description_in_manual,

'CFILE' : """There can be any number of these cards starting with character
string CFILE in the input file. <quote>CFILE</quote> DBHANDLE DBFNAME""",

# *** 2.

'*** 2. Data for standard mesh' : """EIRENE follows atoms, molecules or test
ions in a 3-dimensional computational box. This box is discretized by zones
(mesh cells), the boundaries of which are defined either by regular
&quot;standard mesh surfaces&quot;, i.e., co-ordinate surfaces, which are
described here, and/or by zones whose boundaries are defined more generally by
&quot;additional surfaces&quot; (see below block 3B).""",

'INGRD(1)' : """This index controls the meaning of input
variables of different standard grid options.
<dl>
  <dt>INDGRD(1)</dt><dd>for the radial (or x-direction) grid</dd>
  <dt>INDGRD(2)</dt><dd>for the poloidal (or y-direction) grid</dd>
  <dt>INDGRD(3)</dt><dd>for the toroidal (or z-direction) grid</dd>
</dl>
Data for first standard mesh: radial or x grid RSURF""",

'INGRD(2)' : """This index controls the meaning of input variables of
different standard grid options.
<dl>
  <dt>INDGRD(1)</dt><dd>for the radial (or x-direction) grid</dd>
  <dt>INDGRD(2)</dt><dd>for the poloidal (or y-direction) grid</dd>
  <dt>INDGRD(3)</dt><dd>for the toroidal (or z-direction) grid</dd>
</dl>
Data for first standard mesh: radial or x grid RSURF""",

'INGRD(3)' : """This index controls the meaning of input variables of
different standard grid options.
<dl>
  <dt>INDGRD(1)</dt><dd>for the radial (or x-direction) grid</dd>
  <dt>INDGRD(2)</dt><dd>for the poloidal (or y-direction) grid</dd>
  <dt>INDGRD(3)</dt><dd>for the toroidal (or z-direction) grid</dd>
</dl>
Data for first standard mesh: radial or x grid RSURF""",

'NLRAD' : """
<p>A radial or x grid is defined. Otherwise the complete sub-block 2A
may be omitted.  Depending upon the logical parameters in the next
input card the "geometry - level" variable LEVGEO is set internally.
<dl>
  <dt>LEVGEO=1 </dt><dd>cartesian coordinates x (and y)</dd>
  <dt>LEVGEO=2 </dt><dd>polar coordinates r (and &Theta;)</dd>
  <dt>LEVGEO=3 </dt><dd>general curvilinear coordinates: a full 2D mesh
                        (polygonal coordinate lines) is used in the x - y
                        plane. Grid cuts are permitted in the y-direction.
                        </dd>
  <dt>LEVGEO=4 </dt><dd>a 2D "finite element" mesh of triangles is used in the
                          x - y plane</dd>
  <dt>LEVGEO=5 </dt><dd>a 3D "finite volume" mesh of tetrahedrons used</dd>
  <dt>LEVGEO=10</dt><dd>a general, user defined geometry block is used. All
                        geometrical calculations are performed in problem
                        specific routine VOLUSR, TIMUSR, ...etc.</dd>
</dl>
<p>If NLRAD=.FALSE., then no spatial grid is defined and the default
geometry level</dd> LEVGEO = 1 is used. Volume discretisation may
still be achieved "by hand" by defining</dd> "additional surfaces"
(input block 3b) and appropriate cell number switching.</p>""",

'NLSLB' : """<p>Geometry level: LEVGEO = 1</p> <p> Cartesian geometry, the x
co-ordinate is discretized by setting:</p> <p>x<sub>1</sub> = RSURF(I)  I=1,
NR1ST.</p> <p> Furthermore, the flux-surface labeling grid RHOSRF(I) is
identical with the grid RSURF(I).</p>""",

'NLCRC' : """<p>Geometry level: LEVGEO = 2</p> <p>Cylindrical or toroidal
geometry, 1D ("radial") mesh of concentric, circular surfaces.  Polar
coordinates are used in the x-y plane.  The third coordinate (either
<em>z</em> or toroidal angle &phi;)</p> <p>The radial surfaces are given by
<em>r<sup>2</sup> = x<sup>2</sup> + y<sup>2</sup> = const</em>. and radial
coordinate <em>r</em> is discreticized by setting r<sub>1</sub>=RSURF(I) I=I,
NR1ST. Furthermore RHOSRF(I)= &radic; &nbsp;AREA/&pi; where AREA is the
area inside surface number I. Thus for this option one has
again:RHOSRF(I)=RSURF(I), I=1, NR1ST. </p>""",

'NLELL' : """
<p>Geometry level: LEVGEO = 2</p>
<p>Mesh of nested, but
not necessarily concentric or confocal elliptical flux surfaces. The equation
for the "radial" surface is <em>(x-EP)<sup>2</sup> + (y/EL)<sup>2</sup> =
r<sup>2</sup></em>. The radial coordinate <em>r</em> is discretized  by
setting <em>r<sub>I</sub></em>=RSURF(I) I=1, NR1ST.</p>
<p>EP and EL may vary
with coordinate <em>r</em>. These parameters are stored in the arrays
EP(I),EL(I), I=1,NR1ST which now are used in addition to RSURF to define one
co- ordinate surface in the first (radial or <em>x</em>-grid).</p>
 <p>RHOSRF:as in NLCRC option</p> <p>Note: RHOSRF and RSURF may differ in this
case.</p>""",

'NLTRI' : """<p>Geometry level: LEVGEO = 2</p> <p>to be written:
triangularity in mesh of nested closed algebraic surfaces</p>""",

'NLPLG' : """<p>Geometry level: LEVGEO = 3</p> <p>The mesh in the x-y plane is
described by NR1ST polygonal arcs of length NRPLG each.  A polygon may consist
of several "valid" and "invalid" parts (to account for "grid cuts" in CFD
meshes). The "invalid" parts of a polygon are not seen by test particles and
are allowed for in EIRENE only in order to facilitate index mapping in case of
runs coupled to plasma transport models, which resort to computer generated
meshes including grid cuts.</p> <p>The polygons must not intersect each
other.</p> <p>In this case RHOSRF(1)=0., and RHOSRF(I) is the area enclosed by
polygon number 1 and polygon number I.</p>""",

'NLFEM' : """<p>Geometry level: LEVGEO = 4</p> <p>The mesh in the x-y plane
consists of NR1ST triangles,  composed from NRKNOT knots.</p> <p>In this case
a flux surface labeling grid RHOSRF is not defined.</p>""",

'NLTET' : """<p>Geometry level: LEVGEO = 5</p> <p>3D discretisation of volume
by tetrahedrons.  For this grid option please make contact to the
authors.</p>""",

'NLGEN' : """<p>Geometry level: LEVGEO = 10</p> <p>Arbitrary geometrical
configuration.  Mesh consists of NR1ST arbitrarily shapes cells (in  any
dimension).   Particle  tracing  routines  must  be  provided  by  user
(VOLUSR, SAMUSR, TIMUSR, LEAUSR)</p>""",

'NR1ST' : """Number of grid-points in the radial (or x-direction) standard mesh
<p>if NR1ST&le;1, no radial (or x-direction) standard mesh is defined.</p>
<p>if NLPLG = .TRUE. : number of polygons for discretisation in "radial" or x
direction</p> <p>if NLFEM = .TRUE. : number of triangles for discretisation in
x-y plane</p> <p>if NLTET = .TRUE. or if NLGEN = .TRUE. : number of cells in
otherwise arbitrary mesh option NLGEN. Use problem specific routines to set up
mesh, cell volumes, and flight interesction times for test partilces.</p>""",

'NRSEP' : """This flag is active for LEVGEO = 1 or LEVGEO = 2. Otherwise it is
irrelevant. <p>The  first  (x-  or  radial)  standard  mesh  is  composed  by
two  equidistant  x-  or  radial grids of co-ordinate surfaces with different
grid density.  There are NR1ST-NRSEP+1 grid-points  in  the  first,  and
NRSEP  grid-points  in  the  second  part.   The  grid-point RSURF(NR1ST-
NRSEP+1) belongs to both parts.</p>""",

'RIA' : """left endpoint of standard grid (internally set &ge; 0 if LEVGEO = 2)
; RSURF(1)=RIA""",

'RGA' : """boundary separating first and second part of standard grid with
different grid-point densities; RSURF(NR1ST-NRSEP+1)=RGA""",

'RAA' : """right endpoint of standard grid: RSURF(NR1ST)=RAA""",

'RRA' : """if RRA &gt; RAA, one additional, outer void zone is defined
<p>RSURF(NR1ST)=RRA, and the parameter RAA now determines the surface no.
NR1ST- 1.</p> <p>(irrelevant, if RRA &le; RAA)</p>""",

'EPIN' : """if NLELL = .TRUE. : <p>Value of EP(r) for cylindrical co-ordinate
surface number 1 with <em>r<sub>1</sub></em>=RIA (see:  NL- CRC = .TRUE.
option above)</p>""",

'EPOT' : """if NLELL = .TRUE. : <p> Value of EP(r) for cylindrical surface
number NR1ST with <em>r<sub>NR1ST</sub></em>=RAA</p>""",

'EPCH' : """if NLELL = .TRUE. : <p> Value of EP(r) for cylindrical surface
number NR1ST+1 with <em>r<sub>NR1ST+1</sub></em>=RAA</p> <p>(irrelevant, if
RRA &le; RAA)</p>""",

'EXEP' : """if NLELL = .TRUE. : <p>The variation of the "shift function" EP(r)
with r is given by</p> <p><em>EP(r) = EPIN + ((r-RIA)/(RAA-
RIA))<sup>EXEP</sup> * (EPOT - EPIN)</em></p>""",

'ELIN' : """if NLELL = .TRUE. : <p>Value of EL(r) for cylindrical surface
number 1 with <em>r<sub>1</sub></em>=RIA (see: NLELL = .TRUE. option)</p>""",

'ELOT' : """if NLELL = .TRUE. : <p>Value of EL(r) for cylindrical surface
number NR1ST with <em>r<sub>NR1ST</sub></em>=RAA</p>""",

'ELCH' : """if NLELL = .TRUE. : <p>Value of EL(r) for cylindrical surface
number NR1ST+1 with <em>r<sub>NR1ST+1</sub></em>=RAA</p> <p>(irrelevant for
RRA &le; RAA)</p>""",

'EXEL' : """if NLELL = .TRUE. : <p>The variation of the "ellipticity  function"
EP(r) with r is given by</p> <p><em>EP(r) = EPIN + ((r-RIA)/(RAA-
RIA))<sup>EXEP</sup> * (EPOT - EPIN)</em></p>""",

'TRIN' : """if NLTRI = .TRUE. : <p> to  be  written:  the  option  for
algbraically  given  triangular grids is currently no available. </p>""",

'TROT' : """if NLTRI = .TRUE. : <p> to  be  written:  the  option  for
algbraically  given  triangular grids is currently no available. </p>""",

'TRCH' : """if NLTRI = .TRUE. : <p> to  be  written:  the  option  for
algbraically  given  triangular grids is currently no available. </p>""",

'EXTR' : """if NLTRI = .TRUE. : <p> to  be  written:  the  option  for
algbraically  given  triangular grids is currently no available. </p>""",

'NRPLG' : """if NLPLG = .TRUE. : <p>Number of points per polygon</p>""",

'NPPLG' : """if NLPLG = .TRUE. : <p>Number of valid parts on each polygon. Each
polygon is described by the x and y co-ordinates of NRPLG points.  It is not
necessary that all this points are used for the polygon.  One can cut the
polygon into several valid parts interrupted by parts which are not seen by
the test particles.  ( Default :  NPPLG = 1 ).  This option facilitates the
use of 2-d computer generated meshes which contain topological grid
cuts.</p>""",

'XPCOR' : """<p>if NLPLG = .TRUE. : shift whole mesh by that vector in
x,y-plane</p> <p>if NLFEM = .TRUE. : x and y co-ordinates of the knots,
respectively</p>""",

'YPCOR' : """if NLPLG = .TRUE. : <p>shift whole mesh by that vector in
x,y-plane</p> <p>if NLFEM = .TRUE. : x and y co-ordinates of the knots,
respectively</p>""",

'RFPOL' : """if NLPLG = .TRUE. : <p> if RFPOL > 0., one additional polygon zone
is defined, at a distance RFPOL out- side the polygon NR1ST, and then NR1ST is
increased by one.</p> <p>(irrelevant, if RFPOL &le; 0.)</p>""",

'NPOINT(1,J)' : """if NLPLG = .TRUE. : <p>Index of the first point of the valid
part number J (same for each radial polygon)</p> <p>( Default : NPOINT(1,1) =
1 )</p>""",

'NPOINT(2,J)' : """if NLPLG = .TRUE. : <p>Index of the first point of the valid
part number J (same for each radial polygon)</p> <p>( Default : NPOINT(2,1) =
NRPLG  )</p>""",

'XPOL(K,I)' : """if NLPLG = .TRUE. : <p>x-co-ordinate of the polygon point
number K on polygon number I</p>""",

'YPOL(K,I)' : """if NLPLG = .TRUE. : <p>y-co-ordinate of the polygon point
number K on polygon number I</p>""",

'NRKNOT' : """if NLFEM = .TRUE. : <p>There are NRKNOT knots, by which the
triangles are defined</p>""",

'XTRIAN' : """if NLFEM = .TRUE. : <p>x and y co-ordinates of the knots,
respectively</p>""",

'YTRIAN' : """if NLFEM = .TRUE. : <p>x and y co-ordinates of the knots,
respectively</p>""",

'NVERT(I,ITRI)' : """if NLFEM = .TRUE. : <p>Each triangle ITRI is defined by 3
points <em>P<sub>1</sub>, P<sub>2</sub>, P<sub>3</sub></em>  from the set of
NRKNOT knots. NVERT(I,ITRI) is the number of point P<sub>I</sub> (I=1,2,3) in
the set of knots for triangle ITRI.<p>""",

'NSIDE(I,ITRI)' : """if NLFEM = .TRUE. : <p>NSIDE(I,ITRI) is the number (1,2 or
3) of the side of the neighboring triangle, which corresponds to side
S<sub>I</sub> of the triangle ITRI to be written</p>""",

'IPROP(I,ITRI)' : """if NLFEM = .TRUE. : <p>ISTS = ABS(IPROP) is the integer,
by which a particular surface property is assigned to side I of the triangle
ITRI. ISTS=0 stands for default grid option (transparent surface, cell
indexing is done automatically).  Otherwise ISTS is the number of an
additional (ISTS < NLIMI)  or  non-default  standard  (NLIM < ISTS <
NLIM+NSTSI)  surface option as read in sub-blocks 3a or 3b, respectively.  By
default the normal vector of each side of a triangle points out of the
triangle. In case IPROP < 0, this vector points into the triangle. This is
relevant at surface options with ILSIDE &ne; 0.</p>""",

'NLPOL' : """if NLTET or NLGEN = .TRUE.: <p>A poloidal or y grid is defined.
Otherwise the complete block 2B may be omitted and the volume averaged tallies
are then automatically integrated over this co-ordinate.</p> """,

'INDGRD(2)' : """if NLTET or NLGEN = .TRUE.: <dl> <dt>= 1</dt><dd>standard grid
option</dd> <dt>= 2,3,4,5,6</dt><dd>not in use (default: INDGRD(2)=1)</dd>
</dl>""",

'NP2ND' : """if NLTET or NLGEN = .TRUE.: <p>Number of grid-points in y- or
poloidal direction</p>""",

'YIA' : """if NLTET or NLGEN = .TRUE.: <dl> <dt>for the LEVGEO=1
option:</dt><dd>the y grid PSURF is defined in the same way as the x grid,
using the parameters YIA,YGA,.... (cm) instead of RIA,RGA,....</dd> <dt>for
the LEVGEO=2 option:</dt><dd>the  poloidal  angle &theta; grid  PSURF  is
defined  in  the  same  way  as  the  radial <em>r</em> grid was, using the
parameters YIA,YGA,...(poloidal angle in degree) instead of RIA,RGA,... <p>for
all options LEVGEO > 2: this input card is irrelevant.</p></dd> </dl>
<p>Defaults: (needed for scaling, i.e., cell volumes): YIA=0., YGA=0., YAA=1.,
YYA=1. in case of LEVGEO=1, and YIA=0., YGA=0., YAA=360., YYA=360. in case of
LEVGEO=2.</p>""",

'YGA' : """if NLTET or NLGEN = .TRUE.: <dl> <dt>for the LEVGEO=1
option:</dt><dd>the y grid PSURF is defined in the same way as the x grid,
using the parameters YIA,YGA,.... (cm) instead of RIA,RGA,....</dd> <dt>for
the LEVGEO=2 option:</dt><dd>the  poloidal  angle &theta; grid  PSURF  is
defined  in  the  same  way  as  the  radial <em>r</em> grid was, using the
parameters YIA,YGA,...(poloidal angle in degree) instead of RIA,RGA,... <p>for
all options LEVGEO > 2: this input card is irrelevant.</p></dd> </dl>
<p>Defaults: (needed for scaling, i.e., cell volumes): YIA=0., YGA=0., YAA=1.,
YYA=1. in case of LEVGEO=1, and YIA=0., YGA=0., YAA=360., YYA=360. in case of
LEVGEO=2.</p>""",

'YAA' : """if NLTET or NLGEN = .TRUE.: <dl> <dt>for the LEVGEO=1
option:</dt><dd>the y grid PSURF is defined in the same way as the x grid,
using the parameters YIA,YGA,.... (cm) instead of RIA,RGA,....</dd> <dt>for
the LEVGEO=2 option:</dt><dd>the  poloidal  angle &theta; grid  PSURF  is
defined  in  the  same  way  as  the  radial <em>r</em> grid was, using the
parameters YIA,YGA,...(poloidal angle in degree) instead of RIA,RGA,... <p>for
all options LEVGEO > 2: this input card is irrelevant.</p></dd> </dl>
<p>Defaults: (needed for scaling, i.e., cell volumes): YIA=0., YGA=0., YAA=1.,
YYA=1. in case of LEVGEO=1, and YIA=0., YGA=0., YAA=360., YYA=360. in case of
LEVGEO=2.</p>""",

'YYA' : """if NLTET or NLGEN = .TRUE.: <dl> <dt>for the LEVGEO=1
option:</dt><dd>the y grid PSURF is defined in the same way as the x grid,
using the parameters YIA,YGA,.... (cm) instead of RIA,RGA,....</dd> <dt>for
the LEVGEO=2 option:</dt><dd>the  poloidal  angle &theta; grid  PSURF  is
defined  in  the  same  way  as  the  radial <em>r</em> grid was, using the
parameters YIA,YGA,...(poloidal angle in degree) instead of RIA,RGA,... <p>for
all options LEVGEO > 2: this input card is irrelevant.</p></dd> </dl>
<p>Defaults: (needed for scaling, i.e., cell volumes): YIA=0., YGA=0., YAA=1.,
YYA=1. in case of LEVGEO=1, and YIA=0., YGA=0., YAA=360., YYA=360. in case of
LEVGEO=2.</p>""",

'NLTOR' : """<p>A toroidal or z grid is defined.  Otherwise the complete block
2C may be omitted and the volume averaged tallies are then automatically
integrated over this co-ordinate.</p> <p>In case NLTOR = TRUE, sub-block 2C
must be read</p>""",

'INDGRD(3)' :  """<dl> <dt>= 1</dt><dd>standard grid option</dd> <dt>=
2,3,4,5,6</dt><dd>not in use (default: INDGRD(3)=1)</dd> </dl>""",

'NLTRZ' : """=TRUE <p>cylindrical approximation is used, i.e., TSURF is a grid
in z direction. The co-ordinate surfaces are given by z=TSURF(L)</p>
<p>(Default: NLTRZ = TRUE)</p>""",

'NLTRA' : """=TRUE <p>toroidal approximation is used. The coordinate line is a
polygonal approximation of a circle, or an angular section thereof.</p> <p>In
case NLTOR = TRUE, the 3rd grid TSURF is a grid of toroidal angles. The
toroidal segment (or the full torus) is approximated by NT3RD-1 straight
cylindrical segements.</p> <p>In case NLTOR = FALSE, there are NTTRA toroidal
periodicity boundaries, such that the toroidal segment is approximated, again,
by NTTRAM=NTTRA-1 straight cylin- ders, but without toroidal resolution in the
results. (Note: If NLTOR, NTTRA=NT3RD, internally.)</p> <p>The torus axis of
the entire mesh can be shifted in radial direction by adding a radial offset
ROA (see below) to the x coordinates of the poloidal mesh (RSURF,PSURF).</p>
<p>The radial shift of the poloidal mesh RMTOR of the approximated torus is
computed from ROA such that the volume inside radial surface NR1ST is exactly
equal to the volume of an exact torus with poloidal cross section defined by
the shifted radial grid (first standard mesh: RSURF).</p> <p>Due  to  the
approximations  made  by  defining  a  torus  by  NTTRAM  =  NTTRA  -  1
straight cylinders, this condition is fulfilled only approximately for the
other radial sur- faces. RMTOR converges to ROA with increasing NTTRA. NTTRA
&#x2243; 30 is already a very good  approximation.</p> <p>(Default: NLTRA =
FALSE).</p>""",

'NLTRT' : """=TRUE <p>torus co-ordinates R,PHI,THETA. Presently being developed
for NLSLB,NLPLG and NLTRI options. Not ready for use.</p>""",

'NT3RD' : """<p>Number of grid-points in z- or toroidal direction</p>
<p>(default: NT3RD = 1, i.e. no grid is defined)</p>""",

'NTTRA' : """
only needed in case NLTRA and .NOT.NLTOR. See above.""",

'ZIA' : """<p>The 3rd grid ZSURF is defined in the same way as the x grid,
using the parameters ZIA, ZGA,.... (cm) instead of RIA, RGA,....</p> <p>In
case of NLTRZ = TRUE , a z-grid is defined. ROA is irrelevant.</p> <p>In case
of NLTRA = TRUE , ZIA and ZAA are toroidal angles (in degrees). A grid of
toroidal angles is defined.  For example use ZIA=0.0 and ZAA=360.0 for a full
torus. In case NLTOR this grid also defines the toroidal resolution.  If
.NOT.NLTOR, then periodicity at the endpoints ZIA and ZAA is automatically
enforced.</p> <p>ROA is the radial shift of the poloidal cross section defined
by the x-y grids.  E.g.:  if the x-y- grids are given with magnetic axis as
origin, then ROA is the major radius. If the x-y- grids are already given with
respect to the torus axis at their origin, then ROA =0 (or better
e.g.:1.0E-4=ROA &#x226A 1)</p> <p>Note: ROA affects evaluation of cell
volumes.</p> <p>Note also: in case of geometry and trajectory plots (input
block 11), this major radius offset ROA of poloidal cross sections has to be
taken into account when defining plot- frames.</p> <p>(Defaults: NLTRA =
FALSE, ZIA = 0 , ZAA = 1)</p>""",

'ZGA' : """<p>The 3rd grid ZSURF is defined in the same way as the x grid,
using the parameters ZIA, ZGA,.... (cm) instead of RIA, RGA,....</p> <p>In
case of NLTRZ = TRUE , a z-grid is defined. ROA is irrelevant.</p> <p>In case
of NLTRA = TRUE , ZIA and ZAA are toroidal angles (in degrees). A grid of
toroidal angles is defined.  For example use ZIA=0.0 and ZAA=360.0 for a full
torus. In case NLTOR this grid also defines the toroidal resolution.  If
.NOT.NLTOR, then periodicity at the endpoints ZIA and ZAA is automatically
enforced.</p> <p>ROA is the radial shift of the poloidal cross section defined
by the x-y grids.  E.g.:  if the x-y- grids are given with magnetic axis as
origin, then ROA is the major radius. If the x-y- grids are already given with
respect to the torus axis at their origin, then ROA =0 (or better
e.g.:1.0E-4=ROA &#x226A 1)</p> <p>Note: ROA affects evaluation of cell
volumes.</p> <p>Note also: in case of geometry and trajectory plots (input
block 11), this major radius offset ROA of poloidal cross sections has to be
taken into account when defining plot- frames.</p> <p>(Defaults: NLTRA =
FALSE, ZIA = 0 , ZAA = 1)</p>""",

'ZAA' : """<p>The 3rd grid ZSURF is defined in the same way as the x grid,
using the parameters ZIA, ZGA,.... (cm) instead of RIA, RGA,....</p> <p>In
case of NLTRZ = TRUE , a z-grid is defined. ROA is irrelevant.</p> <p>In case
of NLTRA = TRUE , ZIA and ZAA are toroidal angles (in degrees). A grid of
toroidal angles is defined.  For example use ZIA=0.0 and ZAA=360.0 for a full
torus. In case NLTOR this grid also defines the toroidal resolution.  If
.NOT.NLTOR, then periodicity at the endpoints ZIA and ZAA is automatically
enforced.</p> <p>ROA is the radial shift of the poloidal cross section defined
by the x-y grids.  E.g.:  if the x-y- grids are given with magnetic axis as
origin, then ROA is the major radius. If the x-y- grids are already given with
respect to the torus axis at their origin, then ROA =0 (or better
e.g.:1.0E-4=ROA &#x226A 1)</p> <p>Note: ROA affects evaluation of cell
volumes.</p> <p>Note also: in case of geometry and trajectory plots (input
block 11), this major radius offset ROA of poloidal cross sections has to be
taken into account when defining plot- frames.</p> <p>(Defaults: NLTRA =
FALSE, ZIA = 0 , ZAA = 1)</p>""",

'ZZA' : """<p>The 3rd grid ZSURF is defined in the same way as the x grid,
using the parameters ZIA, ZGA,.... (cm) instead of RIA, RGA,....</p> <p>In
case of NLTRZ = TRUE , a z-grid is defined. ROA is irrelevant.</p> <p>In case
of NLTRA = TRUE , ZIA and ZAA are toroidal angles (in degrees). A grid of
toroidal angles is defined.  For example use ZIA=0.0 and ZAA=360.0 for a full
torus. In case NLTOR this grid also defines the toroidal resolution.  If
.NOT.NLTOR, then periodicity at the endpoints ZIA and ZAA is automatically
enforced.</p> <p>ROA is the radial shift of the poloidal cross section defined
by the x-y grids.  E.g.:  if the x-y- grids are given with magnetic axis as
origin, then ROA is the major radius. If the x-y- grids are already given with
respect to the torus axis at their origin, then ROA =0 (or better
e.g.:1.0E-4=ROA &#x226A 1)</p> <p>Note: ROA affects evaluation of cell
volumes.</p> <p>Note also: in case of geometry and trajectory plots (input
block 11), this major radius offset ROA of poloidal cross sections has to be
taken into account when defining plot- frames.</p> <p>(Defaults: NLTRA =
FALSE, ZIA = 0 , ZAA = 1)</p>""",

'ROA' : """<p>The 3rd grid ZSURF is defined in the same way as the x grid,
using the parameters ZIA, ZGA,.... (cm) instead of RIA, RGA,....</p> <p>In
case of NLTRZ = TRUE , a z-grid is defined. ROA is irrelevant.</p> <p>In case
of NLTRA = TRUE , ZIA and ZAA are toroidal angles (in degrees). A grid of
toroidal angles is defined.  For example use ZIA=0.0 and ZAA=360.0 for a full
torus. In case NLTOR this grid also defines the toroidal resolution.  If
.NOT.NLTOR, then periodicity at the endpoints ZIA and ZAA is automatically
enforced.</p> <p>ROA is the radial shift of the poloidal cross section defined
by the x-y grids.  E.g.:  if the x-y- grids are given with magnetic axis as
origin, then ROA is the major radius. If the x-y- grids are already given with
respect to the torus axis at their origin, then ROA =0 (or better
e.g.:1.0E-4=ROA &#x226A 1)</p> <p>Note: ROA affects evaluation of cell
volumes.</p> <p>Note also: in case of geometry and trajectory plots (input
block 11), this major radius offset ROA of poloidal cross sections has to be
taken into account when defining plot- frames.</p> <p>(Defaults: NLTRA =
FALSE, ZIA = 0 , ZAA = 1)</p>""",

'NLMLT' : """<p>the complete "Standard Mesh" data are copied NBMLT
times</p>""",

'NBMLT' : """<p>Number of identical copies of the standard mesh. Transition
from one such mesh (called "block" in EIRENE) into another one has to be
defined by transparent additional surfaces (see block 3B)</p>""",

'VOLCOR' : """<p>The volumes of all cells of the standard mesh as computed by
EIRENE (in sub- routine. VOLUME) are multiplied by one common factor VOLCOR
for each "block".</p>""",

'NLADD' : """<p>There are cells in the computational volume, which are defined
through "additional surfaces" as cell boundaries.  E.g.  a standard mesh (if
there is one) is augmented by "additional cells" in this case.  If NLADD =
FALSE , the complete block 2D may be omitted and the defaults are
used.</p>""",

'NRADD' : """<p>Number of additional zones. The cell indexing along test
flights in these zones has to be specified explicitly by making use of the
ILSWCH, ILCELL parameters (block 3B)</p> <p>(Default: NRADD = 0 ).</p>""",

'VOLADD' : """<p>Volume (<em>cm<sup>-3</sup></em>) of each additional zone as
seen by the test-particles.</p>""",

#2.3 Block 3

'*** 3a. Data for non default standard surfaces' : """Grid surfaces may be
assigned special properties (e.g.: reflecting, absorbing, periodicity, modified
cell index switching, etc...). Their definition is described in subsection
2.3.1. In addition to these grid surfaces also additional surfaces can be seen
by the histories (vacuum boundaries, special surfaces for scoring fluxes,
diagnostic surfaces, ....). Such surfaces can be general linear or second order
surfaces in 3D space. Their definition and properties are described in
subsection 2.3.2.""",

'ILPLG' : """<p>EIRENE can write out information for a finite element mesh
generator to produce a grid of triangles for a multiply connected 2D domain
with cracks and holes. The various (inner and outer) boundaries are given as
polygonal lines, which are composed of selected standard grid surface segments
(NLPLG option) and/or additional surfaces (2 &le; RLBND < 3 option).</p>
<p>This flag identifies closed polygonal lines composed of additional surfaces
given by the 2-point option and/or of standard surfaces in the x-y-plane. For
example if ILPLG(I)=NN, for surfaces I = I1, I2, ...IN, (NN a positive integer)
then these IN surfaces form a closed polygonal line in the x-y-plane. The
region inside this closed line is part of the com- putational domain. By a
negative integer value of NN a closed polygonal region can be excluded from the
computational domain, i.e., a hole in the domain is specified by these
surfaces. EIRENE writes an output file appropriate for a finite element mesh
gen- erator (available from FZ-Juelich) to produce a triangular discretization
of the resulting (possibly multiply connected) domain. This option can be used
to discretize arbitrarily complex 2D domains with internal and external
boundaries given by the additional or non-default standard surfaces.</p>""",

'ILCELL' : """Parameter ILBLCK and ILACLL for the ILSWCH flags described above.
Let ILCELL = NM, with N and M being integers with 3 digits each. Then N =
ILBLCK and M = ILACLL.""",

'ILBOX' : no_description_in_manual,

'NSTSI' : """<p>Total number of non-default standard surfaces that do not act
as prescribed by the default transparent standard co-ordinate surface
model.</p>""",

'TXTSFL' : """<p>Text to characterize a surface (&ldquo;name of the
surface&rdquo;) on the printout file.</p>""",

'ISTS' : """<p> irrelevant; labelling index</p>""",

'IDIMP' : """<p>flag to identify mesh from which this particular surface is
chosen.</p> <p>= 1 surface from the x- (radial) standard mesh (RSURF) Note that
for the unstructured grid options NLTRI and NLTET (i.e. for the 2D triangular
grid option or for the general 3D grids of tetrahedra) all surfaces are
referred to as 1st grid (x or radial) surfaces, by abuse of language.</p>""",

'INUMP' : """<p>Number of the surface in mesh RSURF, PSURF or TSURF
respectively</p>""",

'IRPTA' : """<p>Only a subregion of the surface acts by the &ldquo;non-default
options&rdquo; specified for this particular surface. This subregion is defined
by these flags.</p> <p>If JMP is a surface from the first mesh, then IRPTA2
&rarr; IRPTE2 and IRPTA3 &rarr; IRPTE3 are the surface index ranges of the 2nd
and 3rd mesh, respectively,for which this surface acts as non-default surface.
IRPTA1 and IRPTE1 are irrelevant.</p> <p>If JMP is a surface from the 2nd mesh,
then IRPTA1 &rarr; IRPTE1 and IRPTA3 &rarr; IRPTE3 are the surface index ranges
of the 1st and 3rd mesh, respectively, for which this surface acts as non-
default surface. IRPTA2 and IRPTE2 are irrelevant.</p> <p>If JMP is a surface
from the 3rd mesh, then IRPTA1 &rarr; IRPTE1 and IRPTA2 &rarr; IRPTE2 are the
surface index ranges of the 1st and 2rd mesh, respectively, for which this
surface acts as non-default surface. IRPTA3 and IRPTE3 are irrelevant.</p>""",

'IRPTE' : """<p>Only a subregion of the surface acts by the &ldquo;non-default
options&rdquo; specified for this particular surface. This subregion is defined
by these flags.</p> <p>If JMP is a surface from the first mesh, then IRPTA2
&rarr; IRPTE2 and IRPTA3 &rarr; IRPTE3 are the surface index ranges of the 2nd
and 3rd mesh, respectively,for which this surface acts as non-default surface.
IRPTA1 and IRPTE1 are irrelevant.</p> <p>If JMP is a surface from the 2nd mesh,
then IRPTA1 &rarr; IRPTE1 and IRPTA3 &rarr; IRPTE3 are the surface index ranges
of the 1st and 3rd mesh, respectively, for which this surface acts as non-
default surface. IRPTA2 and IRPTE2 are irrelevant.</p> <p>If JMP is a surface
from the 3rd mesh, then IRPTA1 &rarr; IRPTE1 and IRPTA2 &rarr; IRPTE2 are the
surface index ranges of the 1st and 2rd mesh, respectively, for which this
surface acts as non-default surface. IRPTA3 and IRPTE3 are irrelevant.</p>""",

# 2.3.2

'*** 3b. Data for additional surfaces' : """Internally each additional surface
is defined by an algebraic equation and some algebraic inequalities specifying
the boundary of that surface""",

'CH-card' : """<p><b>CH0 n1/m1 n2/m2 ... </b> surfaces from the range n1 to m1,
n2 to m2, ..., are ignored by EIRENE. Specifying a surface in such a CH0-card
is identical to taking it out from the input file. It may be more convenient in
some cases, however, to use the CH0 option, because the labelling index of the
remaining valid surfaces is not altered then. No input is read for these
surfaces, and the input segment for the next valid surface (identified by the
string &rsquo;*text&rsquo;) is read next.</p> <p><b>CH1(ILIMI) n1/m1 n2/m2 ...
</b> surfaces from the range n1 to m1, n2 to m2, ..., are considered invisible
for a particle located on this current surface ILIMI. Intersection of
trajectories starting from surface ILIMI with those &ldquo;invisible&rdquo;
surfaces is not checked.</p> <p><b>CH2(ILIMI) n1/m1 n2/m2 ... </b> Only for
second order surfaces ILIMI, n1-m1, ... The first of the two possible
intersections is ignored for particles located on surface no. ILIMI.</p>""",

'NLIMI' : """<p>Number of surfaces in the input block</p>""",

'TXTSUR' : """<p> Text to identify a surface (&ldquo;name of the
surface&rdquo;) <on the printout file/p>""",

'RLBND' : """flag for different options to define the boundary of the
surface</p>
<dl>
<dt>RLBND = 0</dt>
<dd>No boundary inequalities specified, i.e. the whole surface is seen by the
test particles.</dd>
<dt>0< RLBND < 2</dt>
<dd>= 1 Only that part of the surface, which lies inside the right
parallelepiped defined by the two vectors (XLIMS1, YLIMS1, ZLIMS1) and
(XLIMS2, YLIMS2, ZLIMS2), is seen by the particles. I.e. the three
inequalities</dd><br>
<dd>= 1.5   Complement to RLBND = 1.
Only the surface element outside the parallelepiped is seen by the particles.
</dd>
<dt>RLBND &ge; 2</dt>
<dd>In this case the surface will be defined by the input of the coordinates of
at least 2 and at highest 5 points on a plane surface. If there are only 2
points, the surface is parallel to one axis.&nbsp;&nbsp; If there are 3 or
more points,&nbsp; then the boundary of this plane surface is a closed
polygon (<em>P<sub>1</sub></em><em>, ..., P <sub>n</sub></em><em>,
P<sub>1</sub></em>). Therefore, the correct order of points at input is
relevant.&nbsp; The orientation of the positive surface normal vector is
defined by the first&nbsp; 3 points, and it is given by the vector product
(<em>P3 </em>- <em>P1 </em>)x(<em>P3</em>- <em>P2 </em>). Thus, the&nbsp;
orientation can be reversed e.g. by interchanging <em>P<sub>2</sub></em>&nbsp;
and <em>P<sub>3</sub></em>.</dd><br>
<dd>2.1 plane surface parallel to z axis. The surface equation of this plane
eads ax+by+c=0 with the coefficients a,b and c such that the points
<em>P<sub>1</sub></em><em>, P<sub>2</sub></em> lie on this surface and the
valid part of that surface ranges from <em>P<sub>1</sub></em> to
<em>P<sub>2</sub></em> in the xy-plane. The z-coordinates of these two points
define the boundaries in z direction</dd><br>
<dd>>= 2.2 Complement to RLBND = 2.1</dd><br>
<dd>>= 2.4 as RLBND=2.1 option, but with z and y exchanged. I.e., now the y
coordinates of the points <em>P<sub>1</sub></em>, <em>P<sub>2</sub></em> are
the boundaries of the surface ax+bz+c=0 in y direction.</dd><br>
<dd>>= 2.5Complement to RLBND = 2.4</dd><br>
<dd>>= 2.7 as RLBND=2.1 option, but with z and x exchanged. I.e., now the x
coordinates of the points <em>P<sub>1</sub></em>, <em>P<sub>2</sub></em> are
the boundaries of the surface ay+bz+c+0 in x direction.</dd><br>
<dd>>= 2.8 Complement to RLBND = 2.7</dd><br>
<dd>>= 3 plane triangle defined by the corners style="text-indent: 25px;",
P<sub>2</sub><em>, P<sub>3</sub></em><p><em>P</em>1=(P1(1),P1(2),P1(3))</p>
<p><em>P</em>2=(P2(1),P2(2),P2(3))</p>
<p><em>P</em>3=(P3(1),P3(2),P3(3))</p></dd><br>
<dd>= 3.5 complement to RLBND = 3; only The plane surface outside the triangle
is seen by the test particles.</dd><br>
<dd>>= 4 plane quadrangle; surface inside the polygon</p>
<p>(<em>P<sub>1</sub></em> , <em>P<sub>2</sub></em> , <em>P<sub>4</sub></em> ,
<em>P<sub>3</sub></em> , <em>P<sub>1</sub></em> ).</p> <p>Here
<em>P<sub>1</sub></em> , <em>P<sub>2</sub></em> ,
<em>P<sub>3</sub></em> are as in the RLBND=3 option, and
<em>P<sub>4</sub></em> = (P4(1), P4(2), P4(3)) Thus this surface is the union
of the triangles with vertices <em>P<sub>1</sub></em> , <em>P<sub>2</sub></em>,
<em>P<sub>3</sub></em> and <em>P<sub>2</sub></em> , <em>P<sub>4</sub></em> ,
<em>P<sub>3</sub></em> respectively.</dd><br>
<dd>= 4.5 complement to RLBND = 4; only the part of the plane surface outside
the quad- rangle is seen by the test particles</dd><br>
<dd>= 5 plane quint-angle; surface inside the polygon (<em>P<sub>1</sub></em> ,
<em>P<sub>2</sub></em> , <em>P<sub>4</sub></em> , <em>P<sub>5</sub></em> ,
<em>P<sub>3</sub></em> , <em>P<sub>1</sub></em>) <em>P<sub>1</sub></em> ,
<em>P<sub>2</sub></em> , <em>P<sub>3</sub></em> , <em>P<sub>4</sub></em>
as RLBND=4, and <em>P<sub>5</sub></em> = (P5(1), P5(2), P5(3))</dd><br>
<dd>= 5.5 complement to RLBND = 5; only the part of the plane surface outside
the quint- angle is seen by the test particles.</dd><br>
<dt>RLBND &lt; 0</dt>
<dd>-KL</dd><br>
<dd>The surface is bounded by L linear inequalities and by K second order
inequalities.</dd><br>
<dd><em>ALIMS </em>+ <em>XLIMS </em>&middot; <em>x </em>+ <em>Y LIMS
</em>&middot; <em>y </em>+ <em>ZLIMS </em>&middot; <em>z </em>&le; 0
(L inequalities)</dd><br>
<dd><em>ALIMS</em>0&nbsp; +&nbsp;&nbsp; <em>XLIMS</em>1 &middot; <em>x
</em>+ <em>Y LIMS</em>1 &middot; <em>y </em>+ <em>ZLIMS</em>1 &middot;
<em>z</em></p> <p>+&nbsp;&nbsp; <em>XLIMS</em>2 &middot; <em>x<sup>2</sup>;
</em>+ <em>YLIMS</em>2 &middot; <em>y<sup>2</sup>; </em>+ <em>ZLIMS</em>2
 &middot; <em>z <sup>2</sup></em></p><p>+ <em>XLIMS</em>3 &middot; <em>xy
 </em>+ <em>YLIMS</em>3 &middot; <em>xz </em>+ <em>ZLIMS</em>3 &middot;
 <em>yz </em>&le; 0(K inequalities)
 </dd><br>
</dl>
""",

# 2.4

'*** 4. Data for species and atomic physics module' : """EIRENE can handle up
to NATM &quot;atomd&quot; species, NMOL &quot;moleculed&quot; species, NION
&quot;test iond&quot; species, NPHOT &quot;photond&quot; species (lines) and
NREAC different atomic, molecular or photonic reactions between these
&quot;test particlesd&quot; and the &quot;bulk ionsd&quot; or electrons. There
may be up to NPLS &quot;bulk iond&quot; species, and one electron gas derived
internally from the assumption of local charge neutrality. Amongst the heavy
background particles (the &quot;bulk ionsd&quot;) may be species with charge
state zero, i.e., neutral particles. By abuse of language, we refer to them as
&quot;bulk ionsd&quot; as well, but we mean in this case: heavy background
particles, i.e. more general objects.""",

'NREACI' : """Total number of different reactions to be read.</p>
<dl> <dd><p>The next block has different meanings for &ldquo;real
particles&rdquo; and &ldquo;photons&rdquo;. Cross section and rate coefficients
are specified for particles, but emission and absorbtion line shapes are
specified for photons.</p>
<b>&ldquo;real particles&rdquo;</b>
<p>An interaction potential em>V /em>(em>r/em>), cross section em>&sigma;
</em>plus a reaction rate coefficient &lang;em>&sigma;v/em>&rang; for one
<process counts as one reaction, but higher order rate coefficients such as
<energy or momentum weighted rate coefficients for the same process count as
<new reaction and must be labelled by a different index em>IR /em>(see
<below)./p>
<p>Storage is provided for up to NREAC different additional reactions (see
<&ldquo;Parameter Statements&rdquo;, section a href="#_bookmark169">3.1/a>),
<i.e., one must guarantee NREACI.LE.NREAC/p></dd></dl>""",

'NATMI' : """Total number of atomic species blocks""",

'NMOLI' : """Total number of molecule species blocks""",

'NIONI' : """Total number of test ion species blocks""",

'NPHOTI' : """Total number of photon species blocks""",

'INDPRO' : """<dl>dd>Flag-array for the type of profile. The last digit
(between 1 and 9) <controls the type of profile. A second digit and/or the sign
control further <options, as described below. A third digit for each entry can
be used to <switch from a cell-wise constant profile (default) to a smooth
(interpolated <into cells) profile. This option is currently being tested for
the magnetic <field input profiles. I.e. INDPRO(5)=103 provides the same
magnetic field as <INDPRO(3)=3, however the magnetic field is evaluated on the
fly (along <particle trajectories) by interpolation, at the very point of
particle <position rather than at the cell center (=const. per cell).
<p>INDPRO is an array of length 12. Each element in this array controls one
<particular input tally, namely:/p>
<p>INDPRO(1) for TEIN</p>
<p>INDPRO(2)</p>
<dl>dd>for TIIN By the default (em>0 &lt; INDPRO(2) &lt; 10/em>): one common
<em>T/em>em>sub>i /sub>/em>profile for all &ldquo;bulk ion&rdquo; species is
<set. I.e., read only one profile card. p>b>New options since 2001:/b>/p>
<p>Values of INDPRO(2) larger than 10: use only the last digit, and one
<em>T/em>em>sub>i /sub>/em>profile card must be read for each bulk ion species
<IPLS. For example: em>INDPRO(2)=15 /em>or em>=25/em>, means: one separate ion
<temperature must be specified for each bulk ion species, and the profile type
<is 5. (em>INDPRO(2)=-5 /em>would do the same.)/p> /dd> /dl></dd></dl>
<dl><dd><p>INDPRO(3) read NPLSI cards, for DIIN , IPLS = 1, NPLSI</p>
<p>INDPRO(4) read NPLSI cards, for VXIN, VYIN, VZIN , IPLS = 1, NPLSI</p>
<dl>dd>b>New options since 2001:/b> p>By the default (em>0 &lt; INDPRO(4) &lt;
<10/em>): one separate flow field for each bulk species is set, velocity is
<given in cm/sec./p> p>Negative value of INDPRO(4) means: Mach number units
<instead. The sound speed em>cs /em>is taken to be the isothermal ion acoustic
<speed of species IPLS. em>ABS(INDPRO(4) /em>is then used as flag for the
<choice of profile type./p> p>Values of INDPRO(4) larger than 10: use only the
<last digit, and only one com- mon flow field is set for all bulk ion species.
<Note the difference to the em>T/em>em>sub>i/sub> /em>options: there the
<meaning of INDPRO larger than 10 was exactly opposite to the meaning here for
<the flow fields (due to historical reasons and for backward compatibility of
<input files. EIRENE had originally by default one single common ion temper-
<ature, but one flow field for each bulk ion species)./p> /dd>/dl>
<p>INDPRO(5)</p>
<dl>dd>for PITCH (later, in initialization phase, converted into cartesian unit
<B- field vector BXIN,BYIN,BZIN) Pitch is defined as em>B/em>em>sub>y/sub>
</em>em>/B/em>em>sub>tot/sub> /em>(LEVGEO=1), em>B/em>em>sub>&theta;/sub>
</em>em>/B/em>em>sub>tot/sub>/em>(LEVGEO=2), or as
<em>B/em>em>sub>pol/sub>/em>em>/B/em>em>sub>tot/sub> /em> (LEVGEO=3), where
<em>B/em>em>sub>pol/sub>/em> is the direction along the polygons./dd> dd>b>New
<options since 2001: /b>In case INDPRO(5)=3 (flat profile) the two redundant
<input parameters B2, B3 are used to define a constant B-field strength [T],
<see below under profile type INDPRO=3./dd>/dl> /dd>
<dd><p>INDPRO(6) for ADIN</p></dd>
<dd><p>INDPRO(7) for WGHT (to be written)</p></dd>
<dd><p>INDPRO(12) for VOL.</p></dd>
<dd>p>For the input tally profiles no. 6 and 7 (ADIN, WGHT) only the options
<INDPRO=5 or INDPRO=6 exist./p> p>For the profile no. 12 (cell volumes) the
<options INDPRO(12) = 4, 5, 6, or INDPRO(12)/p> p>= 7 are active options. For
<all other values of INDPRO for these latter four profiles the default profiles
<described above (&ldquo;General remarks&rdquo;) are set./p> p>For each profile
<up to 6 parameters P0 , . . . , P5 are read, e.g. TE0, ..., TE5 forthe/p>
<p>em>T/em>em>e/em>-profile, TI0, ... , TI5 for the
<em>T/em>em>sub>i/sub>/em>-profile, and so on./p> p>Depending upon the value of
<INDPRO one of the profile routines PROFN, PROFE, PROFS, . . . etc. is called
<from subroutine PLASMA./p> p>INDPRO = 1-4/p> dl> dd>""",

# 2.5

'*** 5. Data for plasma background' : """The background medium (mostly plasma)
consists of NPLS (sometimes in the code: NPLSI) different so called &quot;bulk
particle&quot; species, also referred to as &quot;bulk ions&quot;, by abuse of
language. For each of these species arrays of the parameters: particle density,
temperature, flow velocity (3 cartesian components), are defined, one value per
parameter and per grid cell. There are, in total, NSBOX cells in a run.""",

'NLTRIM' : """<dl><dd>TRIM database is used, if &ldquo;Database Reflection
Model&rdquo; is specified in at least one block for local reflection data. Data
are read from data-set FT21 (no &ldquo;Path Card&rdquo; specified, old option),
or from the domain specified by the &ldquo;Path Card&rdquo; (new option, see
next card). If the old option is used, then the complete TRIM file is read,
containing the first 12 TRIM target-projectile combination data-sets listed in
section 1.4, i.e., the files H_on_Fe to_Ton_W.</dd> <dd>If the parameter NHD6
<em>&lt; </em>12, (section 3.1>) then only the first NHD6 files are read from
FT21.</dd> </dl>""",

'PATH CARD' : """<dl><dd>This card is machine specific. If EIRENE finds a card
containing the string &rsquo;PATH&rsquo; or &rsquo;path&rsquo;, it assumes that
this card specifies the path to the domain containing the TRIM surface
reflection data files.</dd> </dl>""",

'A_on_B' : """<dl> <dd>Name of a particular TRIM data file in the domain
specified by the path card. E.g., H_on_Fe would include the data file for
hydrogen onto iron into the EIRENE run. Up to NHD6 such &ldquo;Target-
Projectile Specification Cards&rdquo; may be included. For a complete list of
such files currently available see again section 1.4.</dd> </dl>""",

'DATD' : """<dl> <dd> distribution for sampling the species index of reflected
or otherwise emitted atoms. <dd>The NATMI relative   <dd>frequencies DATD(IATM)
IATM = 1,NATMI</dd>
<dd>are used to produce the corresponding cumulative distribution DATM in order
to facil- itate sampling (inversion method). Normalization of DATD such
that</dd>
<dd><em>&sum;<sub>IATM</sub> </em><em>DATD</em>(<em>IATM</em> ) = 1</dd> <dd>is
carried out internally.</dd>""",

'DMLD' :  """as for DATD, but for molecules. Cumulative distribution is
DMOL.""",

'DIOD' : """as for DATD, but for test ions. Cumulative distribution is DION.
""",

'DPLD' : """as for DATD, but for bulk ions. Cumulative distribution is
DPLS.""",

'RLARE' : """<p>Area (in <em>cm<sup>2</sup></em>) of the surface element which
is seen by the test particles. (Default: 666.0) (needed only for scaling of non
default surface averaged tallies) If RLARE is not specified here, (i.e., if a
value less than or equal to zero is read) then EIRENE tries to evaluate this
area itself. For some surfaces this is still not possible
automatically.</p>""",

'RLWMN' : """<p>lower weight limit for space weight window for particles
crossing the surface in positive direction. (not in use)</p>""",

'RLWMX' : """<p> upper weight limit for space weight window for particles
<crossing the surface in positive direction. (not in use)/p>""",

'ILIIN' : """<p>defines the type of surface</p>
<dl>
  <dt>&gt; 0 non-transparent surface</dt>
<dl>
<dt>= 1 reflecting, partly or purely absorbing surface. local reflection model
has to be specified unless default model is to be used; all surface tallies
are updated and a switch can be operated.</dt><p></p>
<dt>= 2 purely absorbing surface ;. surface tallies for incident fluxes are
updated and the particle history is stopped then.</dt><p></p>
<dt>= 3 mirror for incident test particles. I.e., specular reflection for
neutral test particles, and for charged test particles the sign of the velocity
 component parallel to the B-field is reversed.</t><p></p>
<dt>=m4 periodicity surface, with regard to x, y, or z coordinate, depending
upon whether this surface is a standard x, y, or z grid surface, respectively.
Move particle to x / radial grid surface no. m, m integer (or to y / poloidal
 or to z / toroidal surface no. m, respectively) and continue track from there
  with otherwise identical particle parameters. <br />This option is currently
   implemented only for Cartesian grids (NLSLB and NLTRZ) and for non-default
    standard grid surfaces only.</dt><p></p>
<dt>The periodicity options are not fully implemented yet. Please contact the
 author for the current status of your particular version.</dt><p></p>
</dl>
  <dt>&le; 0 transparent surface (for example: hole in one of the other
 "additional surfaces"). Particle and energy fluxes onto and from these
 surfaces do not contribute to global balances.</dt><dd>IBM</dd>
<dl>
<dt>= 0 Particle history is not interrupted
No surface tallies are updated, no switches can be operated. Fastest option.
</dt><p></p>
<dt>= -1 Particle history will be stopped and restarted. A switch can be
operated. I.e., this surface is used only for switching (see below: ILSWCH)
or reinitializing the particle's track at the point of intersection.
No surface tallies are updated.</dt><p></p>
<dt>>= -2 as -1, and, additionally:<p> if a particle is crossing the surface in
the positive direction, (one sided-) sur- face tallies are updated, e.g., by
default: partial particle and energy currents <em>J<sup>+</sup></em> (Amp) and
<em>K<sup>+</sup></em> (Watt). These are stored in the POT... and EOT...
tallies of Table. If the paed in the PRF... and ERF... tallies of Table 5.3
.article crosses the surface in the direction opposite to the surface normal,
then negative partial particle and energy currents <em>J<sup>-</sup></em>;
(Amp) and <em>K<sup>-</sup></em>; (Watt) are updated. These are stored in the
PRF... and ERF... tallies of Table.<p></dt><p></p>
<dt>= -3 Net currents (e.g. J+ -J-), are evaluated, and stored on the POT...
and EOT... tallies (see Table 5.3 ). The PRF... and ERF... tallies are empty
for these surfaces.</dt><p></p>
<dt> -4 Not in use. Currently: same as ILIIN=-2 option.</dt><p></p>
</dl>
</dl>""",

'ILSIDE' : """<dl>
<dt>=  0 both sides of the surface act as described by ILIIN option (default).
</dt>
<dt>=  1 particles incident on the surface in the negative direction will be
absorbed (i.e., ILIIN = 2 option from that side).</dt>
<dt>=  2 particles incident on the surface in the negative direction will be
killed and the message</dt>
<dd>"ERROR IN ADDCOL"<br> or <br> "ERROR IN STDCOL" <br> will be printed. The
contribution of these particles to the particle- and energy flux balances will
be called PTRASH and ETRASH respectively. This option should be used for
geometry testing whenever the user expects particles incident only from one
side.</dd>
<dt>=  3 particles incident on the surface in the negative direction will
not see the surface, i.e., this surface acts like a (semi) transparent surface
(ILIIN = 0 option) from that side.</dt>
<dt>= -1 as 1, but with the opposite direction of the surface normal</dt>
<dt>= -2 as 2, but with the opposite direction of the surface normal</dt>
<dt>= -3 as 3, but with the opposite direction of the surface normal</dt>
</dl>""",

'ILSWCH' : """= IJKLMN, i.e. six digits I, J, K, L, M and N
<dl>
<dt>= 0 no switch is operated</dt>
<dt>N EIRENE flag ITIME</dt><dd><p>N = 1   The calculation of the step sizes in
 the standard mesh is abandoned for a
particle which crosses the surface in the positive direction, and is
reactivated,
if the particle strikes in the negative direction</p><p>
N = 2   as 1, but with the direction of the surface normal reversed for this
option.</p></dd>
<dt>M EIRENE flag IFPATH</dt><dd><p>M = 1   Abandon the calculation of the
collision rates (entry into the vacuum) for
a particle which is striking the surface in the direction of the surface
normal.
For particles incident from the other direction, evaluation of collision rates
is
reactivated.</p><p>M = 2 as 1, but with the direction of the surface normal
 reversed.</p></dd>
<dt>L EIRENE flag IUPDTE</dt><dd><p>L = 1   Abandon the updating of
volume-averaged tallies for a particle which is
striking the surface in the direction of the surface normal. For particles
incident from the other direction, updating of volume averaged tallies is
reactivated.</p><p>L = 2 as 1, but with the direction of the surface normal
reversed for this option.</p></dd>
<dt>I,J,K flags for switching cell numbers at transition into a different mesh
cell.</dt>
<dt>K for particles in an additional cell, i.e., not in one of the "standard
mesh" blocks:</dt><dd><p>K = 1   Increase the actual additional cell number
NACELL for a particle striking the surface in the direction of the surface
normal by ILACLL. Decrease NACELL by ILACLL if the particle is striking in the
negative direction. Specification of ILACLL is via the input variable ILCELL,
see below.</p><p>
K = 2   as K = 1,  but with the direction of the surface normal reversed for
this
option.</p><p>for particles inside the "standard mesh ", i.e., not in the
"additional cell region"</p><p>K = 1   Increase the standard mesh block number
 NBLOCK for a particle strik-
ing the surface in the direction of the surface normal by ILBLCK. Decrease
NBLOCK  by  ILBLCK  if  the  particle  is  striking  in  the  negative
direction.
Specification of ILBLCK is via the input variable ILCELL, see below.</p><p>K
 = 2 as K = 1, but with the direction of the surface normal reversed.</p></dd>
<dt>J for particles at the boundary between "additional" and "standard" mesh
 regions.</dt><br><dd> = 1   entrance into standard mesh, block no.
NBLOCK = ILBLCK or exit from standard mesh into additional cell NACELL =
ILACLL.
Specification of ILACLL and ILBLCK is via the input variable ILCELL, see
below.  If ILACLL = 0, then no switch to additional cell is operated.  (E.g.:
for surfaces which are reflecting from this side).</dd><br><dd>J = 2 as J = 1.
The direction of the surface normal does not matter here.</dd><br>
<dt>I similar to J-flag, i.e., for transitions between standard and additional
meshes, but
different cell number switching.</dt><br><dd>I = 1   Entrance into standard
mesh, block no. NBLOCK = NACELL+ILBLCK, if the particle is striking in the
positive direction, or
NBLOCK = NACELL-ILBLCK,
if the particle is striking in the negative direction.  Exit from standard mesh
into additional cell
NACELL = NBLOCK+ILACLL,
for a particle striking the surface in the positive direction, or
NACELL = NBLOCK-ILACLL,
if the particle is striking in the negative direction.
Specification of ILACLL and ILBLCK is via the input variable ILCELL, see
below.</dd><br><dd>I = 2 as I = 1, but with the direction of the surface
normal reversed.</dd>
<dd>If a test particle history starts from a surface (NLSRF option), then
ILSWCH acts as if
this particle had struck the surface prior to the birth process in the
positive direction.
This default setting is only available for ILSIDE 6=0 and can (must) be
overruled by
the SORIFL flag , e.g.  if a surface source needs to be defined on a
surface with ILSIDE = 0.</dd>
</dl>""",

'ILEQUI' : """<p>The algebraic equations for the surfaces J and
IABS(ILEQUI(J)) will be described by exactly the same coefficients (up to a
common sign, if ILEQUI(J) .lt. 0). For example a triangle can be specified by
the three corners and another part of the same plane surface can be specified
directly by its algebraic coefficients. To avoid round-off errors one should
use the ILEQUI option in such cases, in particular if surface J is a
transparent &ldquo;hole&rdquo; in surface ILEQUI(J), or vice versa.</p>""",

'ILTOR' : """For NLTRA option only (see block 2c): <p>if ILTOR<em>&gt;</em>0
:</p> <p>the surface is defined with respect to the local coordinate system of
the toroidal segment with &ldquo;cell-number&rdquo; ILTOR, hence: 1 &le;ILTOR
&le;NTTRAM.</p> <p>if ILTOR=0 :</p> <p>the surface is defined with respect to
any local coordinate system. I.e., the surface equations are taken to be the
same in each local system.</p> <p>If the surface equations are z-independent,
then this surface is toroidally symmetric (within the NLTRA-approximation).</p>
<p>Otherwise the surface has NTTRAM-fold periodicity.</p> <p>This flag is
irrelevant for NLTRZ (i.e., if cylindrical coordinates are used) or for NL-
TRT.</p> <p>Default: ILTOR = 0</p>""",

'ILCOL' : """<p>Flag for the color that is used for plotting this surface on 2d
or 3d geometry plots. If ILCOL &le; 0 than -ILCOL is used and the surface area
is filled in by that color on the 3d geometry plots.</p><p>Default:
ILCOL=1</p>""",

'ILFIT' : """<p>This option is relevant only for surfaces with one ignorable
coordinate, i.e. it only works for the 2<em>. </em>&le; <em>RLBND </em>&le; 3.
surface boundary options.</p> <p>It is a tool to facilitate a neat fitting of
surfaces, in particular for connecting curved and plane surfaces (i.e. to avoid
particle leakage due to numerical round-off errors in the algebraic surface
coefficients.</p> <p>M and N (3 digits each, M may be omitted if not needed)
are the numbers of the surfaces (which must have the same ignorable coordinate)
the boundaries of which should match to those of the actual surface J. The
boundaries of these neighboring surfaces M and N must be specified by the RLBND
= 1 or RLBND = 1.5 option.</p> <p>The fitting is achieved by a small automatic
internal modification of the surface data P1 and/or P2 of surface number J in
subroutine SETFIT. Printout of the modifications made there is activated with
the TRCSUR flag (input block 11).</p> <p><b>ILCELL </b> Parameter ILBLCK and
ILACLL for the ILSWCH flags described above. Let ILCELL = NM, with N and M
being integers with 3 digits each. Then N = ILBLCK and M = ILACLL.</p>
<p><b>ILBOX </b> to be written</p> <p><b>ILPLG </b> EIRENE can write out
information for a finite element mesh generator to produce a grid of triangles
for a multiply connected 2D domain with cracks and holes. The various (inner
and outer) boundaries are given as polygonal lines, which are composed of
selected standard grid surface segments (NLPLG option) and/or additional
surfaces <br>(2 &le; RLBND <em>&lt; </em>3 option). <br>This flag identifies
closed polygonal lines composed of additional surfaces given by the 2-point
option and/or of standard surfaces in the x-y-plane. For example if
ILPLG(I)=NN, for surfaces I = I1, I2, ...IN, (NN a positive integer) then these
IN surfaces form a closed polygonal line in the x-y-plane. The region inside
this closed line is part of the com- putational domain. By a negative integer
value of NN a closed polygonal region can be excluded from the computational
domain, i.e., a hole in the domain is specified by these surfaces. EIRENE
writes an output file appropriate for a finite element mesh gen- erator
(available from FZ-Juelich) to produce a triangular discretization of the
resulting (possibly multiply connected) domain. This option can be used to
discretize arbitrarily complex 2D domains with internal and external boundaries
given by the additional or non-default standard surfaces. <br>These finite
element grids can be combined with the regular grids by using the problem
specific geometry routines (see section 3) or the code interfacing routines
INFCOP (see section 4).</p>""",

'RINTEG' : """<dl>
<dt>>0</dt>
<dd> Fixed (independent of energy and angle ofincidence) particle
reflection co- efficient. <br>The fast particle reflection probabilities
RPROBF are set to <em>p<sub>f</sub>= MIN(1 - p<sub>a</sub>,RINTEG)</em>,
regardless of the reflection model selected by the flag ILREF in block 6B.
<em>p<sub>a</sub></em> is kept as specified, and <em>p<sub>t</sub></em> is
then recomputed as <em>p<sub>t</sub> = 1 - p<sub>f</sub> - p<sub>a</sub></em>.
<em>RINTEG &ge; 1 - p<sub>a</sub></em> enforces the fast particle reflection
model for all un-pumped incident particles, i.e., RINTEG is internally reset
<em>to 1 - p<sub>a</sub></em>.</dd><br>
<dt>=0</dt>
<dd>Default: fast particle
reflection probability as defined by the reflection model chosen.
</dd><br>
<dt><0</dt>
<dd>The fast particle reflection probabilities <em>RPROBF</em> are
set to 1.0, i.e., even pump- ing is turned off (as distinct from the choice
<em>RINTEG=1.0</em>, which would preserve the pumping speed at a surface).
</dd>""",

'RPROBO' : """""",

'EINTEG' : """<dl>
<dt>>0</dt>
<dd> Fixed (independent of energy and angle of incidence) energy reflection
coefficient.
<br>particle reflection model by an reflection assumption: <em>E<sub>out</sub>
= E<sub>in</sub> &middot. EINTEG.</em>
</dd><br>
<dt>=0</dt>
<dd>Default: no modification of energy distribution in the reflection model for
 fast particle reflection.
</dd><br>
<dt><0</dt>
<dd>elastic <em>(E<sub>out</sub> = E<sub>in</sub>)</em> reflection for all
particles reflected according to the fast particle reflection model. Hence:
same as <em>EINTEG=1.0.</em>
</dd>
</dl>""",

'AINTEG' : """<dl>
<dt>>0</dt>
<dd> (not ready to use) <br>
Fixed (independent of energy and angle of incidence) momentum reflection
coefficient.<br>
This choice replaces the angle random sampling procedure in the fast particle
reflection model by a momentum reflection assumption such that, on average:
<em>v&#772;<sub>out</sub> = v<sub>in</sub> &middot; AINTEG</em>.
</dd><br>
<dt>=0</dt>
<dd>Default: no modification of angular distributions in reflection model for
fast particle reflection.
</dd><br>
<dt><0</dt>
<dd>specular reflection for all particles reflected according to the fast
particle reflection model.</em>
</dd>
</dl>
""",

'NPLSI' : """ Number for how many species card to read.""",

'VL' : no_description_in_manual,

'P1' : point_example,
'P2' : point_example,
'P3' : point_example,
'P4' : point_example,
'P5' : point_example,

# 2.6

'*** 6a. General data for reflection model' : """An outline of surface
interaction models in general terms was given in section 1.4. As for the
implementation of such models in EIRENE, there are two parts to the surface
interaction data block. The first part contains data which are general to the
EIRENE reflection model (&quot;Block for General Reflection Data&quot;), at all
surfaces. The second part may be different for each individual surface element
(label: MSURF ) and thus must be specified for each reflecting &quot;non-
default&quot; surface of the &quot;standard mesh&quot; and for each reflecting
&quot;additional surface&quot;.""",

'ERMIN' : """For incident particle energies below ERMIN, the
<quote>fast</quote> particle reflection model is switched off. Only the
<quote>thermal</quote> particle model is used.""",

'ERCUT' : """<p>These variables may be used to modify the default
<quote>Behrisch Matrix</quote> reflection coefficients for particles incident
on a surface at low energies E<sub>in</sub> . The original data [16] are used
only for E<sub>in</sub> > ERCUT and for normal incidence &theta;<sub>in</sub> =
0.</p>
<p>In the range ERMIN < E<sub>in</sub> < ERCUT the particle reflection
coefficient p<sub>f</sub>(E<sub>in</sub> , &theta;<sub>in</sub> = 0) is
replaced by a smooth cubic interpolation curve p<sub>f</sub>(E<sub>in</sub>)
such that p<sub>f</sub>(0) = RPROBF .</p>
<p>The original <quote>Behrisch Matrix</quote> is recovered by setting ERCUT
&le; <0./p>""",

'RPROB0' : """<p>These variables may be used to modify the default
<quote>Behrisch Matrix</quote> reflection coefficients for particles incident
on a surface at low energies E<sub>in</sub> . The original data [16] are used
only for E<sub>in</sub> > ERCUT and for normal incidence &theta;<sub>in</sub> =
0.</p>
<p>In the range ERMIN < E<sub>in</sub> < ERCUT the particle reflection
coefficient p<sub>f</sub>(E<sub>in</sub> , &theta;<sub>in</sub> = 0) is
replaced by a smooth cubic interpolation curve p<sub>f</sub>(E<sub>in</sub>)
such that p<sub>f</sub>(0) = RPROBF .</p>
<p>The original <quote>Behrisch Matrix</quote> is recovered by setting ERCUT
&le; <0./p>""",

'ILREF' : """Flag for choice of local reflection model
<dl>
<dt>=1</dt>
<dd>TRIM database reflection model is used. NLTRIM must be .TRUE..</dd>
<dt>=2</dt>
<dd>"modified Behrisch Matrix model" is used</dd>
<dt>=3</dt>
<dd>user supplied reflection model (see section 3.3: Subroutine REFUSR)</dd>
</dl>
Default: ILREF = 2""",

'ILSPT' : """Flag for choice of local sputtering model.<br>
Let ILSPT = MN, with M and N single digit integers each. Then N controls the
options for physical sputtering, and M controls chemical sputtering. See
subroutine SPUTER.
<dl>
<dt>N=0</dt>
<dd>no physical sputtering at this surface</dd>
<dt>N=1</dt>
<dd>constant physical sputtering rate (see parameter RECYCS below)</dd>
<dt>N=2</dt>
<dd>modified Roth-Bogdansky formula for sputter yield, Thompson energy
distribution  and cosine angular distribution for emitted particles.</dd>
<dt>N=9</dt>
<dd>(was option N=3 in Eirene-2004 and older)<br>
user supplied sputtering model (see section 3.3: Entry SPTUSR to subroutine
REFUSR)</dd>
<dt>M=0</dt>
<dd>no chemical sputtering at this surface</dd>
<dt>M=1</dt>
<dd>constant chemical sputtering rate</dd>
<dt>M=2</dt>
<dd>"Roth formula" for chemical sputter yield, thermal distribution for
emitted particles , "weak flux dependence option A6".</dd>
<dt>M=3</dt>
<dd>"Roth formula" for chemical sputter yield, thermal distribution for emitted
 particles , "strong flux dependence option A7".</dd>
<dt>M=4</dt>
<dd>"Roth formula" for chemical sputter yield, thermal distribution for emitted
 particles , "new flux dependence option A8 (2004)".</dd>
<dt>M=5</dt>
<dd>not in use</dd>
<dt>M=6</dt>
<dd>"Haasz-Davis 1998 formula" for chemical sputter yield</dd>
<dt>M=7</dt>
<dd>"Haasz-Davis 1998 formula" for chemical sputter yield, and multiplicative
factor for flux dependence (Roth, 2004).</dd>
<dt>M=9</dt>
<dd>(was option N=3 in Eirene-2004 and older)
user supplied sputtering model (see section 3.3: Entry SPTUSR to subroutine
REFUSR)</dd>
</dl>
Default: ILSPT=0""",

'ISRS' : """sputtered particle species flag (physical sputtering).
<dl>
<dt>>0</dt>
<dd>both the sputtered particle and the reflected particle (if any) will be
followed. Their contribution to surface particle and energy fluxes is stored in
 surface averaged tallies 1 to 24, i.e., sputtered particles are not explicitly
 distinguished from reflected particles in the particle and energy balances.
Furthermore the "sputtered flux surface tallies" 33 to 37 (5.1.2 in older
versions before 2002, and on tallies 51 to 81, (5.1.1) else, are also updated.
The species index of the sputtered particle (atom) is IATM=ISRS. Hence, on
input, one must have 1 &le; ISRS &le; NATMI, otherwise: error exit.</dd>
<dt>&le;0</dt>
<dd>Same as ISRS > 0, however, the species index of the sputtered particle is
determined automatically from comparing the charge and mass numbers of the
available atomic species (input block 4a) with the corresponding surface
material (nuclear mass and charge) data of the surface element. If no suitable
atomic test particle is is found, then only sputter tallies are scored, but no
sputtered particles are then subsequently traced.</dd>
<dt>=0</dt>
<dd>same as ISRS &le; 0, but in this case a sputtered particle is NOT followed,
 even if its atomic test particle species could be identified. Only the
reflected particles are followed. and only their contribution to surface
particle and energy fluxes is stored in regular surface averaged tallies 1 to
24. Sputter tallies are still scored.</dd>
</dl>
Note: ISRS=ISRS(ISPZ,MSURF), so the above described options for sputtered
particle species, as well as for either only scoring fluxes or even tracing
these sputtered particles, can be made dependent on the incident species index
ISPZ.""",

'ISRC' : """sputtered particle species flag (physical sputtering).
<dl>
<dt>>0</dt>
<dd>both the sputtered particle and the reflected particle (if any) will be
followed. Their contribution to surface particle and energy fluxes is stored in
 surface averaged tallies 1 to 24, i.e., sputtered particles are not explicitly
 distinguished from reflected particles in the balances. Furthermore the
"sputtered flux surface tallies" 25 to 28 are updated. The species index of the
 sputtered particle (atom) is IATM=ISRC, if ISRC&le;NATMI, or (molecules) IMOL,
if ISRC = NATMI+IMOL and NATMI < ISRC &le; NATMI+NMOLI. Hence, on input, ISRC
&le; NATMI+NMOLI.</dd>
<dt>&le;0</dt>
<dd>There is no chemical sputtering for the particular surface element and
incident species (note: ISRC=ISRC(ISPZ,MSURF), i.e., p<sub>c</sub> = 0 here.
Only the reflected particles are followed. Their contribution to surface
particle and energy fluxes is stored in surface averaged tallies 1 to 24.</dd>
<dt>=0</dt>
<dd>Same as ISRC > 0, however, the species index of the sputtered particle is
determined automatically from comparing the charge and mass numbers of the
atomic species (input block 4a) with the corresponding data of the surface
element. I.e., in case of Carbon surfaces the sputtered particle is a C-atom,
if such an atom has been specified in input block 4a</dd>
</dl>""",

'ZNML' : """= KLMN (4 digits)
<dl>
<dt>KL</dt>
<dd>atomic weight of wall material. Note: the nearest integer of the mass
number in the TRIM runs is used. For example, a copper target is specified in
the TRIM files with an atomic weight of 63.54, and the corresponding TRIM file
is used for surfaces with KL=64.</dd>
<dt>MN</dt>
<dd>nuclear charge number of wall material</dd>
</dl>
Example: Carbon: ZNML=1206.<br>
Example: Molybdenum: ZNML=9642.<br>
Example: Copper: ZNML=6429.<br>
Default: ZNML = 5.626E3 (stands for Fe).""",

'EWALL' : """<dl>
<dt><0</dt>
<dd>-EWALL = TW is a (surface-) temperature (eV) in a Maxwellian flux
distribution for the thermal particle energy. The resulting mean energy is
E<sub>mean</sub>= 2 &middot; T W .</dd>
<dt>> 0</dt>
<dd>+EWALL = Energy of mono-energetic (thermal) particles.
The relation between surface temperature TW and the mean energy of particles
then reads EWALL = E<sub>mean</sub> = 1.5 &middot; T W .</dd>
<dt>= 0</dt>
<dd>Energy is sampled from a Thompson distribution, using the flag EWBIN (see
below) as parameter for the surface binding energy</dd>
</dl>
Default: EWALL = +0.0388 ( TW &cong; 0.026 eV &cong; 300 K)<br>
Note that the EW ALL > 0 option enables EIRENE to include boundary conditions
in "one speed transport equation" approximations, which often are of great
interest in general linear transport theory.""",

'EWBIN' : """see EWALL = 0 option.<br>Default: EWBIN = 0.0 (irrelevant for
"Default Model")""",

'TRANSP(1,N)' : """Semi-transparency for particles incident from the positive
side. Renders a nontransparent surface (ILIIN > 0) semi-transparent. The
probability for passing through the surface is TRANSP. Hence: the probability
for reflection/re-emission etc. is 1-TRANSP.<br>
Default: 0.0 (i.e., fully reflecting surface).<br>
Irrelevant for transparent surfaces.""",

'TRANSP(2,N)' : """Semi-transparency for particles incident from the negative
side on a non-transparent surface.<br>
Default: 0.0 (i.e., fully reflecting surface).<br>
Irrelevant for transparent surfaces.""",

'FSHEAT' : """surface sheath potential factor. The sheath potential is
<em>FSHEAT &middot; T<sub>e</sub></em> with T<sub>e</sub> the electron
temperature at the point of incidence. This sheath potential is applied if
ions (test ions or bulk ions) hit a non-transparent surface.<br>
If FSHEAT &le; 0.0, then a sheath potential computed from the local background
plasma flow conditions is used (function SHEATH), assuming ambi-polar flow, a
Boltzmann distribution for electrons and zero secondary electron emission.
See section 1.5. In case of zero (undefined) background plasma flow velocity at
 the place of incidence, a default of FSHEAT = 2.8 is used (corresponding to
T<sub>e</sub> = T<sub>i</sub>, and a single ion species D<sup>+</sup> plasma
flowing at ion acoustic speed parallel to the B-field into the sheath.<br>
Default: FSHEAT=0.0""",

'RECYCF' : """<p>Multiplier for reflection probability RPROBF:</p>
<p<>Particles can be re-emitted from surfaces by either the "fast reflection"
model or by a "thermal emission" model. Flag RECYCF controls (scales) the "fast
 particle reflection" probability p<sub>f</sub> .</p>
<p>The probability <em>p<sub>f</sub> = RPROBF (E<sub>in</sub> ,
&theta;<sub>in</sub> , ispez, wall)</em> for the "fast" particle reflection
model, as specified by other flags for this surface, is modified to<br>
<em>RPROBF (E<sub>in</sub> , &theta;<sub>in</sub> , ispez, wall) = AMIN
(RECYCF &middot; RPROBF, RECYCT )</em>,<br>
where RPROBF was evaluated from the reflection model specified by ILREF.
Note the cut-off at recycling coefficient RECYCT (defined below).</p>
<p>The total recycling coefficient RECYCT = p<sub>f</sub> + p<sub>t</sub> is
unchanged by flag RECYCF.</p>
<p>Hence, by the use of RECYCF not only the fast particle reflection
probability, but also the probability for thermal particle emission
p<sub>t</sub> is altered to maintain a total recycling coefficient at this
surface of RECYCT.</p>
Default: RECYCF = 1 for incident atoms, test ions and bulk ions.<br>
Default: RECYCF = RPROBF = 0 for incident molecules.""",

'RECYCT' : """Recycling coefficient (must not be negative):<br>
<p>A flux RECYCT &middot; Influx is re-emitted from a surface, for any Influx
of particles of any species, where all fluxes are measured as "atomic fluxes"
(=fluxes of nuclei). RECYCT hence defines the sticking probability p a [and
hence also the pumping speed (6.7)] of any surface in EIRENE, for all incident
species.</p>
<p>The fraction p<sub>a</sub> = (1 - RECYCT) of incident (atomic) flux will be
absorbed at the surface. The non-sticking, i.e. the re-emitted fraction
RECYCT = 1 - p<sub>a</sub> is split into a "fast" and a "thermal" component.
</p>
<p>A fraction p<sub>f</sub>= RPROBF [see (6.6)] of the incident particles is
reflected as described by the "fast particle reflection model". However, by
relation (6.6) it is ensured that RPROBF is always less than or equal to
RECYCT.</p>
<p>The fraction p<sub>t</sub> = RPROBT = (RECYCT - RPROBF) will be re-emitted
by the "thermal particle reflection model". This flag is to be used to define
an effective pumping speed at certain surfaces, see paragraph 2.6.1 below.</p>
Note: RPROBF = 0 for incident molecules (ITYP=2) by default.<br>
Default: RECYCT = 1. , i.e. p a = 0""",

'RECPRM' : """free model parameter for user supplied recycling models ILREF =
9. Default: RECPRM = 0.""",

'EXPPL' : """(only for ILREF = 2 option)<br>
angular dependence of fast particle reflection coefficient. The formula<br>
<em>R(&Phi;) = 1 - (1 - RPROBF) &middot; cos<sup>EXPPL</sup>(&Phi;)</em><br>
is used, e1 = EXP P L, see equation 4.60, where:<br>
RPROBF Reflection probability from "Behrisch Matrix" model, which is valid only
for normal incidence.
<dl><dt>&Theta;</dt>
<dd>Angle of incidence against surface normal</dd>
<dt>R(&Theta;)</dt>
<dd>Reflection probability for particles incident with angle &Theta;
note: R(&Theta;) = 1 for &Theta; = 90 &middot; and EXPPL > 0.</dd></dl>
Default: EXPPL = 1. (recommended from a comparison with the TRIM database)""",

'EXPEL' : """as EXPPL, but for the energy reflection coefficient.<br>
Default: EXPEL = 0.5 (recommended from a comparison with the TRIM database). e2
= EXPEL, see equations 4.61 and 4.62""",

'EXPIL' : """Index for angular distribution of re-emitted atom or molecule;
affects both models ILREF = 1 and ILREF = 2<br>
<dl><dt>EXPIL=0</dt>
<dd>cosine distribution, independent of choice of fast particle reflection
model</dd>
<dt>EXPIL > 0</dt>
<dd>mixed cosine-specular model.<br>
In case of ILREF=1 the angular distribution given by the database is used.<br>
In case of ILREF=2 the specular contribution increases according to equations
4.63 with angle of incidence &Theta; and with e3 = EXPIL (recommended: EXP IL
&le;1).</dd></dl>
Default: EXPIL = 0.""",

'RECYCS' : """The meaning of this flag for the "physical sputtering" options
depends upon the value of the first digit N of ILSPT:<br>
<dl><dt>N=0</dt>
<dd>no physical sputtering, YIELD1 = 0. RECYCS is irrelevant.</dd>
<dt>N=1</dt>
<dd>constant physical sputtering yield, YIELD1 = RECYCS</dd>
<dt>N=2</dt>
<dd>RECYCS is a multiplier for the sputtered particle flux YIELD1. YIELD1 is
computed from the incident species, energy, angle and surface parameters by the
sputter model N = 2. Hence: the sputtered particle yield YIELD1 as computed
from subroutine SPUTER is modified to
YIELD1 = RECY S &middot; YIELD1.</dd>
<dt>N=9</dt>
<dd>RECYCS is a free model parameter, which can be used in the user supplied
sputter model for any particular surface element.</dd></dl>
Default: RECYCS = 1.""",

'RECYCC' : """The meaning of this flag for the "chemical sputtering" options
depends upon the mvalue of the second digit M of ILSPT:<br>
<dl><dt>M=0</dt>
<dd>no chemical sputtering, YIELD2 = 0. RECYCC is irrelevant.</dd>
<dt>M=1</dt>
<dd>constant chemical sputtering yield, YIELD2 = RECYCC.</dd>
<dt>M=2</dt>
<dd>RECYCC is a multiplier for the sputtered particle flux YIELD2. YIELD2 is
computed from the incident species, energy, angle and surface parameters by the
sputter model M = 2. Hence: the sputtered particle flux YIELD2 as computed
from subroutine SPUTER is modified to YIELD2 = RECYCC &middot; YIELD2.</dd>
<dt>M=9</dt>
<dd>RECYCC is a free model parameter, which can be used in the user supplied
sputter model for any particular surface element.</dd></dl>
Default: RECYCC = 1.""",

'SPTPRM' : """free model parameter for user supplied sputtering models N=3,
M=3.<br> Default: SPTPRM = 0.""",

'ESPUTC' : """(new: March 2015) parameter (flag) for energy of chemically
sputtered particle. By default: chemically sputtered particles are released
from the wall by the "thermal surface emission model", as also used for the
recycling/reflection thermal emission, i.e. with wall temperature
(as specified by EWALL parameter, see above) and either a cosine
(for monoenergetic emission at EWALL = 1.5 TWALL) angular distribution, or
sampling from a stationary Maxwellian flux distribution at -EWALL = TWALL.<br>
If ESPUTC .GT. 0, then the the chemically sputtered particles are released with
 a monoenergetic distribution at E0 = ESPUTC, and a cosine angular
distribution.<br>Default: ESPUTC = 0.""",

'ESPUTS' : """(new: March 2015) parameter (flag) for energy of physically
sputtered particle. Currently not in use. Default: ESPUTS = 0.""",

# 2.7

'*** 7. Data for primary sources, nstrai strata' : """The primary source (and:
initial distribution of test particles, in time dependent mode) is given as a
function Q(i, r, t, v). Q is the density of the probability distribution from
which the species index i, the starting point r, the velocity vector v and the
starting time t are sampled in subroutine LOCATE. (i, r, t, v) is the state of
the starting particle, which then will be &quot;followed&quot; (traced) in
subroutine FOLNEUT or FOLION. There are five primary types of spatiotemporal
distributions for primary sources (&quot;Strata&quot;) , namely Point sources,
Line sources (to be written), Surface sources, Volume sources and &quot;Census
sources&quot;. The first four are uniform in a time-interval (or time-
independent), and the fifth one is an initial distribution (in volume) at a
given point in time.""",

'NSTRAI' : """Number of different sources ("Strata"), which are computed one
after the other and are linearly superimposed at the end of the run.<br>
(NSTRAI &le: NSTRA, see "Parameter-Statements")""",

'INDSRC' : """<p>INDSRC(ISTRA)=0-5 the input data for stratum ISTRA are read
here, but may be modified in some user routine (SAMUSR) or interface routine
(INFCOP, at entry IF2COP(ISTRA))</p>
<p/INDSRC(ISTRA)=6 no input data for stratum ISTRA are read here. The
definition of this stratum must be entirely in some problem specific routine
(IF2COP, etc.). See section 3.4 for one such example, namely the default
surface recycling source model as specified in coupled B2-EIRENE runs.</p><p>
INDSRC(ISTRA)=-1 the input data for stratum ISTRA are read here, and no attempt
is made to modify these. I.e. IF2COP(ISTRA) is not called.</p>""",

'ALLOC' : """Allocation of CPU-time to stratum weighted as
(1-ALLOC)*NPTS+ALLOC*FLUX""",

'AMPTS' : """(available since 2014 in master version) Multiplier, used
simultaneously for permitted total CPU time NTCPU (input block 1), and for
specified number of MC histories NPTS(ISTRA) (see below). Default:
AMPTS=1.0""",

'TXTSOU' : """Text to characterize the stratum (name of the source) on the
printout file.""",

'NLAVRP' : """= .TRUE. not in use""",

'NLAVRT' : """= .TRUE. not in use""",

'NLSYMP' : """= .TRUE.<br>
Symmetrize profiles with respect to poloidal (y-) co-ordinate x<sup>2</sup> ,
i.e., with respect to the poloidal surface x<sup>2</sup> = PSURF((NP2ND+1)/2)
in case NP2ND is an odd integer, or with respect to the cell center
x<sup>2</sup> = PZONE(NP2ND/2) in case NP2ND is an even integer.""",

'NLSYMT' : """same as NLSYMP, but for toroidal (z-) co-ordinate, i.e., for
toroidal surface TSURF((NT3RD+1)/2) or TZONE(NT3RD/2) respectively.""",

'NPTS' : """<dl>
<dt>> 0</dt>
<dd> Maximum number of test particle histories.<br>
If there is more than one stratum (NSTRAI > 1) then the total CPU-time NTIME
(input block 1) will be distributed proportional to NPTS to the single strata.
NPTS is the maximum number of test-particles only if sufficient CPU time is
available. Otherwise a message "NO FURTHER COMPUTATION TIME FOR THIS STRATUM"
is printed and the particle loop for the respective stratum is stopped.</dd>
<dt>= 0</dt><dd>: this stratum is "turned off".</dd>
<dt>< 0</dt><dd>: no limitation in the number of particles. The entire CPU time
assigned to this stratum will be used up. (NPTS is reset to the largest
integer on the machine. Hence: some care is needed here in case of multiple
strata, in combination with the ALLOC-options to assign CPU time to individual
strata).<dd>""",

'NINITL' : """<dl>
<dt>>0</dt>
<dd>seed for initialization of random number generator. The results for all
those individual strata can be reproduced exactly for which the same number of
test-flights is computed as in a previous run.<dd>
<dt>=0</dt>
<dd>no initialization of random numbers for the particular stratum. In case of
the first stratum, the default initialization is used. Runs can only be
reproduced, if the same number of test-flights is computed for each stratum.
Somewhat weakened correlation between subsequent runs as compared to the
NINITL > 0 option.</dd>
<dt><0</dt>
<dd>truly random initialization (determined by machine clock). These runs
cannot be reproduced exactly. Subsequent runs are uncorrelated. (E.g.:
recommended for stochastic approximation procedures in nonlinear
applications.</d>""",

'NEMODS' : """Flag to select one of the preprogrammed source energy conditional
distributions given the source particle's position and species. (See:
"distribution in velocity space")""",

'NAMODS' : """Flag to select one of the preprogrammed conditional source
angular distributions given the position, species and energy of the source
particle. (See: "distribution in velocity space")""",

'NMINPTS' : """Minimum number of test particles enforced for this stratum,
independent of NTCPU flag in input block 1. Hence: setting this flag may
increase EIRENE run time above the cpu-time assigned to a run in the first
input line in input block 1. Default: NMINPTS = 0""",

'NLATM' : """Atomic source. History starts in subroutine FOLNEUT with type
index ITYP=1, species index ISPZ = IATM and initial weight NPRTA(IATM) (see
block 4A)
<p>Out of NLATM, NLMOL, NLION, NLPHOT, NLPLS one and only one of these
five variables must be .TRUE. .</p>""",

'NLMOL' : """Molecule source. History starts in subroutine FOLNEUT with type
index ITYP=2, species index ISPZ = IMOL and initial weight NPRTM(IMOL) (see
block 4B)
<p>Out of NLATM, NLMOL, NLION, NLPHOT, NLPLS one and only one of these
five variables must be .TRUE. .</p>""",

'NLION' : """Test ion source. History starts in subroutine FOLION with type
index ITYP=3, species index ISPZ = IION and initial weight NPRTI(IION) (see
block 4C)
<p>Out of NLATM, NLMOL, NLION, NLPHOT, NLPLS one and only one of these
five variables must be .TRUE. .</p>""",

'NLPHOT' : """<p>Photon source. History starts in subroutine FOLNEUT with type
index ITYP=0, species index ISPZ = IPHOT and initial weight NPRTPH(IPHOT) (see
block 4D)</p>
<p>Not all options for direct photon sources are fully programmed. Currently we
mostly use the bulk particle volume recombination source (see next) to
simulated radiative decay from excited states as birth profile for (bound-
bound) line-photons.</p><p>Out of NLATM, NLMOL, NLION, NLPHOT, NLPLS one and
only one of these five variables must be .TRUE. .</p>""",

'NLPLS' : """Bulk ion source. Initial co-ordinates of a bulk ion with species
index ISPZ = IPLS and initial weight NPRTP(IPLS) (see block 5) are generated,
then a surface reflection model or a volume re-combination model is called and
atoms, molecules or test ions with species index either IATM, IMOL or IION are
created.<p>Out of NLATM, NLMOL, NLION, NLPHOT, NLPLS one and only one of these
five variables must be .TRUE. .</p>""",

'NSPEZ' : """Species index of the source particle
<dl>
<dt>1 &le; NSPEZ &le; NATMI, NMOLI, NIONI, NPLSI</dt>
<dd>NSPEZ is the (fixed) species index of the source particle. No random
sampling for the species index is done. </dd>
<dt>NSPEZ > NATMI, NMOLI, NIONI, NPLSI</dt>
<dd>(depending upon the type of the source particle) the species index is
sampled from the distribution DATM, DMOL, DION, DPLS, respectively. The
"surface species distributions" DATM, DMOL, DION and DPLS are read in the block
"Data for General Reflection Models", see 2.6.</dd>
<dt>NSPEZ = 0</dt>
<dd><p>the species index of the particle is directly sampled from the "analog
distribution" WEISPZ, i.e., no biased source species sampling. WEISPZ is
defined internally by the code.</p>
<p>The distribution WEISPZ is currently defined only for NLPLS=TRUE sources,
and here only for surface recycling sources using the STEP-function option (in
SAMSRF, see further below this section and paragraph 2.7.1). There it is set
according to the local bulk ion flux composition.</p>
<p>WEISPZ may also be transferred into a run via user specified source sampling
(SAMUSR.f, see section 3.4 ) <br>In all other cases NSPEZ must be positive.</p>
</dd>
<dt>NSPEZ < 0</dt>
<dd>The "surface species distributions" DATM, DMOL, DION and DPLS are consid-
ered as biased source species distributions, whereas the analog (physical)
distri- bution is provided automatically by the array WEISPZ from the source
sampling routines SAMPNT, SAMLNE, SAMSRF or SAMVOL respectively. An appro-
priate weight correction is carried out after sampling from DATM, DMOL, DION or
DPLS, respectively, in subroutine LOCATE.</dd></dl>
Note: If a step function (function STEP, see below) is used for sampling the
start po- sition of a test particle on a surface, then the species index NSPEZ
automatically also fixes the choice of the index ISPZ for the spatial step
function STEP(ISTEP,ISPZ,...) selected by the flags SORLIM and SORIND (=ISTEP)
(see below). This default can be overruled when SORIND has three digits.""",

'Plasma properties. Section 2.7' : """
<b>FLUX SCALV IVLSF ISCLS ISCLT ISCL1 ISCL2 ISCL3 ISCLB ISCLA</b>
<b>FLUX, SCALV</b>
<dt>SCALV=0 (default) FLUX = Source strength in Ampere.</dt>
<dd>FLUX is the scaling factor for all surface- or volume averaged tallies.<br>
FLUX is an "atomic flux" (or: an "atomic ion flux"). Each source particle may
carry a different flux NPRT(ISPZ) (initial weight) depending on the species
ISPZ (see: distribution for the species index). NPRT is specified in the blocks
4 and 5. The total "atomic" source particle flux for each stratum is scaled to
be FLUX. For example, a H 2 molecule source, with NPRT <sub>H<sub>2</sub></sub>
 = 2, is treated as if a flux of FLUX/1.602E-19/2 H<sub>2</sub> -molecules per
second is emitted, resulting in an equivalent "atomic flux" FLUX/1.602E-19 per
second.</dd>
<dt>SCALV &ne; 0</dt>
<dd>The default scaling of tallies with FLUX can be overruled by this flag. The
common scaling factor for all surface- and volume averaged tallies is
determined such that one particular tally has the prescribed value SCALV. This
determines the scaling of all other volume av- eraged and surface averaged
tallies. By this option, for example, one can set the neutral particle density
to a prescribed value in one particular cell. Hence, one can prescribe the
local Knudsen number for nonlinear applications including neutral-neutral
interactions.</dd></dl>
<b>IVLSF</b>
<dl><dt>=1</dt><dd>
The following ISCL..-flags select one particular volume averaged tally</dd>
<dt>=2</dt>
<dd>The following ISCL..-flags select one particular surface averaged
tally</dd></dl>
<b>ISCLS</b>
<p>species index of selected tally</p>
<b>ISCLT</b>
<p>tally number of selected tally (refer to tables 5.2, 5.3)</p>
<b>ISCL1</b>
<p><dl><dt>IVLSF=1</dt>
<dd>cell numbers NRCELL, NPCELL, NTCELL, NBLOCK, NACELL, respectively.
if (NPCELL = 0) or (NTCELL = 0), then ISCL1 = NCELL, the cell number in
the 1-dimensional arrays (see end of section 2.2.1).
The additional cell region is specified by NRCELL=0, NPCELL=1, NTCELL=1,
NBLOCK=NBMLT+1 (see section 2.2) and the proper value of NACELL.</dd>
<dt>IVLSF=2</dt><dd>to be written</dd></dl></p>""",

'NLPNT' : """Point Source""",

'NLLNE' : """Line Source (not ready)""",

'NLSRF' : """Surface Source""",

'NLVOL' : """Surface Source""",

'NLCNS' : """Initial conditions source (sampling from census array), for time-
dependent mode of operation, see input blocks 1. and 13.""",

'NSRFSI' : """<b>(=NPNTSI)</b> <p> Total number of different points, over which
the starting points for this stratum are distributed (corresponds to
<quote>sub- strata<quote> option for surface and volume sources, there to
facilitate sampling  of spatial coordinates).</p>
<p>Total number of different surfaces, or surface segments, over which the
starting points for this stratum are distributed (<quote>sub-strata<quote>,
to facilitate sampling of spatial coordinates).</p>""",

'INUM' : """irrelevant; labelling index for sub-strata""",

'SORWGT' : """Relative frequency for starting point labelled INUM. The sum of
SORWGT for all NPNTSI points is normalized to one internally.""",

'NRSOR' : """<p> 0 x- or radial cell number NRCELL of the zone containing the
point source.</p>
<p>= 0 NRCELL is found automatically from the <quote>standard mesh<quote>
zoning.</p>
<p>< 0 only for surface sources (NLSRF), see below.</p>""",

'NPSOR' : """ditto from NRSOR, for y- or poloidal cell number NPCELL""",

'NTSOR' : """ditto from NRSOR, for z- or toroidal cell number NTCELL""",

'NBSOR' : """standard mesh block number NBLOCK. Defaulted to NBLOCK = 1, if
NBSOR &le; 0""",

'NASOR' : """additional cell number NACELL, if point source is located outside
the standard mesh. Defaulted to NACELL = 0, if at least one of the variables
NRCELL, NPCELL or NTCELL are larger than zero.""",

'NISOR' : """polygon index IPOLG. Meaningless if NLPLG = .FALSE.""",

'SORAD1' : """x-co-ordinate of source point X0""",

'SORAD2' : """y-co-ordinate of source point Y0""",

'SORAD3' : """z-co-ordinate of source point Z0""",

'SORAD4' : """SORAD4, SORAD5, SORAD6, are the x,y and z coordinates of a vector
C = (CRT X, CRT Y, CRT Z) which may be used to distinguish one particular
direction for the distribution in velocity space (see below). Internally this
vector is normalized to length 1. Irrelevant for an isotropic velocity
distribution.""",

'SORAD5' : """SORAD4, SORAD5, SORAD6, are the x,y and z coordinates of a vector
C = (CRT X, CRT Y, CRT Z) which may be used to distinguish one particular
direction for the distribution in velocity space (see below). Internally this
vector is normalized to length 1. Irrelevant for an isotropic velocity
distribution.""",

'SORAD6' : """SORAD4, SORAD5, SORAD6, are the x,y and z coordinates of a vector
C = (CRT X, CRT Y, CRT Z) which may be used to distinguish one particular
direction for the distribution in velocity space (see below). Internally this
vector is normalized to length 1. Irrelevant for an isotropic velocity
distribution.""",

'INDIM' : """<dl><dt>= 0</dt>
<dd>source on <quote>additional surface<quote> ASURF (see block 3B)</dt></d>
<dt>= 1</dt>
<dd>source on <quote>standard surface<quote> RSURF, x- (or radial) mesh
(see block 2A and 3A)</dd>
<dt>= 2</dt>
<dd>source on <quote>standard surface<quote> PSURF, y- (or poloidal) mesh
(see block 2B and 3A)</dd>
<dt>= 3</dt>
<dd>source on <quote>standard surface<quote> TSURF, z- (or toroidal) mesh
(see block 2C and 3A)</dd>
<dt>= 4</dt>
<dd><p>source on a surface composed of one or more segments of radial and/or
poloidal polygons. The further details of the spatial distribution are defined
in code cou- pling routines, i.e., the code coupling routine IF1COP must be
called. Spe- cial versions of IF1COP are available, e.g., in the code segments
COUPLE<sub>B2</sub> , COUPLE<sub>B2.5</sub> (coupling to B2 (BRAAMS) multi-
fluid plasma code) , COUPLE<sub>DIVIMP</sub> (coupling to DIVIMP impurity ion
kinetic transport code) or COUPLE<sub>U file</sub> (TRANSP-code format).</p>
<p>The position on the surface is sampled from a (piecewise constant) step
function defined from plasma fluxes onto that surface vs. arc-length. The flags
INSOR, INGRDA and INGRDE described below are set automatically in this option
and hence need not be specified.</p>
</dl>""",

'INSOR' : """number of the surface in the mesh RSURF, PSURF, TSURF or ASURF
respec- tively. (Redundant in case INDIM=4)""",

'INGRDA' : """same as IRPTA, IRPTE flags in input block 3a. Defines subrange on
standard surfaces, on which the source is distributed. Irrelevant for sources
on additional surfaces.""",

'INGRDE' : """same as IRPTA, IRPTE flags in input block 3a. Defines subrange on
standard surfaces, on which the source is distributed. Irrelevant for sources
on additional surfaces.""",

'SORWGT' : """Relative frequency for starting points on surface labelled INUM.
The sum of SORWGT for all NSRFSI surfaces is normalized to one internally.""",

'SORLIM' : """= KLMN
<p>if SORLIM &le; 0, the user supplied Subroutine SAMUSR is called to sample
all 3 initial co-ordinates (X0,Y0,Z0), see section 3.4.</p>
<p>if SORLIM > 0, then one of the preprogrammed options is used (the digits L,M
and N are relevant only for surface sources). In this case:</p>
<dl><dt>N</dt><dd>Index to select one of the preprogrammed distributions in
radial or x-direction on the surface.</dd>
<dt>M</dt><dd>Index to select one of the preprogrammed distributions in
poloidal or y-direction on the surface.</dd>
<dt>L</dt><dd>Index to select one of the preprogrammed distributions in
toroidal or z-direction on the surface.</dd>
<dt>K</dt><dd>Index to select one of the preprogrammed distributions for the
<starting time.</dd>
<dt>M,N,L = 0</dt><dd>The respective co-ordinate is computed from the 2 others
and from the equation for surface number INSOR.</dd></dl>
<p>Thus, one and only one of these 3 digits must be equal to 0, because the
birth-point for a surface source is determined already by two coordinates and
the labeling o index of the surface.</p>
<p>If INDIM=0, any one of the 3 digits can be the 0, depending upon the
particular equation for the surface ASURF(INSOR).</p>
<p>In case INDIM=1, one has to set N=0 (is now done automatically), and the
poloidal (or y) and toroidal (or z) co-ordinate is sampled according to the
flags M and L.</p>
<p>Correspondingly in case INDIM=2 one must specify M=0, and in case INDIM=3
the flag L=0 has to be set (is redundant).</p>
<p>L,M,N = 1 &delta;-distribution at (a+b)/2</p>
<p>L,M,N = 2 Uniform distribution on the interval [a,b]</p>
<p>L,M,N = 3 Truncated exponential decay with decay length &lambda; on the
interval [a,b]. I.e. the sampling distribution reads:<dd>
f(x) = c &middot; exp(-x/&lambda;) if x &isin; [a, b] and f (x) = 0 elsewhere,
</dd><br>
<dd>with normalized constant<dd><br>
<dd>c = {&lambda;(exp[-a/&lambda;] - exp[-b/&lambda;])}<sup>-1</sup></p></dd>
<p>L,M,N = 4 Step-function (see below: Function STEP, subsection 2.7.1) (only
one of either L or M or N should be 4)</p>
<p>K = 1 &delta;-distribution at TIME0 for time of particle birth. (A delta
function source in time for the kinetic equation in integral form corresponds
to an initial condition for time-dependent linear kinetic integro-differential
equation).</p>
<p>K = 2 Uniform distribution in [TIME0,TIME0+DTIMV] for time of particle
birth.
Default: K=2 in time-dependent mode (NTIME >0) and K=1, TIME0=0 in time-
independent mode (NTIME = 0), see section 2.1.</p>""",

'SORIND' : """<p>Flag to choose one from the various step functions (SORLIM-
option 4), which have been defined in the initialization phase. Up to NSTEP
(PARMUSR, see section 3.1) step functions can be described there. SORIND is the
labelling index of the se- lected step function.</p>
<p>Each step function STEP(ISTEP,...) can consist of step functions for fluxes
of up to NSPZ species, see 2.7.1. NSPZ depends upon the initialization of this
function. By default the source species index NSPEZ is used when sampling from
step functions.</p>
<p>New option (Aug. 2006), e.g. for testing isotope effects: If SORIND &ge;
100, then the 3rd digit is used to select the species index from step function
ISTEP. I.e.: Let SORIND = LMN, then MN is used to sample from step function
ISTEP = MN for species ISPZ</p>
<p>= L. This concerns the spatial distribution. The species index itself of the
sampled particle is still determined by the flag NSPEZ, see above.</p>""",

'SOREXP' : """Decay length &lambda; in the exponential distribution  (option
3)""",

'SORIFL' : """<p>The first of the 4 digits can be used to overrule the default
orientation of the surface normal at the birth point, or if ILSIDE = 0 for this
particular surface. If this digit is nonzero, a value 1 would lead to a test
flight originating from the surface as if a particle has been incident onto
this surface in the positive direction, and the value 2 means that this
imaginary particle has been striking in the negative direction.</p>
<p>The last 3 digits of SORIFL act as LMN of the ILSWCH flag described in
section 2.3B assuming incidence in the positive direction.</p>
<p>If any of this 3 digits equals zero, than the ILSWCH flag for this
particular surface is activated. (See also: section 2.3B, input flag
ILSWCH)</p>""",

'SORCOS' : """<p>Depending upon the value of the flag NAMODS various different
angular distributions may be selected. Each one depends upon the two parameter
P = SORCOS and Q = SORMAX.</p>
<dl><dt>NAMODS = 1</dt>
<dd><p>The polar angle &theta; against the unit vector (C = C<sub>X</sub>,
C<sub>Y</sub>, C<sub>Z</sub>) of the source particle's velocity is sampled
from a cosine**P distribution around the <quote>inner normal vector<quote>
(-1.0) &middot;C, i.e., f (&theta;)d&theta; ~ sin(&theta;) &middot;
cos<sup>p</sup> (&theta;)d&theta;.</p>
<p>Important special cases:</p>
<p>P = 0 isotropic distribution</p>
<p>P = 1 cosine distribution</p>
<p>P &#8811; 1 close to &delta;-distribution around vector -&delta; &middot;
C</p></dd>
<dt>NAMODS = 2</dt>
<dd>The polar angle against -1 &middot; C is sampled from a Gaussian
distribution with zero mean value, and the parameter P now is used for the
standard deviation (degree) of that distribution.</dd></dl>
<p>The second parameter Q is the cut-off angle (degree) for the polar angle
<distribution/p>
<p>note:</p>
<dl><dt>Q &le; 180° is enforced internally</dt>
<dt>Q &le; 90° is enforced internally for surface sources</dt>
<dt>Q = 0 for a beam, i.e., for an angular &delta;-distribution at -1 &middot;
C</dt></dl""",

'SORMAX' : """<p>Depending upon the value of the flag NAMODS various different
angular distributions may be selected. Each one depends upon the two parameter
P = SORCOS and Q = SORMAX.</p>
<dl><dt>NAMODS = 1</dt>
<dd><p>The polar angle &theta; against the unit vector (C = C<sub>X</sub>,
C<sub>Y</sub>, C<sub>Z</sub>) of the source parti- cle's velocity is sampled
from a cosine**P distribution around the <quote>inner normal vector<quote>
(-1.0) &middot;C, i.e., f (&theta;)d&theta; ~ sin(&theta;) &middot;
cos<sup>p</sup> (&theta;)d&theta;.</p>
<p>Important special cases:</p>
<p>P = 0 isotropic distribution</p>
<p>P = 1 cosine distribution</p>
<p>P &#8811; 1 close to &delta;-distribution around vector -&delta; &middot;
C</p></dd>
<dt>NAMODS = 2</dt>
<dd>The polar angle against -1 &middot; C is sampled from a Gaussian
distribution with zero mean value, and the parameter P now is used for the
standard deviation (degree) of that distribution.</dd></dl>
<p>The second parameter Q is the cut-off angle (degree) for the polar angle
<distribution/p>
<p>note:</p>
<dl><dt>Q &le; 180° is enforced internally</dt>
<dt>Q &le; 90° is enforced internally for surface sources</dt>
<dt>Q = 0 for a beam, i.e., for an angular &delta;-distribution at -1 &middot;
C</dt></dl""",

'SORCTX' : """<p>The unit vector C mentioned above is given by normalization of
SORCTX, SORCTY, SORCTZ (if this vector is not zero) or else by the surface
normal vector (in case of surface sources) or else by the default (1.,0.,0.)
(point, line, or volume sources).</p>
<p>By this option, for example, the main direction of emission from a surface
can be influenced. The new distribution of the polar angle is then not
necessarily centered around the inner surface normal vector any longer, in case
of surface sources.</p>""",

'SORCTY' : """<p>The unit vector C mentioned above is given by normalization of
SORCTX, SORCTY, SORCTZ (if this vector is not zero) or else by the surface
normal vector (in case of surface sources) or else by the default (1.,0.,0.)
(point, line, or volume sources).</p>
<p>By this option, for example, the main direction of emission from a surface
can be influenced. The new distribution of the polar angle is then not
necessarily centered around the inner surface normal vector any longer, in case
of surface sources.</p>""",

'SORCTZ' : """<p>The unit vector C mentioned above is given by normalization of
SORCTX, SORCTY, SORCTZ (if this vector is not zero) or else by the surface
normal vector (in case of surface sources) or else by the default (1.,0.,0.)
(point, line, or volume sources).</p>
<p>By this option, for example, the main direction of emission from a surface
can be influenced. The new distribution of the polar angle is then not
necessarily centered around the inner surface normal vector any longer, in case
of surface sources.</p>""",

'SORENI' : no_description_in_manual,

'SORENE' : no_description_in_manual,

'SORVDX' : no_description_in_manual,

'SORVDY' : no_description_in_manual,

'SORVDZ' : no_description_in_manual,

#2.8

'*** 8. Additional data for specific zones' : """Input data in this block
permit explicit specification of plasma parameters T<sub>e</sub> ,
T<sub>i</sub> , D<sub>i</sub> , V<sub>x</sub> , V<sub>y</sub> , V<sub>z</sub>
and of zone volumes VOL in selected cells ICELL. Furthermore, information may
be given to the geometrical block of EIRENE that some &quot;additional
surfaces&quot; are &quot;invisible&quot; for a particle located in cell ICELL
and, therefore, possible crossings need not be checked for advancing this
particle at the next step. (Intelligent use of this option can lead to a
considerable speeding up of the code, less intelligent use will lead to
dramatic errors.) All this information will be included in the EIRENE arrays
after the initialization phase (Subroutines INPUT, PLASMA, GRID, VOLUME) and
before setting the derived profiles (D<sub>e</sub> , flux-surface labelling
grids,...)""",

'NZADD' : """Number of specific zones.""",
# No actual description in this section.

#2.9

'*** 9. Data for statistic and nonanalog model' : """The statistical
performance (FOM, d&quot;figure of merit&quot, see equation 3.25 in section
1.3.3) of an EIRENE run (as for any Monte Carlo application in general) is very
sensitive to the non- analog methods used by EIRENE. Therefore the input
parameters in this block, which define the non-analog setting of an EIRENE run,
should only be used, if the user has carefully worked through the code and has
a detailed knowledge of the Monte Carlo techniques acti- vated by setting the
flags in this block.""",

'NLPRCA' : """conditional expectation estimator (eq. 3.22) is used for atom
species IATM""",

'NLPRCM' : """conditional expectation estimator is used for molecule species
IMOL""",

'NLPRCI' : """conditional expectation estimator is used for test ion species
IION (not ready to use)""",

'NLPRCPH' : """conditional expectation estimator is used for photon species
IPHOT (in versions 2004 and younger)""",

'IPRSF' : """<p>conditional expectation estimator is used, if trajectory points
towards additional sur- face IPRSF. IPRSF &le; NLIMI, the total number of
additional surfaces read in input block 3B.</p>
<p>NPRCSF surfaces have that property of <quote>attracting
trajectories<quote>.</p>""",

'NPRCSF' : """Number of surfaces that have property of <quote>attracting
trajectories<quote>""",

'MAXLEV' : """Maximum number of levels for splitting (&le; 15)""",

'MAXRAD' : """<p>Total number of radial splitting surfaces (-NR1ST &le; MAXRAD
&le; NR1ST)</p>

<dl><dt>MAXRAD < 0</dt>
<dd>-MAXRAD is used, the position of the radial splitting surfaces is
automatically defined, and a constant splitting parameter (SPLPAR, see below)
is used for radial splitting and RR.</dd>
<dt>MAXRAD > 0</dt>
<dd>radial surfaces with numbers NSSPL(IN), IN=1,MAXRAD are S&R-surfaces.
The splitting parameter for surface NSSPL(IN) is PRMSPL(IN).</dd></dl>""",

'MAXPOL' : """Total number of poloidal splitting surfaces (0 &le; MAXPOL &le;
NP2ND). The S&R-surfaces and splitting parameters are selected as in the case
of radial surfaces, see above.""",

'MAXTOR' : """Total number of toroidal splitting surfaces (0 &le; MAXTOR &le;
NT3RD). The S&R-surfaces and splitting parameters are selected as in the case
of radial surfaces, see above.""",

'MAXADD' : """Total number of additional splitting surfaces (0 &le; MAXADD &le;
NLIMI). The S&R-surfaces and splitting parameters are selected as in the case
of radial surfaces, see above.""",

'PRMSPL' : """Splitting parameter for surface.""",

'WMINV' : """minimum weight used for suppression of absorption at collisions
(<quote>survival bi- assing<quote>). If a particle goes into a collision with
weight less than WMINV, then sup- pression of absorption or any other non-
analog weight correction is abandoned, and the analog game is played. WMINV
acts only for events in the volume including volume source birth events, but
not for events at surfaces.""",

'WMINS' : """Same as WMINV, but for surface events (including surface source
birth events).""",

'WMINC' : """<p>minimum acceptable weight for conditional expectation
estimators (by abuse of language). More precisely, WMINC is the minimal
acceptable probability for a test flight to reach a particular cell without
collision. If this probability is smaller than WMINC, the particle track is
stopped and restarted. E.g. for WMINC &ge; 1, the estimator used in the NIMBUS
code results (ref. [14]), whereas for WMINC = 0 each particle path is
integrated according to equation 3.22, until the nearest non transparent
surface along the track is reached, regardless of any collisions. Periodicity
surfaces are regarded as <quote>transparent<quote> in this context.</p>
<p>Note: strictly speaking this is not a non-analog method, but rather a
particular choice of an unbiased estimator. Hence: the flag NLANA in input
block 1 does not affect flags for conditional expectation estimators.</p>""",

'WMINL' : """to be written""",

'SPLPAR' : """splitting parameter for default radial splitting option (MAXRAD <
0)""",

'NSIGVI' : """number of standard deviation profiles for volume averaged tallies
to be estimated. NSIGVI must be less than or equal to the parameter NSD in
PARMUSR 3.1.""",

'NSIGSI' : """number of standard deviation profiles for surface averaged
tallies to be estimated. NSIGSI must be less than or equal to the parameter
NSDW in PARMUSR 3.1.""",

'NSIGCI' : """number of correlation coefficients between volume tallies to be
estimated. NSIGCI must be less than or equal to the parameter NCV in PARMUSR
3.1.""",

'NSIGI_BGK' : """if NSIGI_BGK > 0, then the standard deviations are evaluated
for all tallies needed for the iteration procedure for the nonlinear BGK
collision terms. See subroutine STATIS_BGK in code segment BGK.F""",

'NSIGI_COP' : """if NSIGI_COP > 0, then the standard deviations are evaluated
for all tallies needed for the iteration procedure for the coupling to a plasma
fluid model. The rele- vant tallies are selected in subroutine STATIS_COP in
code segment COUPLE_....F, section 4.2""",

'NSIGI_SPC' : """if NSIGI_SPC > 0, then the standard deviations are evaluated
for all surface flux spectra defined in sub-block 10F below.""",

'IGH' : """Index of species for selected volume averaged tally""",

'IIH' : """Index of volume averaged tally for which empirical standard
deviation is to be calcu- lated (see table 5.2).""",

'IGHW' : """Index of species for selected surface averaged tally""",

'IIHW' : """Index of surface averaged tally for which empirical standard
deviation is to be calcu- lated (see table 5.3)""",

'IGHC1' : """Species and tally index for first and second tally, respectively,
between which the cor- relation coefficient is evaluated""",

'IIHC1' : """Species and tally index for first and second tally, respectively,
between which the cor- relation coefficient is evaluated""",

'IGHC2' : """Species and tally index for first and second tally, respectively,
between which the cor- relation coefficient is evaluated""",

'IIHC2' : """Species and tally index for first and second tally, respectively,
between which the cor- relation coefficient is evaluated""",

#2.10

'*** 10. Data for additional tallies' : """There is a large number of
preprogrammed d&quot;default&quot volume or surface averaged tallies, which
have been selected mainly to allow assessment of global particle and energy
balances for all test particle species, as well as coupling of neutral gas and
plasma transport equations. These tallies are estimated at each EIRENE run
unless they are explicitly abandoned by the surface crossing switches ILSWCH
(section 2.3.2), or are turned off in input block 2.11.""",

'NADVI' : """Total number of additional volume averaged, track-length estimated
tallies""",

'NCLVI' : """Total number of additional volume averaged, collision estimated
tallies""",

'NALVI' : """Total number of tallies defined as algebraic expressions of other
volume averaged tallies""",

'NADSI' : """Total number of additional surface averaged tallies""",

'NALSI' : """Total number of tallies defined as algebraic expressions of other
surface averaged tallies""",

'NADSPC' : """Total number of surface or cell averaged energy spectra""",

'IADVE' : """flag for scaling factor for this tally (carried out in subroutine
MCARLO)
<dl><dt>=1</dt><dd>scale tally per unit volume [1/cm<sup>3</sup> ]. The tally
is printed and plotted in the units [1/cm<sup>3</sup>] &middot; [units of
g<sup>∗</sup>] &middot; [cm] &middot; [source strength FLUX] however, with FLUX
converted to units [1/s] (rather than input units [Ampere]). For the definition
of the detector functions g and g ∗ see section 3.2, the variable FLUX is
explained in input block no. 2.7. This scaling is default for <quote>density
tallies<quote> of particles, momentum and energy.</dd>
<dt>=2</dt><dd>scale tally per unit cell. Same units as above, however not per
cm<sup>3</sup> but per cell instead.</dd>
<dt>=3</dt><dd>same as IADVE = 1, but with FLUX in Ampere, rather than 1/s.
This scaling is default for <quote>source rate tallies<quote>,
e.g. for particle, momentum and energy sources.</dd>
<dt>=4</dt>same as IADVE = 2, but with FLUX in Ampere, rather than 1/s.</dd>
</dl>
else no re-scaling done, units as chosen in subroutine UPTUSR.""",

'IADVS' : """species index of default volume averaged tally, which is to be
replaced by this ad- ditional track-length estimated tally. In case of tallies
with no species index, IADVS must be set equal to 1.""",

'IADVT' : """number of default volume averaged tally, which is to be replaced
by this tracklength estimated tally.""",

'IADVR' : """If automatic re-scaling of volumetric tallies is performed (i.e.
if NLSCL = TRUE), then re-scale this tally with EIRENE recommended factor FATM
(IADVR = 1), FMOL (IADVR = 2) or FION (IADVR = 3) (see block 1 for the flag
NLSCL and the variables FATM,FMOL,FION)""",

'TXTTAL' : """Text to label tally on numerical or graphical output.""",

'TXTSPC' : """Text describing the species of particles contributing for this
tally in output rou- tines.""",

'TXTUNT' : """Text describing the units of this tally in output routines.""",

'ICLVE' : """as IADVE, for collision estimated tally (subroutine UPCUSR).""",

'ICLVS' : """species index of default volume averaged tally, which is to be
replaced by this col- lision estimated tally. In case of tallies with no
species index, ICLVS must be set equal to 1.""",

'ICLVT' : """number of default volume averaged tally, which is to be replaced
by this collision estimated tally.""",

'ICLRC' : """as IADVR above, for collision estimated tally (subroutine
UPCUSR).""",

'ALSTRNG' : """<p>character string which is interpreted as an algebraic
expression in some volume averaged tallies. An operand <i, j> stands for tally
number j, first (species) index i, in tables 5.1 (input tallies) and 5.2
(output tallies) . Note that the first index for tallies with no species index
must read 1, and the tally number of input tallies must be nega- tive. Example:
<1, -1> for the electron temperature tally, <2, 3> for the particle density of
test ion species no. IION=2 . Expressions <c> with an integer or real constant
c are interpreted as scalars. The string may contain an arbitrary (but &le; 20)
number of operands, and of operators +, -, *, /, **, and of properly nested
parentheses (...).</p>
<p>Standard deviations are not available, generally, for algebraic tallies. For
linear combi- nations of tallies it is, in principle, possible to obtain also
the standard deviations, this evaluation of error estimates for such
combinations of tally is, however, is currently carried out only in a
proprietary code segment (available from the author).</p>
<p>E.g., the total electron particle source due to test particle - plasma
interaction in units:#/s/m<sup>3<sup>can be obtained by the line:</p>
<p>(<1,7> + <1,12> + <1,17>)*<1.e6>/<1.6022e-19></p>
<p>in code versions older than 2002 (see tables in section 5.1.2), and the same
expressions in versions 2002 and younger, i.e. after implementation of photons
as further species type (and the related default tallies, tables in section
5.1.1):</p>
<p>(<1,9> + <1,15> + <1,21>)*<1.e6>/<1.6022e-19></p>
<p>and it would be stored on the tally: <quote>ALGV<quote> with the first
(labelling) index IALVI. Note that the cell volume array VOL is regarded as a
volume averaged tally, by abuse of language (tally number = -14, see table
5.1).</p>""",

#2.11

'*** 11. Data for numerical and graphical output' : """The input flags in this
block control all the numerical and graphical output of an EIRENE run. This
comprises diagnostics during the initialization phase (e.g. 2d and 3d geometry
plots) as well as selected test particle histories printed and plotted during
their generation. All numerical output of a run is arranged in so called
d&quot;tallies&quot. There are volume averaged tallies, surface averaged
tallies (d&quot;surface crossing tallies&quot) and global tallies. These latter
tallies are derived from the former ones by integration over the total
computational volume, or over all non-transparent surfaces, respectively.""",

'TRCPLT' : """Trace-back from plot routines.""",

'TRCHST' : """Printout of trajectories of selected test particle histories into
geometry plots. These histories are selected by the flags I1TRC and I2TRC, see
below, sub-block 11B.2.""",

'TRCNAL' : """Trace-back for non-analog methods, i.e. splitting surfaces,
suppression of ab- sorption, weighted post-collision species sampling etc.""",

'TRCMOD' : """Trace-back from routines for iterative mode (MOD TMSTEP, MODBGK,
and problem specific routines called from MODUSR).""",

'TRCSIG' : """Trace-back from post processing line integral diagnostics block
DIAGNO""",

'TRCGRD' : """Printout of <quote>standard mesh surface data<quote>""",

'TRCSUR' : """Printout of data for <quote>additional surfaces<quote>""",

'TRCREF' : """Printout of reflection model related data. In particular a list
of all non-perfect recycling surfaces is printed, i.e., a list of surfaces for
which there is some absorption at least for one incident particle species.""",

'TRCFLE' : """Trace-back from subroutines WRSTRT, WRGEOM, WRPLAS (writing on
and reading from the dump files FT10, FT11, FT12, FT13 etc.""",

'TRCAMD' : """Trace-back from atomic and molecular data routines
XSECTA, XSECTM, XSECTI""",

'TRCINT' : """Traceback from user specified interfacing routine INFCOP, e.g. of
data related to coupling of EIRENE to other codes.""",

'TRCLST' : """Printout of information during the last history of each stratum.
E.g., sampling efficiencies, and other accumulated information, which is only
available in the history generation routines during particle tracing.""",

'TRCSOU' : """Traceback from primary source sampling routines, e.g. from
LOCATE, SAMPNT, SAMLNE, SAMSRF, SAMVOL and SAMUSR""",

'TRCREC' : """Printout of EIRENE recommendations for next run on same case:<br>
A) stratified source sampling, at present: for proportional allocation of
weights.<br> B) weight windows, at present: to be written""",

'TRCTIM' : """Printout cpu-time information for each history""",

'TRCBLA' : """Global particle and energy balance for atoms is printed.""",

'TRCBLM' : """Global particle and energy balance for molecules is printed.""",

'TRCBLI' : """Global particle and energy balance for test ions is printed.""",

'TRCBLP' : """Global particle and energy balance for bulk ions is printed.""",

'TRCBLE' : """Global particle and energy balance for electrons is printed.""",

'TRCBLPH' : """Global particle and energy balance for photons is printed.""",

'TRCTAL' : """Print list of activated and de-activated tallies. The default
settings eliminate some tallies from storage and estimators which are likely to
be irrelevant in a particular run, e.g. all photon related tallies are
deactivated automatically if no radiation trans- fer calculation is included in
a run. These default settings are overruled by the flags NTLVOUT and NTLSOUT at
the end of this sub-block 11A, see below.""",

'TRCOCT' : """to be written: printout from octree geometry optimization
procedure""",

'TRCCEN' : """printout from census array stored in time dependent mode: species
and stratum resolved census fluxes""",

'TRCSRC(i)' : """The selected global, volumetric and surface crossing tallies
are printed for those strata for which TRCSTR(ISTRA) = .TRUE.. In case
TRCSTR(0) = .TRUE., the results after summation over all strata is printed for
these tallies.
Note: printout for individual strata is only possible if the data for strata
    have been saved
on file (NFILE-N=1,2 option, input block 1). Otherwise only the last stratum
currently on storage arrays (mostly: sum over strata) is available.
""",

'NVOLPR': """Total number of volume averaged tallies to be printed.""",

'NSPCPR': """Flag for printout of surface or cell based spectra (defined in
input block 10F) If NSPCPR &gt; 0 : spectra are printed on output stream
fort.(20+ioff), name: spectra.out""",

'NPRTLV': """Index of the tally to be printed (first column in
table 5.1 or 5.2).  If the tally has a species index, it is printed for all
species, for which the integral of the tally over the computational area is
nonzero. Otherwise the statement

ZERO INTEGRAL FOR SPECIES ISPZ = ......

is printed below the header for this tally.   The term "species index" is
used here in a more general sense for the first index (if any) for any given
tally.  In case of some "additional tallies" or other tallies,  in which the
first index does not label a particle species but something else, this term
"species index" then is to be understood in a more general sense.
If NPRTLV = 0, then the user defined post processing routine TALUSR is
called (3.7.
""",

'NFLGV': """Flag to specify the level of printout
<dl>
  <dt>= -1</dt><dd>print only header</dd>
  <dt>= 0</dt><dd>additionally: print global quantities
  (total and block averages)</dd>
  <dt>= 1</dt><dd>additionally:  print 1D profiles (if any), averaged over all
  (if any) higher dimen-sions</dd>
  <dt>= 2</dt><dd>additionally:  print 2D profiles (if any), averaged over all
  (if any) higher dimen-sions</dd>
  <dt>= 3</dt><dd>additionally:  print 3D profiles (if any), averaged over all
  (if any) higher dimen-sions</dd>
  <dt>= 4</dt><dd>print 3D profiles, but no lower dimensional averages</dd>
</dl>""",

'NSPZV1': """If NSPEZV(..,1) &ne; 0, then this tally is printed only for the
species index range: I1 = NSPEZV(...,1) to I2 = MAX(I1,NSPEZV(...,2)), rather
than for all species relevant for the specified tally.""",

'NSPZV2': """If NSPEZV(..,1) &ne; 0, then this tally is printed only for the
species index range: I1 = NSPEZV(...,1) to I2 = MAX(I1,NSPEZV(...,2)), rather
than for all species relevant for the specified tally.""",

'NTLV': """In addition to the standard output stream fort.IUNOUT, this tally
is also printed onto output stream fort.NTLVFL, for all species selected,
and also the corresponding standard deviations are printed, if available.
The format for this extra output stream is specified in subroutine PRTTAL,
in code segment EIRASS.""",

'NSURPR': """Total number of surfaces, for which surface averaged tallies are
to be printed.""",

'NSRF': """Index of the surface to be printed. By default all tallies listed
in tables (5.3, 5.4, 5.7) (depending on code version) are printed for this
surface.""",

'NTLS': """These next flags are only needed for those surfaces, for which a
further spatial resolution within one surface is provided (this is enabled by
providing storage through setting the flag NGSTAL = 1 in input block1). Their
meaning then corresponds to the meaning of flags NPRTLV(J), NFLAGV(J),
NSPEZV(J,1), NSPEZV(J,2) for volume tallies, respectively.  If the NPRTLS,...
flags are not specified (i.e.: default=0), then no spatially resolved surface
tallies are printed.""",

'NFLGS': """These next flags are only needed for those surfaces, for which a
further spatial resolution within one surface is provided (this is enabled by
providing storage through setting the flag NGSTAL = 1 in input block1). Their
meaning then corresponds to the meaning of flags NPRTLV(J), NFLAGV(J),
NSPEZV(J,1), NSPEZV(J,2) for volume tallies, respectively.  If the NPRTLS,...
flags are not specified (i.e.: default=0), then no spatially resolved surface
tallies are printed.""",

'NSPZS1': """These next flags are only needed for those surfaces, for which a
further spatial resolution within one surface is provided (this is enabled by
providing storage through setting the flag NGSTAL = 1 in input block1). Their
meaning then corresponds to the meaning of flags NPRTLV(J), NFLAGV(J),
NSPEZV(J,1), NSPEZV(J,2) for volume tallies, respectively.  If the NPRTLS,...
flags are not specified (i.e.: default=0), then no spatially resolved surface
tallies are printed.""",

'NSPZS2': """These next flags are only needed for those surfaces, for which a
further spatial resolution within one surface is provided (this is enabled by
providing storage through setting the flag NGSTAL = 1 in input block1). Their
meaning then corresponds to the meaning of flags NPRTLV(J), NFLAGV(J),
NSPEZV(J,1), NSPEZV(J,2) for volume tallies, respectively.  If the NPRTLS,...
flags are not specified (i.e.: default=0), then no spatially resolved surface
tallies are printed.""",

'NTLSF': """The  spatially  resolved  tallies  (if  any)  and/or  the  flux
energy  spectra  (if  any, see input block 10F) are printed on additional
output stream fort.NTLSFL(J) for this surface.
""",

'NTLVOUT': """total number of volume averaged tallies to be explicitly
abandoned or enabled""",

'NUMTAL(J)': """Number of a tally from table 5.2, e.g. NUMTAL(J)=1 for neutral
atom density tally PDENA. The tally with this number NUMTAL(J) is explicitly
enabled.  With an additional  negative  sign  this  tally  is  removed  from
the  run  (and  the  balances),  e.g. NUMTAL(J)=-2 would remove the evaluation
(and storage) of tally PDENM from this run.""",

'NTLSOUT': """To be written""",

'PL1ST': """plot the x- (radial) standard grid surfaces into a 2D geometry
plot""",

'PL2ND': """plot the y- (poloidal) standard grid surfaces into a 2D geometry
plot""",

'PL3RD': """plot the z- (toroidal) standard grid surfaces into a 2D geometry
plot""",

'PLADD': """plot the additional surfaces into a 2D geometry plot""",

'PLHST': """Plot the track of some selected test particle histories into the
geometry plot (2D or 3D).""",

'PLCUT(i)': """Flag for the choice of a plane, in which the 3 dimensional
geometrical configuration is plotted in case of a 2D geometry plot.
This plane may be defined by either x = CONST, y = CONST or by z = CONST.
<dl>
  <dt>=PLCUT(1) = .TRUE.</dt><dd>x = CONST ; plotting plane is the yz-plane.
y is the ordinate, z is the abscissa</dd>
  <dt>=PLCUT(2) = .TRUE.</dt><dd>ay = CONST ; plotting plane is the xz plane.
z is the ordinate, x is the abscissa</dd>
  <dt>=PLCUT(3) = .TRUE.</dt><dd>z = CONST ; plotting plane is the xy plane.
y is the ordinate, x is the abscissa</dd>
</dl>""",

'PLBOX': """plot box defined by surface inequalities in addition to valid part
of surface""",

'PLSTOR': """produce file of coordinates along 2D projections of
"additional surfaces" for later use in some graphics ("PATRAN format",  also
for RAPS-graphics,  see below,  sub-block:  11B3).  These coordinates are
stored on arrays XPL2D, YPL2D in subroutine STCOOR called from subroutine
PLTADD.""",

'PLNUMV': """print cell number into standard mesh cells""",

'PLNUMS': """print numbers near additional surfaces""",

'PLARR': """plot arrows to indicate surface normal vector""",

'CH2MX': """horizontal half width of 2D plot window (cm)""",

'CH2MY': """vertical half width of 2D plot window (cm)""",

'CH2X0': """horizontal co-ordinate of midpoint of 2D plot window (cm).""",

'CH2Y0': """vertical co-ordinate of midpoint of 2D plot window (cm).""",

'CH2Z0': """distance CONST of plotting plane to origin.""",

'NPLINR': """radial standard surfaces with labels IR1ST = NPLINR, NPLOTR,
NPLDLR are plotted.""",

'NPLOTR': """radial standard surfaces with labels IR1ST = NPLINR, NPLOTR,
NPLDLR are plotted.""",

'NPLDLR': """radial standard surfaces with labels IR1ST = NPLINR, NPLOTR,
NPLDLR are plotted.""",

'NPLINP': """poloidal standard surfaces with labels IP2ND= NPLINP, NPLOTP,
NPLDLP are plotted.""",

'NPLOTP': """poloidal standard surfaces with labels IP2ND= NPLINP, NPLOTP,
NPLDLP are plotted.""",

'NPLDLP': """poloidal standard surfaces with labels IP2ND= NPLINP, NPLOTP,
NPLDLP are plotted.""",

'NPLINT': """toroidal standard surfaces with labels IT3RD= NPLINT, NPLOTT,
NPLDLT are plotted.""",

'NPLOTT': """toroidal standard surfaces with labels IT3RD= NPLINT, NPLOTT,
NPLDLT are plotted.""",

'NPLDLT': """toroidal standard surfaces with labels IT3RD= NPLINT, NPLOTT,
NPLDLT are plotted.""",

'CH3MX': """half width of plot chamber in x- direction, used for 3D geometry plot""",

'CH3MY': """half width of plot chamber in y- direction, used for 3D geometry plot""",

'CH3MZ': """half width of plot chamber in z- direction, used for 3D geometry plot""",

'CH3X0': """x-co-ordinate of midpoint of plot-chamber in user co-ordinates,
3D geometry plot only""",

'CH3Y0': """y-co-ordinate of midpoint of plot-chamber in user co-ordinates, 3D
geometry plot only""",

'CH3Z0': """z-co-ordinate of midpoint of plot-chamber in user co-ordinates, 3D
 geometry plot only""",

'ANGLE1': """First viewing angle for 3D geometry plot""",

'ANGLE2': """Second viewing angle for 3D geometry plot""",

'PL3A(j)': """logical flag, indicating if the additional surfaces specified in
this card are to be plotted or not. If PL3A=.FALSE., the rest of this card is
irrelevant""",

'TEXTLA': """text written onto plot, characterizing this group of additional
surfaces""",

'IPLTA': """number of different subgroups of additional surfaces comprising
this group""",

'IPLAA': """each subgroup consists of additional surfaces ranging from no.
IPLAA(J) to IPLEA(J), J=1,IPLTA""",

'IPLEA': """each subgroup consists of additional surfaces ranging from no.
IPLAA(J) to IPLEA(J), J=1,IPLTA""",

'I1TRC': """Number of first particle history to be traced in printout and/or 2D
or 3D plot""",

'I2TRC': """Number of last particle history to be traced in printout and/or 2D
or 3D plot""",

'ISYPLT(i)': """Indices to plot symbols along the particle tracks for different
 events. Up to 8 different events can be picked in any order in the array
 ISYPLT.

<dl>
  <dt>0</dt><dd>no symbol</dd>
  <dt>1</dt><dd>symbol at particle’s birth point (at primary source)</dd>
  <dt>2</dt><dd>symbol at the point of an electron impact collision event</dd>
  <dt>3</dt><dd>symbol at the point of a hard elastic collision event</dd>
  <dt>4</dt><dd>symbol at the point of a charge exchange event</dd>
  <dt>5</dt><dd>symbol at the point of a soft elastic collision event</dd>
  <dt>6</dt><dd>symbol at an intersection with a "non-default" or "additional"
  surface</dd>
  <dt>7</dt><dd>symbol at a non-analog particle splitting point</dd>
  <dt>8</dt><dd>symbol at a non-analog particle killing point
  ("Russian Roulette")</dd>
  <dt>9</dt><dd>symbol at a periodicity surface intersection point</dd>
  <dt>10</dt><dd>symbol at restart after splitting</dd>
  <dt>11</dt><dd>symbol at collision point saved for conditional exp.
  estimator</dd>
  <dt>12</dt><dd>symbol at a continuation of track for conditional exp.
  estimator</dd>
  <dt>13</dt><dd>symbol at a particle stopped at time limit (t-dep. mode)</dd>
  <dt>14</dt><dd>symbol at a particle stopped at generation limit (t-dep.
  mode)</dd>
  <dt>15</dt><dd>If an error is detected, by default a symbol is always
  plotted. Plotting this symbol cannot be abandoned.</dd>
</dl>
""",

'ILINIE': """
<dl>
  <dt>&ne; 0</dt><dd>connect two successive events by a straight line.  If a
continuation of a track is computed for the conditional expectation
estimators, this part is represented by a dotted line, see eq. (1.2.5).</dd>
  <dt>= 0</dt><dd> only symbols (if any selected) will be plotted along the
history</dd>
</dl>
""",

'NVOLPL': """Total number of pictures from volume averaged tallies.""",

'TRCDUMM' : no_description_in_manual,
'TRCDBG2' : """CVK TRACING FOR DEBUGGING:  not in use in present eirene""",
'TRCDBGE' : """CVK TRACING FOR DEBUGGING:  not in use in present eirene""",
'TRCDBGM' : """CVK TRACING FOR DEBUGGING:  not in use in present eirene""",
'TRCDBGF' : """CVK TRACING FOR DEBUGGING:  not in use in present eirene""",
'TRCDBGL' : """CVK TRACING FOR DEBUGGING:  not in use in present eirene""",
'TRCDBGS' : """CVK TRACING FOR DEBUGGING:  not in use in present eirene""",
'TRCDBGG' : """CVK TRACING FOR DEBUGGING:  not in use in present eirene""",
'TRCDBGMPI' : """CVK TRACING FOR DEBUGGING:  not in use in present eirene""",
'TRCDBGC' : """CVK TRACING FOR DEBUGGING:  not in use in present eirene""",

#2.12

'*** 12. Data for diagnostic module' : """The data in this block are used to
define a line-of-sight (LOS) across the computational do- main, are
evaluated.This is done in subroutine LININT, which is called from subroutine
DIAGNO at the end (post processing phase) of an EIRENE run. The spatial
dependence of the function g(l) is defined as function of one or more of the
estimated volume averaged tallies (e.g., atom density), and/or input tallies
(e.g. plasma temperatures). At present there are two (version 2004 and older)
or three preprogrammed functions g(l), and the option to call a user supplied
integrant. Firstly there are the Lyman- and Balmer series volume source rates
(emissivity), see Subr. SIGAL. Secondly the neutral atom charge exchange source
rate can be integrated along a line of sight for a given energy of the
impacting plasma ion (Subr. SIGCX). This routine includes re-absorption along
the line of sight. A LOS spectrum (also: d&quot;side-on spec- trum&quot) of up
to NCHEN energies may be obtained by this procedure. Thirdly (version 2005 and
younger) the side-on radiances of selected lines (photon test particle
species), including reabsorption, can be obtained (Subr. SIGRAD). A number of
different emission line shape profiles is available for these.""",

'NCHORI' : """Total number of different line of sights""",

'NCHENI' : """<p>ABS(NCHENI) is the total number of energies, at which the
spectrum is eval- uated (irrelevant e.g. for total signals, such as Lyman and
Balmer emissivity without line shape resolution).</p>
<p>The energy grid is equidistant on a linear scale, if NCHENI ≥ 0, and
equidistant on a logarithmic scale otherwise.</p>""",

'TXTSIG' : """Text in printout at the beginning of the data from this line of
sight integral.""",

'NSPTAL' : """Flag for choice of preprogrammed function which is <quote>line
integrated<quote>.
<dl><dt>=1</dt>
<dd>charge exchange source rate (SIGCX)</dd>
<dt>=2</dt>
<dd>Hydrogen line emission source rate (SIGAL)</dd>
<dt>=3</dt>
<dd>spectral radiance of photonic lines (SIGRAD) (new in versions 2005 and
<younger)/dd>
<dt>=10</dt>
<dd>user supplied integrand (SIGUSR) (this was option NSPTAL =3, in versions
2004 and older)</dd></dl>""",

'NSPSCL' : """Flag for choice of linear or logarithmic axes in plots of spectra
(vs. energy or wavelength, resp.) and of source term distribution along line of
sight.
<dl><dt>=0</dt>
<dd>both axes linear</dd>
<dt>=1</dt>
<dd>x axis linear, y axis logarithmic</dd>
<dt>=2</dt>
<dd>x axis logarithmic, y axis linear</dd>
<dt>=3</dt>
<dd>both axes logarithmic</dd></dl>""",

'NSPNEW' : """Flag for the choice whether a spectrum is plotted on the same
picture as the previous one (NSPNEW = 0) or onto a new graph (otherwise).""",

'NSPCHR' : """if .gt. 0: then automatically all cells along chord are
identified, and energy re- solved spectra (input block 10f) are computed in all
these cells by automatically aug- menting input block 10f correspondingly.
These spectra are line-of-sight spectra in the direction of the chord specified
here (direction SPCVX, SPCVY, SPCVZ in augmented input block 10f is taken to be
a unit vector along this present line of sight).""",
'NSPSTR' : """Index for stratum, which is to be used for line integration
(NSPSTR = 0: sum over strata).""",
'NSPSPZ' : """<p>In case NSPTAL=1:</p>
<p>Index for atomic species IATM, with IATM &le; NATM, for which charge
exchange spectrum is to be computed (NSPSPZ = 0: sum over atom species
index)</p>
<p>In case NSPTAL=2:</p>
<p>Number of contribution to line intensity, as programmed in Subr.
Ba<sub>Alpha</sub , Ba<sub>Gamma</sub> , Ly<sub>Beta</sub> , etc. (Currently up
to 6 contributions for each H atom spectral line, and the total)</p>
<dl><dt>=1</dt>
<dd>coupling to ground state: H(1s)</dd>
<dt>=2</dt>
<dd>coupling to continuum: H<sup>+</sup></dd>
<dt>=3</dt>
<dd>coupling to: H<sub>2</sub></dd>
<dt>=4</dt>
<dd>coupling to: H<sub>2</sub><sup>+</sup></dd>
<dt>=5</dt>
<dd>coupling to: H<sup>-</sup></dd>
<dt>=6</dt>
<dd>coupling to: Hsub>3/sub>sup>+/sup>(new in versions 2012 and younger)</dd>
<dt>=0</dt>
<dd>total, sum over all contributions to a particular line (was = 6, in
versions 2011 and older)</dd>
<p>In case NSPTAL=3:</p>
<p>Index for photon species (line), i.e. for IPHOT, with IPHOT &le; NPHOT, for
which side-on spectrum is to be computed (NSPSPZ = 0: sum over photon species
index, not ready)</p>""",

'NSPINI' : """only for NSPTAL=1:
<p>Multipliers for the maximum ion temperature
Ti<sub>max</sub> found along line of sight, for tem- perature fitting. The CX
ion temperature is fitted from the CX line of side spectrum in the interval
[NSPINI × Ti<sub>max</sub> , NSPEND × Ti<sub>max</sub> ]</p>""",

'NSPBLC' : """Standard mesh block number of 2nd point on line of sight.""",

'NSPADD' : """Additional cell number of 2nd point on line of sight.
<p>If NSPADD = 0 , then this 2nd point must lie in standard mesh block
<NSPBLC./p>
<p>If NSPADD &ne; 0, then the block number NSPBLC must be NSPBLC = NBMLT+1,
i.e. the second point on the line of sight is in the <quote>additional cell
regionq<quote>.</p>""",

'EMIN1' : """<p>for NSPTAL=1,3,10: minimum and maximum energy for spectral
resolution, respectively.</p>
<p>for NSPTAL=2:</p>
<p>Old input version (still maintained for backward compatibility of input
files: EMIN1 is an energy parameter to identify the particular hydrogen line
and EMAX1 is not used. EMIN1 is given in eV, by Ry × (1/n<sup>2</sup> -
1/m<sup>2</sup>), with Ry = 13.6 (eV).</p>
<p>EMIN1 = 12.089: Lyman-beta line<br>
EMIN1 = 3.0222: Balmer-delta line<br>
EMIN1 = 2.8560: Balmer-gamma line<br>
EMIN1 = 2.5500: Balmer-beta line<br>
EMIN1 = 1.8889: Balmer-alpha line<br></p>
<p>Other side on line emissivities can be obtained using the user supplied line
of side inte- gral SIGUSR (option NSPTAL=10) and analogy to the preprogrammed
options, as well as the internal EIRENE hydrogen atom collisional radiative
routine H-COLRAD.F to obtain the required reduced population coefficients for H
∗ (n). For the preprogrammed options these latter coefficients for n = 2, 3, 4,
5, 6 are stored in AMJUEL, section H12, see this web page under: EIRENE AMS
data files.</p>""",

'ESHIFT' : """(for NSPTAL=1, 3, 10 options only)
<p>energy shift for spectral resolution in printout, and plot</p>""",

'IPIVOT' : """(only needed for NLTRA option, <quote>toroidal
approximation<quote>, sub-block2c)
<dl><dt>1 &le; IPIVOT &le; NTTRA-1 (currently no available, error exit)</dt>
<dd>number of local toroidal co-ordinate system (NTTRA: see sub-block 2c), in
which this pivot point is specified. The pivot point is then given in cartesian
coordinates is this local system</dd>
<dt>IPIVOT=0</dt>
<dd>pivot point is given in global cylindrical coordinates,
XPIVOT,YPIVOT,ZPIVOT = r, z, &phi;, with &phi; in degrees. The corresponding
toroidal block numbers ITTRA are found automatically.</dd></dl>""",

'XPIVOT' : """1st co-ordinate of pivot point for line of sight, e.g. x""",

'YPIVOT' : """2nd co-ordinate of pivot point for line of sight, e.g. y""",

'ZPIVOT' : """3rd co-ordinate of pivot point for line of sight, e.g. z""",

'ICHORD' : """(only needed for NLTRA option, sub-block 2c) Meaning analogous to
that of first point flag IPIVOT:""",

'XCHORD' : """1st co-ordinate of second point for line of sight""",

'YCHORD' : """2nd co-ordinate of second point for line of sight""",

'ZCHORD' : """3rd co-ordinate of second point for line of sight""",

'PLCHOR' : """the lines of sight are plotted into (2D or 3D) geometry plots.
This, however, is automatically turned off if other plots are done between
geometry plots (initialization phase) and line-of-sight integration (post
processing phase).""",

'PLSPEC' : """the spectra along the lines of sight are plotted (irrelevant in
case of NSPTAL = 2).""",

#2.13

'*** 13. Data for nonlinear and time dep. option' : """The data in this block
are used to define a discretisation in time, and the test-particle self
interaction effects. These latter options are based upon the d&quot;Bird’s
Direct Monte Carlo Sim- ulation&quot (DMCS) procedure, and are currently not in
use (see [23] for a detailed description of its implementation in EIRENE). They
can be activated by replacing the current dummy routine STOSS, which is called
after each time-step from subroutine EIRENE, by a routine that reads the
particle population from the d&quot;census arrays&quot described below, and
which then carries out the binary self-collisions (modification of the
individual particle velocity vectors). The rest of the code for time dependency
and the DMCS algorithm is the same and described in this section. Note that,
currently, with the use of a dummy routine STOSS, non-linear self collision
effects can still be simulated, in BGK approximation, by using the iterative
mode of operation (NITERI, NITERE, input block 1), see section 1.9.""",

'NPRNLI' : """<p>Total number of test particles in time dependent arrays
(<quote>census arrays<quote>) (in old versions before 2001: NPRNLI must be &le;
NPRNL, see: PARMUSR). The scoring on census arrays stops at latest when NPRNLI
scores are on the census array.</p>

<p>If NPRNLI > 0, but the rest of the data in this block are not specified,
then a default time-horizon is defined. See default values specified below.</p>

<p>If NPRNLI = 0, no census arrays are scored</p>

<p>In case NLERG = TRUE (see input block 1), a time horizon is absolutely
necessary in order to prevent infinite histories. Therefore, in case NLERG=TRUE
and NPRNLI=0 an automatic correction to NPRNLI=100 is carried out.</p>""",

'NINITL_READ' : """(new: 2013) Same as NINITL in block 7: provides random
number seed for <quote>time-stratum<quote> (sampling from census array
(default: =0, no fresh initialization of random number generator for this
stratum)""",

'NPRMUL' : """(new: 2013) Multiplicative factor for NPRNLI, in order to
increase size of cen- sus to more than 999999 particles, which otherwise would
be the maximum due to I6 formatted integer input. Default: = 0: no
multiplication carried out""",

'NPTST' : """<p>Same as NPTS in block 7. This is the number of histories, which
are continued from a previous time-cycle (<quote>Time dependence stratum
ISTRA=NSTRAI+1<quote>). The initial coordinates are randomly sampled (with
replacement) from the census-array data from an earlier time-cycle. The
probability for sampling a particular particle from the census array is
proportional to its weight stored on the census array as well. Due to
<quote>sampling with replacement<quote> an individual particle, which is on
census, may be sampled more than once, or not at all, with the likelihood for
these events given by its weight (<quote>warm restart<quote>). This census
array is either defined at the end of the previous time cycle in the same run
(subr. TMSTEP), or it is read from an earlier run from stream 15 (via a call to
subr. RSNAP from subr. INPUT) in the initial phase of the run, for the very
first time-cycle (continuation of an earlier sequence of time-cycles).</p>
<p>If NPTST = 0 , then NPTST is reset to IPRNL. IPRNL is the the number of
scores on the census array in the previous time cycle.</p> <p>If NPTST < 0 ,
then NPTST is reset to IPRNL, and the random sampling from the census array is
now replaced by a one-to-one re-launch of all particles from the census array
without random sampling (<quote>cold restart<quote>). Until Aug. 2015 this
option was avail- able only in connection with the NLMOVIE option (movies of
trajectories) and had led to other modifications of the run parameters as well.
(Automatically then internally: NLMOVIE = TRUE). New: NLMOVIE AND NPTST < 0
options are now indepen- dent from each other. In both cases: one by one re-
launch from old census is enforced, rather than random sampling from old
census.</p> <p>Default: NPTST=0</p>""",

'NTMSTP' : """<p>Total number of time-steps for particle tracing. Each
trajectory can score on census up to NTMSTP times. Particle trajectories are
stopped after NTMSTP time- steps.</p>
<p>Default: NTMSTP=1</p>
<p>For convenience and by abuse of language, we refer to the 3-dimensional
hyper-surface t = t<sub>n</sub> of the four dimensional (r, t)-space as
<quote>time- surface<quote>, and, hence, tallies evalu- ated at fixed time t n
(<quote>snapshot-tallies<quote>) are surface averaged tallies in this
terminology.</p>
<p>Fluxes onto this surface are stored on the arrays for a surface no.
NLIM+NSTSI+1, which is added automatically to the NLIM additional and NSTSI
non-default standard surfaces.</p>
<p>The time-surface is transparent for NTMSTP-1 steps and absorbing afterwards,
i.e., absorbing at time t = NTMSTP × DTIMV. Snapshot tallies are averages over
NTMSTP time-steps.</p>
<p>If NTMSTP < 0, then each particle can score an unlimited number of times on
census, i.e., the time-surface is always transparent. This option can be used
for initialization of census arrays for time dependent runs. The census arrays
then represent a stationary distribution corresponding to a certain constant
(in time) influx of particles, rather than an estimate at a fixed time. Hence,
for any fixed detector function (volume averaged tally), the snapshot estimator
should give the same results (up to statistical precision) as the track-length
estimator or the collision estimator. Note that in order to obtain this
stationary estimate from snapshot estimates an additional multiplicative factor
DTIMV (s) (see next) is applied to snapshot tallies in case NTMSTP < 0.</p>""",

'DTIMV' : """Length of each individual internal time-step (seconds)
<p>Default: DTIMV=1.D-02</p>""",

'TIME0' : """Initial time t<sub>0</sub> of the first time-step. (irrelevant,
only for printout and book-keeping)
<p>Default: TIME0=0.</p>""",

'NSNVI' : """Number of snapshot tallies computed from census arrays. In old
EIRENE ver- sions without dynamic allocation of storage NSNVI must be less or
equal NSNV (see PARMUSR), and the detector functions are user supplied in
subroutine UPNUSR, see Sub-section 3.2.3.
<p>Default: NSNVI=0</p>""",

#2.14

'*** 14. Data for interfacing routine "infusr"' : """Data in input block 14
control additional input for an EIRENE run. In case NMODE = 0 (see input block
1), i.e., no call to interfacing subroutine INFCOP, only the additional input
tallies ADIN (see table 5.1), if any, are specified here. Otherwise, if NMODE
&ne;  0 the data in this block are read from the code interfacing subrou- tine
INFCOP (at entry IF0COP) rather than from subroutine INPUT. They may be used to
modify or complete the model defined by the formatted input file so far. For
example, by this option the entire geometry specification (blocks 2,3) can be
modified or overwritten by a few geometry parameters without rewriting input
blocks 2 and 3. This allows rapid geometry op- timization (geometry parameter
studies), which otherwise would require to generate a large set of different
geometry input blocks. As this routine is problem specific, it must be written
by the user and, therefore, input can be from any file and in any format chosen
there.""",

'LSYMET' : """<dl>
<dt>=.TRUE.</dt>
<dd>Upside-down symmetry of all tallies transferred to external code via common
block EIRBRA) is enforced.</dd>
<dd>Symmetry plane is the PSURF/2. surface, i.e., the poloidal (or y) co-
ordinate surface PSURF(NP2ND/2) at the center of the computational interval in
this co- ordinate.</dd>
<dd>This option has historical reasons. The very first B2-EIRENE runs ever have
been performed for &quot;upside-down symmetric&quot; ITER double null
configurations (Reiter et al., 1991, [2]). In more recent versions this option
may not be available anymore.</dd>
<dt>=.FALSE:</dt>
<dd>no such symmetry is enforced</dd>
</dl>""",

'LBALAN' : """dl>
<dt>=.TRUE.</dt>
<dd>Global particle and energy flux balance is performed and printed at
the end of an EIRENE stand alone run (steady state or single time-step) and at
the end of a short cycle between a plasma transport code and EIRENE. These
balances compare plasma particle and energy fluxes at the boundaries, volume
sources in plasma balance equations and neutral-plasma interaction sources and
sinks.</dd>
<dt>=.FALSE:</dt>
<dd>no such balances are computed</dd>
</dl>""",

'LCHKQUD' : """Check quadrangles switch ???""",

'NFLA' : """Number of different (bulk) ion species in plasma code.""",

'NCUTB' : """Number of mesh cells in each grid cut in plasma code (specific to
grid generator used in connection with B2 fluid code).""",

'NCUTL' : """Number of mesh cells in each grid cut in EIRENE.
<p>Note: if NCUT 6 &ne; NCUTL, the index mapping routines INDMAP and INDMPI are
called at each call to the interfacing routines.</p>""",

'MSHFRM' : """new flags, available only since 2013, see section 2.14.3""",
'NTRFRM' : """new flags, available only since 2013, see section 2.14.3""",
'NFULL' : """new flags, available only since 2013, see section 2.14.3""",
'IBRAD' : """new flags for magnetic field orientation, available only since
March 2015, see section 2.14.3""",
'IBPOL' : """new flags for magnetic field orientation, available only since
March 2015, see section 2.14.3""",
'IBTOR' : """new flags for magnetic field orientation, available only since
March 2015, see section 2.14.3""",

'I' : """irrelevant, labelling index for EIRENE bulk ion species IPLS, runs
from 1 to NPLS""",

'IFLB' : """<dl><dt>>0</dt>
<dd>labelling index of bulk ion species in plasma code. EIRENE bulk ion species
IPLS corresponds to plasma code species IFLB(IPLS). Hence: IFLB &le; NFLA,
otherwise: error exit.</dd>
<dd>The drift velocity vector for all EIRENE species IPLS is set identical to
the drift velocity of the plasma code species IFLB(IPLS).</dd>
<dd>Only one common ion temperature is available from B2, B2.5 code runs, even
for multi-species applications. The bulk ion temperature TIIN(IPLS,....) for
all EIRENE species IPLS, which are read from the plasma code data files, i.e.,
for all species with IFLB(IPLS) > 0</dd>
<dt><0</dt>
<dd>The plasma density, flow field and temperature field for EIRENE species
IPLS is read from the input stream fort.II, with II=-IFLB. (Currently only
II=13). This file fort.13 must be available, e.g., from a previous EIRENE run,
in which NFILEL = 1 or NFILEL = 3 options have been used to produce that file.
(see input block 1). This option permits iteration on some species, which are
not treated in the plasma code, e.g.: for neutral-neutral interactions.</dd>
<dt>=0</dt>
<dd>The corresponding bulk ion species IPLS in EIRENE has zero density, i.e.
bulk ions of this species are not present in this EIRENE run. Note the issue
re. electron density and quasi-neutrality mentioned above.</dd></dl""",

'FCTE' : """<p>bulk ion density (and flux) multiplication factor. The EIRENE
bulk ion density (and fluxes) for species IPLS are obtained by multiplying the
corresponding plasma code profiles for species IFLB(IPLS) with the factor FCTE.
This option is needed, e.g., if the plasma code treats one ion species of mass
2.5 AMU, while EIRENE treats D ions and T ions separately.</p>
<p>Note: in an iterative mode all plasma species in the plasma code should also
be in EIRENE. There may be more in EIRENE, with charge state zero (see
introduction to section 2.4), but not less, because otherwise the electron
density computed in EIRENE from quasi-neutrality (and used, e.g., for
ionization mean free paths), may be inconsis- tent with the electron density in
the plasma code.</p>""",

'BMASS' : """Mass of plasma code species IFLB(IPLS) is BMASS(IPLS) in AMU.""",

'NDXA' : """grid size in 2D plasma code. NDXA is the size of the grid
tangential to the flux surfaces, and NDYA is the size of the grid normal to the
flux surfaces.<br> These grid sizes have to be equal to the grid sizes (1st and
2nd grid RSURF and PSURF) of the mesh, on which plasma code data are specified
for EIRENE.<br> I.e., NDYA=NR1ST-1 and NDXA=NP2ND-1 must be obeyed.""",

'NDYA' : """grid size in 2D plasma code. NDXA is the size of the grid
tangential to the flux surfaces, and NDYA is the size of the grid normal to the
flux surfaces.<br> These grid sizes have to be equal to the grid sizes (1st and
2nd grid RSURF and PSURF) of the mesh, on which plasma code data are specified
for EIRENE.<br> I.e., NDYA=NR1ST-1 and NDXA=NP2ND-1 must be obeyed.""",

'NTARGI' : """Number of different surface recycling sources defined from the
plasma code sur- face effluxes at specified boundaries.""",

'NTGPRT' : """Number of different surface segments (radially or poloidally), by
which this target recycling stratum no. ITARGI is composed.""",

'NDT' : """number of surface in plasma code mesh, either in tangential or in
normal direction. If the plasma code uses cell centered indexing, then the
north and the east surfaces of a cell are labeled by the indices of the cell.
In EIRENE cell indexing, the south and the west surface have the same index as
the corresponding cell in the first (radial) and second (poloidal) mesh,
respectively. Therefore NDT may be different from the surface labelling index
in EIRENE input block 2.3.1. Note also that NDT refers to cell numbers after
index mapping, if NCUTL is not equal to NCUTB.""",

'NINCT' : """<dl>
<dt>=1</dt>
<dd>positive (i.e., outer) surface normal is in the positive co-ordinate
direction (as it is the case by default for EIRENE standard co-ordinate
surfaces).</dd>
<dt>=-1</dt>
<dd>positive surfaces normal is in the negative co-ordinate
<direction./dd>/dl>""",

'NIXY' : """<dl>
<dt>=1</dt>
<dd>surface in the direction normal to the flux surface, i.e., it belongs to
the 2nd EIRENE mesh PSURF (usually: divertor target)</dd>
<dt>=2</dt>
<dd>surface is in the tangential direction, i.e., it belongs to the 1st EIRENE
mesh RSURF (usually: vessel, liner, interface to vacuum region)</dd></dl>""",

'NTIN' : """<p>The surface source is restricted to the cells ranging from cell
number NTIN to cell number NTEN-1, along the co-ordinate surface.</p>
<p> Note that NTIN and NTEN label cell boundaries, hence the NTEN-1 above.</p>
<p> Note further: the total number of surface cells in one surface recycling
source ITARG (i.e., summed over NTGPRT(ITARG)) must not be larger then
NR1ST+NP2ND (see definition of parameter NGITT in Common Deck PARMMOD).</p>""",

'NTEN' : """<p>The surface source is restricted to the cells ranging from cell
number NTIN to cell number NTEN-1, along the co-ordinate surface.</p>
<p> Note that NTIN and NTEN label cell boundaries, hence the NTEN-1 above.</p>
<p> Note further: the total number of surface cells in one surface recycling
source ITARG (i.e., summed over NTGPRT(ITARG)) must not be larger then
NR1ST+NP2ND (see definition of parameter NGITT in Common Deck PARMMOD).</p>""",

'NIFLG' : """This corresponds to the SORIFL flag in input block 7, and is
needed only if IND- SRC=6, i.e., if the source is specified by data from block
14 alone.""",

'NPTC' : """This corresponds to the NPTS flag in input block 7, and is needed
only if IND- SRC=6, i.e., if the source is specified by data from block 14
alone.""",

'NSPZI' : """Species range for this stratum. Only the EIRENE fluids IPLS
corresponding to plasma code fluids IFL with NSPZI < IFL < NSPZE are sampled
from this stratum. See index map ILFB(IPLS) specified above in this same input
block.<br> One (geometrical) target may appear several times, with different
species ranges. This permits to apply stratified sampling within the species
distribution, and hence to remove statistical noise resulting from species
source sampling.""",

'NSPZE' : """Species range for this stratum. Only the EIRENE fluids IPLS
corresponding to plasma code fluids IFL with NSPZI < IFL < NSPZE are sampled
from this stratum. See index map ILFB(IPLS) specified above in this same input
block.<br> One (geometrical) target may appear several times, with different
species ranges. This permits to apply stratified sampling within the species
distribution, and hence to remove statistical noise resulting from species
source sampling.""",

'NEMOD' : """This corresponds to the NEMODS flag in input block 7, and is
needed only if INDSRC=6, i.e., if the source is specified by data from block 14
alone. As for NPTC, only the value from the first stratum segment is used.""",

'CHGP' : """The short cycle between EIRENE and the plasma code (i.e., only
recomputing of source term profiles in subroutine EIRSRT at each time-step, but
no new random walks) is stopped, if the total volume integrated particle source
rate has changed by more than CHGP per cent as compared to the previous full
EIRENE run.""",

'CHGEE' : """as CHGP, but for total electron energy source rate.""",
'CHGEI' : """as CHGP, but for total electron energy source rate.""",
'CHGMOM' : """as CHGP, but for total electron energy source rate.""",

'NAINB' : """total number (=NAINI) of additional plasma code tallies
transferred onto EIRENE input tally ADIN (e.g. in order to utilize EIRENE
output facilities for plasma code data, or for the options described in sub
block 10c.""",

'NAINS': """species index of tally in B2 arrays.""",

'NAINT' : """lag to determine which particular quantity is put onto input tally
ADIN(I,...).<br> In the current version of subroutine INFCOP for interfacing to
B2 the following <quot>;B2- quantities<quot>; can be selected.<br>
<em>1 &le; NAINT 1 &le; 16: </em>
<dl>
<dt>=1</dt><dd>
<dd>DI :plasma ion density [m<sup>-3</sup>], also on DIIN, by IPLS species</dd>
<dt>=2</dt>
<dd>UU :poloidal velocity [m/s]</dd>
<dt>=3</dt>
<dd>VV :radial velocity [m/s]</dd>
<dt>=6</dt>
<dd>PR :plasma pressure [N/m<sub>2</sup>]</dd>
<dt>=7</dt>
<dd>UP :parallel velocity [m/s]</dd>
<dt>=8</dt>
<dd>RR :pitch angle [1]</dd>
<dt>=9</dt>
<dd>FNIX: Particle fluxes along the field [1/s]</dd>
<dt>=10</dt>
<dd>FNIY Particle fluxes across the field [1/s]</dd>
<dt>=11</dt>
<dd>FEIX Ion energy fluxes along the field [W att]</dd>
<dt>=12</dt>
<dd>FEIY Ion energy fluxes across the field [W att]</dd>
<dt>=13</dt>
<dd>FEEX Electron energy fluxes along the field [W att]</dd>
<dt>=14</dt>
<dd>FEEY Electron energy fluxes across the field [W att]</dd>
<dt>=15</dt>
<dd>VOL: cell volume [m<sup>3</sup>]</dd>
<dt>=16</dt>
<dd>BFELD: magnitude of magnetic field [T ]</dd>
</dl>
<p>21 &le; NAINT &le; 30 : normalized EIRENE atomic/molecular data profiles
(rate co- efficients in atomic units). These can be selected also in the
NMODE=0 (subroutine INFCOP not called) option, see previous paragraph for their
description. These op- tions allow verification of selected atomic/molecular
data on the computational grid and evaluated using the plasma background data
of a particular run (in particular: check for extrapolation errors in A&amp;M
data)</p>""",

'TXTPLS' : """text for printout and plotting, same as described for additional
output tallies in bock 10.""",
'TXTPSP' : """text for printout and plotting, same as described for additional
output tallies in bock 10.""",
'TXTPUN' : """text for printout and plotting, same as described for additional
output tallies in bock 10.""",

'NAOTB' : """total number of additional EIRENE surface tallies transferred to
B2 code (e.g. in order to allow re-scaling in B2 such that total number of
particles (neutrals and ions) is conserved.""",

'NAOTS' : """not in use""",
'NAOTT' : """not in use""",

# *** 15.

'*** 15. Data for interfacing routine "geousr"': """This input block is used to
adjust the edges of the additional walls in the Eirene description of the
vacuum vessel walls to match exactly the location of the grid corners from the
plasma solver in B2.5. This block may begin with an optional text line
containing either GENERAL or BIASED GARCHING, which changes the format below.
The SOLPS-ITER default is to not include this text line. By default, the grid
corners at the targets will be adjusted to the additional surfaces specified,
and there should be one such additional surface per grid corner. Each
additional surface can only serve for one grid corner adjustment, no more.""",

'NADMOD' : """Number of additional surfaces to be modified (should be 2 per
divertor target, and 2 for a limiter geometry case)""",

'NASMOD' : """Number of standard surfaces to be modified. Should be 0 for
standard SOLPS-ITER couplings.""",

'NORMOD' : """ Number of cell faces whose normal is to inverted. Should be 0
for standard SOLPS-ITER couplings.""",

'NRS' : """Index of the additional surface being modified""",

'IPUNKT' : """ABS(IPUNKT) is the index of the vertex of that additional surface
being modified""",

'XCOOR' : """New X-coordinate of the point being modified (in cm). Not
necessary in standard SOLPS-ITER couplings.""",

'YCOOR' : """New Y-coordinate of the point being modified (in cm). Not
necessary in standard SOLPS-ITER couplings.""",

'ZCOOR' : """New Z-coordinate of the point being modified (in cm). Not
necessary in standard SOLPS-ITER couplings.""",

'XPOLPOS' : """X-index (poloidal) of the grid cell to which the additional
surface vertex must be matched""",

'YPOLPOS' : """Y-index (radial) of the grid cell to which the additional
surface vertex must be matched""",

'NAS' : """Index of the standard surface to be modified""",

'NSSIR' : """Radial position of the standard surface to be modified""",

'NSSIP' : """Poloidal position of the standard surface to be modified""",

'IDIR' : """Direction of the face whose normal is being inverted (1 = radial,
2=poloidal)""",

'IR' : """Radial index of the cell where the normal is being inverted""",

'IP' : """Poloidal index of the cell where the normal is being inverted""",


#*** OPEN MPI DISTRIBUTION

'*** INFORMATION FOR MPI' : """Choose the MPI parallelization strategy to be
applied""",

'DISTRIBUTION' : """<p>MPI parallelization strategies</p>
<dl>
<dt>BALANCED_DISTRIBUTION</dt>
<dd>A balanced strategy where the work is attempted to be divided evenly among
processors (currently the SOLPS-ITER default). If the initial setup for the
BALANCED strategy fails, the code then attempts the APCAS strategy.</dd>
<dt>APCAS_DISTRIBUTION</dt>
<dd>meaning All Processors Compute All Strata, where the work of each stratum
is divided among all processors. Usually involves more communication between
processors.</dd>
<dt>ORIGINAL_DISTRIBUTION</dt>
<dd>The original strategy implemented in versions of Eirene prior to SOLPS-ITER
version 3.0.5. In that strategy, each processor is handed either part of a
large stratum or one or several full smaller strata. This strategy works well
if the number of processors is larger than the number of strata, but is not
recommended if the number of strata is larger than the number of
processors.</dd>
<dt>AUTOMATIC_DISTRIBUTION</dt>
<dd>tells the code to use the current default, whatever it may be.</dd>
</dl>""",
}

class FFormat:
    """Class holding the species card spacing format.
    If there is a dictionary, that only means that there can be
    optional flags. [e.g. Reactions Cards]
    """
    ReactionsCard = [
        3, 6, 4, 11, 3, 3, 3, 11, 11, 11
    ]
    NeutralsAndMolecules = [
        2, 8, 2, 2, 2 ,2 ,2 ,2 ,2, 2, 2, 2, 2
    ]
    PlasmaBackground = [
        2, 9, 2, 2, 2, 2, 2, 2, 2, 2, 2
    ]

class MyValidator(QValidator):
    """This is a custom validator for the Delegator editors. Depending on the
    line contents it creates an appropriate mask.

    Attributes:
        n (int): Number of certain elements in the line
        mask (string): A regex mask for validating current line.
    """
    def __init__(self, parent=None, n=None, type=None, old_text=None):
        super(MyValidator, self).__init__(parent)
        self.old_text = old_text
        self.n = n
        if type == 'L':
            self.length = self.n + int(self.n / 5)
            self.n = self.length
            self.mask = "T|F|t|f|\s"
        elif type == 'R5':
            self.length = self.n * 12
            self.mask = "-?\d\.\d\d\d\d\dE(\+|\-)\d\d"
        elif type == 'R4':
            self.length = self.n * 10
            self.mask = "-?\d\.\d\d\d\dE(\+|\-)\d\d"
        elif type == 'I':
            self.length = self.n * 6
            self.mask = "-?[0-9]+"
        elif type == 'S':
            self.length = self.n
            self.mask = '.'
        else:
            #Reactions card...
            self.length = len(self.old_text)
            self.mask = '\S+'
        #elif type == 'RC':
        #    self.length = self.n
        #    self.mask = '.'
        #elif type == 'NC':
        #    self.length = self.n
        #    self.mask = '.'
        #...

    def fixup(self, string):
        if self.old_text:
            return self.old_text
        else:
            return string

    def validate(self, string, pos):
        """The overloaded validate function from QValidator class. Any illegal
        changes are rejected: String length changed, added/removed element,
        type changed of the element.

        First it checks if the length of the string in the editor is different
        than the predetermined length. It doesn't reject the input right away
        since the length of the string might deviate while editing but it can
        be the same at the end.

        Then the regex search is called to see if the number of elements of
        predetermined type doesn't the predetermined number.

        Finally if the previous checks are not executed, it returns that the
        change is valid.
        """
        if len(string) != self.length:
            return QValidator.Intermediate, string, pos

        search = re.findall(self.mask, string)
        if len(search) != self.n:
            return QValidator.Invalid, string, pos
        return QValidator.Acceptable, string, pos


class MyLineEdit(QLineEdit):
    """This is the custom QLineEdit for the QStyledItemDelegation. It contains
    functions that handle the help description for the current selected
    cardrole. Insert and some overloaded functions for additional cosmetics.

    Attributes:
        parameter_description (array): Contains the parameter name of the
            help_description dictionary. Whenever you click on a position in
            the editor the paramameter name is selected and then the proper
            help text selected and displayed.
        last_param (string): Last parameter selected.
        parameter_help (pyqtSignal): This is the signal that emits whenever a
            keyboard release or a mouse release event is occured.
    """
    parameter_help = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MyLineEdit, self).__init__(parent)
        self.parameter_description = []
        self.last_param = None

    def set_card_help(self, card_type, variables_name, number_of_args):
        """Setting the help description for current card. The card has multiple
        types of values, so each is handled accordingly.

        Args:
            card_ty (str): This string contains the type of the card.
            variables_name (array): This array contains the variables name at
                the current card
            number_of_args (int): This intiger contains the number of items on
                the current card. This is used for the free format or for the
                not-described cards.
        """
        if card_type is None:
            return
        self.parameter_description.append(variables_name[0])
        if card_type == 'I':
            for param_name in variables_name:
                for i in range(6):
                    self.parameter_description.append(param_name)

        elif card_type == 'L':
            i = 1
            for param_name in variables_name:
                if i % 6 == 0:
                    self.parameter_description.append(' ')
                self.parameter_description.append(param_name)
                i += 1
        elif card_type == 'R5':
            for param_name in variables_name:
                for j in range(12):
                        self.parameter_description.append(param_name)
        elif card_type == 'S':
            for param_name in variables_name:
                N = self.determine_format_of_free_type(param_name)
                N = N if N is not None else number_of_args
                for i in range(N):
                    self.parameter_description.append(param_name)
        elif card_type == 'RC':
            for i, el in enumerate(variables_name):
                for j in range(FFormat.ReactionsCard[i]):
                    self.parameter_description.append(el)
                if el != 'H123':
                    self.parameter_description.append(' ')
        elif card_type == 'CN' or card_type == 'MC' or card_type =='IC' or\
             card_type == 'PC':
            for i,el in enumerate(variables_name):
                for j in range(FFormat.NeutralsAndMolecules[i]):
                    self.parameter_description.append(el)
                self.parameter_description.append(' ')
        elif card_type == 'PB':
            for i,el in enumerate(variables_name):
                for j in range(FFormat.PlasmaBackground[i]):
                    self.parameter_description.append(el)
                self.parameter_description.append(' ')

    def focusInEvent(self, e):
        """This overloaded function causes the editor to de-highlight the curr-
        ent editor text and set the cursor position to 0.
        """
        self.deselect()
        self.setCursorPosition(0)
        return super(MyLineEdit, self).focusInEvent(e)

    def event(self, ev):
        if ev.type() == QEvent.MouseButtonRelease \
                or ev.type() == QEvent.KeyRelease:
            p = self.cursorPosition()
            if p < len(self.parameter_description):
                if self.parameter_description[p] != self.last_param:
                    self.parameter_help.emit(self.parameter_description[p])
                    self.last_param = self.parameter_description[p]

            else:
                self.parameter_help.emit('NOD')
                self.last_param = None
        return super(MyLineEdit, self).event(ev)

    def determine_format_of_free_type(self, variables):
        """ This function tries to determine the spacings in free format cards.
        Important: There is no fixed spacings for type, e.g.: integer
        can be 3 characters or up to 6 characters long, so this function should
        be used only on cards that have a mixed default type cards.
        """
        for variable in variables:
            if variable.startswith('LG') or variable.startswith('TRC') or \
               variable.startswith('NL'):
                return 1
            elif variable.startswith('C') or variable.startswith('T'):
                return None
            elif variable.startswith('I') or variable.startswith('J') or\
               variable.startswith('N'):
               return 6
            else:
                return 12


    # TODO: BACKGROUND PIXMAP FOR EDITING
    # Using paintEvent function to draw alternate columns colors to the card.
    # The format are different, as the types of the cards are:
    # Integers
    # Reals
    # Booleans
    # "quasi free" format of different types
    # Free format string

class CardEditDelegate(QStyledItemDelegate):
    """Custom QStyledItemDelegate for creating editors and help descriptions
    for card. The Delegate creates an editor and provides data for help desc-
    ription to it. It also handels the events for the help description and the
    modified event.

    Attributes:
        parameter_help (pyqtSignal): The signal responsible for help descrip-
            tion handling.
        lineEdit (QLineEdit): The editor it creates and provide the help to.
    """

    parameter_help = pyqtSignal(str)

    def __init__(self, parent=None):
        super(CardEditDelegate, self).__init__(parent)
        self.lineEdit = None

    def createEditor(self, parent, option, index):
        """The overloaded function from QStyledItemDelegate that creates a
        custom editor, handles data for help description to it and changing
        some geometrics for the editor.

        Args:
            parent (QWidget): The parent widget for the editor
            option (QQStyleOptionViewItem): The object that contains graphical
                data for painting and rendering.
            index (QModelIndex): The index object that contains the current
                location the editing line.

        Returns:
            lineEdit (QLineEdit): A custom QLineEdit that acts as the editor.
        """
        self.lineEdit = MyLineEdit(parent)
        self.lineEdit.setFrame(True)

        if index.data(Qt.UserRole):
            card_type = index.data(Qt.UserRole)[0]
            number_of_args = index.data(Qt.UserRole)[1]
            variables_name = index.data(Qt.UserRole)[2]
            self.lineEdit.set_card_help(card_type, variables_name,
                                        number_of_args)

            # if card_type:
            #     val = MyValidator(self.lineEdit, number_of_args, card_type,
            #                       index.data(Qt.DisplayRole))
            #     self.lineEdit.setValidator(val)

            self.lineEdit.parameter_help.connect(self.parameter_help)
        self.lineEdit.editingFinished.connect(self.parent().changed)

        return self.lineEdit

    def destroyEditor(self, editor, index):
        """Overloaded function from QStyledItemDelegate that sets the help
        description to 'EDIT_HELP'.

        Otherwise it is a default function that acts as the editor destroyer
        when we stop editing.
        """
        editor.parameter_help.emit('EDIT_HELP')
        super(CardEditDelegate, self).destroyEditor(editor, index)

    @pyqtSlot(str)
    def help(self, parameter):
        self.parameter_help.emit(parameter)


class MyException(Exception):
    pass

class EireneEdit(QTreeWidget):
    def __init__(self, parent=None):
        super(EireneEdit, self).__init__(parent)
        self.TextModified = False
        self.setSortingEnabled(False)
        self.headerItem().setHidden(True)
        self.setColumnWidth(0, 32)
        font = QFont()
        font.setFamily('Monospace')
        font.setPixelSize(12)
        self.setFont(font)
        self.setAlternatingRowColors(True)
        self.card_edit_delegate = CardEditDelegate(self)
        self.setItemDelegate(self.card_edit_delegate)
        self.setCurrentIndex(self.model().index(0, 0))
        self.values = {}
        self.currentLine = ''
        self.blocks = [self.block_1, self.block_2, self.block_3a,
                       self.block_3b, self.block_4, self.block_5, self.block_6,
                       self.block_7, self.block_8, self.block_9, self.block_10,
                       self.block_11, self.block_12, self.block_13,
                       self.block_14, self.block_15, self.block_16]
        self.number_of_blocks = len(self.blocks)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setIndentation(20)

    def setPlainText(self, text):
        """This function sets the text from the input configuration file for
        EIRENE into the tree. The way it works is that we have block functions
        and dummy block functions.

        The block functions have the predetermined help description parameters
        set to lines of the input file. The block functions are written in a
        way that if there is a pattern in the input file, the work needed
        to add more help description parameters should be easy.
        """
        self.old_text = text
        self.text = text.splitlines()
        self.text_size = len(self.text)
        self.row = 0
        self.clear()
        self.curr_par = self.grup_par =self
        self.successful_reading = 1
        # Initiator
        try:
            self.dummy_block()
        except MyException as e:
            pass
        except IndexError as e:
            pass
        for i in range(self.number_of_blocks):
            try:
                self.blocks[i]()
            except MyException as e:
                # New Block
                continue
            except Exception as e:
                if type(e) != IndexError:
                    print('Block: ', i + 1)
                    print('Line: ', self.currentLine)
                    print('Error type:', type(e))
                    print('Error:', e)
                    self.successful_reading = 0

            try:
                self.dummy_block()
            except IndexError as e:
                pass
        self.setCurrentItem(self.topLevelItem(0))

    def looks_like_boolean_card(self, line):
        """ A check function that accepts a string and then determine if the
        string is composed of booleans. Usually is enough only to check if
        the string 'F' or 'T' are in the line.

        Example:
            'FTTTF FTTFF T' - is a boolean card
            '     2     1'  - is not a boolean card

        Args:
            line [str]: A line from the input file
        Returns:
            bool: A boolean saying if the string is indeed composed only of
                booleans.
        """
        return any([c in line for c in 'fFtT'])

    def block_1(self):
        """Function for setting help desc. parameters for block 1:
        *** 1. Data for operating mode
        """
        self.getline(['I', 'NMACH', 'NMODE', 'NTCPU', 'NFILE', 'NITER0',
                      'NITER', 'NTIME0', 'NTIME', 'DUMMY'])

        line = self.getline()
        if not self.looks_like_boolean_card(line):
            role = ['I', 'NOPTIM', 'NOPTM1', 'NGEOM_USR', 'NCOUP_INPUT',
                    'NSMSTRA', 'NSTORAM', 'NGSTAL', 'NRTAL', 'NREAC_ADD']
            self.getline(role)

        role = ['L', 'NLSCL', 'NLTEST', 'NLANA', 'NLDRFT', 'NLCRR', 'NLERG',
                     'NLIDENT', 'NLONE', 'NLMOVIE', 'NLDFST', 'NLOLDRAN',
                     'NLCASCAD', 'NLOCTREE', 'NLWRMSH', 'NEXVS', 'NLTRIMESH']
        self.getline(role)
        # Arbitrary lines
        line = self.getline()
        while line[:3] != '***':
            if 'CFILE' in line:
                self.getline(['S', 'CFILE'])
            else:
                self.getline(['S', 'NOD'])
            line = self.getline()

    def block_2(self):
        """Function for setting help desc. parameters for block 2:
        *** 2. Data for standard mesh
        """

        self.getline(['I', 'INGRD(1)', 'INGRD(2)', 'INGRD(3)'])
        self.getline(['L', 'NLRAD'])
        if self.values['NLRAD']:
            self.getline(['L', 'NLSLB', 'NLCRC', 'NLELL', 'NLTRI',
                               'NLPLG', 'NLFEM', 'NLTET', 'NLGEN'])

            self.getline(['I', 'NR1ST', 'NRSEP', 'NRPLG', 'NPPLG', 'NRKNOT',
                               'NCOOR'])

            if self.values['INGRD(1)'] <= 5:

                if self.values['NLSLB'] or self.values['NLCRC'] or \
                   self.values['NLELL'] or self.values['NLTRI']:
                    self.getline(['R5', 'RIA', 'RGA', 'RAA', 'RRA'])

                    if self.values['NLELL'] or self.values['NLTRI']:
                        self.getline(['R5', 'ER1IN', 'EP1OT', 'EP1CH', 'EXEP1'])
                        self.getline(['R5', 'ELLIN', 'ELLOT', 'ELLCH', 'EXELL'])
                        if self.values['NLTRI']:
                            self.getline(['R5', 'TRIIN', 'TRIOT', 'TRICH',
                                               'EXTRI'])

                    elif self.values['NLPLG']:
                        self.getline(['R5', 'XPCOR', 'YPCOR', 'ZPCOR',
                                      'PLREFL'])
                        role = ['R5']
                        for k in range(1, self.values['NPPLG'] + 1):
                            role.append('NPOINT(1,' + str(k) + ')')
                            role.append('NPOINT(2,' + str(k) + ')')
                        if len(role) >= 1:
                            self.getline(role)

                        for i in range(1, self.values['NR1ST'] + 1):
                            role = ['R5']
                            for j in range(1, self.values['NRPLG'] + 1):
                                role.append('XPOL(' + str(self.counter) + ',' +
                                            str(j) + ')')
                                role.append('YPOL(' + str(self.counter) + ',' +
                                            str(j) + ')')
                            if len(role) > 1:
                                self.getline(role)
                    elif self.values['NLFEM'] or self.values['NLTET']:
                        self.getline(['R5', 'XPCOR', 'YPCOR', 'ZPCOR'])

            elif self.values['INGRD(1)'] == 6:
                if self.values['NLSLB'] or self.values['NLCRC'] or \
                   self.values['NLELL'] or self.values['NLTRI']:
                    self.getline(['R5', 'RIA', 'RGA', 'RAA'])
                elif self.values['NLPLG'] or self.values['NLFEM'] or\
                self.values['NLTET']:
                    self.getline(['R5', 'XPCOR', 'YPCOR', 'ZPCOR'])

        self.getline(['L', 'NLPOL'])
        self.getline(['L', 'NLPLY', 'NLPLA', 'NLPLP'])
        self.getline(['I', 'NP2ND', 'NPSEP', 'NPPLA', 'NPPER'])
        if self.values['INGRD(2)'] < 5:
            self.getline(['R5', 'YIA', 'YGA', 'YAA', 'YYA'])

        self.getline(['L', 'NLTOR'])
        self.getline(['L', 'NLTRZ', 'NLTRA', 'NLTRT'])
        self.getline(['I', 'NT3RD', 'NTSEP', 'NTTRA', 'NTPER'])
        if self.values['INGRD(3)'] < 5:
            self.getline(['R5', 'ZIA', 'ZGA', 'ZAA', 'ZZA', 'ROA'])

        self.getline(['L', 'NLMLT'])
        # Sometimes even though NLMLt is false the next line can still
        # be NBLMT, an integer.

        line = self.getline()
        if line.split()[0].isdigit():
            self.getline(['I', 'NBLMT'])

        if self.values['NLMLT']:
            role = ['R5']
            for i in range(1, self.values['NBLMT'] + 1):
                role.append('VOLCOR(i)')
            self.getline(role)
        # 2e. Data for additional cells outside standard mesh
        self.getline(['L', 'NLADD'])
        self.getline(['I', 'NRADD'])
        role = ['R5']
        for i in range(1, int(self.values['NRADD']) + 1):
            role.append('VOLADD(i)')
        if len(role) != 1:
            self.getline(role)

    def block_3a(self):
        """Function for setting help desc. parameters for block 3a:
        *** 3a. Data for non default standard surfaces
        """
        self.getline(['I', 'NSTSI'])

        for i in range(self.values['NSTSI']):
            self.getline(['I', 'TXTSFL', 'ISTS', 'IDIMP', 'INUMP',
                               'IRPTA', 'IRPTE', 'IRPTA', 'IRPTA', 'IRPTE'])
            self.getline(['I', 'ILIIN', 'ILSIDE', 'ILSWCH', 'ILEQUI', 'ILCOL',
                               'ILFIT', 'ILCELL', 'ILBOX', 'ILPLG'])
            line = self.getline()
            if 'SURFMOD' in line:
                self.getline(['S', 'SURFMOD_MODNAME'])
            elif line[:1] == '*':
                pass
            elif self.values['ILIIN'] > 0:
                # Optional
                self.getline(['I', 'ILREF', 'ILSPT', 'ISRS', 'ISRC'])
                self.getline(['R5', 'ZNML', 'EWALL', 'EWBIN', 'TRANSP(1,N)',
                                   'TRANSP(2,N)', 'FSHEAT'])
                self.getline(['R5', 'RECYCF', 'RECYCT', 'RECPRM', 'EXPPL',
                              'EXPEL', 'EXPIL'])
                self.getline(['R5', 'RECYCS', 'RECYCC', 'SPTRM', 'ESPUTS',
                              'ESPUTC'])

    def block_3b(self):
        """Function for setting help desc. parameters for block 3b:
        *** 3b. Data for additional surfaces

        For this block there is a problem in certain cases: when real RLBND
        parameter is negative, I have found no way to determine the -KL ine-
        qualities.

        L is the linear inequality.
        K is the second order inequality.

        """
        self.getline(['I', 'NLIMI'])
        line = self.getline()
        while 'CH' in line:
            self.getline(['S', 'CH-card'])
            line = self.getline()
        for i in range(self.values['NLIMI']):
            self.getline(['R5', 'RLBND', 'RLARE', 'RLWMN', 'RLWMX'])
            self.getline(['I', 'ILIIN', 'ILSIDE', 'ILSWCH', 'ILEQUI', 'ILTOR',
                          'ILCOL', 'ILFIT', 'ILCELL', 'ILBOX', 'ILPLG'])

            if self.values['RLBND'] < 2:
                self.getline(['R5', 'A0LM', 'A1LM', 'A2LM', 'A3LM', 'A4LM',
                              'A5LM', 'A6LM', 'A7LM', 'A8LM', 'A9LM'])
                if self.values['RLBND'] > 0:
                    self.getline(['R5', 'XLIMS1', 'YLIMS1', 'ZLIMS1',
                                  'XLIMS2', 'YLIMS2', 'ZLIMS2'])
            elif self.values['RLBND'] >= 2:
                self.getline(['R5', 'P1(1,..)', 'P1(2,..)', 'P1(3,..)',
                             'P2(1,..)', 'P2(2,..)', 'P2(3,..)'])

                # Cannot determine K!
            line = self.getline()
            if self.values['ILIIN'] > 0 and line.split()[0].isdigit():
                #Optional!
                self.getline(['I', 'ILREF', 'ILSPT', 'ISRS', 'ISRC'])
                self.getline(['R5', 'ZNML', 'EWALL', 'EWBIN', 'TRANSP(1,N)',
                                   'TRANSP(2,N)', 'FSHEAT'])
                self.getline(['R5', 'RECYCF', 'RECYCT', 'RECPRM', 'EXPPL',
                              'EXPEL', 'EXPIL'])
                self.getline(['R5', 'RECYCS', 'RECYCC', 'SPTRM', 'ESPUTS',
                              'ESPUTC'])
                line = self.getline()
            if 'SU' in line:
                self.getline(['S', 'SURFMOD_MODNAME'])

    def block_4(self):
        line = self.getline()
        if line.startswith('INCLUDE'):
            # Omit the next functions
            return
        #  Reactions
        self.getline(['I', 'NREACI'])

        role = ['RC', 'IR', 'FILNAM', 'H123']
        optional = ['FTFLAG']
        tail = ['REAC', 'CRC', 'MASSP', 'MASST', 'DP', 'RMN1', 'RMX1']
        while 1:

            # Reactions card:
            # IR FILNAME H123 FTFLAG CRC MASST DP RMN1 RMNX
            # at least one space between the flags
            flags = self.getline().split()
            IR = int(flags[0])
            FILNAM = flags[1]
            if flags[3].startswith('FT'):
                tail = optional + tail

            self.getline(role + tail[:len(flags[3:])]) # Assigning role to the card

            # Checking if there are additional sub-cards
            if FILNAM == 'ADAS':
                self.getline(['S', 'ELNAME', 'IZ'])
            elif FILNAM =='PHOTON':
                line = self.getline()
                self.getline(['S', 'IPRFTYPE', 'IPLSC3', 'IMESS', 'IFREMD',
                                   'NRJPRT'])
                for j in range(int(line.split()[3])):
                    self.getline(['S', 'II', 'KENN', 'IK6']) # This should be
                                                             # checked
            elif FILNAM == 'CONST':
                # 12 Numbers in two lines, but only
                self.getline(['R4', 'F1', 'F2', 'F3', 'F4', 'F5'])
                self.getline(['R4', 'F6', 'F7', 'F8'])

            N = len(flags)
            # Awkward way of seeing if there are additional lines when
            # RMN1 .gt. 0 nd RMX1 .g. 0
            if N >= 9:
                if float(flags[8]) > 0:
                    self.getline(['S', 'IFEXMN', 'FPARM(1)', 'FPARM(2)',
                                       'FPARM(3)'])
            if N == 10:
                if float(flags[9]) > 0:
                    self.getline(['S', 'IFEXMN', 'FPARM(4)', 'FPARM(5)',
                                       'FPARM(6)'])
            if IR == self.values['NREACI']:
                break
        # **4a.   Neutral atom species
        self.getline(['I', 'NATMI'])
        for j in range(self.values['NATMI']):
            # The first line contains
            # NC type is NEUTRAL ATOMS SPECIES CARDS
            line = self.getline().split()
            self.getline(['NC', 'I', 'TEXTS(ISPZ)', 'NMASSA(IATM)',
                          'NCHARA(IATM)', 'NDUMM1', 'NDUMM2', 'ISRF(ISPZ,1)',
                          'ISRT(ISPZ,1)', 'NUMSEC', 'NRCA(IATM)',
                          'NFOLA(IATM)', 'NGENA(IATM)', 'NHSTS(ISPZ)'])
            NRCA_IATM = int(line[9])
            NUMSEC = int(line[8])
            for i in range(NRCA_IATM):
                if NUMSEC < 3:
                    self.getline(['I', 'IREACA(IATM,K)', 'IBULKA(IATM,K)',
                                  'ISCD1A(IATM,K)', 'ISCD2A(IATM,K',
                                  'ISCDEA(IATM,K)', 'IESTMA(IATM,K)',
                                  'IBKA(IATM,K)'])
                elif NUMSEC == 3:
                    self.getline(['I', 'IREACA(IATM,K)', 'IBULKA(IATM,K)',
                                  'ISCD1A(IATM,K)', 'ISCD2A(IATM,K)',
                                  'ISCD3A(IATM,K)', 'ISCDEA(IATM,K)',
                                  'IEASTMA(IATM,K)', 'IBGKA(IATM,K)'])
                elif NUMSEC == 4:
                    self.getline(['I', 'IREACA(IATM,K)', 'IBULKA(IATM,K)',
                                  'ISCD1A(IATM,K)', 'ISCD2A(IATM,K)',
                                  'ISCD3A(IATM,K)', 'ISCD4A(IATM,K)',
                                  'ISCDEA(IATM,K)', 'IESTMA(IATM,K)',
                                  'IBGKA(IATM,K)'])
                # Reading mandatory line containing EELEC, EBULKA,...

                self.getline(['R5', 'EELECA(IATM,K)', 'EBULKA(IATM,K)',
                              'ESCD1A(IATM,K)', 'ESCD2A', 'FREACA(IATM,K)',
                              'FLDLMA(IATM,K)'])

        # **4b.   Neutral molecule species
        self.getline(['I', 'NMOLI'])

        for j in range(self.values['NMOLI']):
            line = self.getline().split()
            self.getline(['MC', 'I', 'TEXTS(ISPZ)', 'NMASSM(IMOL)',
                          'NCHARM(IMOL)', 'NPRT(ISPZ)', 'NDUMM',
                          'ISRF(ISPZ,1)', 'ISRT(ISPZ,1)', 'NUMSEC',
                          'NRCM(IMOL)', 'NFOLM(IMOL)', 'NGENM(IMOL)',
                          'NHSTS(ISPC)', 'lkindm(imol)'])

            NRCM_IMOL = int(line[9])
            NUMSEC = int(line[8])
            for i in range(NRCM_IMOL):
                if NUMSEC < 3:
                    # Some cards have less than 7 integers
                    self.getline(['I', 'IREACM(IMOL,K)', 'IBULKM(IMOL,K)',
                                  'ISCD1M(IMOL,K)', 'ISCD2M(IMOL,K)',
                                  'ISCDEM(IMOL,K)', 'IESTMM(IMOL,K)',
                                  'IBGKM(IMOL,K)'])
                elif NUMSEC == 3:
                    self.getline(['I', 'IREACM(IMOL,K)', 'IBULKM(IMOL,K)',
                                  'ISCD1M(IMOL,K)', 'ISCD2M(IMOL,K)',
                                  'ICSD3M(IMOL,K)',
                                  'ISCDEM(IMOL,K)', 'IESTMM(IMOL,K)',
                                  'IBGKM(IMOL,K)'])
                elif NUMSEC == 4:
                     self.getline(['I', 'IREACM(IMOL,K)', 'IBULKM(IMOL,K)',
                                  'ISCD1M(IMOL,K)', 'ISCD2M(IMOL,K)',
                                  'ICSD3M(IMOL,K)', 'ISCD4M(IMOL,K)',
                                  'ISCDEM(IMOL,K)', 'IESTMM(IMOL,K)',
                                  'IBGKM(IMOL,K)'])
                self.getline(['R5', 'EELECM(IMOL,K)', 'EBULKM(IMOL,K)',
                              'ESCD1M(IMOL,K)', 'ESCD2M, FREACM(IMOL,K)'])

        # **4c.   Test ion species
        self.getline(['I', 'NIONI'])
        for j in range(self.values['NIONI']):
            # Reading first line... yet again
            line = self.getline().split()
            self.getline(['IC', 'I', 'TEXTS(ISPZ)', 'NMASSI(ION)',
                          'NCHARI(IION)', 'NPRT(ISPZ)', 'NCHRGI(IION)',
                          'ISRF(ISPZ,1)', 'ISRT(ISPZ,1)', 'NUMSEC',
                          'NRCI(IION)', 'NFOLI(IION)', 'NGENI(IION)',
                          'NHSTS(ISPZ)', 'lkindi(iion)'])
            NRCI_IION = int(line[9])
            NUMSEC = int(line[8])
            for i in range(NRCI_IION):
                # Number of arguments on the following lines may not be the
                # same as the number of switches...
                if NUMSEC < 3:
                    self.getline(['I', 'IREACI(IION,K)', 'IBULKI(IION,K)',
                                  'ISC1I(IION,K)', 'ISCD2I(IION,K)',
                                  'ISCDEI(IION,K)', 'IESTMI(IION,K)',
                                  'IBGKI(IION,K)'])
                elif NUMSEC == 3:
                    self.getline(['I', 'IREACI(IION,K)', 'IBULKI(IION,K)',
                                  'ISC1I(IION,K)', 'ISCD2I(IION,K)',
                                  'ISCD3I(IION,K)',
                                  'ISCDEI(IION,K)', 'IESTMI(IION,K)',
                                  'IBGKI(IION,K)'])
                elif NUMSEC == 4:
                    self.getline(['I', 'IREACI(IION,K)', 'IBULKI(IION,K)',
                                  'ISC1I(IION,K)', 'ISCD2I(IION,K)',
                                  'ISCD3I(IION,K)', 'ISCD4I(IION,K)',
                                  'ISCDEI(IION,K)', 'IESTMI(IION,K)',
                                  'IBGKI(IION,K)'])
                self.getline(['R5', 'EELECI(IION,K)', 'EBULKI(IION,K)',
                              'ESCD1I(IION,K)', 'ESCD2I', 'FREACI(IION,K)'])

        # **4d. Photon species

        if self.getline()[:3] == '***':
            self.values['NPHOTI'] = 0
            return
        else:
            self.getline(['I', 'NPHOTI'])
            for j in range(self.values['NPHOTI']):
                line = self.getline().split()
                self.getline(['PC', 'I', 'TEXTS(ISPZ)', 'NDUMM1', 'NDUMM2',
                              'NDUMM3', 'NDUMM4', 'ISRF(ISPZ,1)',
                              'ISRT(ISPZ,1)', 'NUMSEC', 'NRCPH(IPHOT)',
                              'NFOLPH(IPHOT)', 'NGENPH(IPHOT)', 'NHSTS(ISPZ)'])
                NUMSEC = int(line[8])
                NRCPH_IPHOT = int(line[9])

                for i in range(NRCPH_IPHOT):
                    if NUMSEC < 3:
                        self.getline(['I', 'IREACPH(IPHOT,K)',
                                      'IBULKPH(IPHOT,K)', 'ISCD1PH(IPHOT,K)',
                                      'ISCD2PH(IPHOT,K)',
                                      'ISCDEPH(IPHOT,K)', 'IESTMPH(IPHOT,K)',
                                      'IBGKPH(IPHOT,K)'])
                    if NUMSEC == 3:
                        self.getline(['I', 'IREACPH(IPHOT,K)',
                                      'IBULKPH(IPHOT,K)', 'ISCD1PH(IPHOT,K)',
                                      'ISCD2PH(IPHOT,K)', 'ISCD3PH(IPHOT,K)',
                                      'ISCDEPH(IPHOT,K)', 'IESTMPH(IPHOT,K)',
                                      'IBGKPH(IPHOT,K)'])
                    if NUMSEC == 4:
                        self.getline(['I', 'IREACPH(IPHOT,K)',
                                      'IBULKPH(IPHOT,K)', 'ISCD1PH(IPHOT,K)',
                                      'ISCD2PH(IPHOT,K)', 'ISCD3PH(IPHOT,K)',
                                      'ISCD4PH(IPHOT,K)',
                                      'ISCDEPH(IPHOT,K)', 'IESTMPH(IPHOT,K)',
                                      'IBGKPH(IPHOT,K)'])
                    self.getline(['R5', 'EELECPH(IPHOT,K)', 'EBULKPH(IPHOT,K)',
                                  'ESCD1PH(IPHOT,K)', 'ESCD2PH',
                                  'FREACPH(IPHOT,K)', 'FLDLMPH(IPHOT,K)'])

    def block_5(self):
        self.getline(['I', 'NPLSI'])
        for i in range(self.values['NPLSI']):
            line = self.getline().split()
            self.getline(['PB', 'I', 'TEXTS(ISPZ)', 'NMASSP(IPLS)',
                           'NCHARP(IPLS)', 'NPRT(ISPZ)', 'NCHRGP(IPLS)',
                           'ISRF(ISPZ,1)', 'ISRT(ISPZ,1)', 'NUMSEC',
                           'NRCP(IPLS)', 'NDUMM1', 'NDUMM2', 'NHSTS(ISPZ)',
                           'NDUMM4', 'CDENMODEL(IPLS)', 'NRE'])
            NRCP_IPLS = int(line[9])
            NUMSEC = int(line[8])

            for j in range(NRCP_IPLS):
                if NUMSEC < 3:
                    self.getline(['I', 'IREACP(IPLS,K)', 'IBULKP(IPLS,K)',
                                  'ISCD1P(IPLS,K)', 'ISCD2P(IPLS,K)',
                                  'ISCDEP(IPLS,K)'])
                elif NUMSEC == 3:
                    self.getline(['I', 'IREACP(IPLS,K)', 'IBULKP(IPLS,K)',
                                  'ISCD1P(IPLS,K)', 'ISCD2P(IPLS,K)',
                                  'ISCD3P(IPLS,K)', 'ISCDEP(IPLS,K)'])
                elif NUMSEC == 4:
                    self.getline(['I', 'IREACP(IPLS,K)', 'IBULKP(IPLS,K)',
                                  'ISCD1P(IPLS,K)', 'ISCD2P(IPLS,K)',
                                  'ISCD3P(IPLS,K)', 'ISCD4P(IPLS,K)',
                                  'ISCDEP(IPLS,K)'])
                self.getline(['R5', 'EELECP(IPLS,K)', 'EBULKP(IPLS,K)',
                              'ESCD1P(IPLS,K)', 'ESCD2P', 'FREACP(IPLS,K)'])

        line = self.getline()
        while not line.startswith('**'):
            self.getline(['S', 'Plasma species card'])
            line = self.getline()

        # ** 5b. Plasma background data
        self.getline(['I'] + ['INDPRO(' + str(i) +')' for i in range(1, 13)])

        if self.values['INDPRO(1)'] <= 5:
            self.getline(['R5', 'TE0', 'TE1', 'TE2', 'TE3', 'TE4', 'TE5'])
        elif self.values['INDPRO(2)'] <= 5:
            for i in range(1, self.values['NPLSI'] + 1):
                self.getline(['R5', 'TI0(i)', 'TI1(' + str(i) +')',
                              'TI2(i)', 'TI3(i)',
                              'TI4(i)', 'TI5(i)'])
        elif self.values['INDPRO(3)'] <= 5:
            for i in range(1, self.values['NPLSI'] + 1):
                self.getline(['R5', 'DI0(i)', 'DI1(' + str(i) +')',
                              'DI2(i)', 'DI3(i)',
                              'DI4(i)', 'DI5(i)'])
        elif self.values['INDPRO(4)'] <= 5:
            for i in range(1, self.values['NPLSI'] + 1):
                self.getline(['R5', 'VX0(i)', 'VX1(' + str(i) +')',
                              'VX2(i)', 'VX3(i)',
                              'VX4(i)', 'VX5(i)'])
            for i in range(1, self.values['NPLSI'] + 1):
                self.getline(['R5', 'VY0(i)', 'VY1(' + str(i) +')',
                              'VY2(i)', 'VY3(i)',
                              'VY4(i)', 'VY5(i)'])
            for i in range(1, self.values['NPLSI'] + 1):
                self.getline(['R5', 'VZ0(i)', 'VZ1(' + str(i) +')',
                              'VZ2(i)', 'VZ3(i)',
                              'VZ4(i)', 'VZ5(i)'])
        elif self.values['INDPRO(5)'] <= 5:
            self.getline(['R5', 'B0', 'B1', 'B2', 'B3', 'B4', 'B5'])
        elif self.values['INDPRO(12)'] <= 5:
            self.getline(['R5', 'VL0', 'VL1', 'VL2', 'VL3', 'VL4', 'VL5'])

    def block_6(self):
        self.getline(['L', 'NLTRIM'])
        self.getline(['S', 'A_on_B'])
        line = self.getline()
        while '_' in line:
            self.getline(['S', 'A_on_B'])
            line = self.getline()
        while 'path' in line or 'PATH' in line:
            self.getline(['S', 'PATH CARD'])

        # The switches NATMI, NMOLI, NIONI, NPLSI can be greater than 6,
        # which means that the real numbers will go to the next line
        NATMI = self.values['NATMI']
        N_NATMI = NATMI // 6
        R_NATMI = NATMI % 6
        CARD_TYPE = ['DATD(i)' for i in range(6)]
        for i in range(N_NATMI):
            self.getline(['R5'] + CARD_TYPE)
        if R_NATMI:
            self.getline(['R5'] + ['DATD(i)' for i in range(R_NATMI)])

        NMOLI = self.values['NMOLI']
        N_NMOLI = NMOLI // 6
        R_NMOLI = NMOLI % 6
        CARD_TYPE = ['DMLD(i)' for i in range(6)]
        for i in range(N_NMOLI):
            self.getline(['R5'] + CARD_TYPE)
        if R_NMOLI:
            self.getline(['R5'] + ['DMLD(i)' for i in range(R_NMOLI)])

        NIONI = self.values['NIONI']
        N_NIONI = NIONI // 6
        R_NIONI = NIONI % 6
        CARD_TYPE = ['DIODI(i)' for i in range(6)]
        for i in range(N_NIONI):
            self.getline(['R5'] + CARD_TYPE)
        if R_NIONI:
            self.getline(['R5'] + ['DIOD(i)' for i in range(R_NIONI)])

        NPLSI = self.values['NPLSI']
        N_NPLSI = NPLSI // 6
        R_NPLSI = NPLSI % 6
        CARD_TYPE = ['DPLD(i)' for i in range(6)]
        for i in range(N_NPLSI):
            self.getline(['R5'] + CARD_TYPE)
        if R_NPLSI:
            self.getline(['R5'] + ['DPLD(i)' for i in range(R_NPLSI)])

        if self.values['NPHOTI'] > 0:
            self.getline(['R5'] + ['DPHT(i)' for i in
                 range(1, self.values['NPLSI'] + 1)])
        self.getline(['R5', 'ERMIN', 'ERCUT', 'RPROB0', 'RINTEG', 'EINTEG',
                      'AINTEG'])

        line = self.getline()
        while line[:3] != '***':
            self.getline(['S', 'SURFMOD'])
            self.getline(['I', 'ILREF', 'ILSPT', 'ISRS', 'ISRC'])
            self.getline(['R5', 'ZNML', 'EWALL', 'EWBIN', 'TRANSP(1,N)',
                          'TRANSP(2,N)', 'FSHEAT'])
            self.getline(['R5', 'RECYCF', 'RECYCT', 'RECPRM', 'EXPPL', 'EXPEL',
                          'EXPIL'])
            self.getline(['R5', 'RECYCS', 'RECYCC', 'SPTPRM', 'ESPUTS',
                          'ESPUTC'])
            line = self.getline()

    def block_7(self):
        self.getline(['I', 'NSTRAI'])
        self.getline(['I'] + ['INDSRC('+str(i)+')' for i in
                     range(1, self.values['NSTRAI'] + 1)])
        self.getline(['R5', 'ALLOC', 'AMPTS'])

        for i in range(1, self.values['NSTRAI'] + 1):
            INDSRC = self.values['INDSRC(%d)' % (i)]
            if INDSRC == 6:
                continue
            # If indsrc[i] == 6 then skip reading the currant strai and go to
            # the next one
            line = self.getline()
            self.row += 1
            self.curr_par = self.createItem(self.grup_par,
                                            line, ['S', 'TXTSOU'])

            self.getline(['L', 'NLAVRP', 'NLAVRT', 'NLSYMP', 'NLSYMT'])
            self.getline(['I', 'NPTS', 'NINITL', 'NEMODS', 'NAMODS',
                          'NMINPTS'])
            self.getline(['S', 'Plasma properties. Section 2.7'])
            self.getline(['L', 'NLATM', 'NLMOL', 'NLION', 'NLPLS', 'NLPHOT'])
            self.getline(['I', 'NSPEZ'])
            self.getline(['L', 'NLPNT', 'NLLNE', 'NLSRF', 'NLVOL', 'NLCNS'])
            self.getline(['I', 'NSRFSI'])
            for i in range(1, self.values['NSRFSI'] + 1):
                self.getline(['I', 'INUM', 'INDIM', 'INSOR', 'INGRDA(1)',
                              'INGRDE(1)', 'INGRDA(2)', 'INGRDE(2)',
                              'INGRDA(3)', 'INGRDE(3)'])
                self.getline(['R5', 'SORWGT', 'SORLIM', 'SORIND',
                              'SOREXP', 'SORIFL'])
                self.getline(['I', 'NRSOR', 'NPSOR', 'NTSOR', 'NBSOR',
                              'NASOR', 'NISOR'])
                self.getline(['R5', 'SORAD1', 'SORAD2', 'SORAD3', 'SORAD4',
                              'SORAD5', 'SORAD6'])
                self.getline(['R5', 'SORENI', 'SORENE', 'SORVDX', 'SORVDY',
                              'SORVDZ'])
                self.getline(['R5', 'SORCOS', 'SORMAX', 'SORCTX', 'SORCTY',
                              'SORCTZ'])

    def block_8(self):
        self.getline(['I', 'NZADD'])
        for i in range(1, self.values['NZADD'] + 1):
            self.getline(['I', 'INI', 'INE'])

    def block_9(self):
        role = ['L']
        role += ['NLPRCA('+str(i)+')' for i in range(self.values['NATMI'])]
        role += ['NLPRCM('+str(i)+')' for i in range(self.values['NMOLI'])]
        role += ['NLPRCI('+str(i)+')' for i in range(self.values['NIONI'])]
        role += ['NLPRCPH('+str(i)+')' for i in range(self.values['NPHOTI'])]
        self.getline(role)
        self.getline(['I', 'NPRCSF'])
        self.getline(['I', 'MAXLEV', 'MAXRAD', 'MAXPOL', 'MAXTOR', 'MAXADD'])
        for i in range(1, self.values['MAXLEV'] + 1):
            self.getline(['R5', 'ID', 'NSSPL(i)', 'PRMSPL(' +
                          str(i) + ')'])
        for i in range(1, self.values['MAXPOL'] + 1):
            self.getline(['R5', 'ID', 'NSSPL(' + str(self.values['N1ST'] + i) +
                         ')', 'PRMSPL(' + str(self.values['N1ST'] + i) + ')'])
        for i in range(1, self.values['MAXTOR'] + 1):
            self.getline(['R5', 'ID', 'NSSPL(' + str(self.values['N1ST'] +
                          self.values['N2ST'] + i) + ')',
                          'PRMSPL(' + str(self.values['N1ST'] +
                                          self.values['N1ST'] + i) + ')'])
        for i in range(1, self.values['MAXADD'] + 1):
            self.getline(['R5', 'ID', 'NSSPL(' + str(self.values['N1ST'] +
                                                    self.values['N2ND'] +
                                                    self.values['N3RD'] + i) +
                               ')',
                          'PRMSPL(' + str(self.values['N1ST'] +
                                          self.values['N1ST'] +
                                          self.values['N3RD'] + i) + ')'])
        self.getline(['R5', 'WMINV', 'WMINS', 'WMINC', 'WMINL'])
        self.getline(['R5', 'SPLPAR'])
        self.getline(['I', 'NSIGVI', 'NSIGSI', 'NSIGCI', 'NSIGI_BGK',
                      'NSIGI_COP', 'NSIGI_SPC'])
        for i in range(1, self.values['NSIGVI'] + 1):
            self.getline(['R5', 'IGH', 'IIH'])
        for i in range(1, self.values['NSIGSI'] + 1):
            self.getline(['R5', 'IGHW', 'IIHW'])
        for i in range(1, self.values['NSIGCI'] + 1):
            self.getline(['R5'] + ['IGHC(1,i)',
                                  'IIHC(1,i)',
                                  'IGHC(2,i)',
                                  'IIHC(2,i)'])

    def block_10(self):
        self.getline(['I', 'NADVI', 'NCLVI', 'NALVI', 'NADSI', 'NALSI',
                      'NADSPC'])
        line = self.getline()
        self.row += 1
        self.curr_par = self.createItem(self.grup_par,
                                        line, ['S', 'Tracklength estimator'])

        for i in range(1, self.values['NADVI'] + 1):
            self.getline(['I', 'IADVE', 'IADVS', 'IADVT', 'IADVR'])
            self.getline(['S', 'TXTTAL'])
            self.getline(['S', 'TXTSPC', 'TXTUNT'])

        line = self.getline()
        self.row += 1
        self.curr_par = self.createItem(self.grup_par,
                                        line, ['S', 'Collisional estimator'])

        for i in range(1, self.values['NCLVI'] + 1):
            self.getline(['I', 'ICLVE', 'ICLVS', 'ICLVT', 'ICLRC'])
            self.getline(['S', 'TXTTAL'])
            self.getline(['S', 'TXTSPC', 'TXTUNT'])
        line = self.getline()
        self.row += 1
        self.curr_par = self.createItem(self.grup_par,
                                        line, ['S', 'Algebraic expressions'])

        for i in range(1, self.values['NALVI'] + 1):
            self.getline(['S', 'ALSTRNG'])
            self.getline(['S', 'TXTTAL'])
            self.getline(['S', 'TXTSPC', 'TXTUNT'])

        line = self.getline()
        self.row += 1
        self.curr_par = self.createItem(self.grup_par,
                                        line, ['S',
                                        'Additional surface tallies'])

        for i in range(1, self.values['NADSI'] + 1):
            self.getline(['I', 'IADSE','IADSS', 'IADST', 'IADSR'])
            self.getline(['S', 'TXTTAL'])
            self.getline(['S', 'TXTSPC', 'TXTUNT'])

        line = self.getline()
        self.row += 1
        self.curr_par = self.createItem(self.grup_par,
                                        line, ['S', 'Tracklength estimator'])

        for i in range(1, self.values['NALSI'] + 1):
            self.getline(['S', 'ALSTRNG'])
            self.getline(['S', 'TXTTAL'])
            self.getline(['S', 'TXTSPC', 'TXTUNT'])

    def block_11(self):
        self.getline(['L', 'TRCPLT', 'TRCHST', 'TRCNAL', 'TRCREA', 'TRCSIG',
                           'TRCGRD', 'TRCSUR', 'TRCREF', 'TRCFLE', 'TRCAMD',
                           'TRCINT', 'TRCLST', 'TRCSOU', 'TRCREC', 'TRCTIM',
                           'TRCBLA', 'TRCBLM', 'TRCBLI', 'TRCBLP', 'TRCBLE',
                           'TRCBLPH', 'TRCTAL', 'TRCOCT', 'TRCCEN', 'TRCDUMM',
                           'TRCDBG2', 'TRCDBGE', 'TRCDBGM', 'TRCDBGF',
                           'TRCDBGL', 'TRCDBGS', 'TRCDBGG', 'TRCDBGMPI', 'TRCDBGC'])
        # Some reading involving NSTRA
        # A for loop going from 0 to NSTRA with a step of 60
        role = ['L']
        for i in range(self.values['NSTRAI']+1):
            role += ['TRCSRC(i)']
        self.getline(role)

        self.getline(['I', 'NVOLPR', 'NSPCPR'])

        for i in range(self.values['NVOLPR']):
            self.getline(['I', 'NTLV', 'NFLGV', 'NSPZV1', 'NSPZV2', 'NTLVF'])

        self.getline(['I', 'NSURPR'])

        for i in range(self.values['NSURPR']):
            self.getline(['I', 'NSRF', 'NTLS', 'NFLGS', 'NSPZS1', 'NSPZS2',
                               'NTLSF'])

        line = self.getline() # Reading the line to see if there are either
                              # logicals or numbers inside

        if not self.looks_like_boolean_card(line):
            self.getline(['I', 'NTLVOUT'])
            NTLVOUT = self.values['NTLVOUT']
            ITLVOUT = 0
            while NTLVOUT > 0 and ITLVOUT < NTLVOUT:
                self.getline(['I', 'NUMTAL(j)', 'NUMTAL(j)', 'NUMTAL(j)',
                                   'NUMTAL(j)', 'NUMTAL(j)', 'NUMTAL(j)',
                                   'NUMTAL(j)', 'NUMTAL(j)', 'NUMTAL(j)',
                                   'NUMTAL(j)', 'NUMTAL(j)', 'NUMTAL(j)'])
                ITLVOUT += 12


            self.getline(['I', 'NTLSOUT'])
            NTLSOUT = self.values['NTLSOUT']
            ITLSOUT = 0
            while NTLSOUT > 0 and ITLSOUT < NTLSOUT:
                self.getline(['I', 'NUMTAL(j)', 'NUMTAL(j)', 'NUMTAL(j)',
                                   'NUMTAL(j)', 'NUMTAL(j)', 'NUMTAL(j)',
                                   'NUMTAL(j)', 'NUMTAL(j)', 'NUMTAL(j)',
                                   'NUMTAL(j)', 'NUMTAL(j)', 'NUMTAL(j)'])
                ITLSOUT += 12

        # Reading logicals
        self.getline(['L', 'PL1ST', 'PL2ND', 'PL3RD', 'PLADD', 'PLHST',
                           'PLCUT(i)', 'PLCUT(i)', 'PLCUT(i)', 'PLBOX',
                           'PLSTOR', 'PLNUMV', 'PLNUMS', 'PLARR', 'LRPSCUT',
                           'PLIDL', 'PLVTK'])
        # Reading integers
        self.getline(['I', 'NPLINR', 'NPLOTR', 'NPLDLR', 'NPLINL', 'NPLOTP',
                           'NPLDLP', 'NPLINT', 'NPLOTT', 'NPLDLT', 'nsrflcs'])
        for j in range(abs(self.values['nsrflcs'])):
            self.getline(['I', 'msrfcls(j)'])
            msrfcls_j = self.values['msrfcls(j)']
            if msrfcls_j:
                role = ['I']
                for i in range(1, msrfcls_j + 1):
                    role.append(['lsrfcls(i,j)'])
                self.getline(role)

        # Reading 5 lines
        # 6662
        for j in range(1, 6):
            line = self.getline()
            if len(line.split()) == 2:
                self.getline(['S', 'PL3A(j)', 'IPLTS(j)'])
            else:
                self.getline(['S', 'These are settings for graphical output for standalone eirene runs!'])
        for j in range(1, 4):
            line = self.getline()
            if len(line.split()) == 2:
                self.getline(['S', 'PL3A(j)', 'IPLTS(j)'])
            else:
                self.getline(['S', 'These are settings for graphical output for standalone eirene runs!'])


        self.getline(['R5', 'CH2MX', 'CH2MY', 'CH2X0', 'CH2Y0', 'CH2Z0'])
        self.getline(['R5', 'CH3MX', 'CH3MY', 'CH3MZ', 'CH3X0', 'CH3Y0',
                            'CH3Z0'])
        self.getline(['R5', 'ANGLE1', 'ANGLE2', 'ANGLE3'])
        role = ['I', 'I1TRC', 'I2TRC',]
        for i in range(1, 9):
            role.append('ISYPLT(i)')
        role.append('ILINIE')
        self.getline(role)

        self.getline(['I', 'NVOLPL'])
        if  self.values['NVOLPL'] <= 0:
            return
        """
        for i in range(self.values['NSTRAI'] % 60):
            role = ['L']
            line = self.getline()
            logicals = sum([1 if char in 'fFtT' else 0 for char in line])
            for j in range(logicals):
                role.append('PLTSRC(j)')
            self.getline(role)

        if self.values['LRPSCUT']:
            self.getline(['R', '1', '2', '3', '4', '5', '6'])

        for j in range(1, self.values['NVOLPL']):
            self.getline(['I', 'NSP'])
            self.getline(['L', 'PLTL2D(j)',
                               'PLTLLG(j)',
                               'PLTLER(j)',])
            self.getline(['R5', 'TALZMI(j)', 'TALZMA(j)', 'TALXMI(j)',
                                'TALXMA(j)', 'TALYMI(j)', 'TALYMA(j)'])
            if self.values['PLTL2D(j)']:
                self.getline(['L', 'LHIST2(j)', 'LSMOT2(j)'])
        """


        # Following lines are not sufficiently described in manual or in
        # input.f.
        line = self.getline()
        while line[:3] != '***':
            self.getline(['S', '*** 11. Data for numerical and graphical'
                               'output'])
            line = self.getline()

    def block_12(self):
        self.getline(['I', 'NCHORI', 'NCHENI'])
        if self.values['NCHORI'] > 0:
            for i in range(1, self.values['NCHORI']+1):
                self.getline(['S', 'TXTSIG'])
                self.getline(['I', 'NSPTAL', 'NSPSCL', 'NSPNEW', 'NSPCHR'])
                self.getline(['I', 'NSPSTR', 'NSPSPZ', 'NSPINI', 'NSPEND',
                              'NSPBLC', 'NSPADD'])
                self.getline(['I', 'EMIN1', 'EMAX1', 'ESHIFT'])
                self.getline(['I', 'IPIVOT', 'XPIVOT', 'YPIVOT', 'ZPIVOT'])
                self.getline(['I', 'ICHORD', 'XCHORD', 'YCHORD', 'ZCHORD'])
            self.getline(['I', 'PLCHOR', 'PLSPEC'])

    def block_13(self):
        self.getline(['I', 'NPRNLI', 'NINITL_READ', 'NPRMUL'])
        if self.values['NLERG'] == 0 and self.values['NPRNLI'] == 0:
            self.values['NPRNLI'] = 100
        if self.values['NPRNLI'] > 0:
            self.getline(['I', 'NPTST', 'NTMSTP'])
            self.getline(['R5', 'DTIMV', 'TIME0'])
        self.getline(['I', 'NSNVI'])
        if self.values['NSNVI'] > 0:
            self.dummy_block()  # No additional descritpion in the manual

    def block_14(self):
        self.getline(['L', 'LSYMET', 'LBALAN', 'LCHKQUD'])
        self.getline(['I', 'NFLA', 'NCUTB', 'NCUTL', 'IMF', 'NTRFRM', 'NFULL',
                           'IBRAD', 'IBPOL', 'IBTOR'])
        for i in range(1, self.values['NPLSI'] + 1):
            self.getline(['S', 'I', 'IFLB', 'FCTE', 'BMASS', 'LKINDP'])
        self.getline(['I', 'NDXA', 'NDYA'])
        self.getline(['I', 'NTARGI'])

        role = ['I']
        for i in range(1, self.values['NTARGI'] + 1):
            role.append('NTGPRT(i)')
        self.getline(role)

        for i in range(1, self.values['NTARGI'] + 1):
            for j in range(1, self.values['NTGPRT(i)'] + 1):
                self.getline(['I', 'I', 'NDT', 'NINCT', 'NIXY', 'NTIN', 'NTEN',
                                   'NIFLG', 'NPTC', 'NPTCM', 'NSPZI', 'NSPZE',
                                   'NEMOD'])

        self.getline(['R5', 'CHGP', 'CHGEE', 'CHGEI', 'CHGMOM'])
        self.getline(['I', 'NAINB', 'NCOPIB', 'NCOPEB'])

        for i in range(1, self.values['NAINB'] + 1):
            self.getline(['I', 'I', 'NAINS', 'NAINT', 'TXTPLS', 'TXTPSP',
                               'TXTPUN'])
        self.getline(['I', 'NAOTB'])

        for i in range(1, self.values['NAOTB'] + 1):
            self.getline(['I', 'I', 'NAOTS', 'NAOTT'])

    def block_15(self):
        line = self.getline()
        if 'GENERAL' in line:
            self.row += 1
            self.getline('I', 'NADMOD', 'NASMOD', 'NORMOD')
            for i in range(1, self.values['NADMOD'] + 1):
                self.getline(['S', 'NRS', 'IPUNKT', 'XCOOR', 'YCOOR', 'ZCOOR'])
            for i in range(1, self.values['NASMOD'] + 1):
                self.getline(['S', 'NAS', 'IPUNKT', 'NSSIR', 'NSSIP'])
            for i in range(1, self.values['NORMOD']):
                self.getline(['S', 'IDIR', 'IR', 'IP'])
        elif 'BIASED_GARCHING' in line:
            self.row += 1
            for i in range(max(1, int(self.values['NPPLG']/3)) * 4):
                line = self.getline().split()
                if int(line[1]) < 0:
                    role = ['S', 'NRS', 'IPUNKT', 'XPOLPOS', 'YPOLPOS']
                else:
                    role = ['I', 'NRS', 'IPUNKT']
        else:
            self.getline(['I', 'NADMOD', 'NASMOD'])
            for i in range(1, self.values['NADMOD'] + 1):
                line = self.getline().split()
                if int(line[1]) < 0:
                    role = ['S', 'NRS', 'IPUNKT', 'XPOLPOS', 'YPOLPOS']
                else:
                    role = ['I', 'NRS', 'IPUNKT']
                self.getline(role)
            for i in range(1, self.values['NASMOD'] + 1):
                self.getline(['S', 'NAS', 'IPUNKT', 'NSSIR', 'NSSIP'])


    def block_16(self):
        """ Acording to the Eirene manual, this block can have a free styled
        format, including empty lines.
        """
        line = self.getline()
        while line == '':
            self.row+=1
            line = self.getline()
        self.getline(['S', 'DISTRIBUTION'])

    def dummy_block(self):
        """This function reads the lines from the input file and then simply
        put it into the tree structure but without help parameters.
        """
        line = self.getline()
        while line is not None:
            self.row += 1
            if line.startswith('***'):
                role = ['S', line]
                item = self.createItem(self, line, role)
                self.curr_par = self.grup_par = item
                break

            elif line.startswith('**'):
                self.curr_par = self.createItem(self.grup_par, line)

            elif line.startswith('*'):
                item = self.createItem(self.grup_par, line)
                if self.curr_par != self:
                    self.curr_par = item
            else:
                self.createItem(self.curr_par, line)
            line = self.getline()

    def readInput(self, path):
        if os.path.exists(path):
            try:
                with open(path) as file:
                    self.filename = path
                    self.text = file.read()
                    self.setPlainText(self.text)
            except PermissionError as error:
                logging.error(str(error))
        else:
            msg = path + " does not exist"
            logging.error(msg)
        return

    def getline(self, role=None):
        """ Function getline is the main function which ties the lines from the
        input file to the tree structure in the editor.

        When the function is given a role, the role is then added to a widget
        tree item as Qt.UserData, a user specified data in a widget. This data
        is then used for displaying help description.

        Args:
            role [array]: This array contains the help desc. parameters

        Returns:
            line [str]: When there is no role passed as argument getline
                function returns the current line without changing the main row
                index
            IndexError [error]: If for some the main row index is raised beyond
                the size of the text, the IndexError exception is returned.
        """
        if self.row >= self.text_size:
            raise IndexError
        line = self.text[self.row]
        self.currentLine = line

        if role is None:
            return line

        parent = self.curr_par
        group = self.grup_par

        self.row += 1

        if line[:3] == '***':
            block_item = self.createItem(self, line)
            self.curr_par = self.grup_par = block_item
            raise MyException

        elif line[:1] == '*':
            item = self.createItem(group, line)
            if group != self:
                self.curr_par = item

            self.getline(role)
        elif role:
            self.createItem(parent, line, role)

    def createItem(self, parent, text, role=None):
        """This function creates a QTreeWidgetItem and then is put into the
        tree. Besides the default flags this itam has, there are also added
        the Qt.ItemIsEditable and Qt.ItemIsSelectable flag.

        Args:
            parent [QTreeWidgetItem]: Who it belongs to for the tree
                structure hiearchy
            text [str]: The text string to display
            role [array]: Possible help description parameters
        Returns:
            item [QTreeWidgetItem]: The created item is returned for furthur
                tree structure.
        """
        item = QTreeWidgetItem(parent)
        item.setText(0, text)
        item.setFlags(item.flags() | Qt.ItemIsEditable | Qt.ItemIsSelectable)

        if role:
            self.set_variables(role, text)
            # user_role = (type, number of args, variables name)
            user_role = (role[0], role[1], role[2:])
        else:
            user_role = (None, None, None)
        item.setData(0, Qt.UserRole, user_role)
        return item

    def set_variables(self, role, text):
        """This function sets the values to the parameters of the input file.
        This is mainly used for certain situations when a card or cards are
        dependant on other previous values or booleans.

        The values are then stored on the dictionary self.values.

        In the role array there is also stored the numbers of variables in the
        given time. This is used in the validator for validating input.

        Args:
            role [array]: The name of variables in a card
            text [str]: The text containing values for the roles

        """
        args = self.get_arguments(text, role[0], len(role) - 1)
        for i in range(1, len(role)):
            if i <= len(args) and role[0] != 'S':
                self.values[role[i]] = args[i - 1]
        role.insert(1, len(args))

    def get_arguments(self, line, type, numOfVals):
        """This function accepts a string line and then based on a pattern, it
        extracts the correct typed values and then return it via an array.

        Args:
            line [str]: A line from the input file
            type [str]: Type of variables in the line
        Returns:
            arguments [array]: Depending on the line it can contain booleans,
                integers or real numbers.
        """
        if type == 'L':
            arguments = []
            for char in line:
                if char != ' ':
                    arguments.append(True if char in 'tT' else False)
        elif type == 'R5':
            arguments = []
            for i in range(numOfVals):
                val = line[12 * i:12 * (i + 1)]
                if val.strip():
                    arguments.append(float(val))
        elif type == 'R4':
            arguments = [float(e) for e in line.replace('E ', 'E+').split()]
        elif type == 'I':
            arguments = []
            for i in range(numOfVals):
                val = line[i * 6:(i + 1) * 6]
                if val.strip():
                    arguments.append(int(val))
        elif type == 'S':
            arguments = ''.join([char for char in line])
        else:
            # Reactions card
            arguments = line.split()
        #elif type == 'RC':
        #    arguments = line.split()
        #elif type == 'NC':
        #    arguments = line.split()
        #...

        return arguments

    @pyqtSlot()
    def changed(self):
        """This function is called whenever an item is modified in the editor.
        It does not accept or return anything, since it only changes a boolean
        to True.
        """
        self.TextModified = True

    def isModified(self):
        """ Usually if there is a slight change in format the editor would go
        in full error mode. But now that the lines are nonetheless read, the
        only difference is that there are no tooltips.
        """
        # if self.successful_reading == 0:
        #     return False
        return self.TextModified

    def setModified(self, flag):
        self.TextModified = False

    def toPlainText(self):
        """ It returns the text from the editor. It is first gathered from the
        elements of the tree then returned.

        Returns:
            text [str]: Text from the editor.
        """
        items = [self.topLevelItem(i) for i in range(self.topLevelItemCount())]
        text = self.gatherText(items)
        return text

    def gatherText(self, childs):
        """ The text is gathered through the elements or children from the
        tree. It is also propagated for instances when children have their
        children.

        Args:
            childs [QTreeWidgetItem]: Element or elements from the tree
        Returns:
            text [str]: Text from the editor
        """
        text = ''
        for el in childs:
            text += el.data(0, Qt.DisplayRole) + '\n'
            if el.childCount():
                childs = [el.child(i) for i in range(el.childCount())]
                text += self.gatherText(childs)
        return text

    def keyPressEvent(self, e):
        #if e.key() == Qt.Key_F2:  # Edit key F2
        #    if self.selectedItems():
        #        item = self.selectedItems()[0]
        #        self.scrollToItem(item, QAbstractItemView.PositionAtTop)
        if e.key() == Qt.Key_Enter:
            self.card_edit_delegate.lineEdit.editingFinished.emit()
        elif e.key() == Qt.Key_I and e.modifiers() == Qt.ControlModifier:
            self.insertRow(self.selectedItems()[0])
        elif e.key() == Qt.Key_K and e.modifiers() == Qt.ControlModifier:
            self.removeRow(self.selectedItems()[0])

        return super(EireneEdit, self).keyPressEvent(e)

    def insertRow(self, at_item):
        parent = at_item.parent()
        item = QTreeWidgetItem()
        item.setText(0, '*')

        item.setFlags(item.flags() | Qt.ItemIsEditable | Qt.ItemIsSelectable)
        if parent is None:
            item.setData(0, Qt.UserRole, (None, None, None))
            self.insertTopLevelItem(self.indexOfTopLevelItem(at_item),
                                    item)
        else:
            item.setData(0, Qt.UserRole, (None, None, None))
            parent.insertChild(parent.indexOfChild(at_item),
                               item)
        self.setCurrentItem(item)
        self.TextModified = True

    def removeRow(self, item):
        parent = item.parent()
        if parent is None:
            self.takeTopLevelItem(self.indexOfTopLevelItem(item))
        else:
            parent.removeChild(item)
        self.TextModified = True

    def rowNumber(self, item):
        parent = item.parent()
        if parent is None:
            row = self.indexOfTopLevelItem(item)
            for i in range(row):
                row += self.rowCount(self.topLevelItem(i))
            return row

        else:
            row = parent.indexOfChild(item)




class Eirene(QWidget):
    """Eirene(QComboBox)
    Provides a custom widget for Eirene input.
    """
    returnPressed = pyqtSignal()
    def __init__(self, parent=None):
        super(Eirene, self).__init__(parent)
        # The following array contains the variables, that are numbered
        # in the settings file but has the same description!
        self.group_cards = ['NTGPRT', 'INDSRC', 'INDPRO', 'NLPRCA', 'PRMSPL',
                            'INGRDA', 'INGRDE', 'DPLD', 'DIOD', 'DMLD', 'DATD',
                            'VL',
                            'P1', 'P2', 'P3', 'P4', 'P5']
        self.splitter = QSplitter(self)
        self.splitter.setOrientation(Qt.Vertical)
        self.tree = EireneEdit(self.splitter)
        self.help = QTextBrowser(self.splitter)
        self.splitter.setStretchFactor(0, 7)
        self.splitter.setStretchFactor(1, 3)
        self.tree.card_edit_delegate.parameter_help.connect(self.show_help)
        self.tree.itemSelectionChanged.connect(self.show_help)
        self.show_help('EDIT_HELP')

    def sizeHint(self):
        return QSize(600, 400)

    def resizeEvent(self, event):
        self.splitter.resize(event.size())

    @pyqtSlot()
    @pyqtSlot(str)
    def show_help(self, parameter='EDIT_HELP'):
        if parameter == '':
            self.help.clear()
        elif parameter == 'EDIT_HELP':
            text = ''
            if self.tree.selectedItems():
                item = self.tree.selectedItems()[0]
                card_data = item.data(0, Qt.UserRole)
                if card_data and card_data[0]:
                    type_of_card = card_data[0]
                    card_variables = card_data[2]
                    text = '<p>' + type_of_card + " :" +\
                           " ".join(card_variables) + '</p>'
                elif item.data(0, Qt.DisplayRole).startswith('***'):
                    text = "Block: " + item.data(0, Qt.DisplayRole)
            self.help.setText(text + "<p> Press F2 to edit line."
                              "<p>Use arrow keys to navigate through rows "
                              "and to expand/collapse rows.</p>"
                              "<p>CTRL + I to insert rows. "
                              "CTRL + K to remove row</p>")
        elif parameter in eirene_params:
                self.help.setText('<b>' + parameter + '</b>:' +
                                  '<p>' + eirene_params[parameter] + '<p>')
        else:
            for card in self.group_cards:
                if parameter.startswith(card):
                    self.help.setText('<b>' + parameter + '</b>:' +
                                      '<p>' + eirene_params[card] + '<p>')
                    return

            self.help.setText('<b>' + parameter + '</b>:' +
                              eirene_params['NOD'])

    def setPlainText(self, text):
        self.tree.setPlainText(text)

    def toPlainText(self):
        return self.tree.toPlainText()

    def setReadOnly(self, state):
        return

    def setPlaceholderText(self, text):
        self.tree.setPlainText(text)

    def document(self):
        return self.tree


if __name__ == "__main__":

    import sys
    import os
    from PyQt5.QtWidgets import (QApplication, QMainWindow,
                                 QTreeWidgetItemIterator)

    os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'  # for solving high-dpi
    app = QApplication(sys.argv)                     # problems

    class Standalone(QMainWindow):
        def __init__(self, parent=None):
            super(Standalone, self).__init__(parent)
            self.eirene = Eirene(self)
            self.eirene.tree.setSelectionMode(
                QAbstractItemView.SingleSelection)
            self.setCentralWidget(self.eirene)

        def closeEvent(self, e):
            self.documentSave()
            super(Standalone, self).closeEvent(e)

        def documentSave(self):
            if self.eirene.tree.TextModified:
                path = self.eirene.tree.filename

                if os.path.exists(path):
                    try:
                        with open(path, 'w') as f:
                            text = self.eirene.tree.toPlainText()
                            f.write(text)
                    except PermissionError as error:
                        logging.error(str(error))
                else:
                    logging.error('Path does not exist.')

        def event(self, e):
            if e.type() == QEvent.KeyRelease:
                self.UpdateStatusBar()
            return super(Standalone, self).event(e)

        def UpdateStatusBar(self):
            selectedItem = self.eirene.tree.selectedItems()[0]

            # Cursor position
            # TODO
            try:
                editor = self.eirene.tree.card_edit_delegate.lineEdit
                if editor:
                    cursor_position = editor.cursorPosition()
                else:
                    cursor_position = 0
            except RuntimeError as e:
                cursor_position = 0

            # Row
            row = 0
            iterator = QTreeWidgetItemIterator(self.eirene.tree)
            while iterator.value():
                item = iterator.value()
                if item == selectedItem:
                    row = row
                    break
                else:
                    iterator += 1
                    row += 1

            # Block
            parentItem = selectedItem.parent()
            if parentItem is not None:
                block = parentItem.data(0, Qt.DisplayRole)
            else:
                block = selectedItem.data(0, Qt.DisplayRole)
            message = '%6d' % row + ' ' + '%3d' % cursor_position + ' ' + \
                      '%s' % block
            self.statusBar().showMessage(message)

    if len(sys.argv) > 1:
        input_dat = sys.argv[1]
    else:
        print('Provide path to Eirene input file!')
        sys.exit()
        # input_dat='input_2.dat'
    mainwindow = Standalone()
    mainwindow.eirene.tree.readInput(os.path.expanduser(input_dat))
    mainwindow.show()
    sys.exit(app.exec_())
