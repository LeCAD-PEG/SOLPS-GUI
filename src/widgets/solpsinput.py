#!/usr/bin/env python3

"""
A PyQt custom widget with embedded SOLPS configuration editor and viewer
for files if tabs with filenames are added to it and then ``view_files``
is called though selected tab index signal.

Tooltips are created in solps-iter/doc with::

  xsltproc create-tooltips.xslt solps-input.xml > ~/solps-gui/src/widgets/tooltips.py
"""

from PyQt5.QtCore import (QSize, QEvent, QRegExp, Qt,
                          pyqtProperty,  pyqtSignal, pyqtSlot, QSettings)
from PyQt5.QtWidgets import (QTabWidget, QPlainTextEdit, QSizePolicy,
                             QGridLayout, QToolTip)
from PyQt5.QtGui import (QFont, QTextCursor, QSyntaxHighlighter,
                         QTextCharFormat, QBrush)

import os
import logging
import gzip
import textwrap

from eirene import Eirene
from b2 import B2Edit

class SolpsInput(QTabWidget):
    """SolpsInput(QTabWidget)
    
    Provides a custom widget that holds all SOLPS input files available for
    editing before starting the run.
    """
    lineInsert = pyqtSignal(str)

    def __init__(self, parent=None):
        super(SolpsInput, self).__init__(parent)
        self.setWindowTitle('SOLPS input file editor and viewer')
        self.setMovable(True)
        self.rundir = None
        self.currently_viewing = None
        self.editors = dict()

    def restore_tab_positions(self):
        """ Get tabs ordering from settings and restore the to saved position.
        """
        settings = QSettings("ITER", "solps-gui")
        settings.beginGroup("SolpsInputTabPosition")
        for i in range(self.count()):
            settings.value("%s" % self.tabText(i), i)
            tab_text = settings.value("%s" % self.tabText(i), "")
            if tab_text != "":
                self.tabBar().moveTab(i, int(tab_text))
        settings.endGroup()

    def store_tabs_position(self):
        """ Tabs arrangement is saved into settings.
        """
        settings = QSettings("ITER", "solps-gui")
        settings.beginGroup("SolpsInputTabPosition")
        for i in range(self.count()):
            settings.setValue("%s" % self.tabText(i), i)
        settings.endGroup()

    @pyqtSlot()
    def setup_input_tabs(self):
        """ Setups tabs for input and restores last saved position of the
            tabs from the settings.
        """
        font = QFont()
        font.setFamily('Monospace')
        for filename, tooltip in solps_input_files:            
            plainTextEdit = QPlainTextEdit(self)
            plainTextEdit.setObjectName(filename)
            plainTextEdit.setFont(font)
            plainTextEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
            tab_index = self.addTab(plainTextEdit, filename)

            self.editors[filename] = plainTextEdit
            if filename == 'input.dat':
                eirene = Eirene()
                self.removeTab(tab_index)
                tab_index = self.addTab(eirene, filename)
                self.editors[filename] = eirene
            elif filename.startswith('b2'):
                editor = B2Edit(filename=filename)
                self.lineInsert.connect(editor.display_widget.insert_line)
                self.removeTab(tab_index)
                tab_index = self.addTab(editor, filename)
                self.editors[filename] = editor
            self.setTabToolTip(tab_index, tooltip)
        self.restore_tab_positions()

    @pyqtSlot(int)
    def view_files(self, tab_index):
        """ Adds QPlainTextEdit widget inside the tabs that are not yet
            in dictionary of editors. Tabs need to exist and should be created
            by Qt Designer. Files are read only if the widget is visible
            and ``runDir`` is set. Signal currentIndexChanged should be
            connected here. If file is ending with .gz then gzip decompression
            is applied to read the file.
        """

        if not self.isVisible():
            return

        if not self.rundir:
            logging.debug("Run directory not prescribed to view view files.")
            return

        if self.currently_viewing == self.rundir:
            return

        font = QFont()
        font.setFamily('Monospace')
        for i in range(self.count()):
            filename = self.tabText(i)
            if not filename in self.editors:
                tab = self.widget(i)
                layout = QGridLayout(tab)
                tab.setLayout(layout)
                plainTextEdit = QPlainTextEdit(tab)
                plainTextEdit.setObjectName(filename)
                plainTextEdit.setFont(font)
                plainTextEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
                layout.addWidget(plainTextEdit)
                self.editors[filename] = plainTextEdit

            plainTextEdit = self.editors[filename]
            plainTextEdit.setReadOnly(True)
            path = self.rundir + '/' + filename
            if os.path.exists(path):
                try:
                    _dummy, file_extension = os.path.splitext(filename)
                    if file_extension == '.gz':
                        # TODO handle decompress errors
                        with gzip.open(path, 'rb') as file:
                            text_content = file.read().decode("utf-8")
                            plainTextEdit.setPlainText(text_content)
                    else:
                        with open(path) as file:
                            plainTextEdit.setPlainText(file.read())
                except PermissionError as error:
                    plainTextEdit.setPlainText(str(error))
                    plainTextEdit.setEnabled(False)
            else:
                msg = filename + " does not exist in " + self.rundir
                plainTextEdit.setPlaceholderText(msg)
        self.currently_viewing = self.rundir

    @pyqtSlot()
    def read_input_files(self):
        """ Reads SOLPS input files if they exists and ads them in tabs.

            Rundir must be set beforehand. If the file cannot be written back
            then editing is not alowed.
        """
        if not self.rundir:
            logging.warning("Run directory not prescribed for input edits.")
            return

        if len(self.editors) == 0:  # Setup tabs on the fly
            self.setup_input_tabs()

        for filename in self.editors:
            plainTextEdit = self.editors[filename]

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

    @pyqtSlot(str)
    def insert_line(self, line):
        if type(self.currentWidget()) == type(B2Edit()):
            self.currentWidget().display_widget.insert_line(line)
        print('Reemmiting' + line)
        

    @pyqtSlot()
    def save_modified_input_files(self):
        """ Saves modified input files when Input tab losts its focus.
            At the same time it saves arrangement of the tabs that can be
            freely moved by the user.
        """
        if self.rundir:
            self.store_tabs_position()
            for filename in self.editors:
                plainTextEdit = self.editors[filename]
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
            self.store_tabs_position()
            super(SolpsInput, self).closeEvent(event)

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

