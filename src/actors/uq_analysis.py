#!/usr/bin/env python3
"""UQ Analysis actor: reads the quantities of interest (QoI) from b2fplasmf
of every sample run, fits a PCE or Kriging metamodel with OpenTURNS and
computes Sobol' indices. Writes uq_outputs.csv and uq_results.csv.
"""

import csv
import os
import re

import numpy as np

from PySide6.QtCore import Slot, Signal, Property, QSize
from PySide6.QtWidgets import (QGridLayout, QGroupBox, QPushButton, QVBoxLayout,
                               QHBoxLayout, QMessageBox, QWidget, QTableWidgetItem,
                               QSpinBox, QLabel, QProgressBar, QTableWidget)

from uq_common import (QOI_VARIABLES, QOI_STATISTICS, METAMODELS, DEFAULT_QOIS,
                       LOCATIONS, RING_CHOICES, SAMPLES_FILE, OUTPUTS_FILE,
                       RESULTS_FILE, readSetup, updateSetup, readCsv, inputNames,
                       runDirs, writeCsv, jointDistribution, fitMetamodel,
                       crossValidationQ2, readQois, findGeometry, GridLocations,
                       newTable, newCombo, UQWorkerMixin)


class UQAnalysisActor(UQWorkerMixin, QWidget):
    """ UQAnalysisActor(QWidget)

        Collects outputs of a UQ study and computes its statistics.

        Attributes:
            outputsCollected(str): Signal emits the study directory when
                uq_outputs.csv is written or loaded.
            resultsReady(str): Signal emits the study directory when
                uq_results.csv is written or loaded.
            busy(bool): Signal emits True when a task starts, False at end.
            logMessage(str): Signal emits progress and error messages.
    """
    icon = ''

    outputsCollected = Signal(str)
    resultsReady = Signal(str)
    busy = Signal(bool)
    logMessage = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.studyDirectory_ = ''
        self.setup = {}
        self.samples = None
        self.outputs = None
        self.prepareUserInterface()
        self.updateButtons()

    def sizeHint(self):
        return QSize(520, 420)

    def prepareUserInterface(self):
        layout = QGridLayout(self)

        self.studyLabel = QLabel('Study: none (waiting for samplesReady)', self)
        layout.addWidget(self.studyLabel, 0, 0, 1, 2)

        qoiBox = QGroupBox('Quantities of interest (from b2fplasmf)', self)
        qoiLayout = QVBoxLayout(qoiBox)
        self.qoiTable = newTable(['Name', 'Variable', 'Location', 'Rings', 'Statistic'],
                                 qoiBox)
        self.qoiTable.setToolTip(
            'Rings: separatrix, separatrix+1, SOL, inside separatrix, all, or ring '
            'numbers such as 9, 10 or 9-12 (1 = innermost ring).\n'
            'With Location "Custom CVs" type SOLPS cell numbers instead.\n'
            'With several cells the statistic (mean, max, min) is taken over them; '
            '"value" uses the first cell.')
        qoiLayout.addWidget(self.qoiTable)
        buttons = QHBoxLayout()
        addButton = QPushButton('+ Add', qoiBox)
        addButton.clicked.connect(lambda: self.addQoiRow())
        removeButton = QPushButton('- Remove', qoiBox)
        removeButton.clicked.connect(
            lambda: self.qoiTable.removeRow(self.qoiTable.currentRow()))
        self.collectButton = QPushButton('Collect outputs', qoiBox)
        self.collectButton.clicked.connect(self.collectOutputs)
        buttons.addWidget(addButton)
        buttons.addWidget(removeButton)
        buttons.addStretch()
        buttons.addWidget(self.collectButton)
        qoiLayout.addLayout(buttons)
        layout.addWidget(qoiBox, 1, 0, 1, 2)

        modelBox = QGroupBox("Metamodel and Sobol' indices", self)
        modelLayout = QVBoxLayout(modelBox)
        controls = QHBoxLayout()
        controls.addWidget(QLabel('Metamodel', modelBox))
        self.metamodelCombo = newCombo(METAMODELS, 'PCE', modelBox)
        controls.addWidget(self.metamodelCombo)
        controls.addWidget(QLabel('PCE degree', modelBox))
        self.degreeSpin = QSpinBox(modelBox, minimum=1, maximum=6, value=2)
        controls.addWidget(self.degreeSpin)
        controls.addStretch()
        self.analyseButton = QPushButton('Fit metamodel + Sobol', modelBox)
        self.analyseButton.clicked.connect(self.analyse)
        controls.addWidget(self.analyseButton)
        modelLayout.addLayout(controls)
        self.resultsTable = QTableWidget(0, 0, modelBox)
        self.resultsTable.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        modelLayout.addWidget(self.resultsTable)
        self.progressBar = QProgressBar(modelBox)
        self.progressBar.setRange(0, 0)
        self.progressBar.setMaximumHeight(10)
        self.progressBar.setTextVisible(False)
        modelLayout.addWidget(self.progressBar)
        layout.addWidget(modelBox, 2, 0, 1, 2)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 1)

        for row in DEFAULT_QOIS:
            self.addQoiRow(*row)

    def addQoiRow(self, name='', variable='te', location='OMP', rings='separatrix',
                  statistic='value'):
        row = self.qoiTable.rowCount()
        self.qoiTable.insertRow(row)
        self.qoiTable.setItem(row, 0, QTableWidgetItem(name))
        self.qoiTable.setCellWidget(row, 1, newCombo(QOI_VARIABLES, variable,
                                                     self.qoiTable))
        self.qoiTable.setCellWidget(row, 2, newCombo(LOCATIONS, location,
                                                     self.qoiTable))
        ringsCombo = newCombo(RING_CHOICES, rings, self.qoiTable)
        ringsCombo.setEditable(True)
        ringsCombo.setCurrentText(rings)
        self.qoiTable.setCellWidget(row, 3, ringsCombo)
        self.qoiTable.setCellWidget(row, 4, newCombo(QOI_STATISTICS, statistic,
                                                     self.qoiTable))

    def updateButtons(self):
        running = self.isBusy()
        self.collectButton.setEnabled(self.samples is not None and not running)
        self.analyseButton.setEnabled(self.outputs is not None and not running)
        self.progressBar.setVisible(running)

    @Slot(str)
    def log(self, text):
        self.logMessage.emit(f'[UQ Analysis] {text.rstrip()}')

    # ------------------------------------------------------------------
    # Slots and properties
    # ------------------------------------------------------------------
    @Slot(str)
    def setStudy(self, studyDir):
        """Load the study; existing outputs and results are shown and
        re-emitted so that connected plot actors are updated.
        """
        self.studyDirectory_ = studyDir
        self.setup = readSetup(studyDir)
        samplesPath = os.path.join(studyDir, SAMPLES_FILE)
        self.samples = readCsv(samplesPath)[2] if os.path.isfile(samplesPath) else None
        if self.setup.get('qois'):
            self.qoiTable.setRowCount(0)
            for qoi in self.setup['qois']:
                if 'location' in qoi:
                    self.addQoiRow(qoi['name'], qoi['variable'], qoi['location'],
                                   qoi['rings'], qoi['statistic'])
                else:
                    self.addQoiRow(qoi['name'], qoi['variable'], 'Custom CVs',
                                   ', '.join(str(cv) for cv in qoi['cvs']),
                                   qoi['statistic'])
        analysis = self.setup.get('analysis', {})
        self.metamodelCombo.setCurrentText(analysis.get('metamodel', 'PCE'))
        self.degreeSpin.setValue(analysis.get('degree', 2))
        self.studyLabel.setText(f'Study: <b>{os.path.basename(studyDir)}</b>')
        self.studyLabel.setToolTip(studyDir)

        self.outputs = None
        self.resultsTable.setRowCount(0)
        outputsPath = os.path.join(studyDir, OUTPUTS_FILE)
        if os.path.isfile(outputsPath) and self.samples is not None:
            self.loadOutputs()
            self.showStatistics()
            self.outputsCollected.emit(studyDir)
            if os.path.isfile(os.path.join(studyDir, RESULTS_FILE)):
                self.showResultsFile()
                self.resultsReady.emit(studyDir)
        self.updateButtons()

    def getStudy(self):
        return self.studyDirectory_

    studyDirectory = Property(str, getStudy, setStudy, doc='Directory of the UQ study')

    @Slot(str)
    def collect(self, studyDir):
        """Load the study and collect its outputs (e.g. from runsFinished)."""
        self.setStudy(studyDir)
        self.collectOutputs()

    @Slot(str)
    def setMetamodel(self, kind):
        self.metamodelCombo.setCurrentText(kind)

    def getMetamodel(self):
        return self.metamodelCombo.currentText()

    metamodel = Property(str, getMetamodel, setMetamodel, doc='PCE or Kriging')

    @Slot(int)
    def setPceDegree(self, degree):
        self.degreeSpin.setValue(degree)

    def getPceDegree(self):
        return self.degreeSpin.value()

    pceDegree = Property(int, getPceDegree, setPceDegree, doc='PCE total degree')

    # ------------------------------------------------------------------
    # Outputs
    # ------------------------------------------------------------------
    def qois(self):
        """QoIs of the table with their cell numbers resolved on the grid of
        the base run. Raises ValueError for unknown rings or a missing grid.
        """
        baseRun = self.setup.get('base_run', '')
        geometryDir = findGeometry(baseRun) if baseRun else None
        grid = GridLocations(geometryDir) if geometryDir else None
        qois = []
        for row in range(self.qoiTable.rowCount()):
            name = self.qoiTable.item(row, 0)
            qoi = {
                'name': name.text().strip() if name else f'qoi{row + 1}',
                'variable': self.qoiTable.cellWidget(row, 1).currentText(),
                'location': self.qoiTable.cellWidget(row, 2).currentText(),
                'rings': self.qoiTable.cellWidget(row, 3).currentText().strip(),
                'statistic': self.qoiTable.cellWidget(row, 4).currentText(),
            }
            if qoi['location'] == 'Custom CVs':
                qoi['cvs'] = [int(cv) for cv in re.split(r'[,\s]+', qoi['rings']) if cv]
            elif grid is None:
                raise ValueError(f'b2fgmtry not found for the base run {baseRun}')
            else:
                qoi['cvs'] = grid.cvs(qoi['location'], qoi['rings'])
            qois.append(qoi)
        return qois

    def loadOutputs(self):
        header, ids, values = readCsv(os.path.join(self.studyDirectory_, OUTPUTS_FILE))
        self.outputs = (header, ids, self.samples[np.asarray(ids) - 1], values)

    @Slot()
    def collectOutputs(self):
        if self.samples is None:
            QMessageBox.warning(self, 'UQ', 'No samples. Generate or load a study first.')
            return
        try:
            qois = self.qois()
        except ValueError as error:
            QMessageBox.warning(self, 'UQ', str(error))
            return
        if not qois or any(not qoi['cvs'] for qoi in qois):
            QMessageBox.warning(self, 'UQ', 'Every QoI needs at least one cell.')
            return
        for qoi in qois:
            cells = ', '.join(str(cv) for cv in qoi['cvs'][:6])
            more = ', ...' if len(qoi['cvs']) > 6 else ''
            self.log(f"{qoi['name']}: {qoi['location']}, {qoi['rings']} "
                     f"-> {len(qoi['cvs'])} cell(s) [{cells}{more}]")
        self.setup = updateSetup(self.studyDirectory_, qois=qois)
        dirs = runDirs(self.studyDirectory_, self.setup.get('prefix', 'sample_'),
                       len(self.samples))
        studyDir = self.studyDirectory_

        def work(log):
            ids, outputs = [], []
            for i, runDir in enumerate(dirs, start=1):
                name = os.path.basename(runDir)
                if not os.path.isfile(os.path.join(runDir, 'b2fplasmf')):
                    log(f'{name}: no b2fplasmf, skipped')
                    continue
                try:
                    values = readQois(runDir, qois)
                except Exception as error:
                    log(f'{name}: FAILED ({error})')
                    continue
                if not np.all(np.isfinite(values)):
                    log(f'{name}: NaN/Inf in outputs, skipped')
                    continue
                ids.append(i)
                outputs.append(values)
            log(f'Collected {len(ids)}/{len(dirs)} runs.')
            if ids:
                writeCsv(os.path.join(studyDir, OUTPUTS_FILE),
                         [q['name'] for q in qois], outputs, ids)
            return len(ids)

        def done(count):
            if not count:
                return
            self.loadOutputs()
            self.resultsTable.setRowCount(0)
            self.showStatistics()
            self.log(f'Outputs written to {os.path.join(studyDir, OUTPUTS_FILE)}')
            self.outputsCollected.emit(studyDir)

        self.startWorker(work, done)

    # ------------------------------------------------------------------
    # Metamodel and Sobol' indices
    # ------------------------------------------------------------------
    @Slot()
    def analyse(self):
        if self.outputs is None:
            QMessageBox.warning(self, 'UQ', 'Collect outputs first.')
            return
        try:
            import openturns as ot
            distribution = jointDistribution(self.setup['inputs'])
        except Exception as error:
            QMessageBox.warning(self, 'UQ', str(error))
            return
        try:
            ot.TBB.SetNumberOfThreads(2)
        except AttributeError:
            pass
        # Kriging prints a warning for every scale bound adjustment.
        ot.Log.Show(ot.Log.ERROR)
        qoiNames, ids, X, Y = self.outputs
        names = inputNames(self.setup['inputs'])
        kind = self.metamodelCombo.currentText()
        degree = self.degreeSpin.value()
        self.setup = updateSetup(self.studyDirectory_,
                                 analysis={'metamodel': kind, 'degree': degree})
        studyDir = self.studyDirectory_

        def work(log):
            rows = []
            for k, qoiName in enumerate(qoiNames):
                y = Y[:, k]
                metamodel, pceResult = fitMetamodel(X, y, distribution, kind, degree)
                q2 = crossValidationQ2(X, y, distribution, kind, degree)
                if pceResult is not None:
                    sobol = ot.FunctionalChaosSobolIndices(pceResult)
                    first = [sobol.getSobolIndex(i) for i in range(len(names))]
                    total = [sobol.getSobolTotalIndex(i) for i in range(len(names))]
                else:
                    size = 2000
                    inputDesign = ot.SobolIndicesExperiment(distribution, size).generate()
                    algorithm = ot.SaltelliSensitivityAlgorithm(
                        inputDesign, metamodel(inputDesign), size)
                    first = list(algorithm.getFirstOrderIndices())
                    total = list(algorithm.getTotalOrderIndices())
                rows.append([qoiName, kind, y.mean(), y.std(ddof=1), np.quantile(y, 0.05),
                             np.quantile(y, 0.95), q2] + first + total)
                log(f'{qoiName}: Q2={q2:.3f}  ' + '  '.join(
                    f'{n}: S1={s:.2f} ST={t:.2f}' for n, s, t in zip(names, first, total)))
            with open(os.path.join(studyDir, RESULTS_FILE), 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['qoi', 'metamodel', 'mean', 'std', 'q05', 'q95', 'Q2'] +
                                [f'S1_{n}' for n in names] + [f'ST_{n}' for n in names])
                for row in rows:
                    writer.writerow(row[:2] + [f'{v:.6g}' for v in row[2:]])

        def done(_):
            self.showResultsFile()
            self.log(f'Results written to {os.path.join(studyDir, RESULTS_FILE)}')
            self.resultsReady.emit(studyDir)

        self.log(f'Fitting {kind} metamodels on {len(ids)} runs...')
        self.startWorker(work, done)

    # ------------------------------------------------------------------
    # Tables
    # ------------------------------------------------------------------
    def showStatistics(self):
        qoiNames, _, _, Y = self.outputs
        rows = [[Y[:, k].mean(), Y[:, k].std(ddof=1), np.quantile(Y[:, k], 0.05),
                 np.quantile(Y[:, k], 0.95)] for k in range(Y.shape[1])]
        self.showTable(['mean', 'std', 'q05', 'q95'], qoiNames, rows)

    def showResultsFile(self):
        with open(os.path.join(self.studyDirectory_, RESULTS_FILE), newline='') as f:
            rows = list(csv.reader(f))
        header = rows[0][2:]
        self.showTable(header, [row[0] for row in rows[1:]],
                       [[float(v) for v in row[2:]] for row in rows[1:]])

    def showTable(self, header, rowNames, rows):
        self.resultsTable.setColumnCount(len(header))
        self.resultsTable.setHorizontalHeaderLabels(header)
        self.resultsTable.setRowCount(len(rows))
        self.resultsTable.setVerticalHeaderLabels(rowNames)
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.resultsTable.setItem(i, j, QTableWidgetItem(f'{value:.4g}'))
        self.resultsTable.resizeColumnsToContents()


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = UQAnalysisActor()
    widget.logMessage.connect(print)
    if len(sys.argv) > 1:
        widget.setStudy(sys.argv[1])
    widget.show()
    sys.exit(app.exec())
