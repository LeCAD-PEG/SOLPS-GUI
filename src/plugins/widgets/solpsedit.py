#!/usr/bin/env python3

"""

A PyQt custom widget with embedded SOLPS configuration editor.

"""

from PyQt5.QtCore import (QSize, Qt, pyqtProperty,  pyqtSignal, pyqtSlot)
from PyQt5.QtWidgets import (QTabWidget, QPlainTextEdit)
from PyQt5.QtGui import QFont, QTextCursor

import os
import logging


class SolpsEdit(QTabWidget):
    """SolpsEdit(QDialog)
    
    Provides a custom widget that holds all SOLPS Gnuplot script names
    for combining them with
    """
    
    def __init__(self, parent=None):
        super(SolpsEdit, self).__init__(parent)
        self.setWindowTitle('SOLPS input file editor')
        self.setMovable(True)
        self.rundir = None
        self.editors = list()

    @pyqtSlot()
    def read_input_files(self):
        """ Reads SOLPS input files if they exists and ads them in tabs.

            Rundir must be set beforehand. If the file cannot be written back
            then editing is not alowed.
        """
        if not self.rundir:
            logging.error("Run directory not prescribed for input edits.")
            return

        if len(self.editors) == 0:  # Setup tabs on the fly
            font = QFont()
            font.setFamily("Monospace")
            for filename, tooltip in solps_input_files:
                plainTextEdit = QPlainTextEdit(self)
                plainTextEdit.setObjectName(filename)
                plainTextEdit.setFont(font)
                plainTextEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
                tab_index = self.addTab(plainTextEdit, filename)
                self.setTabToolTip(tab_index, tooltip)
                self.editors.append((filename, plainTextEdit))

        for filename, plainTextEdit in self.editors:
            if not os.access(self.rundir, os.W_OK):
                    plainTextEdit.setReadOnly(True)
            path = self.rundir + '/' + filename
            if os.path.exists(path):
                if not os.access(path, os.W_OK):
                    plainTextEdit.setReadOnly(True)
                try:
                    with open(path) as file:
                        plainTextEdit.setPlainText(file.read())
                except PermissionError as error:
                    plainTextEdit.setPlainText(str(error))
                    plainTextEdit.setEnabled(False)
            else:
                if os.access(self.rundir, os.W_OK):
                    msg = "File does not exist yet. Start typing here."
                else:
                    msg = "File cannot be saved in " + self.rundir
                plainTextEdit.setPlaceholderText(msg)



    @pyqtSlot()
    def save_modified_input_files(self):
        """ Saves modified input files.
        """
        if self.rundir:
            for filename, plainTextEdit in self.editors:
                if plainTextEdit.document().isModified():
                    try:
                        path = self.rundir + '/' + filename
                        with open(path, 'w') as f:
                            f.write(plainTextEdit.toPlainText())
                        print("Saving " + filename)
                    except OSError as error:
                        logging.error(error)

    if __name__ == "__main__":
        def closeEvent(self, event):
            self.save_modified_input_files()
            super(SolpsEdit, self).closeEvent(event)

    def sizeHint(self):
        return QSize(320, 200)

    @pyqtSlot(str)
    def setRundir(self, directory):
        """
        Args:
             directory (str): Absolute path to SOLPS directory with run data.

        """
        self.rundir = directory

    def getRundir(self):
        return self.rundir

    runDir = pyqtProperty(str, getRundir, setRundir)

solps_input_files = [ # filename and its description for tooltip
    ('b2mn.dat',
     "Input file to the b2mn main B2.5 program containing the run switches\n"
     "and eventually overriding parameters to those specified in b2ah.dat"),
    ('b2ag.dat',
     "Input file to the b2ag B2.5 pre-processor that builds the geometry\n"
     "file b2fgmtry in the B2.5 format from the *.geo CARRE grid file."),
    ('b2ah.dat',
     "Input file to the b2ah B2.5 pre-processor that builds the parameters\n"
     "file b2fpardf containing the default set of transport coefficients and\n"
     "boundary conditions to be used by the plasma solver."),
    ('b2ai.dat',
     "Input file to the b2ai B2.5 pre-processor that builds the initial\n"
     "state file b2fstati containing the initial plasma state from which\n"
     "to start the B2.5 or B2-Eirene run."),
    ('b2ar.dat',
     "Input file to the b2ar B2.5 pre-processor that builds\n"
     "the atomic physics rates file b2frates containing\n"
     "the look-up tables to be used by B2.5"),
    ('b2.boundary.parameters',
     "Input files containing the namelists used by b2mn,\n"
     "which complete the input provided  by  the b2??.dat files"),
    ('b2.neutrals.parameters',
     "Input files containing the namelists used by b2mn,\n"
     "which complete the input provided  by  the b2??.dat files"),
    ('b2.numerics.parameters',
     "Input files containing the namelists used by b2mn,\n"
     "which complete the input provided  by  the b2??.dat files"),
    ('b2.transport.parameters',
     "Input files containing the namelists used by b2mn,\n"
     "which complete the input provided  by  the b2??.dat files"),
    ('b2.wall_save.parameters',
     "Input files containing the namelists used by b2mn,\n"
     "which complete the input provided  by  the b2??.dat files"),
]

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = SolpsEdit()
    window.setRundir(os.path.expanduser("~")+
                     '/solps-iter/runs/AUG_16151_D/run1')
    window.read_input_files()
    window.read_input_files()
    window.show()

    sys.exit(app.exec_())


