#!/usr/bin/env python3

"""

A PyQt custom widget with Eirene input edit capabilities.

"""

from PyQt5.QtCore import (Qt, QProcess, QSize, pyqtProperty,
                          pyqtSignal, pyqtSlot, QEvent)
from PyQt5.QtGui import QImage, QPixmap, QFont, QValidator
from PyQt5.QtWidgets import (QWidget, QSplitter, QTreeWidget, QTextBrowser,
                             QTreeWidgetItem, QAbstractItemView,
                             QStyledItemDelegate, QLineEdit)

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
This flag is not in use any more. In the past (eighties of last century) it only affected
the round-off error margin used for geometrical computations. In case NMACH=1, the
error tolerated in the geometry routines is EPSGEO=1.D-10, and EPSGEO=1.D-6 for
all other values of NMACH.</p>""",
'NMODE' : """<b>Operating mode</b>
<dl>
<dt>= 0</dt><dd>EIRENE run as stand-alone-code. Code coupling segment couple_Dummy.f may
be used. Input block 14 has a fixed format, see section 2.14.</dd>
<dt> &ne; 0</dt><dd> EIRENE calls the code coupling subroutine INFCOP in the code coupling segment
couple_Name.f where ’Name’ is a character string identifying the
particular external code, to which EIRENE is to be coupled (e.g.: Name=B2,
Name=DIVIMP, Name=U-file, Name=FIDAP, Name=EMC3, Name=OSM, etc.).
Hence: the routine INFCOP is called by EIRENE for communication with external
data sources, e.g., external data structures for iterative mode by coupling to
other codes. The calling program for the first 3 entries of INFCOP is subroutine
INPUT, and the call to subroutine INFCOP is after reading 13 blocks from the formatted
input file (READ (IUNIN,...)). A 14th block of the input file is read from
subroutine INFCOP with the format (if any) specified there. At entry IF0COP
geometrical data are provided (overruling corresponding data in input block 2).
At entry IF1COP plasma profiles (more generally: background medium data) are
defined (overruling the background data specified in block 5).
Any other data (e.g., surface- or volume source distributions overruling the data
in input block 7) are expected from entry IF2COP.</dd>
<dt>&gt; 0</dt> <dd>0 If NMODE &gt; 0, subroutine INFCOP is called once again after each completed
stratum (at the entry IF3COP(ISTRAA,ISTRAE)) to return data to another code
(post-processing). The call to IF3COP is from subroutine MCARLO, at the end
of the DO 1000 -loop over the strata. One final call to the interfacing routine
(entry IF4COP) is implemented after the calls to the EIRENE printout- and plot
routines, e.g. to perform global balances etc. after summation of the contributions
from the individual strata.</dd>
</dl>
""",

'NTCPU' : """<p>Maximum number of CPU seconds allowed for this run. NTCPU must be less than
or equal to the time parameter in the job-card (if any).</p>
<p>If more than one iteration is carried out (NITER, see below, this section) or more than
one time cycle (NTIME, see below, this section), then each iteration or cycle can take
up to NTCPU seconds.</p>
<p>In 2008 the definition of NTCPU was slightly changed: the initialisation overhead is
not any longer included in NTCPU. I.e., this variable NTCPU now is close to the true
Monte Carlo sampling time. The total cpu-time, including initialisation overhead as
well as post-processing is printed at the end of an EIRENE run (see: “total cpu-time of
this run” in printout file).</p>""",

'NFILE' : """<b>Flag for the use of dump files FT10, FT11, FT12, FT13, FT14 and FT15.</b>
<dl>
<dt>= 0</dt><dd>Neither reading nor saving of data is done.</dd>
<dt>= JKLMN:</dt>
<dt>N = 1</dt><dd>EIRENE writes output data from this run into files FT10 and FT11 to save them
for plot or printout options in this or in later ’read only’ runs with the same input
file.</dd>
<dt>N = 6</dt><dd>same as N=1, but only the data for the sum over all strata are written (sufficient,
e.g., for BGK-iterations, or for post processing, (subroutine DIAGNO, see input
block 12) as long as this post processing only is to be done on total results (not on
contributions from individual strata).</dd>
<dt>N = 2</dt><dd> EIRENE reads output data from an earlier run from files FT10 and FT11. No
new particle histories are computed, only the requested output is printed and plots
are produced. Iteration cycles or time cycles (if any) are abandoned.</dd>
<dt>N = 7</dt><dd>same as N=2, but only the data for the sum over strata are read. See N=6 option
described above.</dd>
<dt>M = 1</dt><dd>EIRENE writes geometry data into file FT12. These data are the output from
subroutines GRID and VOLUME in the initialization phase.</dd>
<dt>M = 2</dt><dd>EIRENE reads geometry data from file FT12. The geometry subroutines GRID
and VOLUME are not called. This option should be used if the geometry has not
changed as compared to an earlier run. It reduces the CPU costs for the overhead.</dd>
<dt>L = 1</dt><dd>EIRENE writes plasma data and atomic and molecular data (“A&M data”)
into file FT13. These data are output from subroutines PLASMA, XSECTA,
XSECTM, XSECTI, XSECTP in the initialization phase. At the end of a run,
some background medium data may have been modified in subroutine MODUSR,
(iterative mode) see NITER flag below. In this case FT13 may be re-written to
prepare for next iterations.</dd>
Also the primary source parameters (input block 7) are saved, for later iterations
or time-steps.</dd>
<dt>L = 2</dt><dd>EIRENE reads plasma data, A&M data from file FT13. It also reads the entire
input block 7 from FT13, and overwrites the input read from this block 7 by
those data. Routines PLASMA, XSECTA, XSECTM, XSECTI, XSECTP are
not called. This option should be used if neither the plasma background nor the
selection of atomic processes to be used, nor the primary source model (block 7)
has changed as compared to an earlier run. It then reduces the CPU costs for the
overhead.</dd>
<dt>L = 3</dt><dd>Acts as if both NFILE-L=1 and NFILE-L=2. I.e. reading background data from
file, and writing new background data onto file at the end of the run, the time-step
or the iteration. For continuation of iterative calculations, for example.</dd>
<dt>L = 4</dt><dd>Same as NFILE-L=3, except: primary source data (input block 7) are not read
from fort.13, but are taken as specified in input block 7. This allows to modify
these primary sources parameters during iterations or time-steps not only via
module MODUSR, but directly via input file.</dd>
<dt>L = 6,7,8,9</dt><dd>Same as L=1,2,3,4, respectively, but XDR file format is used.</dd>
<dt>K = 1</dt><dd>EIRENE saves some data for optimizing non-analog sampling and stratified
source sampling on file FT14.</dd>
<dt>K = 2</dt><dd>EIRENE reads from file FT14 and tries to optimize operation for the next run,
time-step or iteration. Currently only allocation of CPU time in stratified source
sampling is optimized. More details: see paragraph 2.1.1 below.</dd>
<dt>K = 3</dt><dd>Acts as if both NFILE-K=1 and NFILE-K=2.</dd>
<dt>J = 1</dt><dd>Only for time-dependent option (see block 13). EIRENE writes “census data”
at the end of last time-step onto file FT15.</dd>
<dt>J = 2</dt><dd>EIRENE reads “census data” from file FT15, and uses it as initial distribution
for the coming next time-step.</dd>
<dt>J = 3</dt><dd>Acts as if both NFILE-J=1 and NFILE-J=2.</dd>
</dl>""",

'NITER0' : """<p>Initial iteration number: (Default: NITER0=1) Irrelevant parameter. Only needed
for book keeping and printout. EIRENE labels the iterations from NITER0 to NITER.</p>""",

'NITER' : """<p>Number of iterations, if EIRENE runs in "iterative mode".</p>
<dl>
<dt>&gt; 0</dt><dd>EIRENE calls user supplied subroutine MODUSR after completing the run; some
model parameters may be modified here for the next iteration step, and some
results from the previous step may be saved on a file.</dd>
<dt>&gt;1</dt><dd>EIRENE recalls itself but does not read from the formatted input file again. This
recalling is repeated NITER times (including the first iteration). The CPU time
NTCPU is used for each iteration. Hence the true CPU time then is NTCPU NITER.</dd>
</dl>""",
'NTIME0': """<p>Initial time-cycle number: (default: NTIME0=1). Irrelevant. Only needed for
book keeping and printout. EIRENE labels the time steps from NTIME0 to NTIME.</p>""",

'NTIME' : """<p>Total number of iterations (“cycles”) in time carried out in one single run. The total
time per cycle is defined as NTMSTP * DTIMV (see below, input block 13).</p>
<p>After each time-cycle the subroutine TMSTEP is called. In this routine the “census
arrays”, which store the test particle population at time ti:
ti = ti1 + t = t0 + it = TIME0 + ITIME  [NTMSTP * DTIMV ]
are filled and prepared for the next time-cycle. The census arrays from the previous
time cycle (if any), i.e., at t = ti1, are overwritten here.
<p>After the last time-cycle, the census arrays are written on file fort.15, in order to permit
continuation in time in a next run.
The background conditions (and source distributions or any other input parameters) for
the next time cycle can be modified in subroutine TMSUSR(ti), which is called from
subroutine TMSTEP.</p>
<p>If the population on the census array is not empty or known from a previous run
(NFILE-J flag, see above), then this census population defines one additional stratum
for the current cycle. I.e., the census population then determines the initial condition
for the distribution function f(r; v; i; t = t0). The source strength FLUX is computed
from that initial condition.</p>""",

'NOPTIM' : """<p>Default: NRAD, = total number of grid cells
(verify this default in case of older versions: there it may have been NOPTIM=1)
NOPTIM is the first dimension of the arrays IGJUM3(ICELL,ISURF), which may be
used for optimizing code performance by reducing unnecessary geometrical calcula-
tions.</p>""",

'NOPTM1': """<p>Default: 1</p>""",

'NGEOM_USR': """<p>for  value  =1:  user  defined  (external)  geometry  package  (LEVGEO=10),
then no grid storage is provided in EIRENE. Default: 0</p>""",

'NCOUP_INPUT': """<p> =1:  Storage for data transfer via coupling routines, =0:  no such storage.
Default: 1</p>""",

'NSMSTRA': """<p>“Sum over strata” disabled for value 0, enabled for value 1. Default: 1</p>""",

'NSTORAM': """<p>Storage vs.  speed in atomic data evaluation.  Maximum storage, fastest com-
putation: =9. Minimum storage, maximum work (slowest option) =0. Default: 9</p>""",

'NGSTAL': """<p>Storage for spatial distribution of surface tallies on non-default standard surfaces
for value =1. For value =0: only total (spatially integrated) surfaces fluxes. Default: 0</p>""",

'NRTAL': """<p>Condensing mesh cells into fewer larger cells, for output volume tallies. The under-
lying fine mesh has NRAD cells (see input block 2). The coarser mesh, obtained from
condensing cells into one larger cell, has NRTAL cells.  Default:  0:  Then internally:
NRTAL=NRAD, and no condensation is carried out.</p>
<p>NCLTAL(IRAD) = IRTAL: grid cell IRAD is condensed into the larger cell IRTAL.
I.e.: output is average over a larger cell IRTAL, which is comprised of all cells IRAD
such that NCLTAL(IRAD) = IRTAL, IRAD=1, NRAD</p>
<p>The input data in input block 5 (background medium) are always given on the fine mesh
(size: NRAD)</p>
<p>For output tallies (cell averaging) several cells IRAD1, IRAD2,...  can be condensed
into one larger cell IRTAL. Cell volumes, scoring, statistics are automatically done on
the coarser grid (size: NRTAL).</p>
<p>The index array NCLTAL(NRAD) can be defined in the problem specific “user” rou-
tines (see section 3), e.g.: INIUSR, GEOUSR, etc..</p>
<p>Default: NCLTAL(IRAD)=IRAD for IRAD=1,NRAD</p>""",

'NREAC_ADD': """<p> Storage  for  additional  reaction  decks  read  onto  EIRENE  arrays  in  USR-
routines, post-processing, etc. Default: 0</p>""",

# *** 1. Card 2
'NOP' : ' ',
'NLSCL':"""<p>Some volume averaged tallies are re-scaled in order to exactly preserve the total
number of particles, which otherwise would be the case only up to statistical precision
(due to the use of track-length estimators). EIRENE computes three factors FATM,
FMOL and FION such that particle balances for atoms, molecules and test ions, respectively,
are accurately observed, if NLSCL = TRUE.</p>""" ,
'NLTEST':"""<p>Tests for consistency between cell numbers and geometrical data along the particle
tracks are carried out at each point of collision. If inconsistencies are detected, the
history is stopped and an error message is printed. The contribution of these particles
to the particle- and energy balances is stored in the bins “PTRASH” and “ETRASH”
respectively.""",
'NLANA':"""<p>De-activates (NLANA=.TRUE.) all non-analog sampling distributions, such as biased
source sampling, splitting, etc.. Select NLANA=.TRUE., if particle trajectory
plots are used to get an intuitive picture of what is going on physically.</p>""",
'NLDRFT':"""<p>Drift component in the bulk ions velocity distribution is included, i.e. the assumed
underlying distribution in velocity space is a drifting Maxwellian for volumetric
background tallies of bulk particles. (see input block 5, input tallies VXIN, VYIN,
VZIN)). Otherwise (if NLDRFT = FALSE) an isotropic Maxwellian distribution is assumed
for the background particles and the input for VXIN,...VZIN is ignored.
This flag also affects the output tallies for energy exchange, momentum exchange between
test particles and background particles, as well as sampling from linear collision
kernels.</p>""",
'NLCRR':"""<p>Correlated sampling is used. See discussion at end of section 1.8.""",
'NLERG':"""<p>The case is automatically reduced to a case for estimating cell volumes by utilizing
an “ergodic property”. More details: see paragraph 2.1.2 below.</p>""",
'NLIDENT':"""<p>In multi-processor calculation mode NLIDENT forces all processors working
on the same stratum to use the same sequence of random numbers and hence to carry
out exactly identical work. This flag can be used to test the parallelized code version.</p>""",
'NLONE':"""<p>The case is automatically reduced to a single species and “one speed transport”
problem (to simplify setting up cases for comparison with analytic results). (not ready,
don’t use)</p>""",
'NLMOVIE':"""<p>reset a number of model parameters to enable a series of geometry plots for
making particle trajectory movies. This option only works in connection with time
dependent mode, see NTIME flag described above, and input block 2.13. More details:
see paragraph 2.1.3 below.</p>""",

# *** 2.
'INGRD(1)':"""This index controls the meaning of input variables of different standard grid options.
<dl>
<dt>INDGRD(1)</dt><dd>for the radial (or x-direction) grid</dd>
<dt>INDGRD(2)</dt><dd>for the poloidal (or y-direction) grid</dd>
<dt>INDGRD(3)</dt><dd>for the toroidal (or z-direction) grid</dd>
</dl>
Data for first standard mesh: radial or x grid RSURF""",

'INGRD(2)':"""This index controls the meaning of input variables of different standard grid options.
<dl>
<dt>INDGRD(1)</dt><dd>for the radial (or x-direction) grid</dd>
<dt>INDGRD(2)</dt><dd>for the poloidal (or y-direction) grid</dd>
<dt>INDGRD(3)</dt><dd>for the toroidal (or z-direction) grid</dd>
</dl>
Data for first standard mesh: radial or x grid RSURF""",

'INGRD(3)':"""This index controls the meaning of input variables of different standard grid options.
<dl>
<dt>INDGRD(1)</dt><dd>for the radial (or x-direction) grid</dd>
<dt>INDGRD(2)</dt><dd>for the poloidal (or y-direction) grid</dd>
<dt>INDGRD(3)</dt><dd>for the toroidal (or z-direction) grid</dd>
</dl>
Data for first standard mesh: radial or x grid RSURF""",

'NLRAD': """= .TRUE.
<p>A radial or x grid is defined. Otherwise the complete sub-block 2A may be omitted.
Depending upon the logical parameters in the next input card the “geometry - level”
variable LEVGEO is set internally.
<dl>
<dt>LEVGEO=1</dt><dd>cartesian coordinates x (and y)</dd>
<dt>LEVGEO=2</dt><dd>polar coordinates r (and )</dd>
<dt>LEVGEO=3</dt><dd>general curvilinear coordinates: a full 2D mesh (polygonal coordinate
lines) is used in the x - y plane. Grid cuts are permitted in the y-direction.</dd>
<dt>LEVGEO=4</dt><dd> a 2D “finite element” mesh of triangles is used in the x - y plane</dd>
<dt>LEVGEO=5</dt><dd> a 3D “finite volume” mesh of tetrahedrons used</dd>
<dt>LEVGEO=10</dt><dd> a general, user defined geometry block is used. All geometrical calculations</dd>
are performed in problem specific routine VOLUSR, TIMUSR, ...etc.</dd>
</dl>
<p>If NLRAD=.FALSE., then no spatial grid is defined and the default geometry level</dd>
LEVGEO = 1 is used. Volume discretisation may still be achieved “by hand” by defining</dd>
“additional surfaces” (input block 3b) and appropriate cell number switching.</p>""",

'NLSLB': """= .TRUE.
<p>Geometry level: LEVGEO = 1</p>
<p> Cartesian geometry, the x co-ordinate is discretized by setting:</p>
<p>x<sub>1</sub> = RSURF(I)  I=1, NR1ST.</p>
<p> Furthermore, the flux-surface labeling grid RHOSRF(I) is identical with the grid RSURF(I).</p>""",

'NLCRC': """= .TRUE.
<p>Geometry level: LEVGEO = 2</p>
<p>Cylindrical or toroidal geometry, 1D (“radial”) mesh of concentric, circular surfaces.
Polar coordinates are used in the x-y plane.  The third coordinate (either <em>z</em> or toroidal angle &phi;)</p>
<p>The radial surfaces are given by <em>r<sup>2</sup> = x<sup>2</sup> + y<sup>2</sup> = const</em>. and radial coordinate <em>r</em> 
is discreticized by setting r<sub>1</sub>=RSURF(I) I=I, NR1ST. Furthermore RHOSRF(I)=
<span style="white-space: nowrap; font-size:larger">
&radic;<span style="text-decoration:overline;">&nbsp;AREA/&pi;&nbsp;</span>
</span>where AREA is the area inside surface number I. Thus for this option one has again:RHOSRF(I)=RSURF(I), I=1, NR1ST.
</p>""",

'NLELL': """= .TRUE.
<p>Geometry level: LEVGEO = 2</p>
<p>Mesh of nested, but not necessarily concentric or confocal elliptical flux surfaces. The
equation for the “radial” surface is <em>(x-EP)<sup>2</sup> + (y/EL)<sup>2</sup> = r<sup>2</sup></em>. The radial coordinate
<em>r</em> is discretized  by setting <em>r<sub>I</sub></em>=RSURF(I) I=1, NR1ST.</p>
<p>EP and EL may vary with coordinate <em>r</em>. These parameters are stored in the arrays
EP(I),EL(I), I=1,NR1ST which now are used in addition to RSURF to define one co-
ordinate surface in the first (radial or <em>x</em>-grid).</p>
<p>RHOSRF: as in NLCRC option</p>
<p>Note: RHOSRF and RSURF may differ in this case.</p>""",

'NLTRI': """= .TRUE.
<p>Geometry level: LEVGEO = 2</p>
<p>to be written: triangularity in mesh of nested closed algebraic surfaces</p>""",

'NLPLG': """= .TRUE.
<p>Geometry level: LEVGEO = 3</p>
<p>The mesh in the x-y plane is described by NR1ST polygonal arcs of length NRPLG
each.  A polygon may consist of several “valid” and “invalid” parts (to account for
“grid cuts” in CFD meshes). The “invalid” parts of a polygon are not seen by test
particles and are allowed for in EIRENE only in order to facilitate index mapping in
case of runs coupled to plasma transport models, which resort to computer generated
meshes including grid cuts.</p>
<p>The polygons must not intersect each other.</p>
<p>In this case RHOSRF(1)=0., and RHOSRF(I) is the area enclosed by polygon number
1 and polygon number I.</p>""",

'NLFEM': """= .TRUE.
<p>Geometry level: LEVGEO = 4</p>
<p>The mesh in the x-y plane consists of NR1ST triangles,  composed from NRKNOT
knots.</p>
<p>In this case a flux surface labeling grid RHOSRF is not defined.</p>""",

'NLTET': """= .TRUE.
<p>Geometry level: LEVGEO = 5</p>
<p>3D discretisation of volume by tetrahedrons.  For this grid option please make contact
to the authors.</p>""",

'NLGEN': """= .TRUE.
<p>Geometry level: LEVGEO = 10</p>
<p>Arbitrary geometrical configuration.  Mesh consists of NR1ST arbitrarily shapes cells
(in  any  dimension).   Particle  tracing  routines  must  be  provided  by  user  (VOLUSR,
SAMUSR, TIMUSR, LEAUSR)</p>""",

'NR1ST': """Number of grid-points in the radial (or x-direction) standard mesh
<p>if NR1ST&le;1, no radial (or x-direction) standard mesh is defined.</p>
<p>if NLPLG = .TRUE. : number of polygons for discretisation in “radial” or x direction</p>
<p>if NLFEM = .TRUE. : number of triangles for discretisation in x-y plane</p>
<p>if NLTET = .TRUE. or if NLGEN = .TRUE. : number of cells in otherwise arbitrary mesh option NLGEN. Use problem specific
routines to set up mesh, cell volumes, and flight interesction times for
test partilces.</p>""",

'NRSEP': """This flag is active for LEVGEO = 1 or LEVGEO = 2. Otherwise it is irrelevant.
<p>The  first  (x-  or  radial)  standard  mesh  is  composed  by  two  equidistant  x-  or  radial
grids of co-ordinate surfaces with different grid density.  There are NR1ST-NRSEP+1
grid-points  in  the  first,  and  NRSEP  grid-points  in  the  second  part.   The  grid-point
RSURF(NR1ST-NRSEP+1) belongs to both parts.</p>""",

'RIA': """left endpoint of standard grid (internally set &ge; 0 if LEVGEO = 2); RSURF(1)=RIA""",

'RGA': """boundary separating first and second part of standard grid with different grid-point
densities; RSURF(NR1ST-NRSEP+1)=RGA""",

'RAA': """right endpoint of standard grid: RSURF(NR1ST)=RAA""",

'RRA': """if RRA &gt; RAA, one additional, outer void zone is defined
<p>RSURF(NR1ST)=RRA, and the parameter RAA now determines the surface no. NR1ST-
1.</p>
<p>(irrelevant, if RRA &le; RAA)</p>""",

'EPIN': """if NLELL = .TRUE. :
<p>Value of EP(r) for cylindrical co-ordinate surface number 1 with <em>r<sub>1</sub></em>=RIA (see:  NL-
CRC = .TRUE. option above)</p>""",

'EPOT': """if NLELL = .TRUE. :
<p> Value of EP(r) for cylindrical surface number NR1ST with <em>r<sub>NR1ST</sub></em>=RAA</p>""",

'EPCH': """if NLELL = .TRUE. :
<p> Value of EP(r) for cylindrical surface number NR1ST+1 with <em>r<sub>NR1ST+1</sub></em>=RAA</p>
<p>(irrelevant, if RRA &le; RAA)</p>""",

'EXEP': """if NLELL = .TRUE. :
<p>The variation of the “shift function” EP(r) with r is given by</p>
<p><em>EP(r) = EPIN + ((r-RIA)/(RAA-RIA))<sup>EXEP</sup> * (EPOT - EPIN)</em></p>""",

'ELIN': """if NLELL = .TRUE. :
<p>Value of EL(r) for cylindrical surface number 1 with <em>r<sub>1</sub></em>=RIA (see: NLELL = .TRUE. option)</p>""",

'ELOT': """if NLELL = .TRUE. :
<p>Value of EL(r) for cylindrical surface number NR1ST with <em>r<sub>NR1ST</sub></em>=RAA</p>""",

'ELCH': """if NLELL = .TRUE. :
<p>Value of EL(r) for cylindrical surface number NR1ST+1 with <em>r<sub>NR1ST+1</sub></em>=RAA</p>
<p>(irrelevant for RRA &le; RAA)</p>""",

'EXEL': """if NLELL = .TRUE. :
<p>The variation of the “ellipticity  function” EP(r) with r is given by</p>
<p><em>EP(r) = EPIN + ((r-RIA)/(RAA-RIA))<sup>EXEP</sup> * (EPOT - EPIN)</em></p>""",

'TRIN': """if NLTRI = .TRUE. :
<p> to  be  written:  the  option  for  algbraically  given  triangular
grids is currently no available. </p>""",

'TROT': """if NLTRI = .TRUE. :
<p> to  be  written:  the  option  for  algbraically  given  triangular
grids is currently no available. </p>""",

'TRCH': """if NLTRI = .TRUE. :
<p> to  be  written:  the  option  for  algbraically  given  triangular
grids is currently no available. </p>""",

'EXTR': """if NLTRI = .TRUE. :
<p> to  be  written:  the  option  for  algbraically  given  triangular
grids is currently no available. </p>""",

'NRPLG': """if NLPLG = .TRUE. :
<p>Number of points per polygon</p>""",

'NPPLG': """if NLPLG = .TRUE. :
<p>Number of valid parts on each polygon. Each polygon is described by the x and y
co-ordinates of NRPLG points.  It is not necessary that all this points are used for the
polygon.  One can cut the polygon into several valid parts interrupted by parts which
are not seen by the test particles.  ( Default :  NPPLG = 1 ).  This option facilitates the
use of 2-d computer generated meshes which contain topological grid cuts.</p>""",

'XPCOR': """
<p>if NLPLG = .TRUE. : shift whole mesh by that vector in x,y-plane</p>
<p>if NLFEM = .TRUE. : x and y co-ordinates of the knots, respectively</p>""",

'YPCOR': """if NLPLG = .TRUE. :
<p>shift whole mesh by that vector in x,y-plane</p>
<p>if NLFEM = .TRUE. : x and y co-ordinates of the knots, respectively</p>""",

'RFPOL': """if NLPLG = .TRUE. :
<p> if RFPOL > 0., one additional polygon zone is defined, at a distance RFPOL out-
side the polygon NR1ST, and then NR1ST is increased by one.</p>
<p>(irrelevant, if RFPOL &le; 0.)</p>""",

'NPOINT(1,J)': """if NLPLG = .TRUE. :
<p>Index of the first point of the valid part number J (same for each radial polygon)</p>
<p>( Default : NPOINT(1,1) = 1 )</p>""",

'NPOINT(2,J)': """if NLPLG = .TRUE. :
<p>Index of the first point of the valid part number J (same for each radial polygon)</p>
<p>( Default : NPOINT(2,1) = NRPLG  )</p>""",

'XPOL(K,I)': """if NLPLG = .TRUE. :
<p>x-co-ordinate of the polygon point number K on polygon number I</p>""",

'YPOL(K,I)': """if NLPLG = .TRUE. :
<p>y-co-ordinate of the polygon point number K on polygon number I</p>""",

'NRKNOT': """if NLFEM = .TRUE. :
<p>There are NRKNOT knots, by which the triangles are defined</p>""",

'XTRIAN': """if NLFEM = .TRUE. :
<p>x and y co-ordinates of the knots, respectively</p>""",

'YTRIAN': """if NLFEM = .TRUE. :
<p>x and y co-ordinates of the knots, respectively</p>""",

'NVERT(I,ITRI)': """if NLFEM = .TRUE. :
<p>Each triangle ITRI is defined by 3 points <em>P<sub>1</sub>, P<sub>2</sub>, P<sub>3</sub></em> 
from the set of NRKNOT knots.
NVERT(I,ITRI) is the number of point
P<sub>I</sub> (I=1,2,3) in the set of knots for triangle ITRI.<p>""",

'NSIDE(I,ITRI)': """if NLFEM = .TRUE. :
<p>NSIDE(I,ITRI) is the number (1,2 or 3) of the side of the neighboring triangle, which
corresponds to side S<sub>I</sub> of the triangle ITRI to be written</p>""",

'IPROP(I,ITRI)': """if NLFEM = .TRUE. :
<p>ISTS = ABS(IPROP) is the integer, by which a particular surface property is assigned
to side I of the triangle ITRI. ISTS=0 stands for default grid option (transparent surface,
cell indexing is done automatically).  Otherwise ISTS is the number of an additional
(ISTS < NLIMI)  or  non-default  standard  (NLIM < ISTS < NLIM+NSTSI)  surface
option as read in sub-blocks 3a or 3b, respectively.  By default the normal vector of
each side of a triangle points out of the triangle. In case IPROP < 0, this vector points
into the triangle. This is relevant at surface options with ILSIDE &ne; 0.</p>""",

'NLPOL': """if NLTET or NLGEN = .TRUE.:
<p>A poloidal or y grid is defined. Otherwise the complete block 2B may be omitted
and the volume averaged tallies are then automatically integrated over this co-ordinate.</p> """,

'INDGRD(2)': """if NLTET or NLGEN = .TRUE.:
<dl>
<dt>= 1</dt><dd>standard grid option</dd>
<dt>= 2,3,4,5,6</dt><dd>not in use (default: INDGRD(2)=1)</dd>
</dl>""",

'NP2ND':"""if NLTET or NLGEN = .TRUE.:
<p>Number of grid-points in y- or poloidal direction</p>""",

'YIA':"""if NLTET or NLGEN = .TRUE.:
<dl>
<dt>for the LEVGEO=1 option:</dt><dd>the y grid PSURF is defined in the same way as the x grid, using the parameters
YIA,YGA,.... (cm) instead of RIA,RGA,....</dd>
<dt>for the LEVGEO=2 option:</dt><dd>the  poloidal  angle &theta; grid  PSURF  is  defined  in  the  same  way  as  the  radial
<em>r</em> grid was, using the parameters YIA,YGA,...(poloidal angle in degree) instead of RIA,RGA,...
<p>for all options LEVGEO > 2: this input card is irrelevant.</p></dd>
</dl>
<p>Defaults: (needed for scaling, i.e., cell volumes):
YIA=0., YGA=0., YAA=1., YYA=1. in case of LEVGEO=1,
and YIA=0., YGA=0., YAA=360., YYA=360. in case of LEVGEO=2.</p>""",

'YGA':"""if NLTET or NLGEN = .TRUE.:
<dl>
<dt>for the LEVGEO=1 option:</dt><dd>the y grid PSURF is defined in the same way as the x grid, using the parameters
YIA,YGA,.... (cm) instead of RIA,RGA,....</dd>
<dt>for the LEVGEO=2 option:</dt><dd>the  poloidal  angle &theta; grid  PSURF  is  defined  in  the  same  way  as  the  radial
<em>r</em> grid was, using the parameters YIA,YGA,...(poloidal angle in degree) instead of RIA,RGA,...
<p>for all options LEVGEO > 2: this input card is irrelevant.</p></dd>
</dl>
<p>Defaults: (needed for scaling, i.e., cell volumes):
YIA=0., YGA=0., YAA=1., YYA=1. in case of LEVGEO=1,
and YIA=0., YGA=0., YAA=360., YYA=360. in case of LEVGEO=2.</p>""",

'YAA':"""if NLTET or NLGEN = .TRUE.:
<dl>
<dt>for the LEVGEO=1 option:</dt><dd>the y grid PSURF is defined in the same way as the x grid, using the parameters
YIA,YGA,.... (cm) instead of RIA,RGA,....</dd>
<dt>for the LEVGEO=2 option:</dt><dd>the  poloidal  angle &theta; grid  PSURF  is  defined  in  the  same  way  as  the  radial
<em>r</em> grid was, using the parameters YIA,YGA,...(poloidal angle in degree) instead of RIA,RGA,...
<p>for all options LEVGEO > 2: this input card is irrelevant.</p></dd>
</dl>
<p>Defaults: (needed for scaling, i.e., cell volumes):
YIA=0., YGA=0., YAA=1., YYA=1. in case of LEVGEO=1,
and YIA=0., YGA=0., YAA=360., YYA=360. in case of LEVGEO=2.</p>""",

'YYA':"""if NLTET or NLGEN = .TRUE.:
<dl>
<dt>for the LEVGEO=1 option:</dt><dd>the y grid PSURF is defined in the same way as the x grid, using the parameters
YIA,YGA,.... (cm) instead of RIA,RGA,....</dd>
<dt>for the LEVGEO=2 option:</dt><dd>the  poloidal  angle &theta; grid  PSURF  is  defined  in  the  same  way  as  the  radial
<em>r</em> grid was, using the parameters YIA,YGA,...(poloidal angle in degree) instead of RIA,RGA,...
<p>for all options LEVGEO > 2: this input card is irrelevant.</p></dd>
</dl>
<p>Defaults: (needed for scaling, i.e., cell volumes):
YIA=0., YGA=0., YAA=1., YYA=1. in case of LEVGEO=1,
and YIA=0., YGA=0., YAA=360., YYA=360. in case of LEVGEO=2.</p>""",

'NLTOR':"""
<p>A toroidal or z grid is defined.  Otherwise the complete block 2C may be omitted
and the volume averaged tallies are then automatically integrated over this co-ordinate.</p>
<p>In case NLTOR = TRUE, sub-block 2C must be read</p>""",

'INDGRD(3)': """
<dl>
<dt>= 1</dt><dd>standard grid option</dd>
<dt>= 2,3,4,5,6</dt><dd>not in use (default: INDGRD(3)=1)</dd>
</dl>""",

'NLTRZ':"""=TRUE
<p>cylindrical approximation is used, i.e., TSURF is a grid in z direction. The co-ordinate
surfaces are given by z=TSURF(L)</p>
<p>(Default: NLTRZ = TRUE)</p>""",

'NLTRA':"""=TRUE
<p>toroidal approximation is used. The coordinate line is a polygonal approximation of a
circle, or an angular section thereof.</p>
<p>In case NLTOR = TRUE, the 3rd grid TSURF is a grid of toroidal angles. The toroidal
segment (or the full torus) is approximated by NT3RD-1 straight cylindrical segements.</p>
<p>In case NLTOR = FALSE, there are NTTRA toroidal periodicity boundaries, such that
the toroidal segment is approximated, again, by NTTRAM=NTTRA-1 straight cylin-
ders, but without toroidal resolution in the results. (Note: If NLTOR, NTTRA=NT3RD,
internally.)</p>
<p>The torus axis of the entire mesh can be shifted in radial direction by adding a radial
offset ROA (see below) to the x coordinates of the poloidal mesh (RSURF,PSURF).</p>
<p>The radial shift of the poloidal mesh RMTOR of the approximated torus is computed
from ROA such that the volume inside radial surface NR1ST is exactly equal to the
volume of an exact torus with poloidal cross section defined by the shifted radial grid
(first standard mesh: RSURF).</p>
<p>Due  to  the  approximations  made  by  defining  a  torus  by  NTTRAM  =  NTTRA  -  1
straight cylinders, this condition is fulfilled only approximately for the other radial sur-
faces. RMTOR converges to ROA with increasing NTTRA. NTTRA &#x2243; 30 is already a very good 
approximation.</p>
<p>(Default: NLTRA = FALSE).</p>""",

'NLTRT':"""=TRUE
<p>torus co-ordinates R,PHI,THETA. Presently being developed for NLSLB,NLPLG and
NLTRI options. Not ready for use.</p>""",

'NT3RD':"""
<p>Number of grid-points in z- or toroidal direction</p>
<p>(default: NT3RD = 1, i.e. no grid is defined)</p>""",

'NTTRA':"""
only needed in case NLTRA and .NOT.NLTOR. See above.""",

'ZIA':"""
<p>The 3rd grid ZSURF is defined in the same way as the x grid, using the parameters
ZIA, ZGA,.... (cm) instead of RIA, RGA,....</p>
<p>In case of NLTRZ = TRUE , a z-grid is defined. ROA is irrelevant.</p>
<p>In case of NLTRA = TRUE , ZIA and ZAA are toroidal angles (in degrees). A grid of
toroidal angles is defined.  For example use ZIA=0.0 and ZAA=360.0 for a full torus.
In case NLTOR this grid also defines the toroidal resolution.  If .NOT.NLTOR, then
periodicity at the endpoints ZIA and ZAA is automatically enforced.</p>
<p>ROA is the radial shift of the poloidal cross section defined by the x-y grids.  E.g.:  if
the x-y- grids are given with magnetic axis as origin, then ROA is the major radius. If
the x-y- grids are already given with respect to the torus axis at their origin, then ROA
=0 (or better e.g.:1.0E-4=ROA &#x226A 1)</p>
<p>Note: ROA affects evaluation of cell volumes.</p>
<p>Note also: in case of geometry and trajectory plots (input block 11), this major radius
offset ROA of poloidal cross sections has to be taken into account when defining plot-
frames.</p>
<p>(Defaults: NLTRA = FALSE, ZIA = 0 , ZAA = 1)</p>""",

'ZGA':"""
<p>The 3rd grid ZSURF is defined in the same way as the x grid, using the parameters
ZIA, ZGA,.... (cm) instead of RIA, RGA,....</p>
<p>In case of NLTRZ = TRUE , a z-grid is defined. ROA is irrelevant.</p>
<p>In case of NLTRA = TRUE , ZIA and ZAA are toroidal angles (in degrees). A grid of
toroidal angles is defined.  For example use ZIA=0.0 and ZAA=360.0 for a full torus.
In case NLTOR this grid also defines the toroidal resolution.  If .NOT.NLTOR, then
periodicity at the endpoints ZIA and ZAA is automatically enforced.</p>
<p>ROA is the radial shift of the poloidal cross section defined by the x-y grids.  E.g.:  if
the x-y- grids are given with magnetic axis as origin, then ROA is the major radius. If
the x-y- grids are already given with respect to the torus axis at their origin, then ROA
=0 (or better e.g.:1.0E-4=ROA &#x226A 1)</p>
<p>Note: ROA affects evaluation of cell volumes.</p>
<p>Note also: in case of geometry and trajectory plots (input block 11), this major radius
offset ROA of poloidal cross sections has to be taken into account when defining plot-
frames.</p>
<p>(Defaults: NLTRA = FALSE, ZIA = 0 , ZAA = 1)</p>""",

'ZAA':"""
<p>The 3rd grid ZSURF is defined in the same way as the x grid, using the parameters
ZIA, ZGA,.... (cm) instead of RIA, RGA,....</p>
<p>In case of NLTRZ = TRUE , a z-grid is defined. ROA is irrelevant.</p>
<p>In case of NLTRA = TRUE , ZIA and ZAA are toroidal angles (in degrees). A grid of
toroidal angles is defined.  For example use ZIA=0.0 and ZAA=360.0 for a full torus.
In case NLTOR this grid also defines the toroidal resolution.  If .NOT.NLTOR, then
periodicity at the endpoints ZIA and ZAA is automatically enforced.</p>
<p>ROA is the radial shift of the poloidal cross section defined by the x-y grids.  E.g.:  if
the x-y- grids are given with magnetic axis as origin, then ROA is the major radius. If
the x-y- grids are already given with respect to the torus axis at their origin, then ROA
=0 (or better e.g.:1.0E-4=ROA &#x226A 1)</p>
<p>Note: ROA affects evaluation of cell volumes.</p>
<p>Note also: in case of geometry and trajectory plots (input block 11), this major radius
offset ROA of poloidal cross sections has to be taken into account when defining plot-
frames.</p>
<p>(Defaults: NLTRA = FALSE, ZIA = 0 , ZAA = 1)</p>""",

'ZZA':"""
<p>The 3rd grid ZSURF is defined in the same way as the x grid, using the parameters
ZIA, ZGA,.... (cm) instead of RIA, RGA,....</p>
<p>In case of NLTRZ = TRUE , a z-grid is defined. ROA is irrelevant.</p>
<p>In case of NLTRA = TRUE , ZIA and ZAA are toroidal angles (in degrees). A grid of
toroidal angles is defined.  For example use ZIA=0.0 and ZAA=360.0 for a full torus.
In case NLTOR this grid also defines the toroidal resolution.  If .NOT.NLTOR, then
periodicity at the endpoints ZIA and ZAA is automatically enforced.</p>
<p>ROA is the radial shift of the poloidal cross section defined by the x-y grids.  E.g.:  if
the x-y- grids are given with magnetic axis as origin, then ROA is the major radius. If
the x-y- grids are already given with respect to the torus axis at their origin, then ROA
=0 (or better e.g.:1.0E-4=ROA &#x226A 1)</p>
<p>Note: ROA affects evaluation of cell volumes.</p>
<p>Note also: in case of geometry and trajectory plots (input block 11), this major radius
offset ROA of poloidal cross sections has to be taken into account when defining plot-
frames.</p>
<p>(Defaults: NLTRA = FALSE, ZIA = 0 , ZAA = 1)</p>""",

'ROA':"""
<p>The 3rd grid ZSURF is defined in the same way as the x grid, using the parameters
ZIA, ZGA,.... (cm) instead of RIA, RGA,....</p>
<p>In case of NLTRZ = TRUE , a z-grid is defined. ROA is irrelevant.</p>
<p>In case of NLTRA = TRUE , ZIA and ZAA are toroidal angles (in degrees). A grid of
toroidal angles is defined.  For example use ZIA=0.0 and ZAA=360.0 for a full torus.
In case NLTOR this grid also defines the toroidal resolution.  If .NOT.NLTOR, then
periodicity at the endpoints ZIA and ZAA is automatically enforced.</p>
<p>ROA is the radial shift of the poloidal cross section defined by the x-y grids.  E.g.:  if
the x-y- grids are given with magnetic axis as origin, then ROA is the major radius. If
the x-y- grids are already given with respect to the torus axis at their origin, then ROA
=0 (or better e.g.:1.0E-4=ROA &#x226A 1)</p>
<p>Note: ROA affects evaluation of cell volumes.</p>
<p>Note also: in case of geometry and trajectory plots (input block 11), this major radius
offset ROA of poloidal cross sections has to be taken into account when defining plot-
frames.</p>
<p>(Defaults: NLTRA = FALSE, ZIA = 0 , ZAA = 1)</p>""",

'NLMLT':"""<p>the complete “Standard Mesh” data are copied NBMLT times</p>""",

'NBMLT':"""<p>Number of identical copies of the standard mesh. Transition from one such mesh
(called “block” in EIRENE) into another one has to be defined by transparent additional
surfaces (see block 3B)</p>""",

'VOLCOR':"""<p>The volumes of all cells of the standard mesh as computed by EIRENE (in sub-
routine. VOLUME) are multiplied by one common factor VOLCOR for each “block”.</p>""",

'NLADD':"""<p>There are cells in the computational volume, which are defined through “additional
surfaces” as cell boundaries.  E.g.  a standard mesh (if there is one) is augmented by
“additional cells” in this case.  If NLADD = FALSE , the complete block 2D may be
omitted and the defaults are used.</p>""",

'NRADD':"""<p>Number of additional zones. The cell indexing along test flights in these zones has
to be specified explicitly by making use of the ILSWCH, ILCELL parameters (block
3B)</p>
<p>(Default: NRADD = 0 ).</p>""",

'VOLADD':"""<p>Volume (<em>cm<sup>-3</sup></em>) of each additional zone as seen
by the test-particles.</p>""",
}



class MyValidator(QValidator):
    def __init__(self, parent=None, n=None, type=None):
        super(MyValidator, self).__init__(parent)
        self.n = n

        if type == 'B':
            self.length = self.n + int(self.n/5)
            self.n = self.length
            self.mask = "T|F|\s"
        elif type == 'R':
            self.length = self.n * 12
            self.mask = "-?\d\.\d\d\d\d\dE(\+|\-)\d\d"
        elif type == 'I':
            self.length = self.n * 6
            self.mask = "-?[0-9]+"
        else:
            self.validate = lambda string, pos: QValidator.Invalid, string, pos

    def validate(self, string, pos):
        if len(string) != self.length:
            return QValidator.Intermediate, string, pos

        search = re.findall(self.mask, string)
        if len(search) != self.n:
            return QValidator.Invalid, string, pos

        return QValidator.Acceptable, string, pos


class MyLineEdit(QLineEdit):

    parameter_help = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MyLineEdit, self).__init__(parent)
        self.parameter_description = []
        self.last_param = None
        self.key_list = []
        self.current_position = 0

    def set_card_help(self, card_description):
        if card_description == []:
            self.number_of_args = None
            return None
        if card_description[0] == 'I':
            for param_name in card_description[1:]:
                for i in range(6):
                    self.parameter_description.append(param_name)

        elif card_description[0] == 'B':
            for i, param_name in enumerate(card_description[1:]):
                if i % 5 == 0 and i > 0:
                    self.parameter_description.append(' ')
                self.parameter_description.append(param_name)
        elif card_description[0] == 'R':
            for param_name in card_description[1:]:
                for j in range(13):
                    if j % 13 != 0:
                        self.parameter_description.append(param_name)

    def focusInEvent(self, e):
        self.deselect()
        self.setCursorPosition(0)
        return super(MyLineEdit, self).focusInEvent(e)

    def event(self, ev):
        if ev.type() == QEvent.MouseButtonRelease \
                or ev.type() == QEvent.KeyRelease:
            p = self.cursorPosition()-1
            if p < 0:
                p = 0
            if p < len(self.parameter_description):
                if  self.parameter_description[p] != self.last_param:
                    self.parameter_help.emit(self.parameter_description[p])
                    self.last_param = self.parameter_description[p]
                    #print(self.last_param)
            elif not self.last_param is None:
                    self.parameter_help.emit('')
                    self.last_param = None
        return super(MyLineEdit, self).event(ev)

class CardEditDelegate(QStyledItemDelegate):
    """
    See http://stackoverflow.com/questions/2801959
    """

    parameter_help = pyqtSignal(str)

    def __init__(self, parent=None):
        super(CardEditDelegate, self).__init__(parent)
        self.lineEdit = None

    def createEditor(self, parent, option, index):
        if index.column() != 1:
            return None
        self.lineEdit = MyLineEdit(parent)
        self.lineEdit.setFrame(True)

        card_data = index.data(Qt.UserRole)
        if card_data is not None:
            self.lineEdit.set_card_help(card_data)
            val = MyValidator(self.lineEdit, len(card_data)-1, card_data[0])
            self.lineEdit.setValidator(val)
        else:
            self.lineEdit.set_card_help([])

        self.lineEdit.parameter_help.connect(self.parameter_help)
        return self.lineEdit

    @pyqtSlot(str)
    def help(self, parameter):
        self.parameter_help.emit(parameter)


class EireneEdit(QTreeWidget):
    def __init__(self, parent=None):
        super(EireneEdit, self).__init__(parent)


        self.setSortingEnabled(False)
        self.setHeaderLabels(["Card",
            "123456123456123456123456123456123456123456123456123456"])
        self.setColumnWidth(0, 32)
        #self.setHeaderLabel("Use F2 to edit and cursor keys to expand/colapse")
        font = QFont()
        font.setFamily('Monospace')
        font.setPixelSize(12)
        self.setFont(font)
        self.setEditTriggers(QAbstractItemView.SelectedClicked
                            |QAbstractItemView.DoubleClicked
                            |QAbstractItemView.EditKeyPressed)
        self.setAlternatingRowColors(True)
        self.card_edit_delegate = CardEditDelegate(self)
        self.setItemDelegate(self.card_edit_delegate)
        self.values = {}

    def itemSelectionChanged(self):
        print(self.selectedItems())

    def setPlainText(self, text):
        lines = text.splitlines()
        group = parent = self
        self.block2_mark = None
        for i, line in enumerate(lines):
            if line[:3] == '***':
                item = QTreeWidgetItem(self)

                # item.setText(0, line[3:].strip())
                item.setText(1, line.rstrip())
                parent = group = item
            elif line[0] == '*':
                item = QTreeWidgetItem(group)
                # item.setText(0, line[1:].strip())
                item.setText(1, line.rstrip())
                parent = item
            else:
                item = QTreeWidgetItem(parent)
                # item.setText(0, str(i))
                stripped_line = line.rstrip()
                item.setText(1, stripped_line)
                if parent == self:
                    return
                if parent.data(1, Qt.DisplayRole)[:6] == "*** 1.":
                    args, role = self.assign_roles_block_1(item, parent, line)
                    i_type = role[0]
                    self.validate_number_of_args(item, stripped_line, args, role)
                    for i, el in enumerate(role[1:]):
                        self.values[el] = args[i]
                    item.setData(1, Qt.UserRole, role)

                elif parent.data(1, Qt.DisplayRole)[:6] == "*** 2.":
                    args, role = self.assign_roles_block_2(item, parent, line)
                    item.setData(1, Qt.UserRole, role)
                    for i, el in enumerate(role[1:]):
                        self.values[el] = args[i]
                    self.validate_number_of_args(item, stripped_line, args, role)
                elif parent.data(1, Qt.DisplayRole)[:6] == "** 2e.":
                    row = parent.indexOfChild(item)
                    if row == 0:
                        role = ['B', 'NLADD']
                        self.values['NLADD'] = True if line[0] == 'F' else False
                        item.setData(1, Qt.UserRole, role)
                    elif row == 1:
                        role = ['I', 'NRADD']
                        self.values['NRADD'] = int(line.split()[0])
                        item.setData(1, Qt.UserRole, role)
                    elif row == 2:
                        role = ['R']
                        for i in range(1, self.values['NRADD'] + 1):
                            role.append('VOLADD(' + str(i) + ')')
                        item.setData(1, Qt.UserRole, role)
                    self.validate_number_of_args(item, stripped_line, args, role)
                    
            item.setFlags(item.flags() | Qt.ItemIsEditable)

    def validate_number_of_args(self, item, string, args, role):
        type = role[0]
        string_length = len(string)
        num_of_settings = len(role)-1
        if type == 'B':
            if string_length != num_of_settings + int(num_of_settings/5):
                item.setData(1, Qt.DisplayRole,
                             string[:num_of_settings + int(num_of_settings/5)])
        if type == 'I':
            if len(string.split()) != num_of_settings:

                item.setData(1, Qt.DisplayRole, string[:num_of_settings*6])
        if type == 'R':
            if len(string.split()) != num_of_settings:
                item.setData(1, Qt.DisplayRole, string[:num_of_settings*12])

    def readInput(self, path):
        if os.path.exists(path):
            try:
                with open(path) as file:
                    text = file.read()
                    self.setPlainText(text)
            except PermissionError as error:
                logging.error(str(error))
        else:
            msg = path + " does not exist"
            logging.error(msg)
        return

    def assign_roles_block_1(self, item, parent, line):
        row = parent.indexOfChild(item)
        args = self.get_arguments(line)
        if row == 0:
            role = ['I', 'NMACH', 'NMODE', 'NTCPU', 'NFILE',
                    'NITER0', 'NITER', 'NTIME0', 'NTIME']
        elif row == 1:
            if 'F' not in line or 'T' not in line:
                role = ['I', 'NOPTIM', 'NOPTM1', 'NGEOM_USR',
                        'NCOUP_INPUT', 'NSMSTRA', 'NSTORAM',
                        'NGSTAL', 'NRTAL', 'NREAC_ADD']
            else:
                role = ['B', 'NLSCL', 'NLTEST', 'NLANA',
                        'NLDRFT', 'NLCRR', 'NLERG', 'NLIDENT',
                        'NLONE', 'NLMOVIE']
        elif row == 2:
            role = ['B', 'NLSCL', 'NLTEST', 'NLANA',
                    'NLDRFT', 'NLCRR', 'NLERG', 'NLIDENT',
                    'NLONE', 'NLMOVIE']
        return args, role



    def assign_roles_block_2(self, item, parent, line):
        """
        Assigning roles for block 2.
        Because there are some variables that exist only if
        one or some flags are true, this function has so called
        block2_mark, which marks where in those conditions we
        currently are, hence the complexity and length of this
        function.
        """
        row = parent.indexOfChild(item)
        args = self.get_arguments(line)
        if row == 0:
            role = ['I', 'INGRD(1)', 'INGRD(2)', 'INGRD(3)']
            return args, role
        elif row == 1:
            role = ['B', 'NLRAD']
            if args[0]:
                # NLRAD is true
                self.block2_mark = '2a-1'
            else:
                self.block2_mark = '2b-1'
            return args, role
        elif row > 1:
            if self.block2_mark == '2a-1':
                    role = ['B', 'NLSLB', 'NLCRC', 'NLELL', 'NLTRI',
                            'NLPLG', 'NLFEM', 'NLTET', 'NLGEN']
                    self.block2_mark = '2a-2'

            elif self.block2_mark == '2a-2':
                role = ['I', 'NR1ST', 'NRSEP', 'NRPLG', 'NPPLG', 'NRKNOT', 'NCOOR']
                self.block2_mark = '2a-3'

            elif self.block2_mark == '2a-3':
                if self.values['INGRD(1)'] <= 5:
                    if self.values['NLCRC'] or self.values['NLELL'] or self.values['NLTRI']:
                        role = ['R', 'RIA', 'RGA', 'RAA', 'RRA']
                        if self.values['NLELL']or self.values['NLTRI']:
                            self.block2_mark == '2a-4a'
                        elif self.values['NLPLG']:
                            self.block2_mark == '2a-4b'
                        elif self.values['NLFEM']:
                            self.block2_mark == '2a-4c'

                elif self.values['INGRD(1)'] == 6:
                    if self.values['NLSLB'] or self.values['NLCRC'] or self.values['NLELL'] or self.values['NLTRI']:
                        role = ['R', 'RIA', 'RGA', 'RAA']
                    elif self.values['NLPLG'] or self.values['NLFEM'] or self.values['NLTET']:
                        role = ['R', 'XPCOR', 'YPCOR', 'ZPCOR']
                    self.block2_mark = '2b-1'

            elif self.block2_mark == '2a-4a':
                role = ['R', 'ER1IN', 'EP1OT', 'EP1CH', 'EXEP1']
                self.block2_mark = '2a-4a-2'

            elif self.block2_mark == '2a-4a-2':
                role = ['R', 'ELLIN', 'ELLOT', 'ELLCH', 'EXELL']
                if self.values['NLTRI']:
                    self.block2_mark = '2a-4a-3'

            elif self.block2_mark == '2a-4a-3':
                role = ['R', 'TRIIN', 'TRIOT', 'TRICH', 'EXTRI']
                self.block2_mark = '2b-1'

            elif self.block2_mark == '2a-4b':
                role = ['R', 'XPCOR', 'YPCOR', 'ZPCOR', 'PLREFL']
                self.block2_mark = '2a-4b-1'

            elif self.block2_mark == '2a-4b-1':
                role = ['R']
                for k in range(1, self.values['NPPLG']+1):
                    role.append('NPOINT(1,' + str(k) + ')')
                    role.append('NPOINT(2,' + str(k) + ')')
                self.block2_mark = '2a-4b-2'
                self.counter = 1

            elif self.block2_mark == '2a-4b-2':
                if self.counter < self.values['NR1ST']:
                    role = ['R']
                    for j in range(1, self.values['NRPLG']+1):
                        chunk.append('XPOL(' + str(self.counter) + ',' + str(j) + ')')
                        chunk.append('YPOL(' + str(self.counter) + ',' + str(j) + ')')
                    self.counter += 1

                elif self.counter == self.values['NR1ST']:
                    role = ['R']
                    for j in range(1, self.values['NRPLG']+1):
                        chunk.append('XPOL(' + str(self.counter) + ',' + str(j) + ')')
                        chunk.append('YPOL(' + str(self.counter) + ',' + str(j) + ')')
                    self.block2_mark = '2b-1'

            elif self.block2_mark == '2a-4c':
                role = ['R', 'XPCOR', 'YPCOR', 'ZPCOR']
                self.block2_mark = '2a-4c-2'

            elif self.block2_mark == '2a-4c-2':
                role = ['I', 'NRKNOT']
                self.block2_mark = '2a-4c-3'

            elif self.block2_mark == '2a-4c-3':
                role = ['R'] + ['XTRIAN(' + str(i) + ')' for i in range(self.values['NRKNOT'])]
                self.block2_mark = '2a-4c-4'

            elif self.block2_mark == '2a-4c-4':
                block.append(['R'] + ['YTRIAN(' + str(i) + ')' for i in range(self.values['NRKNOT'])])
                self.block2_mark = '2b-1'

            elif self.block2_mark == '2b-1':
                role = ['B', 'NLPOL']
                self.block2_mark = '2b-2'

            elif self.block2_mark == '2b-2':
                role = ['B', 'NLPLY', 'NLPLA', 'NLPLP']
                self.block2_mark = '2b-3'

            elif self.block2_mark == '2b-3':
                role = ['I', 'NP2ND', 'NPSEP', 'NPPLA', 'NPPER']
                if self.values['INGRD(2)'] < 5:
                    self.block2_mark = '2b-4'
                else:
                    self.block2_mark = '2c-1'

            elif self.block2_mark == '2b-4':
                role = ['R', 'YIA', 'YGA', 'YAA']
                self.block2_mark = '2c-1'

            elif self.block2_mark == '2c-1':
                role = ['B', 'NLTOR']
                self.block2_mark = '2c-2'

            elif self.block2_mark == '2c-2':
                role = ['B', 'NLTRZ', 'NLTRA', 'NLTRT']
                self.block2_mark = '2c-3'

            elif self.block2_mark == '2c-3':
                role = ['I', 'NT3RD', 'NTSEP', 'NTTRA', 'NTPER']
                if self.values['INGRD(3)'] < 5:
                    self.block2_mark = '2c-4'
                else:
                    self.block2_mark = '2d-1'

            elif self.block2_mark == '2c-4':
                role = ['R', 'ZIA', 'ZGA', 'ZAA', 'ZZA', 'ROA']
                self.block2_mark = '2d-1'

            elif self.block2_mark == '2d-1':
                role = ['B', 'NLMLT']
                if args[0]:
                    self.block2_mark = '2d-2'
                else:
                    self.block2_mark = '2e-1'

            elif self.block2_mark == '2d-2':
                role = ['I', 'NBLMT']
                self.block2_mark = '2d-3'

            elif self.block2_mark == '2d-3':
                role = ['R']
                for i in range(1, self.values['NBLMT']+1):
                    role.append('VOLCOR('+str(i)+')')
                self.block2_mark = '2e-1'

            elif self.block2_mark == '2e-1':
                role = ['B', 'NLADD']
                self.block2_mark == '2e-2'

            elif self.block2_mark == '2e-2':
                role = ['I', 'NRADD']
                if args[0]:
                    self.block2_mark == '2e-3'              

            elif self.block2_mark == '2e-3':
                role = ['R']
                for i in range(1, self.values['NRADD']+1):
                    role.append('VOLADD(' + str(i) + ')')

            else:
                print('WRONG')
            return args, role
        else:
            print('WRONG')

    def get_arguments(self,line):
        if 'F' in line or 'T' in line:
            arguments = []
            for char in line:
                if char != ' ':
                    arguments.append(True if char == 'T' else False)
        elif 'E' in line:
            arguments = []
            for el in line.split():
                arguments.append(float(el))
        else:
            arguments = []
            for el in line.split():
                arguments.append(int(el))

        return arguments

    def isModified(self):
        return False  # TODO was some line changed?

    def toPlainText(self):
        return None # TODO travese tree and return text


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
        #self.show_help('NTCPU')
        self.tree.card_edit_delegate.parameter_help.connect(self.show_help)


    def sizeHint(self):
        return QSize(600, 400)

    def resizeEvent(self, event):
        self.splitter.resize(event.size())

    def show_help(self, parameter):
        if parameter == '':
            self.help.clear()
        elif parameter in eirene_params:
            self.help.setText('<b>' + parameter + '</b>:'
                              + eirene_params[parameter])
        else:
            self.help.setText('<b>' + parameter + '</b>:'
                              + '<p>No description available</p>')
    def setPlainText(self, text):
        self.tree.setPlainText(text)

    def setReadOnly(self, state):
        return

    def setPlaceholderText(self, text):
        self.tree.setPlainText(text)

    def document(self):
        return self.tree


if __name__ == "__main__":

    import sys, os
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = Eirene()

    input_dat = '~/solps-iter/runs/tutorial/ITER_535_D+He+Ar/baserun/input.dat'
    input_dat = 'input.dat'
    widget.tree.readInput(os.path.expanduser(input_dat))

    widget.show()
    sys.exit(app.exec_())


