#!/usr/bin/env python3
"""Shared helpers for the uncertainty quantification (UQ) actors.

The UQ workflow is split into four actors that are connected with signals in
Qt Designer. Each signal carries the path of the study directory; the actors
exchange data through files in that directory:

    uq_setup.json   - base run, uncertain inputs, sampling, Slurm, QoIs
    uq_samples.csv  - input samples                    (UQSetupActor)
    sample_NNN/     - one SOLPS run per sample         (UQRunsActor)
    uq_outputs.csv  - quantities of interest           (UQAnalysisActor)
    uq_results.csv  - statistics, Q2, Sobol' indices   (UQAnalysisActor)

    UQSetupActor --samplesReady--> UQRunsActor --runsFinished--> UQAnalysisActor
    UQAnalysisActor --outputsCollected/resultsReady--> UQPlotActor
"""

import csv
import json
import os
import re

import numpy as np

from PySide6.QtCore import Signal, QThread
from PySide6.QtWidgets import (QComboBox, QHeaderView, QMessageBox, QTableWidget)

from put_edge_ids import readB2output


EV = 1.602176634e-19

SETUP_FILE = 'uq_setup.json'
SAMPLES_FILE = 'uq_samples.csv'
OUTPUTS_FILE = 'uq_outputs.csv'
RESULTS_FILE = 'uq_results.csv'

DISTRIBUTIONS = ['Uniform', 'Normal', 'LogNormal']
SAMPLING_METHODS = ['LHS', 'Monte Carlo', "Sobol' sequence"]
METAMODELS = ['PCE', 'Kriging']
PARTITIONS = ['all', 'all_debug', 'rigel', 'sun', 'sirius', 'vega']
QOI_VARIABLES = ['te', 'ti', 'ne', 'ni']
QOI_STATISTICS = ['value', 'mean', 'max', 'min']
PLOT_TYPES = ["Sobol' indices", 'Profiles (all runs)', 'Histogram', 'Scatter vs inputs',
              'Input samples']
PROFILE_LOCATIONS = ['OMP', 'Outer target', 'Inner target']
# Variable -> (label, unit) for plots.
VARIABLE_LABELS = {'te': ('$T_e$', 'eV'), 'ti': ('$T_i$', 'eV'),
                   'ne': ('$n_e$', 'm$^{-3}$'), 'ni': ('$n_i$', 'm$^{-3}$')}

# Input files copied from the base run into every sample directory.
FILES_TO_COPY = [
    'b2fgmtry', 'b2fstati', 'b2fpardf', 'b2frates', 'b2mn.dat',
    'b2.boundary.parameters', 'b2.transport.parameters',
    'b2.neutrals.parameters', 'b2.numerics.parameters',
    'b2.user.parameters', 'b2.optimization.parameters',
    'AMJUEL', 'HYDHEL', 'METHANE', 'SPUTER',
]

