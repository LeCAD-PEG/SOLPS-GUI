#!/usr/bin/env python3
import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTreeView, QFileSystemModel
from PyQt5.uic import loadUi

class SolpsImpl(QMainWindow):
    def __init__(self, *args):
        super(SolpsImpl, self).__init__(*args)
        loadUi('solps-gui.ui', self)
        self.actionAbout_Qt.triggered.connect(QApplication.instance().aboutQt)
        self.checkBoxParameterScan.toggled.connect(
            self.plainTextEditScript.setEnabled)
        model = QFileSystemModel()
        model.setRootPath('')
        self.treeViewRuns.setModel(model)

    @pyqtSlot()
    def on_initializeRuns_clicked(self):
        if self.plainTextEditScript.isEnabled():
            script = self.plainTextEditScript.toPlainText()
            exec(script)
        else:
            print("Creating %s" % self.lineEditSequenceName.text())
        
    def on_actionAbout_triggered(self):
        QMessageBox.about(self, "About SOLPS-ITER GUI",
         "GUI will enable users to monitor multiple simultaneously running "
         "cases, which requires defining the working directory (folder) for "
         "each case to be separated from each other. "
         "Input file builder will depend on it to correctly save input files "
         " for multiple parameter scan cases.")

app = QApplication(sys.argv)
widget = SolpsImpl()
widget.show()
sys.exit(app.exec_())