solps_input_files = [ # filename and its description for a tooltip [b2cdcn.F]
    ('b2mn.dat',
     "Input file to the b2mn main B2.5 program containing the run switches\n"
     "and eventually overriding parameters to those specified in b2ah.dat"),
    ('input.dat',
     "Eirene input file"),
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
    ('b2md.dat', "Contains data useful for cataloguing the run\n"
     "(done from 'save_mds' and resave_mds' scripts"),
    ('b2.boundary.parameters',
     "Contains data used to specify the boundary conditions.\n"
     "Input file containing the namelists used by b2mn,\n"
     "which complete the input provided  by  the b2??.dat files"),
    ('b2.neutrals.parameters',
     "Input files containing the namelists used by b2mn,\n"
     "which complete the input provided  by  the b2??.dat files"),
    ('b2.numerics.parameters',
     "Input files containing the namelists used by b2mn,\n"
     "which complete the input provided  by  the b2??.dat files"),
    ('b2.transport.parameters',
     "Allows user to choose between different anomalous transport models.\n"
     "Read if ’b2mod_transport_namelist’ is set to 1.\n"
     "Input files containing the namelists used by b2mn,\n"
     "which complete the input provided  by  the b2??.dat files"),
    ('b2.wall_save.parameters',
     "Input files containing the namelists used by b2mn,\n"
     "which complete the input provided  by  the b2??.dat files"),
    ('b2.feedback_control.parameters',
     "Allows for more complex feedback schemes."),
    ('b2.sources.profile',
     "Allows the user to set external sources to use within the code,\n"
     "Unless specifying a divertor heat source, the source will be\n"
     "located in the core and main SOL regions only."),
    ('b2.transport.inputfile',
     "Allows the user to set transport coefficients profiles.\n"
     "Only used if ’b2tqna_inputfile’ is set to 1."),
    ('b2.user.parameters',
     "Contains additional data for user-specific diagnostics."),
    ('b2.atomic_physics_rescale.parameters',
     "Read if ’b2mndr_atomic_physics_rescale’ is set to 1.\n"
     "Contains rescaling multipliers for atomic physics rates."),
    ('untitled',
     'You will be asked for a file name once you start typing.')
]

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = SolpsInput()
    window.setRundir(os.path.expanduser("~")+
      '/solps-iter/runs/tutorial/ITER_535_D+He+Ar/baserun')
    # '/solps-iter/runs/tutorial/AUG_16151_D/run_for_GUI_demo')
    window.read_input_files()
    #window.read_input_files()  # should be resistant to multiple calls
    window.show()
    window.output = pyqtSignal(str)
    #window.output.emit("test line")
    sys.exit(app.exec_())