# Inputs offered by the "+ Add" menu of UQ Setup:
# (menu group, menu text, name, file, variable, index).
# PHYSICAL_LIMITS below keeps sampled values physical.
# Several variables separated by ';' all get the same sampled value, e.g.
# both target recycling strata, or the same power for electrons and ions.
INPUT_PRESETS = [
    ('Transport', 'Particle diffusion D⊥', 'D_perp',
     'b2.transport.parameters', 'PARM_DNA', [2]),
    ('Transport', 'Ion heat diffusion χi', 'chi_i',
     'b2.transport.parameters', 'PARM_HCI', [2]),
    ('Transport', 'Electron heat diffusion χe', 'chi_e',
     'b2.transport.parameters', 'PARM_HCE', [1]),
    ('Core boundary', 'Core density, D+', 'n_core',
     'b2.boundary.parameters', 'CONPAR(0,1,1)', [2]),
    ('Core boundary', 'Core power, electrons', 'P_core_e',
     'b2.boundary.parameters', 'ENEPAR(1,1)', [1]),
    ('Core boundary', 'Core power, ions', 'P_core_i',
     'b2.boundary.parameters', 'ENIPAR(1,1)', [1]),
    ('Core boundary', 'Core power, electrons and ions (same value)', 'P_core_half',
     'b2.boundary.parameters', 'ENEPAR(1,1); ENIPAR(1,1)', [1]),
    ('Recycling', 'Target recycling, both targets (strata 1, 2)', 'R_target',
     'b2.neutrals.parameters', 'recyc(0,1); recyc(0,2)', [1, 2]),
    ('Recycling', 'Recycling, stratum 1', 'R_1',
     'b2.neutrals.parameters', 'recyc(0,1)', [1, 2]),
    ('Recycling', 'Recycling, stratum 2', 'R_2',
     'b2.neutrals.parameters', 'recyc(0,2)', [1, 2]),
    ('Recycling', 'PFR recycling (strata 3, 4)', 'R_pfr',
     'b2.neutrals.parameters', 'recyc(0,3); recyc(0,4)', [1, 2]),
]

# Physical (lower, upper) limit per variable prefix; None = no limit.
# Sampled distributions are truncated to these limits.
PHYSICAL_LIMITS = [
    ('recyc', (0.0, 1.0)),
    ('PARM_', (0.0, None)),
    ('CONPAR', (0.0, None)),
    ('ENEPAR', (0.0, None)),
    ('ENIPAR', (0.0, None)),
]

# Default table: the three transport coefficients, Uniform ±10%.
DEFAULT_INPUTS = [preset[2:] for preset in INPUT_PRESETS if preset[0] == 'Transport']

# Where a QoI is read. "Custom CVs" takes 1-based SOLPS cell numbers in the
# Rings column instead of ring names.
LOCATIONS = ['OMP', 'Outer target', 'Inner target', 'Custom CVs']
RING_CHOICES = ['separatrix', 'separatrix+1', 'separatrix+2', 'SOL',
                'inside separatrix', 'all']

DEFAULT_QOIS = [
    ('Te_OMP_sep', 'te', 'OMP', 'separatrix', 'value'),
    ('ne_OMP_sep', 'ne', 'OMP', 'separatrix', 'value'),
    ('Te_outer_target_sep', 'te', 'Outer target', 'separatrix', 'value'),
    ('ne_outer_target_sep', 'ne', 'Outer target', 'separatrix', 'value'),
    ('Te_inner_target_sep', 'te', 'Inner target', 'separatrix', 'value'),
]

NUMBER = r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][+-]?\d+)?'


# ----------------------------------------------------------------------
# Namelist values in b2.*.parameters
# ----------------------------------------------------------------------
def parseIndex(text):
    """'2' -> [2]; '1,2' or '1 2' -> [1, 2]. Every listed value of the
    namelist entry gets the same sampled value.
    """
    indices = [int(part) for part in re.split(r'[,\s]+', str(text).strip()) if part]
    return indices or [1]


def indexText(index):
    return ','.join(str(i) for i in index) if isinstance(index, list) else str(index)


def _namelistValueSpan(text, name, index):
    """Return the (start, end) span of the index-th (1-based) value of a
    namelist entry such as ``PARM_DNA= 0.00, 1.5,``. Blanks inside the name
    are ignored, so 'CONPAR(0,1,1)' also finds 'CONPAR(0, 1,1)'.
    """
    pattern = r'\s*'.join(re.escape(c) for c in re.sub(r'\s', '', name))
    match = re.search(r'(?<![\w(])' + pattern + r'\s*=', text, flags=re.IGNORECASE)
    if not match:
        raise ValueError(f'{name} not found')
    numbers = re.compile(r'\s*(' + NUMBER + r')\s*,?')
    pos = match.end()
    for k in range(index):
        m = numbers.match(text, pos)
        if not m:
            raise ValueError(f'{name} has fewer than {index} values')
        if k == index - 1:
            return m.span(1)
        pos = m.end()


