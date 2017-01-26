#!/usr/bin/env python3

"""
EIRENE EDITOR

The goal of the EIRENE editor is to have a readable view into the settings file
and a help that shows us a short description of a setting.

The editor reads the file line by line. If we know the pattern of the sett-
ings in the file, we can add a help description as well as a validation for Edi-
ting. This way we cannot mess up the settings and also have a view into what 
setting we are changing.

The pattern and help description are derived from the manual.

So far only the first 4 blocks have the help description and validation.

MANUAL:
The editor has two main windows, one with the text in a tree-style view and the
second window contains the help description for the variables.

To start editing a line either push "F" key or double-click. If the line
has help description, it also has a validation for editing.



DEV:
TODO
"""

from PyQt5.QtCore import (Qt, QProcess, QSize, pyqtProperty,
                          pyqtSignal, pyqtSlot, QEvent, QAbstractItemModel,
                          QItemSelectionModel, QRect)
from PyQt5.QtGui import (QImage, QFont, QValidator)
from PyQt5.QtWidgets import (QWidget, QSplitter, QTreeWidget, QTextBrowser,
                             QTreeWidgetItem, QAbstractItemView,
                             QStyledItemDelegate, QLineEdit, QAbstractItemView)

import logging
import re

eirene_params = {
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

'NOP' : """No description available.""",

'NLSCL' : """<p>Some volume averaged tallies are re-scaled in order to exactly
preserve the total number of particles, which otherwise would be the case only
up to statistical precision (due to the use of track-length estimators).
EIRENE computes three factors FATM, FMOL and FION such that particle balances
for atoms, molecules and test ions, respectively, are accurately observed,
if NLSCL = TRUE.</p>""" ,

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

# *** 2.
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

'NLSLB' : """ <p>Geometry level: LEVGEO = 1</p> <p> Cartesian geometry, the x
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

'NLTRI' : """ <p>Geometry level: LEVGEO = 2</p> <p>to be written:
triangularity in mesh of nested closed algebraic surfaces</p>""",

'NLPLG' : """ <p>Geometry level: LEVGEO = 3</p> <p>The mesh in the x-y plane is
described by NR1ST polygonal arcs of length NRPLG each.  A polygon may consist
of several "valid" and "invalid" parts (to account for "grid cuts" in CFD
meshes). The "invalid" parts of a polygon are not seen by test particles and
are allowed for in EIRENE only in order to facilitate index mapping in case of
runs coupled to plasma transport models, which resort to computer generated
meshes including grid cuts.</p> <p>The polygons must not intersect each
other.</p> <p>In this case RHOSRF(1)=0., and RHOSRF(I) is the area enclosed by
polygon number 1 and polygon number I.</p>""",

'NLFEM' : """ <p>Geometry level: LEVGEO = 4</p> <p>The mesh in the x-y plane
consists of NR1ST triangles,  composed from NRKNOT knots.</p> <p>In this case
a flux surface labeling grid RHOSRF is not defined.</p>""",

'NLTET' : """ <p>Geometry level: LEVGEO = 5</p> <p>3D discretisation of volume
by tetrahedrons.  For this grid option please make contact to the
authors.</p>""",

'NLGEN' : """ <p>Geometry level: LEVGEO = 10</p> <p>Arbitrary geometrical
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

'XPCOR' : """ <p>if NLPLG = .TRUE. : shift whole mesh by that vector in
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

'NLTOR' : """ <p>A toroidal or z grid is defined.  Otherwise the complete block
2C may be omitted and the volume averaged tallies are then automatically
integrated over this co-ordinate.</p> <p>In case NLTOR = TRUE, sub-block 2C
must be read</p>""",

'INDGRD(3)' :  """ <dl> <dt>= 1</dt><dd>standard grid option</dd> <dt>=
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

'NT3RD' : """ <p>Number of grid-points in z- or toroidal direction</p>
<p>(default: NT3RD = 1, i.e. no grid is defined)</p>""",

'NTTRA' : """
only needed in case NLTRA and .NOT.NLTOR. See above.""",

'ZIA' : """ <p>The 3rd grid ZSURF is defined in the same way as the x grid,
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

'ZGA' : """ <p>The 3rd grid ZSURF is defined in the same way as the x grid,
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

'ZAA' : """ <p>The 3rd grid ZSURF is defined in the same way as the x grid,
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

'ILSWCH' : """ = IJKLMN, i.e. six digits I, J, K, L, M and N
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

'ESPUTS' : """(new: March 2015) parameter (flag) for energy of physically 
sputtered particle. Currently not in use.<br>Default: ESPUTS = 0.""",

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

'FLUX' : """<dl><dt>SCALV=0 (default) FLUX = Source strength in Ampere.</dt>
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
interactions.</dd></dl>""",

'SCALV' : """<dl><dt>SCALV=0 (default) FLUX = Source strength in Ampere.</dt>
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
interactions.</dd></dl>""",

'IVLSF' : """<dl><dt>=1</dt><dd>
The following ISCL..-flags select one particular volume averaged tally</dd>
<dt>=2</dt>
<dd>The following ISCL..-flags select one particular surface averaged 
tally</dd></dl>""",

'ISCLS' : """species index of selected tally""",

'ISCLT' : """tally number of selected tally (refer to tables 5.2, 5.3)""",

'ISCL1' : """<dl><dt>IVLSF=1</dt>
<dd>cell numbers NRCELL, NPCELL, NTCELL, NBLOCK, NACELL, respectively.
if (NPCELL = 0) or (NTCELL = 0), then ISCL1 = NCELL, the cell number in
the 1-dimensional arrays (see end of section 2.2.1).
The additional cell region is specified by NRCELL=0, NPCELL=1, NTCELL=1,
NBLOCK=NBMLT+1 (see section 2.2) and the proper value of NACELL.</dd>
<dt>IVLSF=2</dt><dd>to be written</dd></dl>""",

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

'NSPEZ' : """ Species index of the source particle
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

'NLPNT' : """Point Source""",

'NLLNE' : """Line Source (not ready)""",

'NLSRF' : """Surface Source""",

'NLSRF' : """Surface Source""",

'NLCNS' : """Initial conditions source (sampling from census array), for time-
dependent mode of operation, see input blocks 1. and 13.""",
}



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
        if type == 'B':
            self.length = self.n + int(self.n/5)
            self.n = self.length
            self.mask = "T|F|t|f|\s"
        elif type == 'R':
            self.length = self.n * 12
            self.mask = "-?\d\.\d\d\d\d\dE(\+|\-)\d\d"
        elif type == 'I':
            self.length = self.n * 6
            self.mask = "-?[0-9]+"
        elif type == 'S':
            self.length = self.n
            self.mask = "."

    def fixup(self, string):
        if self.old_text:
            return self.old_text
        else:
            return string

    def validate(self, string, pos):
        """The overloaded validate fucntion from QValidator class. Any illegal
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
    functions that handle the help description for the current selected cardrole.insert
    and some overloaded functions for additional cosmetics.

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
        if card_type==None:
            return
        self.parameter_description.append(variables_name[0])
        if card_type == 'I':
            for param_name in variables_name:
                for i in range(6):
                    self.parameter_description.append(param_name)

        elif card_type == 'B':
            i = 1
            for param_name in variables_name:
                if i % 6 == 0:
                    self.parameter_description.append(' ')
                self.parameter_description.append(param_name)
                i += 1
        elif card_type == 'R':
            for param_name in variables_name:
                for j in range(13):
                        self.parameter_description.append(param_name)
        elif card_type == 'S':
            param_name = variables_name[0]
            for j in range(number_of_args):
              self.parameter_description.append(param_name)
    
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
                if  self.parameter_description[p] != self.last_param:
                    self.parameter_help.emit(self.parameter_description[p])
                    self.last_param = self.parameter_description[p]

            else:
                self.parameter_help.emit('NOP')
                self.last_param = None
        return super(MyLineEdit, self).event(ev)

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
        """The overloaded function from QStyledItemDelegate that creates a cu-
        stom editor, handles data for help description to it and changing
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
            if card_type:
                val = MyValidator(self.lineEdit, number_of_args, card_type,
                                  index.data(Qt.DisplayRole))
                self.lineEdit.setValidator(val)

            self.lineEdit.parameter_help.connect(self.parameter_help)
        self.lineEdit.editingFinished.connect(self.parent().changed)

        return self.lineEdit

    def destroyEditor(self, editor, index):
        """Overloaded function from QStyledItemDelegate that sets the help
        description to 'EDIT'.

        Otherwise it is a default function that acts as the editor destroyer
        when we stop editing.
        """
        editor.parameter_help.emit('EDIT')
        super(CardEditDelegate, self).destroyEditor(editor, index)

    @pyqtSlot(str)
    def help(self, parameter):
        self.parameter_help.emit(parameter)


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
        self.text = text.splitlines()
        self.text_size = len(self.text)
        self.row = 0
        self.clear()
        self.curr_par = self.grup_par =self
        # Initiator
        try:
            self.dummy_block()
        except Exception as e:
            pass
        for i in range(self.number_of_blocks):
            try:
                self.blocks[i]()
                self.dummy_block()
            except Exception as e:
                print(e)
                print('Row:', self.row)
                if self.row < self.text_size:
                    print('Line:', self.text[self.row])
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
                      'NITER', 'NTIME0', 'NTIME'])

        line = self.getline()
        if  not self.looks_like_boolean_card(line):
            role = ['I', 'NOPTIM', 'NOPTM1', 'NGEOM_USR', 'NCOUP_INPUT', 
                    'NSMSTRA', 'NSTORAM', 'NGSTAL', 'NRTAL', 'NREAC_ADD']
            self.getline(role)

        role = ['B', 'NLSCL', 'NLTEST', 'NLANA', 'NLDRFT', 'NLCRR', 'NLERG', 
                'NLIDENT', 'NLONE', 'NLMOVIE']
        self.getline(role)
        # Arbitrary lines
        line = self.getline()
        while line[:3]!='***':
            if 'CFILE' in line:
                self.getline(['S', 'CFILE'])
            else:
                self.getline(['S', 'NOP'])
            line = self.getline()

    def block_2(self):
        """Function for setting help desc. parameters for block 2:
        *** 2. Data for standard mesh 
        """

        self.getline(['I', 'INGRD(1)', 'INGRD(2)', 'INGRD(3)'])
        self.getline(['B', 'NLRAD'])
        if self.values['NLRAD']:
            self.getline(['B', 'NLSLB', 'NLCRC', 'NLELL', 'NLTRI',
                                       'NLPLG', 'NLFEM', 'NLTET', 'NLGEN'])

            self.getline(['I', 'NR1ST', 'NRSEP', 'NRPLG', 'NPPLG', 'NRKNOT', 
                       'NCOOR'])


            if self.values['INGRD(1)'] <= 5:

                if self.values['NLSLB'] or self.values['NLCRC'] or \
                self.values['NLELL'] or self.values['NLTRI']:
                    self.getline(['R', 'RIA', 'RGA', 'RAA', 'RRA'])

                    if self.values['NLELL'] or self.values['NLTRI']:
                        self.getline(['R', 'ER1IN', 'EP1OT', 'EP1CH', 'EXEP1'])
                        self.getline(['R', 'ELLIN', 'ELLOT', 'ELLCH', 'EXELL'])
                        if self.values['NLTRI']:
                            self.getline(['R', 'TRIIN', 'TRIOT', 'TRICH', 
                                       'EXTRI'])

                    elif self.values['NLPLG']:
                        self.getline(['R', 'XPCOR', 'YPCOR', 'ZPCOR',
                                      'PLREFL'])
                        role = ['R']
                        for k in range(1, self.values['NPPLG']+1):
                            role.append('NPOINT(1,' + str(k) + ')')
                            role.append('NPOINT(2,' + str(k) + ')')
                        if len(role)>=1:
                            self.getline(role)

                        for i in range(1,self.values['NR1ST']+1):
                            role = ['R']
                            for j in range(1, self.values['NRPLG']+1):
                                role.append('XPOL('+str(self.counter)+','+
                                            str(j)+')')
                                role.append('YPOL('+str(self.counter)+','+
                                            str(j)+')')
                            if len(role) > 1:
                                self.getline(role)
                    elif self.values['NLFEM'] or self.values['NLTET']:
                        self.getline(['R', 'XPCOR', 'YPCOR', 'ZPCOR'])

            elif self.values['INGRD(1)'] == 6:
                if self.values['NLSLB'] or self.values['NLCRC'] or \
                self.values['NLELL'] or self.values['NLTRI']:
                    self.getline(['R', 'RIA', 'RGA', 'RAA'])
                elif self.values['NLPLG'] or self.values['NLFEM'] or\
                    self.values['NLTET']:
                    self.getline(['R', 'XPCOR', 'YPCOR', 'ZPCOR'])

        self.getline(['B', 'NLPOL'])
        self.getline(['B', 'NLPLY', 'NLPLA', 'NLPLP'])
        self.getline(['I', 'NP2ND', 'NPSEP', 'NPPLA', 'NPPER'])
        if self.values['INGRD(2)'] < 5:
            self.getline(role = ['R', 'YIA', 'YGA', 'YAA'])

        self.getline(['B', 'NLTOR'])
        self.getline(['B', 'NLTRZ', 'NLTRA', 'NLTRT'])
        self.getline(['I', 'NT3RD', 'NTSEP', 'NTTRA', 'NTPER'])
        if self.values['INGRD(3)'] < 5:
            self.getline(['R', 'ZIA', 'ZGA', 'ZAA', 'ZZA', 'ROA'])

        self.getline(['B', 'NLMLT'])
        # Sometimes even though NLMLt is false the next line can still 
        # be NBLMT, an integer.

        line = self.getline()
        if line.split()[0].isdigit():
            self.getline(['I', 'NBLMT'])

        if self.values['NLMLT']:
            role = ['R']
            for i in range(1, self.values['NBLMT']+1):
                role.append('VOLCOR('+str(i)+')')
            self.getline(role)
        # 2e. Data for additional cells outside standard mesh
        self.getline(['B', 'NLADD'])
        self.getline(['I', 'NRADD'])
        role = ['R']
        for i in range(1, int(self.values['NRADD'])+1):
            role.append('VOLADD(' + str(i) + ')')
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
                        'ILIT', 'ILCELL', 'ILBOX', 'ILPLG'])
            line = self.getline()
            if 'SURFMOD' in line:
                self.getline(['S', 'SURFMOD_MODNAME'])
            elif line[:1] == '*':
                pass
            elif self.values['ILIIN']>0:
                # Optional
                self.getline(['I', 'ILREF', 'ILSPT', 'ISRS', 'ISRC'])
                self.getline(['R', 'ZNML', 'EWALL', 'EWBIN', 'TRANSP(1,N)', 
                            'TRANSP(2,N)', 'FSHEAT'])
                self.getline(['R', 'RECYCF', 'RECYCT', 'RECPRM', 'EXPPL',
                              'EXPEL', 'EXPIL'])
                self.getline(['R', 'RECYCS', 'RECYCC', 'SPTRM','ESPUTS', 
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
            self.getline(['R', 'RLBND', 'RLARE', 'RLWMN', 'RLWMX'])
            self.getline(['I', 'ILIIN', 'ILSIDE', 'ILSWCH', 'ILEQUI', 'ILTOR', 
                          'ILCOL', 'ILFIT', 'ILCELL', 'ILBOX', 'ILPLG'])

            if self.values['RLBND'] < 2:
                self.getline(['R', 'A0LM', 'A1LM', 'A2LM', 'A3LM', 'A4LM',
                              'A5LM', 'A6LM', 'A7LM', 'A8LM', 'A9LM'])
                if self.values['RLBND'] > 0:
                    self.getline(['R', 'XLIMS1', 'YLIMS1', 'ZLIMS1',
                                  'XLIMS2', 'YLIMS2', 'ZLIMS2'])
            elif self.values['RLBND'] >= 2:
                self.getline(['R', 'P1(1,..)', 'P1(2,..)', 'P1(3,..)', 
                             'P2(1,..)', 'P2(2,..)', 'P2(3,..)'])

                # Cannot determine K!
            line = self.getline()
            if self.values['ILIIN']>0 and line.split()[0].isdigit():
                #Optional!
                self.getline(['I', 'ILREF', 'ILSPT', 'ISRS', 'ISRC'])
                self.getline(['R', 'ZNML', 'EWALL', 'EWBIN', 'TRANSP(1,N)', 
                            'TRANSP(2,N)', 'FSHEAT'])
                self.getline(['R', 'RECYCF', 'RECYCT', 'RECPRM', 'EXPPL',
                              'EXPEL', 'EXPIL'])
                self.getline(['R', 'RECYCS', 'RECYCC', 'SPTRM','ESPUTS', 
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
        self.getline(['I', 'NATMI'])
        line = self.getline()
        while not line.startswith('**'):
            self.getline(['S', 'Reactions card'])
            line = self.getline()

        #**4a.   Neutral atom species
        self.getline(['I', 'NREACI'])
        line = self.getline()
        while not line.startswith('**'):
            self.getline(['S', 'Neutral atom species card'])
            line = self.getline()

        #**4b.   Neutral molecule species
        self.getline(['I', 'NMOLI'])
        line = self.getline()
        while not line.startswith('**'):
            self.getline(['S', 'Neutral molecule species card'])
            line = self.getline()

        #**4c.   Test ion species
        self.getline(['I', 'NIONI'])
        line = self.getline()
        while not line.startswith('**'):
            self.getline(['S', 'Test ion species card'])
            line = self.getline()

        #**4d. Photon species

        if self.getline()[:3]=='***':
            self.values['NPHOTI'] = 0
            return
        else:
            self.getline(['I', 'NPHOTI'])
            line = self.getline()
            while not line.startswith('**'):
                self.getline(['S', 'Test ion species card'])
                line = self.getline()

    def block_5(self):
        self.getline(['I', 'NPLSI'])
        line = self.getline()
        while not line.startswith('**'):
            self.getline(['S', 'Plasma species card'])
            line = self.getline()

        # ** 5b. Plasma background data
        self.getline(['I'] + ['INDPRO('+str(i)+')' for i in range(1,13)])

        if self.values['INDPRO(1)'] <= 5:
            self.getline(['R','TE0', 'TE1', 'TE2', 'TE3', 'TE4', 'TE5'])
        elif self.values['INDPRO(2)'] <= 5:
            for i in range(1, self.values['NPLSI']+1):
                self.getline(['R', 'TI0('+str(i)+')', 'TI1('+str(i)+')', 
                              'TI2('+str(i)+')', 'TI3('+str(i)+')', 
                              'TI4('+str(i)+')', 'TI5('+str(i)+')'])
        elif self.values['INDPRO(3)'] <= 5:  
            for i in range(1, self.values['NPLSI']+1):
                self.getline(['R', 'DI0('+str(i)+')', 'DI1('+str(i)+')', 
                              'DI2('+str(i)+')', 'DI3('+str(i)+')', 
                              'DI4('+str(i)+')', 'DI5('+str(i)+')'])   
        elif self.values['INDPRO(4)'] <= 5:
            for i in range(1, self.values['NPLSI']+1):
                self.getline(['R', 'VX0('+str(i)+')', 'VX1('+str(i)+')', 
                              'VX2('+str(i)+')', 'VX3('+str(i)+')', 
                              'VX4('+str(i)+')', 'VX5('+str(i)+')'])  
            for i in range(1, self.values['NPLSI']+1):
                self.getline(['R', 'VY0('+str(i)+')', 'VY1('+str(i)+')', 
                              'VY2('+str(i)+')', 'VY3('+str(i)+')', 
                              'VY4('+str(i)+')', 'VY5('+str(i)+')'])  
            for i in range(1, self.values['NPLSI']+1):
                self.getline(['R', 'VZ0('+str(i)+')', 'VZ1('+str(i)+')', 
                              'VZ2('+str(i)+')', 'VZ3('+str(i)+')', 
                              'VZ4('+str(i)+')', 'VZ5('+str(i)+')'])  
        elif self.values['INDPRO(5)'] <= 5:
            self.getline(['R', 'B0', 'B1', 'B2', 'B3', 'B4', 'B5'])
        elif self.values['INDPRO(12)'] <= 5:
            self.getline(['R', 'VL0', 'VL1', 'VL2', 'VL3', 'VL4', 'VL5'])

    def block_6(self):
        self.getline(['B', 'NLTRIM'])
        self.getline(['S', 'A_on_B'])
        line = self.getline()
        while 'path' in line or 'PATH' in line:
            self.getline(['S', 'PATH CARD'])

        self.getline(['R'] + ['DATD('+str(i)+')' for i in\
                     range(1, self.values['NATMI'] + 1)])
        self.getline(['R'] + ['DMLD('+str(i)+')' for i in\
                     range(1, self.values['NMOLI'] + 1)])
        self.getline(['R'] + ['DIOD('+str(i)+')' for i in\
                     range(1, self.values['NIONI'] + 1)])
        self.getline(['R'] + ['DPLD('+str(i)+')' for i in\
                     range(1, self.values['NPLSI'] + 1)])
        if self.values['NPHOTI']>0:
            self.getline(['R'] + ['DPHT('+str(i)+')' for i in\
                 range(1, self.values['NPLSI'] + 1)])
        self.getline(['R', 'ERMIN', 'ERCUT', 'RPROB0', 'RINTEG', 'EINTEG',
                      'AINTEG'])

        line = self.getline()
        while line[:3]!='***':
            self.getline(['S', 'SURFMOD'])
            self.getline(['I', 'ILREF', 'ILSPT', 'ISRS', 'ISRC'])
            self.getline(['R', 'ZNML', 'EWALL', 'EWBIN', 'TRANSP(1,N)', 
                          'TRANSP(2,N)', 'FSHEAT'])
            self.getline(['R', 'RECYCF', 'RECYCT', 'RECPRM', 'EXPPL', 'EXPEL', 
                          'EXPIL'])
            self.getline(['R', 'RECYCS', 'RECYCC', 'SPTPRM', 'ESPUTS', 
                          'ESPUTC'])
            line = self.getline()

    def block_7(self):
        self.getline(['I', 'NSTRAI'])
        self.getline(['I'] + ['INDSRC' for i in \
                     range(1,self.values['NSTRAI']+1)])
        self.getline(['R', 'ALLOC', 'AMPTS'])

        for i in range(1, self.values['NSTRAI']+1):
            line = self.getline()
            self.curr_par = self.createItem(self.grup_par, 
                                                line, ['S', 'TXTSOU'])
            self.row+=1


            self.getline(['B', 'NLAVRP', 'NLAVRT', 'NLSYMP', 'NLSYMT'])
            self.getline(['I', 'NPTS', 'NINITL', 'NEMODS', 'NAMODS',
                          'NMINPTS'])
            self.getline(['S', 'Plasma properties. Section 2.7'])
            self.getline(['B', 'NLATM', 'NLMOL', 'NLION', 'NLPLS', 'NLPHOT'])
            self.getline(['I', 'NSPEZ'])
            self.getline(['B', 'NLPNT', 'NLLNE', 'NLSRF', 'NLVOL', 'NLCNS'])
            self.getline(['I', 'NSRFSI'])
            for i in range(1, self.values['NSRFSI']+1):
                self.getline(['I', 'INUM', 'INDIM', 'INSOR', 'INGRDA(1)', 
                              'INGRDE(1)', 'INGRDA(2)', 'INGRDE(2)', 
                              'INGRDA(3)', 'INGRDE(3)'])
                self.getline(['R', 'SORWGT', 'SORLIM', 'SORIND', 
                              'SOREXP', 'SORIFL',])
                self.getline(['I', 'NRSOR', 'NPSOR', 'NTSOR', 'NBSOR', 
                              'NASOR', 'NISOR'])
                self.getline(['R', 'SORAD1', 'SORAD2', 'SORAD3', 'SORAD4', 
                              'SORAD5', 'SORAD6',])
                self.getline(['R', 'SORENI', 'SORENE', 'SORVDX', 'SORVDY', 
                              'SORVDZ',])
                self.getline(['R', 'SORCOS', 'SORMAX', 'SORCTX', 'SORCTY',
                              'SORCTZ',])
    def block_8(self):
        self.getline(['I', 'NZADD'])
        for i in range(1, self.values['NZADD']+1):
            self.getline(['I', 'INI', 'INE'])

    def block_9(self):
        role = ['B']
        role += ['NLPRCA('+str(i)+')' for i in range(self.values['NATMI'])]
        role += ['NLPRCM('+str(i)+')' for i in range(self.values['NMOLI'])]
        role += ['NLPRCI('+str(i)+')' for i in range(self.values['NIONI'])]
        role += ['NLPRCPH('+str(i)+')' for i in range(self.values['NPHOTI'])]
        self.getline(role)
        self.getline(['I', 'NPRCSF'])
        self.getline(['I', 'MAXLEV', 'MAXRAD', 'MAXPOL', 'MAXTOR', 'MAXADD'])
        for i in range(1, self.values['MAXLEV']+1):
            self.getline(['R', 'ID','NSSPL('+str(i)+')','PRMSPL('+str(i)+')'])
        for i in range(1, self.values['MAXPOL']+1):
            self.getline(['R', 'ID','NSSPL('+str(self.values['N1ST']+i)+')',
                          'PRMSPL('+str(self.values['N1ST']+i)+')'])
        for i in range(1, self.values['MAXTOR']+1):
            self.getline(['R', 'ID','NSSPL('+str(self.values['N1ST']+
                                                 self.values['N2ST']+i)+')',
                          'PRMSPL('+str(self.values['N1ST']+
                                        self.values['N1ST']+i)+')'])
        for i in range(1, self.values['MAXADD']+1):
            self.getline(['R', 'ID','NSSPL('+str(self.values['N1ST']+
                                                 self.values['N2ND']+
                                                 self.values['N3RD']+i)+')',
                          'PRMSPL('+str(self.values['N1ST']+
                                        self.values['N1ST']+
                                        self.values['N3RD']+i)+')'])
        self.getline(['R', 'WMINV', 'WMINS', 'WMINC', 'WMINL'])
        self.getline(['R', 'SPLPAR'])
        self.getline(['I', 'NSIGVI', 'NSIGSI', 'NSIGCI', 'NSIGI_BGK', 
                      'NSIGI_COP', 'NSIGI_SPC',])
        for i in range(1, self.values['NSIGVI']+1):
            self.getline(['R', 'IGH', 'IIH'])
        for i in range(1, self.values['NSIGSI']+1):
            self.getline(['R', 'IGHW', 'IIHW'])
        for i in range(1, self.values['NSIGCI']+1):
            self.getline(['R'] + ['IGHC(1,'+str(i)+')', 'IIHC(1,'+str(i)+')',
                                  'IGHC(2,'+str(i)+')', 'IIHC(2,'+str(i)+')'])

    def block_10(self):
        self.getline(['I', 'NADVI', 'NCLVI', 'NALVI', 'NADSI', 'NALSI', 
                      'NADSPC'])
        for i in range(1, self.values['NADVI']+1):
            self.getline(['R', 'IADVE('+str(i)+')', 'IADVS('+str(i)+')',
                          'IADVT('+str(i)+')', 'IADVR('+str(i)+')',
                          'TXTTAL('+str(i)+',NTALA)',
                          'TXTSPC('+str(i)+',NTALA)',
                          'TXTUNT('+str(i)+',NTALA)'])

        for i in range(1, self.values['NCLVI']+1):
            self.getline(['R', 'ICLVE('+str(i)+')', 'ICLVS('+str(i)+')',
                          'ICLVT('+str(i)+')', 'ICLVR('+str(i)+')',
                          'TXTTAL('+str(i)+',NTALC)',
                          'TXTSPC('+str(i)+',NTALC)',
                          'TXTUNT('+str(i)+',NTALC)'])
        for i in range(1, self.values['NALVI']+1):
            self.getline(['R', 'ALSTRNG', 'TXTTAL('+str(i)+',NTALR)',
                          'TXTSPC('+str(i)+',NTALR)',
                          'TXTUNT('+str(i)+',NTALR)'])
        for i in range(1, self.values['NADSI']+1):
            self.getline(['R', 'IADSE('+str(i)+')', 'IADSS('+str(i)+')',
                          'IADST('+str(i)+')', 'IADSR('+str(i)+')',
                          'TXTTAL('+str(i)+',NTLSA)',
                          'TXTSPC('+str(i)+',NTLSA)',
                          'TXTUNT('+str(i)+',NTLSA)'])
        for i in range(1, self.values['NALSI']+1):
            self.getline(['R', 'ALSTRNG', 'TXTTAL('+str(i)+',NTLSR)',
                          'TXTSPC('+str(i)+',NTLSR)',
                          'TXTUNT('+str(i)+',NTLSR)'])
    def block_11(self):
        pass

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
            self.getline(['R', 'DTIMV', 'TIME0'])
        self.getline(['I', 'NSNVI'])
        if self.values['NSNVI'] > 0 :
            self.dummy_block() # No additional descritpion in the manual for
                               # this part

    def block_14(self):
        pass

    def block_15(self):
        pass

    def block_16(self):
        pass

    def dummy_block(self):
        """This function reads the lines from the input file and then simply
        put it into the tree structure but without help parameters.
        """
        line = self.getline()
        while line != None:
            self.row+=1
            if line.startswith('***'):
                self.curr_par = self.grup_par =  self.createItem(self, line)
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
        parent = self.curr_par
        group  = self.grup_par

        if self.row >= self.text_size:
            raise IndexError
        line = self.text[self.row].rstrip()
        if role==None:
            return line

        self.row += 1 

        if line[:3] == '***':
            block_item = self.createItem(self, line)
            self.curr_par = self.grup_par = block_item
            raise Exception


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
        if self.grup_par == self:
            block = item.data(0, Qt.DisplayRole)
        else:
            block = self.grup_par.data(0, Qt.DisplayRole)
        if role:
            self.set_variables(role, text)
            # user_role = (type, number of args, variables name, row)
            user_role = (role[0], role[1], role[2:], self.row, block)
        else:
            user_role = (None, None, None, self.row, block)
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
        args = self.get_arguments(text, role[0])
        for i in range(1, len(role)):
            if i <= len(args) and role[0] != 'S':
                self.values[role[i]] = args[i-1]
        role.insert(1,len(args))

    def get_arguments(self, line, type):
        """This function accepts a string line and then based on a pattern, it 
        extracts the correct typed values and then return it via an array.

        Args:
            line [str]: A line from the input file
            type [str]: Type of variables in the line
        Returns:
            arguments [array]: Depending on the line it can contain booleans,
                integers or real numbers.
        """
        if  type == 'B':
            arguments = []
            for char in line:
                if char != ' ':
                    arguments.append(True if char == 'T' else False)
        elif type == 'R':
            arguments = []
            for i in range(len(line)//12):
                arguments.append(float(line[12*i:12*(i+1)]))
        elif type == 'I':
            arguments = []
            for i in range(len(line)//6):
                arguments.append(int(line[i*6:(i+1)*6]))
        elif type == 'S':
            arguments = ''.join([char for char in line])

        return arguments

    def changed(self):
        """This function is called whenever an item is modified in the editor.
        It does not accept or return anything, since it only changes a boolean
        to True.
        """
        self.TextModified = True

    def isModified(self):
        return self.TextModified

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
        if parent == None:
            self.insertTopLevelItem(self.indexOfTopLevelItem(at_item)+1,
                                    item)
        else:
            parent.insertChild(self.indexOfChild(at_item)+1,
                               item)
        self.TextModified = True

    def removeRow(self, item):
        parent = item.parent()
        if parent == None:
            self.takeTopLevelItem(self.indexOfTopLevelItem(item))
        else:
            parent.removeChild(item)
        self.TextModified = True

    def rowNumber(self, item):
        parent = item.parent()
        if parent == None:
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
        self.splitter = QSplitter(self)
        self.splitter.setOrientation(Qt.Vertical)
        self.tree = EireneEdit(self.splitter)
        self.help = QTextBrowser(self.splitter)
        self.splitter.setStretchFactor(0, 7)
        self.splitter.setStretchFactor(1, 3)
        self.tree.card_edit_delegate.parameter_help.connect(self.show_help)
        self.show_help('EDIT')

    def sizeHint(self):
        return QSize(600, 400)

    def resizeEvent(self, event):
        self.splitter.resize(event.size())

    def show_help(self, parameter):
        if parameter == '': 
            self.help.clear()
        elif parameter == 'EDIT':
            self.help.setText("<p> Press F2 to edit line."
                              "<p> Use arrow keys to navigate through rows and\
                              to expand/collapse rows.<p>"
                              "<p> CTRL + I to insert rows</p>"
                              "<p> CTRL + K to remove row</p>")
        elif parameter in eirene_params:
            self.help.setText('<b>' + parameter + '</b>:'
                              + '<p>' + eirene_params[parameter] + '<p>')
        else:
            self.help.setText('<b>' + parameter + '</b>:'
                              + eirene_params['NOP'])

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

    import sys, os
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel,
                                QTreeWidgetItemIterator)

    os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1' # for solving high-dpi
    app = QApplication(sys.argv)                    # problems
    widget = Eirene()

    class Standalone(QMainWindow):
        def __init__(self, parent=None):
            super(Standalone, self).__init__(parent)
            self.eirene = Eirene(self)
            self.eirene.tree.itemSelectionChanged.connect(self.UpdateStatusBar)
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

        @pyqtSlot()
        def UpdateStatusBar(self):
            selectedItem = self.eirene.tree.selectedItems()[0]

            # Cursor position
            # TODO

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
            if parentItem != None:
                block = parentItem.data(0, Qt.DisplayRole)
            else:
                block = selectedItem.data(0, Qt.DisplayRole)
            message = '%6d' % row + ' ' + '%s' % block 
            self.statusBar().showMessage(message)

    if len(sys.argv[1]): 
        input_dat = sys.argv[1]
    else:
        input_dat='input.dat'
        #input_dat='input_2.dat'
    mainwindow = Standalone()
    mainwindow.eirene.tree.readInput(os.path.expanduser(input_dat))
    mainwindow.show()
    sys.exit(app.exec_())
