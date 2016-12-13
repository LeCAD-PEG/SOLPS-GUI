#!/usr/bin/env python3

"""

A PyQt custom widget with Eirene input edit capabilities.

"""

from PyQt5.QtCore import (Qt, QProcess, QSize, pyqtProperty,
                          pyqtSignal, pyqtSlot, QEvent)
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtWidgets import (QWidget, QSplitter, QTreeWidget, QTextBrowser,
                             QTreeWidgetItem, QAbstractItemView,
                             QStyledItemDelegate, QLineEdit)

import logging

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
ti = ti􀀀1 + t = t0 + it = TIME0 + ITIME  [NTMSTP  DTIMV ]
are filled and prepared for the next time-cycle. The census arrays from the previous
time cycle (if any), i.e., at t = ti􀀀1, are overwritten here.
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
'INDGRD':"""This index controls the meaning of input variables of different standard grid options.
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
“additional surfaces” (input block 3b) and appropriate cell number switching.</p>"""

}

class MyLineEdit(QLineEdit):

    parameter_help = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MyLineEdit, self).__init__(parent)
        self.parameter_description = []
        self.last_param = None

    def set_card_help(self, card_description):
        for param_name, width in card_description:
            for i in range(width):
                self.parameter_description.append(param_name)

    def event(self, ev):
        if ev.type() == QEvent.MouseButtonRelease\
                or ev.type() == QEvent.KeyRelease:
            p = self.cursorPosition()
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

    def itemSelectionChanged(self):
        print (self.selectedItems())

    def setPlainText(self, text):
        lines = text.splitlines()
        group = self
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
                item.setText(1, line.rstrip())
                if parent.data(1, Qt.DisplayRole)[:6] == "*** 1.":
                    row = parent.indexOfChild(item)
                    if row == 0:
                        item.setData(1, Qt.UserRole, [('NMACH', 6), ('NMODE', 6),
                        ('NTCPU', 6), ('NFILE', 6),  ('NITER0', 6),
                        ('NITER', 6), ('NTIME0', 6), ('NTIME', 6) ])

                    elif row == 1:
                        item.setData(1, Qt.UserRole, [('NLSCL', 1),
                                                  ('NLTEST', 1),
                                                  ('NLANA', 1),
                                                  ('NLDRFT', 1),
                                                  ('NLCRR', 1),
                                                  ('NOP', 1),
                                                  ('NLERG', 1),
                                                  ('NLIDENT', 1),
                                                  ('NLONE', 1),
                                                  ('NLMOVIE', 1)])

                elif parent.data(1, Qt.DisplayRole)[:6] == "*** 2.":
                    row = parent.indexOfChild(item)
                    if row == 0:
                        item.setData(1, Qt.UserRole,
                        [('INDGRD', 6), ('INDGRD', 6), ('INDGRD', 6)])
                    elif row == 1:
                        item.setData(1, Qt.UserRole, [('NLRAD', 1)])
            item.setFlags(item.flags() | Qt.ItemIsEditable)

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
    def setPlainText(self, text):
        self.tree.setPlainText(text)

if __name__ == "__main__":

    import sys, os
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = Eirene()

    input_dat = '~/solps-iter/runs/tutorial/ITER_535_D+He+Ar/baserun/input.dat'
    widget.tree.readInput(os.path.expanduser(input_dat))

    widget.show()
    sys.exit(app.exec_())