def variableNames(variable):
    """'recyc(0,1); recyc(0,2)' -> ['recyc(0,1)', 'recyc(0,2)']."""
    return [name.strip() for name in variable.split(';') if name.strip()]


def getNamelistValue(text, variable, index):
    """Value of the first variable at the first index of the list."""
    first = index[0] if isinstance(index, list) else index
    start, end = _namelistValueSpan(text, variableNames(variable)[0], first)
    return float(text[start:end].replace('D', 'E').replace('d', 'e'))


def setNamelistValue(text, variable, index, value):
    """Set the value of every variable at every index of the list."""
    for name in variableNames(variable):
        for i in (index if isinstance(index, list) else [index]):
            start, end = _namelistValueSpan(text, name, i)
            text = text[:start] + f'{float(value):.6g}' + text[end:]
    return text


# ----------------------------------------------------------------------
# Study directory files
# ----------------------------------------------------------------------
def readSetup(studyDir):
    path = os.path.join(studyDir, SETUP_FILE)
    if not os.path.isfile(path):
        return {}
    with open(path) as f:
        return json.load(f)


def updateSetup(studyDir, **entries):
    """Merge entries into uq_setup.json, keeping what other actors wrote."""
    setup = readSetup(studyDir)
    setup.update(entries)
    os.makedirs(studyDir, exist_ok=True)
    with open(os.path.join(studyDir, SETUP_FILE), 'w') as f:
        json.dump(setup, f, indent=2)
    return setup


def inputNames(inputs):
    names = []
    for entry in inputs:
        if entry.get('name'):
            names.append(entry['name'])
            continue
        name = re.sub(r'\s', '', variableNames(entry['variable'])[0])
        index = entry['index'] if isinstance(entry['index'], list) else [entry['index']]
        if index != [1]:
            name += f'[{indexText(index)}]'
        names.append(name)
    return names


def writeCsv(path, header, rows, sampleIds=None):
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['sample'] + list(header))
        for i, row in enumerate(rows):
            sampleId = sampleIds[i] if sampleIds is not None else i + 1
            writer.writerow([sampleId] + [f'{value:.10g}' for value in row])
    return path


def readCsv(path):
    """Return (header, sample ids, values) of a csv written by writeCsv."""
    with open(path, newline='') as f:
        rows = list(csv.reader(f))
    header = rows[0][1:]
    ids = [int(row[0]) for row in rows[1:]]
    values = np.array([[float(v) for v in row[1:]] for row in rows[1:]])
    return header, ids, values


def readResults(studyDir):
    """Return a list of result dicts from uq_results.csv, or None."""
    path = os.path.join(studyDir, RESULTS_FILE)
    if not os.path.isfile(path):
        return None
    with open(path, newline='') as f:
        rows = list(csv.DictReader(f))
    results = []
    for row in rows:
        results.append({
            'qoi': row['qoi'], 'metamodel': row['metamodel'],
            'Q2': float(row['Q2']),
            'S1': [float(v) for k, v in row.items() if k.startswith('S1_')],
            'ST': [float(v) for k, v in row.items() if k.startswith('ST_')],
        })
    return results


def runDirs(studyDir, prefix, count):
    return [os.path.join(studyDir, f'{prefix}{i:03d}') for i in range(1, count + 1)]


# ----------------------------------------------------------------------
# OpenTURNS
# ----------------------------------------------------------------------
def physicalLimits(variable):
    name = variableNames(variable)[0].lower()
    for prefix, limits in PHYSICAL_LIMITS:
        if name.startswith(prefix.lower()):
            return limits
    return (None, None)


