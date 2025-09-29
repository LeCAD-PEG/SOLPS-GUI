#! /usr/bin/env python3

import sys
import os

from PySide6.QtCore import  QSize, Property, Slot, Signal
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QPlainTextEdit

from PySide6.QtWidgets import QWidget

import logging
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

from ids.quadPlotCanvas import QuadPlotCanvas
from ids.GGDDialog import GetGGDDialog
from ids.getEPGGD import getEPGGD, GetGGDVars

#from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

class EdgeProfiles(QWidget):
    """ Graphical actor
    """

    """Plot edge_profiles (EP) IDS GGD.
    """
    def __init__(self, parent=None, ids=None, *args, **kwargs):
        super().__init__(parent)

        self.gridSubsetDict = {}

        self.gs_id = 0
        self.qLabel = ''
        self.qValues = 0

        self.quantityValuesDict = {}

        self.ggdVars = {}
        for i in range(GetGGDVars.numOfParams):
            # At the begining clear all parameters
            self.ggdVars[i] = ''

        self.ep = None
    
        # Set layout
        self.setLayout(QVBoxLayout())
        # Set empty matplotlib canvas
        self.canvas = QuadPlotCanvas(self, width=1, height=6)
        # Set matplotlib toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)
        # Add widgets to layout
        self.layout().addWidget(self.canvas)
        self.layout().addWidget(self.toolbar)


    @Slot(object)
    def input_edge_profiles(self, edge_profiles):
        """Set edge_profiles IDS."""
        self.ep = edge_profiles


    @Slot()
    def setGGDdata(self):
        """Show dialog for setting GGD parameters.
        """
        if self.ep == None:
            logging.warning('No IDS yet provided.')
            return False
        # Get dialog
        dialog = GetGGDDialog(self)
        # Get variable on dialog close
        dialog.prepareWidgets(self.ggdVars)
        if dialog.exec():
            # Get GGD variables on dialog close
            self.ggdVars = dialog.on_close()
            return True
        else:
            # Canceled!
            return False

    def getQuantityValues(self):
        return self.ggdVars['quantityValues']

    def getQuantityLabel(self):
        return self.ggdVars['quantityLabel']

    def getGridSubsetID(self):
        return self.ggdVars['gridSubsetId']

    def getGGDVars(self):
        return self.ggdVars

    @Slot()
    def plotData(self):
        """Populate (plot) the canvas.
        """
        if self.ep == None:
            return
        # Clear canvas figure if it already exists (to avoid plot overlapping)
        # if self.canvas.figure != None:
        #     self.canvas.figure.clear()
        # Set edge_profiles object
        # Get GGD variables
        ggdVars = self.getGGDVars()
        # Extract array of quantity values

        qValues = ggdVars['quantityValues']
        # Set getGGD object
        getGGD = getEPGGD(self.ep)
        # Get array of nodes coordinates, quad connectivity array and array of
        # quantity values (corresponding to the specified grid subset)
        nodes, quad_conn_array = getGGD.getGSGridGeometry(ggdVars)
        # Plot canvas with the data
        self.canvas.plotData(nodes, quad_conn_array, qValues,
                             title=ggdVars['quantityLabel'])

    @Slot()
    def clearPlot(self):
        """Clear canvas plot.
        """

        self.canvas.figure.clear()
        self.canvas.figure.axes.clear()
        self.canvas.ax = self.canvas.figure.add_subplot(111)

if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    from PySide6.QtUiTools import loadUiType

    uiclass, baseclass = loadUiType("../plugins/pyside6-designer/edgeprofiles.ui")

    class MainWindow(uiclass, baseclass):
        def __init__(self):
            super().__init__()
            self.setupUi(self)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
