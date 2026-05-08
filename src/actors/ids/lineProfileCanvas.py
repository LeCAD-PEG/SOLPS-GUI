#! /usr/bin/env python3

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np


class LineProfileCanvas(FigureCanvasQTAgg):
    """Matplotlib canvas for 1D radial line profiles."""

    def __init__(self, parent=None, width=12, height=8, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(fig)
        self.setParent(parent)
        self.figure = fig

    def plotRegression(self, data):
        """Plot 6-panel regression figure matching MATLAB plot_regression_estimation.m.

        Arguments:
            data (dict): keys:
                ds         - OMP x axis [mm]
                dstrg1     - target x axis [mm]
                ne_omp     - optimized ne @ OMP [1e19 m-3]
                te_omp     - optimized Te @ OMP [eV]
                ne_trg     - optimized ne @ target [1e19 m-3]
                te_trg     - optimized Te @ target [eV]
                dna_omp    - optimized D_perp @ OMP [m2/s]
                chie_omp   - optimized chi_e @ OMP [m2/s]
                ne_omp_ref, te_omp_ref, ne_trg_ref, te_trg_ref,
                dna_omp_ref, chie_omp_ref  - same for reference case
                cf2, cf3, cf4, cf5  - cost fn arrays shape (N,2):
                                      col0=r[m], col1=value  (or None)
        """
        self.figure.clear()

        ocre = [255/255, 218/255, 38/255]
        blue = [51/255, 153/255, 1.0]

        axes = self.figure.subplots(2, 3)
    
        specs = [
            # (ax,         x_opt,           y_opt,             x_ref,           y_ref,                cf_key,  title,                xlabel,           ylabel,          ylim,   xlim,        transport)
            (axes[0, 0], data['ds'],     data['ne_omp'],    data['ds'],     data['ne_omp_ref'],  'cf2',  'nₑ @ OMP',          'r−r_sep [mm]', 'nₑ [10¹⁹ m⁻³]', None,   None,        False),
            (axes[0, 1], data['ds'],     data['te_omp'],    data['ds'],     data['te_omp_ref'],  'cf3',  'Tₑ @ OMP',          'r−r_sep [mm]', 'Tₑ [eV]',        None,   None,        False),
            (axes[0, 2], data['dstrg1'],     data['ne_trg'],    data.get('dstrg1_ref', data['dstrg1']), data['ne_trg_ref'],  'cf4',  'nₑ @ outer target', 's−s_sep [mm]', 'nₑ [10¹⁹ m⁻³]', None,   None,        False),
            (axes[1, 0], data['dstrg1'],     data['te_trg'],    data.get('dstrg1_ref', data['dstrg1']), data['te_trg_ref'],  'cf5',  'Tₑ @ outer target', 's−s_sep [mm]', 'Tₑ [eV]',        None,   None,        False),
            (axes[1, 1], data['ds'],     data['dna_omp'],   data['ds'],     data['dna_omp_ref'], None,   'D⊥ @ OMP',          'r−r_sep [mm]', 'D⊥ [m²/s]',      None,   None,        True),
            (axes[1, 2], data['ds'],     data['chie_omp'],  data['ds'],     data['chie_omp_ref'],None,   'χₑ⊥ @ OMP',        'r−r_sep [mm]', 'χₑ [m²/s]',      None,   None,        True),
        ]

        for panel_idx, (ax, x_opt, y_opt, x_ref, y_ref, cf_key, title, xlabel, ylabel, ylim, xlim, transport) in enumerate(specs):
            # Cost function data — yellow dots
            cf_x_min = None
            cf_x_max = None
            if cf_key and data.get(cf_key) is not None:
                cf = data[cf_key]
                if cf.ndim == 2 and cf.shape[1] >= 2:
                    cf_x = cf[:, 0] * 1e3   # r-r_sep [m] → mm
                    cf_x_min = cf_x.min()
                    cf_x_max = cf_x.max()
                    ax.plot(cf_x, cf[:, 1], 'o',
                            color=ocre, label='cost fn data',
                            markersize=4, linestyle='none')

            def shift_curve(xarr, yarr):
                """Shift curve x so its start aligns with the first yellow dot."""
                xarr = np.asarray(xarr, dtype=float)
                yarr = np.asarray(yarr, dtype=float)
                if cf_x_min is None or len(xarr) == 0:
                    return xarr, yarr
                return xarr + (cf_x_min - xarr.min()), yarr

            # Reference — blue solid line
            if len(x_ref) and len(y_ref):
                xr, yr = shift_curve(x_ref, y_ref)
                ax.plot(xr, yr, '-', color=blue,
                        label='reference', linewidth=2)

            # Optimized — yellow dashed for transport coefficients, red dash-dot for ne/Te
            if len(x_opt) and len(y_opt):
                xo, yo = shift_curve(x_opt, y_opt)
                opt_color = ocre if transport else 'r'
                opt_style = '--'  if transport else '-.'
                ax.plot(xo, yo, opt_style, color=opt_color,
                        label='optimized', linewidth=2)

            ax.set_title(title, fontsize=9)
            ax.set_xlabel(xlabel, fontsize=8)
            ax.set_ylabel(ylabel, fontsize=8)
            if ylim:
                ax.set_ylim(ylim)
            if xlim is not None:
                ax.set_xlim(left=xlim[0], right=xlim[1])
            ax.legend(fontsize=7)
            ax.grid(True, linestyle='--', alpha=0.5)

        try:
            self.figure.tight_layout()
        except Exception as e:
            print(f'Warning: tight_layout failed: {e}')
            self.figure.subplots_adjust(
                left=0.08,
                right=0.98,
                bottom=0.08,
                top=0.92,
                wspace=0.35,
                hspace=0.45
            )

        self.draw_idle()