def duplicateVariables(inputs):
    """Namelist values changed by more than one input row."""
    seen, duplicates = {}, []
    for entry in inputs:
        index = entry['index'] if isinstance(entry['index'], list) else [entry['index']]
        for name in variableNames(entry['variable']):
            for i in index:
                key = (entry['file'], re.sub(r'\s', '', name).lower(), i)
                if key in seen and seen[key] != entry.get('name'):
                    duplicates.append(f"{name} [{i}] ({seen[key]} and {entry.get('name')})")
                seen[key] = entry.get('name')
    return duplicates


def jointDistribution(inputs):
    """Independent marginals around the nominal values, truncated to the
    physical limits (e.g. recycling <= 1).
    """
    import openturns as ot
    marginals = []
    for entry in inputs:
        nominal = entry['nominal']
        label = entry.get('name') or entry['variable']
        if nominal is None:
            raise ValueError(f"No nominal value for {label}. "
                             "Press 'Read nominal values' first.")
        spread = abs(nominal) * entry['spread'] / 100.0
        if spread <= 0.0:
            raise ValueError(f'Spread of {label} must be larger than 0.')
        low, high = physicalLimits(entry['variable'])
        if entry['distribution'] == 'Uniform':
            a, b = nominal - spread, nominal + spread
            a = a if low is None else max(a, low)
            b = b if high is None else min(b, high)
            if a >= b:
                raise ValueError(f'{label}: range is empty within the limits {low}..{high}.')
            marginal = ot.Uniform(a, b)
        else:
            if entry['distribution'].startswith('Normal'):
                marginal = ot.Normal(nominal, spread)
            else:
                marginal = ot.LogNormalMuSigma(nominal, spread).getDistribution()
            if low is not None and high is not None:
                marginal = ot.TruncatedDistribution(marginal, low, high)
            elif low is not None:
                marginal = ot.TruncatedDistribution(marginal, low,
                                                    ot.TruncatedDistribution.LOWER)
            elif high is not None:
                marginal = ot.TruncatedDistribution(marginal, high,
                                                    ot.TruncatedDistribution.UPPER)
        marginals.append(marginal)
    distribution = ot.JointDistribution(marginals)
    distribution.setDescription(inputNames(inputs))
    return distribution


def fitMetamodel(X, y, distribution, kind, degree):
    import openturns as ot
    inputSample = ot.Sample(X)
    outputSample = ot.Sample(y.reshape(-1, 1))
    dimension = X.shape[1]
    if kind == 'PCE':
        marginals = [ot.StandardDistributionPolynomialFactory(
            distribution.getMarginal(i)) for i in range(dimension)]
        basis = ot.OrthogonalProductPolynomialFactory(marginals)
        size = basis.getEnumerateFunction().getBasisSizeFromTotalDegree(degree)
        algorithm = ot.FunctionalChaosAlgorithm(
            inputSample, outputSample, distribution,
            ot.FixedStrategy(basis, size),
            ot.LeastSquaresStrategy(ot.LeastSquaresMetaModelSelectionFactory(
                ot.LARS(), ot.CorrectedLeaveOneOut())))
        algorithm.run()
        result = algorithm.getResult()
        return result.getMetaModel(), result
    covariance = ot.SquaredExponential([1.0] * dimension, [1.0])
    covariance.setScale(X.std(axis=0) + 1e-12)
    algorithm = ot.KrigingAlgorithm(inputSample, outputSample, covariance,
                                    ot.ConstantBasisFactory(dimension).build())
    algorithm.run()
    return algorithm.getResult().getMetaModel(), None


def crossValidationQ2(X, y, distribution, kind, degree, folds=5):
    """Q2 from k-fold cross-validation: 1 - sum((y - y_cv)^2) / sum((y - mean)^2)."""
    n = len(y)
    prediction = np.empty(n)
    for fold in np.array_split(np.arange(n), min(folds, n)):
        train = np.setdiff1d(np.arange(n), fold)
        metamodel, _ = fitMetamodel(X[train], y[train], distribution, kind, degree)
        prediction[fold] = np.array(metamodel(X[fold])).ravel()
    return 1.0 - np.sum((y - prediction) ** 2) / np.sum((y - y.mean()) ** 2)


