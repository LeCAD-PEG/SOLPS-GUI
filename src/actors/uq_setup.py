#!/usr/bin/env python3
"""UQ Setup actor: uncertain inputs of the selected run and their sampling
with OpenTURNS. Writes uq_setup.json and uq_samples.csv to the study
directory and emits samplesReady(studyDir).
"""

import os

import numpy as np

from PySide6.QtCore import Slot, Signal, Property, QSize
from PySide6.QtWidgets import (QGridLayout, QGroupBox, QPushButton, QVBoxLayout,
                               QHBoxLayout, QMessageBox, QWidget, QTableWidgetItem,
                               QSpinBox, QLineEdit, QFormLayout, QFileDialog,
                               QToolButton, QLabel, QMenu)

from uq_common import (DISTRIBUTIONS, SAMPLING_METHODS, DEFAULT_INPUTS, INPUT_PRESETS,
                       SAMPLES_FILE, getNamelistValue, parseIndex, indexText, readSetup,
                       updateSetup, inputNames, writeCsv, jointDistribution,
                       duplicateVariables, newTable, newCombo)


class UQSetupActor(QWidget):
    """ UQSetupActor(QWidget)

        Defines the uncertain inputs of the base run and samples them.

        Attributes:
            baseRunChanged(str): Signal emits the selected base run.
            studyDirChanged(str): Signal emits the new study directory.
            samplesReady(str): Signal emits the study directory once
                uq_samples.csv is written or an existing study is loaded.
            logMessage(str): Signal emits progress and error messages.
    """
    icon = ''

    baseRunChanged = Signal(str)
    studyDirChanged = Signal(str)
    samplesReady = Signal(str)
    logMessage = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.runDir = ''
        self.prepareUserInterface()
        self.updateButtons()

    def sizeHint(self):
        return QSize(520, 420)

    def prepareUserInterface(self):
        layout = QGridLayout(self)

        self.runLabel = QLabel('Base run: none selected', self)
        layout.addWidget(self.runLabel, 0, 0, 1, 2)

        inputsBox = QGroupBox('Uncertain inputs', self)
        inputsLayout = QVBoxLayout(inputsBox)
        self.inputsTable = newTable(
            ['Name', 'File', 'Variable', 'Index', 'Nominal', 'Distribution', 'Spread (%)'],
            inputsBox)
        self.inputsTable.setToolTip(
            'Name is used in the tables and plots.\n'
            'Index = position of the value in the namelist entry '
            '(PARM_DNA= 0.00, 1.5 → index 2); "1,2" sets both to the same value.\n'
            'Several variables separated by ";" all get the same value.\n'
            'Spread: half-width (Uniform) or standard deviation (Normal, LogNormal) '
            'in % of nominal.')
        inputsLayout.addWidget(self.inputsTable)
        buttons = QHBoxLayout()
        addButton = QToolButton(inputsBox, text='+ Add')
        addButton.setToolTip('Choose an input to add')
        addButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        addMenu = QMenu(addButton)
        groups = {}
        for group, label, *preset in INPUT_PRESETS:
            if group not in groups:
                groups[group] = addMenu.addMenu(group)
            action = groups[group].addAction(label)
            action.setToolTip(f'{preset[2]} in {preset[1]}')
            action.triggered.connect(lambda checked=False, p=preset: self.addPreset(*p))
        addMenu.addSeparator()
        addMenu.addAction('Other (empty row)...').triggered.connect(
            lambda: self.addInputRow())
        addMenu.setToolTipsVisible(True)
        addButton.setMenu(addMenu)
        removeButton = QPushButton('- Remove', inputsBox)
        removeButton.clicked.connect(
            lambda: self.inputsTable.removeRow(self.inputsTable.currentRow()))
        self.nominalButton = QPushButton('Read nominal values', inputsBox)
        self.nominalButton.clicked.connect(self.readNominalValues)
        buttons.addWidget(addButton)
        buttons.addWidget(removeButton)
        buttons.addStretch()
        buttons.addWidget(self.nominalButton)
        inputsLayout.addLayout(buttons)
        layout.addWidget(inputsBox, 1, 0, 1, 2)

        samplingBox = QGroupBox('Sampling', self)
        form = QFormLayout(samplingBox)
        self.methodCombo = newCombo(SAMPLING_METHODS, 'LHS', samplingBox)
        form.addRow('Method', self.methodCombo)
        self.sizeSpin = QSpinBox(samplingBox, minimum=2, maximum=100, value=30)
        self.sizeSpin.setToolTip('At most 100 runs (Slurm limit of active jobs per user).')
        form.addRow('Samples', self.sizeSpin)
        self.seedSpin = QSpinBox(samplingBox, minimum=0, maximum=2**31 - 1, value=42)
        form.addRow('Seed', self.seedSpin)
        layout.addWidget(samplingBox, 2, 0)

        studyBox = QGroupBox('Study', self)
        form = QFormLayout(studyBox)
        dirLayout = QHBoxLayout()
        self.studyDirEdit = QLineEdit(studyBox)
        self.studyDirEdit.setPlaceholderText('default: <run>/../UQ_study')
        self.studyDirEdit.textChanged.connect(self.studyDirChanged)
        browseButton = QToolButton(studyBox, text='...')
        browseButton.clicked.connect(self.browseStudyDir)
        dirLayout.addWidget(self.studyDirEdit)
        dirLayout.addWidget(browseButton)
        form.addRow('Directory', dirLayout)
        self.prefixEdit = QLineEdit('sample_', studyBox)
        form.addRow('Run prefix', self.prefixEdit)
        layout.addWidget(studyBox, 2, 1)

        actions = QHBoxLayout()
        self.loadButton = QPushButton('Load study...', self)
        self.loadButton.clicked.connect(self.loadStudy)
        self.generateButton = QPushButton('Generate samples', self)
        self.generateButton.setToolTip('Sample the inputs and emit samplesReady.')
        self.generateButton.clicked.connect(self.generateSamples)
        actions.addWidget(self.loadButton)
        actions.addStretch()
        actions.addWidget(self.generateButton)
        layout.addLayout(actions, 3, 0, 1, 2)
        layout.setRowStretch(1, 1)

        for row in DEFAULT_INPUTS:
            self.addInputRow(*row)

    def addInputRow(self, name='', fileName='b2.transport.parameters', variable='',
                    index=1, distribution='Uniform', spread=10.0, nominal=''):
        row = self.inputsTable.rowCount()
        self.inputsTable.insertRow(row)
        self.inputsTable.setItem(row, 0, QTableWidgetItem(name))
        self.inputsTable.setItem(row, 1, QTableWidgetItem(fileName))
        self.inputsTable.setItem(row, 2, QTableWidgetItem(variable))
        self.inputsTable.setItem(row, 3, QTableWidgetItem(indexText(index)))
        self.inputsTable.setItem(row, 4, QTableWidgetItem(str(nominal)))
        self.inputsTable.setCellWidget(row, 5, newCombo(DISTRIBUTIONS, distribution,
                                                        self.inputsTable))
        self.inputsTable.setItem(row, 6, QTableWidgetItem(str(spread)))
        return row

    def addPreset(self, name, fileName, variable, index):
        """Add an input chosen from the '+ Add' menu and read its nominal
        value from the base run.
        """
        if name in inputNames(self.inputs()):
            self.log(f'{name} is already in the table.')
            return
        row = self.addInputRow(name, fileName, variable, index)
        if self.runDir:
            self.readNominalValue(row)

    def updateButtons(self):
        self.nominalButton.setEnabled(bool(self.runDir))
        self.generateButton.setEnabled(bool(self.runDir))

    @Slot(str)
    def log(self, text):
        self.logMessage.emit(f'[UQ Setup] {text.rstrip()}')

    # ------------------------------------------------------------------
    # Slots and properties
    # ------------------------------------------------------------------
    @Slot(str)
    def setRunDir(self, rundir):
        self.runDir = rundir or ''
        name = os.path.basename(os.path.normpath(self.runDir)) if self.runDir else ''
        self.runLabel.setText(f'Base run: <b>{name}</b>' if name
                              else 'Base run: none selected')
        self.runLabel.setToolTip(self.runDir)
        self.updateButtons()
        self.baseRunChanged.emit(self.runDir)

    def getRunDir(self):
        return self.runDir

    run_dir = Property(str, getRunDir, setRunDir, doc='Base run directory')

    @Slot(str)
    def setStudyDirectory(self, directory):
        self.studyDirEdit.setText(directory)

    def getStudyDirectory(self):
        return self.studyDirEdit.text()

    studyDirectory = Property(str, getStudyDirectory, setStudyDirectory,
                              doc='Directory of the UQ study')

    @Slot(str)
    def setRunPrefix(self, prefix):
        self.prefixEdit.setText(prefix)

    def getRunPrefix(self):
        return self.prefixEdit.text()

    runPrefix = Property(str, getRunPrefix, setRunPrefix,
                         doc='Prefix of the sample run directories')

    @Slot(str)
    def setSamplingMethod(self, method):
        self.methodCombo.setCurrentText(method)

    def getSamplingMethod(self):
        return self.methodCombo.currentText()

    samplingMethod = Property(str, getSamplingMethod, setSamplingMethod,
                              doc="LHS, Monte Carlo or Sobol' sequence")

    @Slot(int)
    def setNumberOfSamples(self, size):
        self.sizeSpin.setValue(size)

    def getNumberOfSamples(self):
        return self.sizeSpin.value()

    numberOfSamples = Property(int, getNumberOfSamples, setNumberOfSamples,
                               doc='Number of samples (at most 100)')

    @Slot(int)
    def setSeed(self, seed):
        self.seedSpin.setValue(seed)

    def getSeed(self):
        return self.seedSpin.value()

    seed = Property(int, getSeed, setSeed, doc='Random seed')

    # ------------------------------------------------------------------
    # Study
    # ------------------------------------------------------------------
    def studyDir(self):
        directory = self.studyDirEdit.text().strip()
        if not directory and self.runDir:
            directory = os.path.join(os.path.dirname(os.path.normpath(self.runDir)),
                                     'UQ_study')
            self.studyDirEdit.setText(directory)
        return directory

    @Slot()
    def browseStudyDir(self):
        directory = QFileDialog.getExistingDirectory(self, 'Select study directory',
                                                     self.studyDir() or os.getcwd())
        if directory:
            self.studyDirEdit.setText(directory)

    def inputs(self):
        inputs = []
        for row in range(self.inputsTable.rowCount()):
            def cell(column):
                item = self.inputsTable.item(row, column)
                return item.text().strip() if item else ''
            nominal = cell(4)
            inputs.append({
                'name': cell(0),
                'file': cell(1),
                'variable': cell(2),
                'index': parseIndex(cell(3)),
                'nominal': float(nominal) if nominal else None,
                'distribution': self.inputsTable.cellWidget(row, 5).currentText(),
                'spread': float(cell(6) or 0.0),
            })
        return inputs

    @Slot()
    def readNominalValues(self):
        if not self.runDir:
            return
        for row in range(self.inputsTable.rowCount()):
            self.readNominalValue(row)

    def readNominalValue(self, row):
        entry = self.inputs()[row]
        path = os.path.join(self.runDir, entry['file'])
        label = entry['name'] or entry['variable']
        try:
            with open(path, 'r', errors='ignore') as f:
                value = getNamelistValue(f.read(), entry['variable'], entry['index'])
        except (OSError, ValueError) as error:
            self.log(f'{label}: {error}')
            return
        self.inputsTable.setItem(row, 4, QTableWidgetItem(f'{value:g}'))
        self.log(f"{label} = {value:g} ({entry['variable']} "
                 f"[{indexText(entry['index'])}] in {entry['file']})")

    @Slot()
    def generateSamples(self):
        if not self.runDir:
            QMessageBox.warning(self, 'UQ', 'Please select a base run first.')
            return
        try:
            import openturns as ot
        except ImportError:
            QMessageBox.critical(self, 'UQ', 'OpenTURNS is not available in this Python.')
            return
        inputs = self.inputs()
        if any(entry['nominal'] is None for entry in inputs):
            self.readNominalValues()
            inputs = self.inputs()
        duplicates = duplicateVariables(inputs)
        if duplicates:
            QMessageBox.warning(self, 'UQ', 'These values are changed by two inputs; '
                                'remove one of them:\n' + '\n'.join(duplicates))
            return
        try:
            distribution = jointDistribution(inputs)
        except ValueError as error:
            QMessageBox.warning(self, 'UQ', str(error))
            return

        studyDir = self.studyDir()
        setup = updateSetup(studyDir, base_run=self.runDir, inputs=inputs,
                            method=self.methodCombo.currentText(),
                            size=self.sizeSpin.value(), seed=self.seedSpin.value(),
                            prefix=self.prefixEdit.text().strip() or 'sample_')
        ot.RandomGenerator.SetSeed(setup['seed'])
        if setup['method'] == 'LHS':
            experiment = ot.LHSExperiment(distribution, setup['size'])
            experiment.setRandomShift(False)
        elif setup['method'] == 'Monte Carlo':
            experiment = ot.MonteCarloExperiment(distribution, setup['size'])
        else:
            experiment = ot.LowDiscrepancyExperiment(ot.SobolSequence(), distribution,
                                                     setup['size'], True)
        samples = np.array(experiment.generate())
        path = writeCsv(os.path.join(studyDir, SAMPLES_FILE), inputNames(inputs), samples)
        self.log(f"{setup['size']} {setup['method']} samples written to {path}")
        for name, marginal in zip(inputNames(inputs),
                                  distribution.getDistributionCollection()):
            self.log(f'  {name}: {marginal}')
        self.samplesReady.emit(studyDir)

    @Slot()
    def loadStudy(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open UQ study',
                                              self.studyDir() or os.getcwd(),
                                              'UQ setup (uq_setup.json)')
        if path:
            self.openStudy(os.path.dirname(path))

    @Slot(str)
    def openStudy(self, studyDir):
        """Fill the actor from an existing study and emit samplesReady."""
        setup = readSetup(studyDir)
        if not setup:
            self.log(f'No uq_setup.json in {studyDir}')
            return
        self.studyDirEdit.setText(studyDir)
        if setup.get('base_run'):
            self.setRunDir(setup['base_run'])
        self.inputsTable.setRowCount(0)
        for entry in setup.get('inputs', []):
            self.addInputRow(entry.get('name', ''), entry['file'], entry['variable'],
                             entry['index'],
                             entry['distribution'], entry['spread'],
                             '' if entry['nominal'] is None else f"{entry['nominal']:g}")
        self.methodCombo.setCurrentText(setup.get('method', 'LHS'))
        self.sizeSpin.setValue(setup.get('size', 30))
        self.seedSpin.setValue(setup.get('seed', 42))
        self.prefixEdit.setText(setup.get('prefix', 'sample_'))
        self.log(f'Loaded UQ study {studyDir}')
        if os.path.isfile(os.path.join(studyDir, SAMPLES_FILE)):
            self.samplesReady.emit(studyDir)


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = UQSetupActor()
    widget.logMessage.connect(print)
    widget.show()
    sys.exit(app.exec())
