#! /usr/bin/env python3

import sys
import os

from PySide6.QtCore import  QSize, Property, Slot, Signal
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QPlainTextEdit

from PySide6.QtWidgets import QWidget

import logging
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

from ids.quadPlotCanvas import QuadPlotCanvas
from ids.lineProfileCanvas import LineProfileCanvas
from ids.GGDDialog import GetGGDDialog
from ids.getEPGGD import getEPGGD, GetGGDVars

from PySide6.QtWidgets import QDialog, QComboBox, QDialogButtonBox, QFormLayout, QLabel

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
        # Set empty matplotlib canvas (2D mesh plot)
        self.canvas = QuadPlotCanvas(self, width=1, height=6)
        # Set matplotlib toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)
        # Add widgets to layout
        self.layout().addWidget(self.canvas)
        self.layout().addWidget(self.toolbar)

        # 1D profile canvas (shown on demand via plotProfiles1D slot)
        self.profileCanvas = LineProfileCanvas(self, width=5, height=4)
        self.profileToolbar = NavigationToolbar(self.profileCanvas, self)
        self.layout().addWidget(self.profileCanvas)
        self.layout().addWidget(self.profileToolbar)
        # Hide by default — shown only when a 1D plot is requested
        self.profileCanvas.setVisible(False)
        self.profileToolbar.setVisible(False)


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
        """Populate (plot) the canvas."""
        if self.ep is None:
            return

        self.canvas.setVisible(True)
        self.toolbar.setVisible(True)
        self.profileCanvas.setVisible(False)
        self.profileToolbar.setVisible(False)

        ggdVars = self.getGGDVars()
        qValues = ggdVars['quantityValues']

        getGGD = getEPGGD(self.ep)
        nodes, quad_conn_array = getGGD.getGSGridGeometry(ggdVars)

        self.canvas.figure.clear()
        self.canvas.ax = self.canvas.figure.add_subplot(111)

        self.canvas.plotData(
            nodes,
            quad_conn_array,
            qValues,
            title=ggdVars['quantityLabel']
        )
        self.canvas.draw()

    @Slot()
    def clearPlot(self):
        """Clear both 2D and 1D plots."""

        self.canvas.figure.clear()
        self.canvas.ax = self.canvas.figure.add_subplot(111)
        self.canvas.draw()

        self.profileCanvas.figure.clear()
        self.profileCanvas.ax = self.profileCanvas.figure.add_subplot(111)
        self.profileCanvas.draw()

        self.canvas.setVisible(True)
        self.toolbar.setVisible(True)
        self.profileCanvas.setVisible(False)
        self.profileToolbar.setVisible(False)

    @Slot()
    def plotProfiles1D(self):
        """Plot 1D regression results — 6 panels matching MATLAB plot_regression_estimation.m.

        Reads from ep.profiles_1d if available (written by put_edge_ids.py),
        otherwise falls back to reading b2fplasmf/b2fgmtry directly from disk.
        Cost function data (cf2-cf5.dat) is read from runDir or the tarball.
        """
        import numpy as np
        import math
        import tarfile
        import base64
        from io import BytesIO
        import sys
        import os

        if self.ep is None:
            logging.warning('No IDS yet provided.')
            return

        ep = self.ep
        ev = 1.602176634e-19

        # ------------------------------------------------------------------ #
        # Helper: read from profiles_1d slots (returns empty array on failure)
        # ------------------------------------------------------------------ #
        def _slot_x(slot):
            try:
                arr = ep.profiles_1d[slot].grid.rho_pol_norm
                return np.array([arr[k] for k in range(len(arr))])
            except Exception:
                return np.array([])

        def _slot_ne(slot):
            try:
                arr = ep.profiles_1d[slot].electrons.density
                return np.array([arr[k] for k in range(len(arr))]) / 1e19
            except Exception:
                return np.array([])

        def _slot_te(slot):
            try:
                arr = ep.profiles_1d[slot].electrons.temperature
                return np.array([arr[k] for k in range(len(arr))]) / ev
            except Exception:
                return np.array([])

        def _slot_dperp(slot):
            try:
                arr = ep.profiles_1d[slot].ion[0].density
                return np.array([arr[k] for k in range(len(arr))])
            except Exception:
                return np.array([])

        def _slot_chie(slot):
            try:
                arr = ep.profiles_1d[slot].electrons.pressure
                return np.array([arr[k] for k in range(len(arr))])
            except Exception:
                return np.array([])

        # Try reading from profiles_1d first
        ds       = _slot_x(0)
        ne_omp   = _slot_ne(0)
        te_omp   = _slot_te(0)
        dna_omp  = _slot_dperp(0)
        chie_omp = _slot_chie(0)
        dstrg1     = _slot_x(1)
        ne_trg     = _slot_ne(1)
        te_trg     = _slot_te(1)
        ne_omp_ref   = _slot_ne(2)
        te_omp_ref   = _slot_te(2)
        dna_omp_ref  = _slot_dperp(2)
        chie_omp_ref = _slot_chie(2)
        dstrg1_ref   = _slot_x(3)
        ne_trg_ref   = _slot_ne(3)
        te_trg_ref   = _slot_te(3)

        ids_ok = len(ds) > 0 and len(dstrg1) > 0
        logging.info(f'profiles_1d: {"OK" if ids_ok else "EMPTY — falling back to b2fplasmf"}')

        if not ids_ok:
            # ------------------------------------------------------------------ #
            # Fallback: read directly from b2fplasmf + b2fgmtry
            # ------------------------------------------------------------------ #
            try:
                runDir = str(ep.ids_properties.comment)
            except Exception:
                runDir = ''
            if not runDir or not os.path.isdir(runDir):
                logging.warning(f'Run directory not found: {runDir!r}')
                return

            actors_dir = os.path.dirname(os.path.abspath(__file__))
            if actors_dir not in sys.path:
                sys.path.insert(0, actors_dir)
            from put_edge_ids import readB2output

            basedir = os.path.normpath(os.path.join(runDir, '..', '..'))
            gmtry_path = os.path.join(basedir, 'baserun', 'b2fgmtry')
            if not os.path.exists(gmtry_path):
                gmtry_path = os.path.join(runDir, 'b2fgmtry')
            if not os.path.exists(gmtry_path):
                logging.warning(f'b2fgmtry not found')
                return

            coorAr = readB2output(os.path.dirname(gmtry_path), os.path.basename(gmtry_path),
                                  variables=['nx,ny,nncut', 'nCi,nCg,nCv,nFc,nVx,nFs,nFt',
                                             'cvX', 'cvY', 'fcLbl', 'fcCv'])
            nx  = int(coorAr['nx,ny,nncut'][0])
            ny  = int(coorAr['nx,ny,nncut'][1])
            nCi = int(coorAr['nCi,nCg,nCv,nFc,nVx,nFs,nFt'][0])
            nCv = int(coorAr['nCi,nCg,nCv,nFc,nVx,nFs,nFt'][2])
            nFc = int(coorAr['nCi,nCg,nCv,nFc,nVx,nFs,nFt'][3])
            cvX = coorAr['cvX']; cvY = coorAr['cvY']
            fcLbl = coorAr['fcLbl']; fcCv = coorAr['fcCv']

            if os.path.exists(os.path.join(runDir, 'b2fplasmf')):
                state = readB2output(runDir, 'b2fplasmf', variables=['ne', 'te', 'dna0', 'hce0'])
            elif os.path.exists(os.path.join(runDir, 'b2fstati')):
                state = readB2output(runDir, 'b2fstati', variables=['ne', 'te'])
            else:
                logging.warning('No b2fplasmf or b2fstati found.')
                return

            refDir = os.path.normpath(os.path.join(runDir, '..', 'reference_reg'))
            statref = {}
            if os.path.exists(os.path.join(refDir, 'b2fplasmf')):
                statref = readB2output(refDir, 'b2fplasmf', variables=['ne', 'te', 'dna0', 'hce0'])

            # -- OMP cells --
            omp_raw = []  # list of (iy, flat, R, Z)
            for iy in range(1, ny + 1):
                cells_iy = []
                for ix in range(1, nx + 1):
                    flat = ix + (nx + 2) * iy
                    if flat < len(cvX):
                        cells_iy.append((flat, cvX[flat], cvY[flat]))
                if not cells_iy:
                    continue
                R_vals = [c[1] for c in cells_iy]
                R_mid = (max(R_vals) + min(R_vals)) / 2.0
                outer = [c for c in cells_iy if c[1] > R_mid] or cells_iy
                best = min(outer, key=lambda c: abs(c[2]))
                omp_raw.append((iy, best[0], best[1], best[2]))

            # Post-filter 1: remove rings with |Z| >> median (clearly off-equator guards)
            if omp_raw:
                absZ_vals = sorted(abs(r[3]) for r in omp_raw)
                median_absZ = absZ_vals[len(absZ_vals) // 2]
                threshold_Z = max(median_absZ * 10.0, 0.05)
                omp_raw = [r for r in omp_raw if abs(r[3]) <= threshold_Z]

            # Post-filter 2: remove rings where step to next cell > 4x median step
            if len(omp_raw) > 2:
                steps = []
                for k in range(1, len(omp_raw)):
                    dR = omp_raw[k][2] - omp_raw[k-1][2]
                    dZ = omp_raw[k][3] - omp_raw[k-1][3]
                    steps.append(math.sqrt(dR*dR + dZ*dZ))
                med_step = sorted(steps)[len(steps) // 2]
                thresh_step = max(med_step * 4.0, 0.005)
                filtered = [omp_raw[0]]
                for k in range(1, len(omp_raw)):
                    if steps[k-1] <= thresh_step:
                        filtered.append(omp_raw[k])
                omp_raw = filtered

            omp_idx = [r[1] for r in omp_raw]
            n_omp = len(omp_idx)
            if n_omp == 0:
                logging.warning('No OMP cells found.')
                return

            # Auto-detect separatrix: the largest jump in ix between consecutive OMP cells
            ix_vals = [r[1] % (nx + 2) for r in omp_raw]
            ix_jumps = [abs(ix_vals[k] - ix_vals[k-1]) for k in range(1, len(ix_vals))]
            if ix_jumps and max(ix_jumps) > 2 * (sorted(ix_jumps)[len(ix_jumps)//2] + 1):
                # Jump is between index k and k+1 → icsep = k+1 (first SOL ring after the cut)
                icsep = ix_jumps.index(max(ix_jumps)) + 1
                logging.info(f'icsep={icsep} auto-detected from ix jump ({max(ix_jumps)} vs median {sorted(ix_jumps)[len(ix_jumps)//2]})')
            else:
                icsep = min(ny // 2, n_omp - 1)
                logging.info(f'No ix jump detected; using icsep={icsep} (ny//2 fallback)')


            def calc_dist(idx_list, icsep_idx):
                arc = [0.0] * len(idx_list)
                for k in range(1, len(idx_list)):
                    dR = cvX[idx_list[k]] - cvX[idx_list[k-1]]
                    dZ = cvY[idx_list[k]] - cvY[idx_list[k-1]]
                    arc[k] = arc[k-1] + math.sqrt(dR*dR + dZ*dZ)
                sep_arc = (arc[icsep_idx] + arc[icsep_idx - 1]) / 2.0 if icsep_idx > 0 else arc[0]
                return np.array([(a - sep_arc) * 1e3 for a in arc])

            ds = calc_dist(omp_idx, icsep)
            omp_sep_iy = omp_idx[icsep] // (nx + 2)
            logging.info(f'OMP: {n_omp} cells, icsep={icsep}, ds=[{ds[0]:.1f},{ds[-1]:.1f}] mm, sep_iy={omp_sep_iy}')

            # -- Target cells: only ix-adjacent faces (abs(diff)==1) on outer plate --
            trg_idx = []
            seen = set()
            if fcLbl and fcCv and nFc > 0:
                for iFc in range(nFc):
                    if int(fcLbl[iFc]) == -34:
                        raw1 = int(fcCv[2*iFc])
                        raw2 = int(fcCv[2*iFc+1])
                        if abs(raw1 - raw2) != 1:   # only ix-adjacent: real outer plate cells
                            continue
                        ic1 = max(raw1, raw2) - 1   # 0-based: max picks the plasma cell (not guard)
                        if ic1 < nCi and ic1 not in seen:
                            seen.add(ic1)
                            trg_idx.append(ic1)
            # Sort by iy (poloidal ring index = flat // (nx+2)), which gives the correct
            trg_idx = sorted(trg_idx, key=lambda i: i // (nx + 2))

            # Find separatrix in target: select the cell with iy closest to omp_sep_iy+0.5
            stride_ = nx + 2
            trg_icsep = min(range(len(trg_idx)),
                            key=lambda k: abs(trg_idx[k] // stride_ - omp_sep_iy - 0.5))
            logging.info(f'trg_icsep={trg_icsep}, trg_iy={trg_idx[trg_icsep]//stride_}, omp_sep_iy={omp_sep_iy}')
            dstrg1 = calc_dist(trg_idx, trg_icsep) if trg_idx else np.array([])
            dstrg1_ref = dstrg1
            logging.info(f'Target: {len(trg_idx)} cells, trg_icsep={trg_icsep}, dstrg1=[{dstrg1[0]:.1f},{dstrg1[-1]:.1f}] mm' if len(dstrg1) else 'Target EMPTY')

            # -- Extract ne/Te from state arrays --
            def _get(src, key, idx_list):
                arr = src.get(key, [])
                if not arr or not idx_list or max(idx_list) >= len(arr):
                    return np.array([])
                return np.array([arr[i] for i in idx_list])

            def _get_dna0(src, idx_list):
                arr = src.get('dna0', [])
                if not arr or len(arr) < 2 * nCv:
                    return np.array([])
                return np.array([arr[nCv + i] for i in idx_list])

            ne_omp    = _get(state, 'ne', omp_idx) / 1e19
            te_omp    = _get(state, 'te', omp_idx) / ev
            ne_trg    = _get(state, 'ne', trg_idx) / 1e19
            te_trg    = _get(state, 'te', trg_idx) / ev
            ne_raw    = _get(state, 'ne', omp_idx)
            hce0_omp  = _get(state, 'hce0', omp_idx)
            dna_omp   = _get_dna0(state, omp_idx)
            chie_omp  = (hce0_omp / ne_raw) if len(ne_raw) and len(hce0_omp) else np.array([])

            ne_omp_ref   = _get(statref, 'ne', omp_idx) / 1e19  if statref else np.array([])
            te_omp_ref   = _get(statref, 'te', omp_idx) / ev    if statref else np.array([])
            ne_trg_ref   = _get(statref, 'ne', trg_idx) / 1e19  if statref else np.array([])
            te_trg_ref   = _get(statref, 'te', trg_idx) / ev    if statref else np.array([])
            ne_raw_ref   = _get(statref, 'ne', omp_idx)         if statref else np.array([])
            hce0_ref     = _get(statref, 'hce0', omp_idx)       if statref else np.array([])
            dna_omp_ref  = _get_dna0(statref, omp_idx)          if statref else np.array([])
            chie_omp_ref = (hce0_ref / ne_raw_ref) if len(ne_raw_ref) and len(hce0_ref) else np.array([])

            runDir_cf = runDir
        else:
            try:
                runDir_cf = str(ep.ids_properties.comment)
            except Exception:
                runDir_cf = ''

        # ------------------------------------------------------------------ #
        # Cost function data — load from runDir first, then tarball fallback
        # ------------------------------------------------------------------ #
        cf = {'cf2': None, 'cf3': None, 'cf4': None, 'cf5': None}
        for key, fname in [('cf2', 'cf2.dat'), ('cf3', 'cf3.dat'),
                           ('cf4', 'cf4.dat'), ('cf5', 'cf5.dat')]:
            fpath = os.path.join(runDir_cf, fname)
            if os.path.exists(fpath):
                try:
                    arr = np.loadtxt(fpath)
                    if arr.ndim == 2 and arr.shape[1] >= 2:
                        cf[key] = arr
                        logging.info(f'{fname}: loaded {len(arr)} rows from disk')
                    else:
                        logging.warning(f'{fname}: unexpected shape {arr.shape}')
                except Exception as e:
                    logging.warning(f'{fname}: failed to load from disk: {e}')
            else:
                logging.info(f'{fname}: not found in {runDir_cf}, trying tarball')
        # Tarball fallback for any still-missing files
        missing = [k for k, v in cf.items() if v is None]
        if missing:
            try:
                raw = base64.b64decode(self.ep.code.parameters.encode())
                with tarfile.open(fileobj=BytesIO(raw)) as tar:
                    for key, fname in [('cf2', 'cf2.dat'), ('cf3', 'cf3.dat'),
                                       ('cf4', 'cf4.dat'), ('cf5', 'cf5.dat')]:
                        if cf[key] is not None:
                            continue
                        try:
                            data_bytes = tar.extractfile(tar.getmember(fname)).read()
                            arr = np.loadtxt(BytesIO(data_bytes))
                            if arr.ndim == 2 and arr.shape[1] >= 2:
                                cf[key] = arr
                                logging.info(f'{fname}: loaded from tarball')
                        except Exception:
                            pass
            except Exception as e:
                logging.info(f'Tarball not available: {e}')
        for k, v in cf.items():
            if v is None:
                logging.warning(f'{k}: not found anywhere — dots will be missing')

        plot_data = dict(
            ds=ds, dstrg1=dstrg1, dstrg1_ref=dstrg1_ref,
            ne_omp=ne_omp,   te_omp=te_omp,
            ne_trg=ne_trg,   te_trg=te_trg,
            dna_omp=dna_omp, chie_omp=chie_omp,
            ne_omp_ref=ne_omp_ref,   te_omp_ref=te_omp_ref,
            ne_trg_ref=ne_trg_ref,   te_trg_ref=te_trg_ref,
            dna_omp_ref=dna_omp_ref, chie_omp_ref=chie_omp_ref,
            **cf
        )

        self.canvas.setVisible(False)
        self.toolbar.setVisible(False)
        self.profileCanvas.setVisible(True)
        self.profileToolbar.setVisible(True)
        self.profileCanvas.plotRegression(plot_data)

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