# ----------------------------------------------------------------------
# Grid locations (OMP, targets, separatrix) from b2fgmtry
# ----------------------------------------------------------------------
def findGeometry(runDir):
    """Return the directory with b2fgmtry for a run (run, run/baserun or
    ../baserun), or None.
    """
    for directory in (runDir, os.path.join(runDir, 'baserun'),
                      os.path.join(os.path.dirname(os.path.normpath(runDir)), 'baserun')):
        if os.path.isfile(os.path.join(directory, 'b2fgmtry')):
            return directory
    return None


class GridLocations:
    """Translates named locations into SOLPS cell (CV) numbers.

    Rings are numbered 1..ny from the innermost ring outwards and positions
    1..nx along the field lines. The separatrix ring is the first ring whose
    cell in the middle of the grid belongs to the SOL region (cvReg 2), the
    OMP is the cell with the largest R on that ring and the targets are the
    two ends of the rings (the inner target has the smaller R).
    """

    def __init__(self, geometryDir):
        data = readB2output(geometryDir, 'b2fgmtry',
                            variables=['nx,ny,nncut', 'imapCv', 'cvReg', 'cvX', 'cvY'])
        self.nx = int(data['nx,ny,nncut'][0])
        self.ny = int(data['nx,ny,nncut'][1])
        self.imap = np.asarray(data['imapCv'], dtype=int).reshape(
            (self.nx + 2, self.ny + 2), order='F')
        region = np.asarray(data['cvReg'], dtype=int)
        R = self.R = np.asarray(data['cvX'])
        self.Z = np.asarray(data['cvY'])

        middle = self.nx // 2
        sol = [j for j in range(1, self.ny + 1) if region[self.cv(middle, j) - 1] == 2]
        if not sol:
            raise ValueError('no SOL region (cvReg 2) found in b2fgmtry')
        self.separatrix = sol[0]
        positions = [i for i in range(1, self.nx + 1)
                     if region[self.cv(i, self.separatrix) - 1] == 2]
        self.omp = max(positions, key=lambda i: R[self.cv(i, self.separatrix) - 1])
        first = R[self.cv(1, self.separatrix) - 1]
        last = R[self.cv(self.nx, self.separatrix) - 1]
        self.innerTarget, self.outerTarget = (1, self.nx) if first < last else (self.nx, 1)

    def cv(self, i, j):
        return int(self.imap[i, j])

    def profile(self, location):
        """Cells of all rings at the OMP or a target and their distance to the
        separatrix ring in mm: R - R_sep at the OMP, s - s_sep along the target.
        Returns (cvs, x_mm, x label).
        """
        position = {'OMP': self.omp, 'Outer target': self.outerTarget,
                    'Inner target': self.innerTarget}[location]
        cvs = np.array([self.cv(position, j) for j in range(1, self.ny + 1)])
        R, Z = self.R[cvs - 1], self.Z[cvs - 1]
        sep = self.separatrix - 1
        if location == 'OMP':
            return cvs, (R - R[sep]) * 1e3, r'$r - r_\mathrm{sep}$ [mm]'
        s = np.concatenate([[0.0], np.cumsum(np.hypot(np.diff(R), np.diff(Z)))])
        return cvs, (s - s[sep]) * 1e3, r'$s - s_\mathrm{sep}$ [mm]'

    def rings(self, text):
        """Ring numbers for 'separatrix', 'separatrix+2', 'SOL',
        'inside separatrix', 'all' or numbers such as '9, 10' and '9-12'.
        """
        text = text.strip().lower()
        if text == 'all':
            return list(range(1, self.ny + 1))
        if text == 'sol':
            return list(range(self.separatrix, self.ny + 1))
        if text == 'inside separatrix':
            return list(range(1, self.separatrix))
        match = re.fullmatch(r'separatrix\s*([+-]\s*\d+)?', text)
        if match:
            return [self.separatrix + int((match.group(1) or '0').replace(' ', ''))]
        rings = []
        for part in re.split(r'[,\s]+', text):
            if '-' in part:
                start, end = part.split('-')
                rings += list(range(int(start), int(end) + 1))
            elif part:
                rings.append(int(part))
        return rings

    def cvs(self, location, rings):
        if location == 'Custom CVs':
            return [int(cv) for cv in re.split(r'[,\s]+', rings.strip()) if cv]
        position = {'OMP': self.omp, 'Outer target': self.outerTarget,
                    'Inner target': self.innerTarget}[location]
        selected = self.rings(rings)
        if not selected or min(selected) < 1 or max(selected) > self.ny:
            raise ValueError(f"rings '{rings}' outside 1..{self.ny}")
        return [self.cv(position, j) for j in selected]


