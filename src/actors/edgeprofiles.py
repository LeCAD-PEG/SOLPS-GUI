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

        # Set IDS object
        self.idsVars = {"user": os.getenv('USER')}
        self.ids = ids

        # Set layout
        self.setLayout(QVBoxLayout())
        # Set empty matplotlib canvas
        self.canvas = QuadPlotCanvas(self, width=1, height=6)
        # Set matplotlib toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)
        # Add widgets to layout
        self.layout().addWidget(self.canvas)
        self.layout().addWidget(self.toolbar)


    def setIDS(self, ids):
        self.ids = ids

    @Slot(str)
    def setRun(self, run: str):
        self.idsVars["run"] = run

    @Slot(str)
    def setShot(self, shot: str):
        self.idsVars["shot"] = shot

    @Slot(str)
    def setUser(self, user: str):
        self.idsVars["user"] = user

    @Slot(str)
    def setDevice(self, device: str):
        self.idsVars["device"] = device

    @Slot()
    def setEPIDS(self):
        """Set and read edge_profiles IDS.
        Check if either:
        1. IDS object was already provided.
        2. The plugin was run from IMASViz (checks for DTV). In this case the
           IDS parameters are taken from IMASViz DataTreeView and the
           corresponding IDS is opened ( 'get()' ) and IDS object is created
        3. If neither condition from the above is satisfied, run the plugin in
           standalone mode using Dialog for IDS parameters specification.
        """
        # self.vars = {}
        # # If IDS object is not provided, display dialog window where the IDS
        # # parameters can be specified. Then open the specified IDS
        # if self.ids != None:
        #     return
        # else:
        #     from ids.getIDS import GetIDSWrapper, GetIDSDialog, GetIDSVars
        #     for i in range(GetIDSVars.numOfParams):
        #         # At the beginning clear all parameters
        #         self.vars[i] = ''

        #     dialog = GetIDSDialog(self)
        #     # Set note
        #     note = 'Note: this plugin should be used \nonly with IDSs which ' \
        #            + 'contain \npopulated edge_profiles IDS!'
        #     dialog.prepareWidgets(self.vars, note=note)
        #     if dialog.exec():
        #         self.vars = dialog.on_close()
        #     else:
        #         # Canceled!
        #         return self.ids == None
        #     # Set IDS with wrapper
        #     self.ids = GetIDSWrapper(self.vars).getIDS()
        # Check if all parameters are there.
        for el in ["shot", "run", "device", "user"]:
            if el not in self.idsVars:
                return

        # Get the IDS object
        import imas

        ids = imas.ids(int(self.idsVars["shot"]), int(self.idsVars["run"]))

        # Open the data entry
        ids.open_env(self.idsVars["user"], self.idsVars["device"], "3")

        if not ids.isConnected():
            logging.info("ids not connected")
            self.ids = None
            return
        self.ids = ids
        logging.info('Getting IDS')
        # Read edge_profiles IDS
        self.ids.edge_profiles.get()

    @Slot()
    def setGGDdata(self):
        """Show dialog for setting GGD parameters.
        """
        if self.ids == None:
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
        if self.ids == None:
            return

        # Clear canvas figure if it already exists (to avoid plot overlapping)
        if self.canvas.figure != None:
            self.canvas.figure.clear()

        # Set edge_profiles objectž
        self.ep = self.ids.edge_profiles
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
