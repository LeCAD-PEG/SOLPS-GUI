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
this run” in printout file).</p>"""
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
            if p < len(self.parameter_description) and \
                            self.parameter_description[p] != self.last_param:
                self.parameter_help.emit(self.parameter_description[p])
                self.last_param = self.parameter_description[p]
                print(self.last_param)
        return super(MyLineEdit, self).event(ev)


class CardEditDelegate(QStyledItemDelegate):
    """
    See http://stackoverflow.com/questions/2801959
    """
    def __init__(self, parent=None):
        super(CardEditDelegate, self).__init__(parent)
    def createEditor(self, parent, option, index):
        if index.column() != 1:
            return None
        lineEdit = MyLineEdit(parent)
        lineEdit.setFrame(True)
        lineEdit.set_card_help([('TXTRUN', 6), ('NMACH', 6), ('NMODE', 6)])
        return lineEdit


class EireneEdit(QTreeWidget):
    def __init__(self, parent=None):
        super(EireneEdit, self).__init__(parent)


        self.setSortingEnabled(False)
        self.setHeaderLabels(["Card / line",
            "123456123456123456123456123456123456123456123456123456"])
        font = QFont()
        font.setFamily('Monospace')
        font.setPixelSize(12)
        self.setFont(font)
        self.setEditTriggers(QAbstractItemView.SelectedClicked
                            |QAbstractItemView.DoubleClicked
                            |QAbstractItemView.EditKeyPressed)
        self.setAlternatingRowColors(True)
        self.setItemDelegate(CardEditDelegate(self))


    def readInput(self, path):
        if os.path.exists(path):
            try:
                with open(path) as file:
                    lines = file.read().splitlines()
                    group = self
                    for i, line in enumerate(lines):
                        if line[:3] == '***':
                            item = QTreeWidgetItem(self)
                            item.setText(0, line[3:].strip())
                            item.setText(1, line.rstrip())
                            parent = group = item
                        elif line[0] == '*':
                            item = QTreeWidgetItem(group)
                            item.setText(0, line[1:].strip())
                            item.setText(1, line.rstrip())
                            parent = item
                        else:
                            item = QTreeWidgetItem(parent)
                            item.setText(0, str(i))
                            item.setText(1, line.rstrip())

                        item.setFlags(item.flags() | Qt.ItemIsEditable)


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
        self.show_help('NTCPU')


    def sizeHint(self):
        return QSize(600, 400)

    def resizeEvent(self, event):
        self.splitter.resize(event.size())

    def show_help(self, parameter):
        if parameter in eirene_params:
            self.help.setText(eirene_params[parameter])

if __name__ == "__main__":

    import sys, os
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = Eirene()

    input_dat = '~/solps-iter/runs/tutorial/ITER_535_D+He+Ar/baserun/input.dat'
    widget.tree.readInput(os.path.expanduser(input_dat))

    widget.show()
    sys.exit(app.exec_())