# ----------------------------------------------------------------------
# SOLPS outputs
# ----------------------------------------------------------------------
def readFields(runDir):
    """te, ti [eV] and ne, ni [m^-3] per cell from b2fplasmf of a run."""
    data = readB2output(runDir, 'b2fplasmf', variables=['ne', 'na', 'te', 'ti'])
    ne = np.asarray(data['ne'])
    ncv = ne.size
    if ncv == 0:
        raise ValueError('ne not found in b2fplasmf')
    na = np.asarray(data['na'])
    fields = {
        'ne': ne,
        # na is species-major; species 1 is the main ion (D+).
        'ni': na[ncv:2 * ncv] if na.size >= 2 * ncv else na[:ncv],
        'te': np.asarray(data['te']) / EV,
        'ti': np.asarray(data['ti']) / EV,
    }
    return fields


def readQois(runDir, qois):
    fields = readFields(runDir)
    values = []
    for qoi in qois:
        cells = fields[qoi['variable']][np.asarray(qoi['cvs'], dtype=int) - 1]
        values.append({'value': cells[0], 'mean': np.mean(cells),
                       'max': np.max(cells), 'min': np.min(cells)}[qoi['statistic']])
    return values


# ----------------------------------------------------------------------
# Widgets and threads
# ----------------------------------------------------------------------
def newTable(headers, parent):
    table = QTableWidget(0, len(headers), parent)
    table.setHorizontalHeaderLabels(headers)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    return table


def newCombo(items, current, parent):
    combo = QComboBox(parent)
    combo.addItems(items)
    if current in items:
        combo.setCurrentText(current)
    return combo


class UQWorker(QThread):
    """Runs a long function outside the GUI thread. The function receives a
    ``log`` callable for progress messages.
    """

    message = Signal(str)
    done = Signal(object)
    failed = Signal(str)

    def __init__(self, function, parent=None):
        super().__init__(parent)
        self.function = function

    def run(self):
        try:
            self.done.emit(self.function(self.message.emit))
        except Exception as error:
            self.failed.emit(f'{type(error).__name__}: {error}')


class UQWorkerMixin:
    """Starts UQWorker threads. The actor must define ``log(str)``, a
    ``busy`` Signal(bool) and ``updateButtons()``.
    """

    worker = None

    def isBusy(self):
        return self.worker is not None and self.worker.isRunning()

    def startWorker(self, function, onDone=None):
        # Buttons are disabled while busy, so this only happens when a
        # connected signal arrives during a task; no dialog then.
        if self.isBusy():
            self.log('Another UQ task is still running; request ignored.')
            return
        self.worker = UQWorker(function, self)
        self.worker.message.connect(self.log)
        self.worker.failed.connect(lambda text: self.log(f'ERROR: {text}'))
        if onDone is not None:
            self.worker.done.connect(onDone)
        self.worker.finished.connect(self.workerFinished)
        self.worker.start()
        self.busy.emit(True)
        self.updateButtons()

    def workerFinished(self):
        self.busy.emit(False)
        self.updateButtons()
