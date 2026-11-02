#!/usr/bin/env python3
"""UQ Plot actor: plots of a UQ study read from uq_samples.csv,
uq_outputs.csv and uq_results.csv: Sobol' indices, output histogram,
outputs against inputs and the input samples. "Profiles (all runs)" reads
b2fplasmf of every finished run and draws the profiles at the OMP or a
target with their mean and 5-95 % band.
"""

import os

import numpy as np

from PySide6.QtCore import Slot, Signal, Property, QSize, Qt
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel, QPushButton,
                               QVBoxLayout, QWidget)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from uq_common import (PLOT_TYPES, PROFILE_LOCATIONS, QOI_VARIABLES, VARIABLE_LABELS,
                       SAMPLES_FILE, OUTPUTS_FILE, readCsv, readResults, readSetup,
                       runDirs, findGeometry, GridLocations, readFields, newCombo)


class UQPlotActor(QWidget):
    """ UQPlotActor(QWidget)

        Draws the results of a UQ study. Connect setStudy(QString) to
        outputsCollected or resultsReady of UQAnalysisActor, or to
        samplesReady of UQSetupActor for the input samples only.

        Attributes:
            logMessage(str): Signal emits error messages.
    """
    icon = ''

    logMessage = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.studyDirectory_ = ''
        self.inputNames = []
        self.samples = None
        self.outputs = None
        self.results = None
        self.profiles = None    # {run name: fields} of runs with b2fplasmf
        self.grid = None
        self.prepareUserInterface()

    def sizeHint(self):
        return QSize(560, 420)

    def prepareUserInterface(self):
        layout = QVBoxLayout(self)
        controls = QHBoxLayout()
        controls.addWidget(QLabel('Plot', self))
        self.plotTypeCombo = newCombo(PLOT_TYPES, PLOT_TYPES[0], self)
        self.plotTypeCombo.currentIndexChanged.connect(self.updatePlot)
        controls.addWidget(self.plotTypeCombo)
        self.qoiLabel = QLabel('QoI', self)
        controls.addWidget(self.qoiLabel)
        self.qoiCombo = QComboBox(self)
        self.qoiCombo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.qoiCombo.currentIndexChanged.connect(self.updatePlot)
        controls.addWidget(self.qoiCombo)

        # Controls of "Profiles (all runs)".
        self.profileControls = [QLabel('Location', self)]
        self.locationCombo = newCombo(PROFILE_LOCATIONS, 'OMP', self)
        self.locationCombo.currentIndexChanged.connect(self.updatePlot)
        self.profileControls.append(self.locationCombo)
        self.profileControls.append(QLabel('Variable', self))
        self.variableCombo = newCombo(QOI_VARIABLES, 'te', self)
        self.variableCombo.currentIndexChanged.connect(self.updatePlot)
        self.profileControls.append(self.variableCombo)
        self.reloadButton = QPushButton('Reload runs', self)
        self.reloadButton.setToolTip('Read b2fplasmf of the runs again '
                                     '(e.g. after more runs have finished).')
        self.reloadButton.clicked.connect(self.reloadProfiles)
        self.profileControls.append(self.reloadButton)
        for widget in self.profileControls:
            controls.addWidget(widget)
        controls.addStretch()
        layout.addLayout(controls)

        self.figure = Figure(figsize=(6, 3.5), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(NavigationToolbar(self.canvas, self))
        layout.addWidget(self.canvas, 1)

    # ------------------------------------------------------------------
    # Slots and properties
    # ------------------------------------------------------------------
    @Slot(str)
    def setStudy(self, studyDir):
        """Read the study files that exist and redraw."""
        self.studyDirectory_ = studyDir
        self.samples = self.outputs = self.results = None
        self.profiles = self.grid = None
        try:
            samplesPath = os.path.join(studyDir, SAMPLES_FILE)
            if os.path.isfile(samplesPath):
                self.inputNames, _, self.samples = readCsv(samplesPath)
            outputsPath = os.path.join(studyDir, OUTPUTS_FILE)
            if os.path.isfile(outputsPath) and self.samples is not None:
                qoiNames, ids, values = readCsv(outputsPath)
                self.outputs = (qoiNames, self.samples[np.asarray(ids) - 1], values)
            self.results = readResults(studyDir)
        except Exception as error:
            self.logMessage.emit(f'[UQ Plot] cannot read {studyDir}: {error}')

        current = self.qoiCombo.currentText()
        self.qoiCombo.blockSignals(True)
        self.qoiCombo.clear()
        if self.outputs is not None:
            self.qoiCombo.addItems(self.outputs[0])
            if current in self.outputs[0]:
                self.qoiCombo.setCurrentText(current)
        self.qoiCombo.blockSignals(False)
        self.updatePlot()

    def getStudy(self):
        return self.studyDirectory_

    studyDirectory = Property(str, getStudy, setStudy, doc='Directory of the UQ study')

    @Slot(str)
    def setPlotType(self, plotType):
        self.plotTypeCombo.setCurrentText(plotType)

    def getPlotType(self):
        return self.plotTypeCombo.currentText()

    plotType = Property(str, getPlotType, setPlotType,
                        doc="Sobol' indices, Histogram, Scatter vs inputs or Input samples")

    @Slot(str)
    def setLocation(self, location):
        self.locationCombo.setCurrentText(location)

    def getLocation(self):
        return self.locationCombo.currentText()

    location = Property(str, getLocation, setLocation,
                        doc='OMP, Outer target or Inner target (profiles)')

    @Slot(str)
    def setVariable(self, variable):
        self.variableCombo.setCurrentText(variable)

    def getVariable(self):
        return self.variableCombo.currentText()

    variable = Property(str, getVariable, setVariable, doc='te, ti, ne or ni (profiles)')

    @Slot()
    def reloadProfiles(self):
        self.profiles = None
        self.updatePlot()

    def loadProfiles(self):
        """Read the grid of the base run and b2fplasmf of every run that has
        one. Kept until the study changes or 'Reload runs' is pressed.
        """
        setup = readSetup(self.studyDirectory_) if self.studyDirectory_ else {}
        if not setup or self.samples is None:
            return
        if self.grid is None:
            geometryDir = findGeometry(setup.get('base_run', ''))
            if geometryDir is None:
                self.logMessage.emit('[UQ Plot] b2fgmtry of the base run not found')
                return
            self.grid = GridLocations(geometryDir)
        self.profiles = {}
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        try:
            for runDir in runDirs(self.studyDirectory_, setup.get('prefix', 'sample_'),
                                  len(self.samples)):
                if os.path.isfile(os.path.join(runDir, 'b2fplasmf')):
                    try:
                        self.profiles[os.path.basename(runDir)] = readFields(runDir)
                    except Exception as error:
                        self.logMessage.emit(f'[UQ Plot] {os.path.basename(runDir)}: {error}')
        finally:
            QApplication.restoreOverrideCursor()
        self.logMessage.emit(f'[UQ Plot] profiles of {len(self.profiles)} runs read')

    @Slot(str)
    def saveFigure(self, path):
        self.figure.savefig(path, dpi=150, bbox_inches='tight')

    # ------------------------------------------------------------------
    # Plots
    # ------------------------------------------------------------------
    def message(self, text):
        ax = self.figure.add_subplot(111)
        ax.text(0.5, 0.5, text, ha='center', va='center', transform=ax.transAxes)
        ax.set_axis_off()

    @Slot()
    def updatePlot(self):
        self.figure.clear()
        plotType = self.plotTypeCombo.currentText()
        k = self.qoiCombo.currentIndex()
        names = self.inputNames
        profiles = plotType == 'Profiles (all runs)'
        for widget in self.profileControls:
            widget.setVisible(profiles)
        self.qoiLabel.setVisible(not profiles and plotType != 'Input samples')
        self.qoiCombo.setVisible(not profiles and plotType != 'Input samples')

        if profiles:
            if self.profiles is None:
                self.loadProfiles()
            if not self.profiles:
                self.message('No runs with b2fplasmf yet')
            else:
                self.plotProfiles()
        elif plotType == 'Input samples':
            if self.samples is None:
                self.message('No samples yet')
            else:
                n = len(names)
                axes = self.figure.subplots(n, n, squeeze=False)
                for i in range(n):
                    for j in range(n):
                        ax = axes[i][j]
                        if i == j:
                            ax.hist(self.samples[:, i], bins='auto', color='#1f77b4')
                        else:
                            ax.scatter(self.samples[:, j], self.samples[:, i], s=6)
                        ax.tick_params(labelsize=7)
                        if i == n - 1:
                            ax.set_xlabel(names[j], fontsize=8)
                        if j == 0:
                            ax.set_ylabel(names[i], fontsize=8)
        elif self.outputs is None or k < 0:
            self.message('No outputs yet (waiting for outputsCollected)')
        elif plotType == "Sobol' indices":
            qoiName = self.qoiCombo.currentText()
            result = next((r for r in self.results or [] if r['qoi'] == qoiName), None)
            if result is None:
                self.message("No Sobol' indices yet (waiting for resultsReady)")
            else:
                ax = self.figure.add_subplot(111)
                position = np.arange(len(names))
                ax.bar(position - 0.2, result['S1'], 0.4, label='First order $S_1$',
                       color='#1f77b4')
                ax.bar(position + 0.2, result['ST'], 0.4, label='Total $S_T$',
                       color='#ff7f0e')
                ax.set_xticks(position, names)
                ax.set_ylim(0, 1.05)
                ax.set_ylabel("Sobol' index")
                ax.set_title(f"{qoiName}  ({result['metamodel']}, "
                             f"$Q^2$ = {result['Q2']:.3f})")
                ax.legend()
        else:
            qoiName = self.qoiCombo.currentText()
            _, X, Y = self.outputs
            if plotType == 'Histogram':
                ax = self.figure.add_subplot(111)
                ax.hist(Y[:, k], bins='auto', color='#1f77b4', edgecolor='white')
                ax.axvline(Y[:, k].mean(), color='k', linestyle='--', label='mean')
                ax.set_xlabel(qoiName)
                ax.set_ylabel('Number of runs')
                ax.legend()
            else:
                axes = self.figure.subplots(1, len(names), sharey=True, squeeze=False)[0]
                for j, ax in enumerate(axes):
                    ax.scatter(X[:, j], Y[:, k], s=12)
                    ax.set_xlabel(names[j])
                axes[0].set_ylabel(qoiName)
        self.figure.tight_layout()
        self.canvas.draw_idle()

    def plotProfiles(self):
        location = self.locationCombo.currentText()
        variable = self.variableCombo.currentText()
        cvs, x, xlabel = self.grid.profile(location)
        Y = np.array([fields[variable][cvs - 1] for fields in self.profiles.values()])
        label, unit = VARIABLE_LABELS[variable]
        ax = self.figure.add_subplot(111)
        for y in Y:
            ax.plot(x, y, color='0.6', linewidth=0.7, alpha=0.6)
        ax.plot([], [], color='0.6', linewidth=0.7, label=f'runs ({len(Y)})')
        ax.fill_between(x, np.quantile(Y, 0.05, axis=0), np.quantile(Y, 0.95, axis=0),
                        color='#1f77b4', alpha=0.25, label='5-95 %')
        ax.plot(x, Y.mean(axis=0), color='#1f77b4', linewidth=2, label='mean')
        ax.axvline(0.0, color='k', linestyle='--', linewidth=0.8, label='separatrix')
        ax.set_xlabel(xlabel)
        ax.set_ylabel(f'{label} [{unit}]')
        ax.set_title(f'{label} at {location}')
        ax.legend(fontsize=8)


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = UQPlotActor()
    widget.logMessage.connect(print)
    if len(sys.argv) > 1:
        widget.setStudy(sys.argv[1])
    widget.show()
    sys.exit(app.exec())
