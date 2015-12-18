#!/usr/bin/env python3

"""

A PyQt custom widget with embedded list of SOLPS scripts.

"""

from PyQt5.QtCore import (Qt, QProcess, QSize, pyqtProperty,
                          pyqtSignal, pyqtSlot)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QComboBox


class SolpsPlots(QComboBox):
    """SolpsPlots(QComboBox)
    
    Provides a custom widget that holds all SOLPS Gnuplot script names
    for combining them with
    """

    returnPressed = pyqtSignal()
    
    def __init__(self, parent=None):
        super(SolpsPlots, self).__init__(parent)

        self.process = QProcess()
        self.setEditable(True)
        self.setMaximumWidth(400)
        self.addItems(_tcsh_solps_scripts)

    @pyqtSlot()
    def triggerTextChanged(self):
        """ Connector that receives a signal and re-emits the current text.
        """
        current_text = self.currentText()
        self.editTextChanged.emit(current_text)
        self.currentTextChanged.emit(current_text)

    def keyPressEvent(self, event):
        """ Catch each key and emit plot command when Return is pressed.
        """
        super(SolpsPlots, self).keyPressEvent(event)
        if event.key() == Qt.Key_Return:
            self.returnPressed.emit()

# List of TCSH plot scripts in solps-iter/scripts obtained by
# grep -H plot * | grep -v .py | \
#  sed 's/\([a-zA-Z0-9_+-]*\):.*/    \"\1 # \",/' | sort | uniq
_tcsh_solps_scripts = [
    'resall_D # all residuals for a D-only case',
    'resall_D+ #  only all residuals for a D+-only case',
    'resall_D+D # all residuals for test cases where we treat\n'
        'two separate D sequences',
    'resall_D+T # all residuals for a D + T case',
    'resall_H # all residuals for a H only case',
    'resrest_residuals # for non-species dependent equations',
    'res_D+C # non-species dependent residuals for a D+C case',
    'res_D+O # non-species dependent residuals for a D+O case',
    'res_D+C+He # non-species dependent residuals for\n'
        'a D + C + He case',
    'res_D+C+Ar+Ne+He # non-species dependent residuals for\n'
        'a D + C + Ar + Ne + He case',
    'resco_continuity # residuals',
    'resco_reg # continuity residuals per region',
    'resco_reg # region #1 continuity residuals per region\n'
    'for species #1 (default 0)',
    'resco_D+C # continuity residuals for a D + C case',
    'resco_D+O # continuity residuals for a D + O case',
    'resco_D+C+He # continuity residuals for a D+C+He case',
    'resmo_parallel # momentum residuals per species',
    'resmo_reg # #1 parallel momentum residuals per species\n'
        'for region #1 (default 0)',
    'resmo_reg # region #1 parallel momentum residuals per\n'
        'region for species #1 (default 0)',
    'resmo_D+C # parallel momentum residuals for a D + C case',
    'resmo_D+O # parallel momentum residuals for a D + O case',
    'resmo_D+C+He # parallel momentum residuals for\n'
        'a D + C + He case',
    'resmt_reg # residuals of the total parallel momentum\n'
        'equation',
    'reshe_reg # residuals of the electron heat equation\n'
        'per region',
    'reshi_reg # residuals of the ion heat equation per region',
    'respo_residuals # of the potential equation, including\n'
        'the internal iterations',
    'respo_num # the number of internal potential equation\n'
        'iterations',
    'respo_reg # residuals of the potential equation\n'
        'per region',
    'resopt # Internal script to apply options to above\n'
        'residuals scripts (see below)',
    'resmod #1 Selects residuals modulo #1 (default all \n'
        'power/particle losses (see section G and Appendix\n'
        '3.6.4 for the region definitions)',
    'b2stbc_sna_reg #1 Boundary particle sources for\n'
        'region #1 (default 0)',
    'b2stbr_sna_reg #1 Recycling particle sources for\n'
        'region #1 (default 0)',
    'b2stbm_sna_reg #1 Additional particle sources for\n'
        'region #1 (default 0)',
    'b2stbc_smo_reg #1 Boundary parallel momentum sources for\n'
        'region #1 (default 0)',
    'b2stbr_smo_reg #1 Recycling parallel momentum sources\n'
        'for region #1 (default 0)',
    'b2stbm_smo_reg #1 Additional parallel momentum sources\n'
        'for region #1 (default 0)',
    'rcxhireg #1 charge exchange energy for region #1\n'
        '(default 0)',
    'rcxnareg #1 charge exchange rate for region #1 (deflt 0)',
    'rqahereg #1 electron heat loss for region #1 (default 0)',
    'rqbrmreg #1 bremsstrahlung losses for region #1 (dflt 0)',
    'rqradreg #1 total radiation rate for region #1 (deflt 0)',
    'rrahireg #1 recombination energy for region #1 (deflt 0)',
    'rranareg #1 recombination rate for region #1 (default 0)',
    'rsahireg #1 ionization energy for region #1 (default 0)',
    'rsanareg #1 ionization rate for region #1 (default 0)',
    'b2stbc_she_reg_region #1 Boundary electron heat sources,\n'
        'by region, for species #1 (default 0)',
    'b2stbc_shi_reg_region #1 Boundary ion heat sources,\n'
        'by region, for species #1 (default 0)',
    'b2stbc_sne_reg_region #1 Boundary electron particle\n'
        'sources, by region, for species #1 (default 0)',
    'b2stbc_sch_reg_region #1 Boundary charge sources, by \n'
        'region, for species #1 (default 0)',
    'b2stbc_sna_reg_region #1 Boundary particle sources, by\n'
        'region, for species #1 (default 0)',
    'b2stbc_smo_reg_region #1 Boundary parallel momentum\n'
        'sources, by region, for species #1 (default 0)',
    'b2stbr_she_reg_region #1 Recycling electron heat sources,\n'
        'by region, for species #1 (default 0)',
    'b2stbr_shi_reg_region #1 Recycling ion heat sources,\n'
        'by region, for species #1 (default 0)',
    'b2stbr_sne_reg_region #1 Recycling electron particle\n'
        'sources, by region, for species #1 (default 0)',
    'b2stbr_sch_reg_region #1 Recycling charge sources,\n'
        'by region, for species #1 (default 0)',
    'b2stbr_sna_reg_region #1 Recycling particle sources,\n'
        'by region, for species #1 (default 0)',
    'b2stbr_smo_reg_region #1 Recycling parallel momentum\n'
        'sources, by region, for species #1 (default 0)',
    'b2stbm_she_reg_region #1 Additional electron heat sources,\n'
        'by region, for species #1 (default 0)',
    'b2stbm_shi_reg_region #1 Additional ion heat sources,\n'
        'by region, for species #1 (default 0)',
    'b2stbm_sne_reg_region #1 Additional electron particle\n'
        'sources, by region, for species #1 (default 0)',
    'b2stbm_sch_reg_region #1 Additional charge sources,\n'
        'by region, for species #1 (default 0)',
    'b2stbm_sna_reg_region #1 Additional particle sources,\n'
        'by region, for species #1 (default 0)',
    'b2stbm_smo_reg_region #1 Additional parallel momentum\n'
        'sources, by region, for species #1 (default 0)',
    'rcxhireg_region #1 charge exchange energy, by region,\n'
        'for species #1 (default 0)',
    'rcxnareg_region #1 charge exchange rate, by region,\n'
        'for species #1 (default 0)',
    'rqahereg_region #1 electron heat loss, by region,\n'
        'for species #1 (default 0)',
    'rqbrmreg_region #1 bremsstrahlung radiation loss,\n'
        'by region, for species #1 (default 0)',
    'rqradreg_region #1 total radiation rate, by region,\n'
        'for species #1 (default 0)',
    'rrahireg_region #1 recombination energy, by region,\n'
        'for species #1 (default 0)',
    'rranareg_region #1 recombination rate, by region, for\n'
        'species #1 (default 0)',
    'rsahireg_region #1 ionization energy, by region, for\n'
        'species #1 (default 0)',
    'rsanareg_region #1 ionization rate, by region, for species\n'
        '#1 (default 0)',
    'xyplot  # alias for simple ”x y” plot',
    'xyplot2 # alias for simple ”x y1 y2” plot',
    'xyplot3 # alias for simple ”x y1 y2 y3” plot',
    'xyplot4 # alias for simple ”x y1 y2 y3 y4” plot',
    'xyplot5 # alias for simple ”x y1 y2 y3 y4 y5” plot',
    'xyplot6 # alias for simple ”x y1 y2 y3 y4 y5 y6” plot',
    'xyplot7 # alias for simple ”x y1 y2 y3 y4 y5 y6 y7” plot',
    'xyplot8 # alias for simple ”x y1 y2 y3 y4 y5 y6 y7 y8 plt',
    'xyplot9 # alias for simple ”x y1 y2 y3 y4 y5 y6 y7 y8 y9',
    'xlyplot # alias for simple ”x log(y)” plot',
    'xlyplot2 # alias for simple ”x log(y1) log(y2)” plot',
    'xlyplot3 # alias for simple ”x log(y1) log(y2) log(y3)”',
    'xlyplot4 # alias for simple ”x log(y1) log(y2) log(y3)\n'
        'log(y4)” plot',
    'xlyplot5 # alias for simple ”x log(y1) log(y2) log(y3)\n'
        'log(y4) log(y5)” plot',
    'xlyplot6 # alias for simple ”x log(y1) log(y2) log(y3)\n'
        'log(y4) log(y5) log(y6)” plot',
    'xlyplot7 # alias for simple ”x log(y1) log(y2) log(y3)\n'
        'log(y4) log(y5) log(y6) log(y7)” plot',
    'xlyplot8 # alias for simple ”x log(y1) log(y2) log(y3)\n'
        'log(y4) log(y5) log(y6) log(y7) log(y8)” plot',
    'xlyplot9 # alias for simple ”x log(y1) log(y2) log(y3)\n'
        'log(y4) log(y5) log(y6) log(y7) log(y8) log(y9) plot',
    'lxyplot # alias for simple ”log(x) y” plot',
    'lxyplot2 # alias for simple ”log(x) y1 y2” plot',
    'lxyplot3 # alias for simple ”log(x) y1 y2 y3” plot',
    'lxyplot4 # alias for simple ”log(x) y1 y2 y3 y4” plot',
    'lxyplot5 # alias for simple ”log(x) y1 y2 y3 y4 y5” plot',
    'lxyplot6 # alias for simple ”log(x) y1 y2 y3 y4 y5 y6”\n'
        'plot',
    'lxyplot7 # alias for simple ”log(x) y1 y2 y3 y4 y5 y6\n'
        'y7” plot',
    'lxyplot8 # alias for simple ”log(x) y1 y2 y3 y4 y5 y6\n'
        'y7 y8” plot',
    'lxyplot9 # alias for simple ”log(x) y1 y2 y3 y4 y5 y6\n'
        'y7 y8 y9” plot',
    'lxlyplot # alias for simple ”log(x) log(y)” plot',
    'lxlyplot2 # alias for simple ”log(x) log(y1) log(y2)” plt',
    'lxlyplot3 # alias for simple ”log(x) log(y1) log(y2)\n'
        'log(y3)” plot',
    'lxlyplot4 # alias for simple ”log(x) log(y1) log(y2)\n'
        'log(y3) log(y4)” plot',
    'lxlyplot5 # alias for simple ”log(x) log(y1) log(y2)\n'
        'log(y3) log(y4) log(y5)” plot',
    'lxlyplot6 # alias for simple ”log(x) log(y1) log(y2)\n'
        'log(y3) log(y4) log(y5) log(y6)” plot',
    'lxlyplot7 # alias for simple ”log(x) log(y1) log(y2)\n'
        'log(y3) log(y4) log(y5) log(y6) log(y7)” plot',
    'lxlyplot8 # alias for simple ”log(x) log(y1) log(y2)\n'
        'log(y3) log(y4) log(y5) log(y6) log(y7) log(y8)” plt',
    'lxlyplot9 # alias for simple ”log(x) log(y1) log(y2)\n'
     'log(y3) log(y4) log(y5) log(y6) log(y7) log(y8) log(y9)',
    '2d # plots time dependent quantities from b2time.nc\n'
        '(Appendix E), 2nd, 3rd etc. versus the 1st argument.',
    '2da # prints time dependent quantities from b2time.nc\n'
        '(Appendix E), 2nd, 3rd etc. versus the 1st argument.',
    '2dt # plots time dependent quantities from b2time.nc\n'
        '(Appendix E) versus time.',
    '2d # plots prepares b2time.ps from b2time.nc (Appendix E).\n'
        'This uses the batch feature of the plot command.',
    '2d_profiles # creates *.last10 files for plotting. When\n'
        'processing fluxes, divides them by the area of\n'
        'contat to the neighbouring cell.',
    '2d_profiles_extended # creates *.last10 files for\n'
        'plotting. When processing fluxes, divides them by\n'
        'the area of contact to the neighbouring cell. The\n'
        'flux files ending in P.last10 are divided by the\n'
        'perpendicular area of the cell face.',
    '2d.summarize # Outputs the time dependent quantities\n'
        'from the last time point in b2time.nc.',
    'D+_fluid_fluxes # Plots the fluxes of D+ ions across the\n'
        'grid boundaries for a B2.5 standalone case',
    'D0_fluid_fluxes # Plots the fluxes of D0 neutrals across\n'
        'the grid boundaries for a B2.5 standalone case',
    'D_coupled_conservation # Plots the particle balance of D\n'
        'for coupled runs',
    'D_coupled_conservation_core # Plots the particle balance\n'
        'of D in the core plasma for coupled runs',
    'D_fluid_conservation # Plots the particle balance of D\n'
        'for B2.5 standalone runs',
    'D_fluid_conservation_core # Plots the particle balance\n'
        'of D in the core plasma for B2.5 standalone runs',
    'D_fluid_fluxes # Plots the fluxes of D across the grid\n'
        'boundaries for a B2.5 standalone case',
    'He_coupled_conservation_core # Plots the particle\n'
        'balance of He in the core plasma for coupled runs',
    'He_fluid_conservation # Plots the particle balance of\n'
        'He for B2.5 standalone runs',
    'He_fluid_fluxes # Plots the fluxes of He across the grid\n'
        'boundaries for a B2.5 standalone case',
    'delta # Plots the maximum fractional change of the\n'
        'primary variables per B2.5 timestep.',
    'density # Plots the time evolution of the density in\n'
        'a B2.5 run.',
    'display # tallies Displays the B2.5 tallies in an\n'
        'easy-to-read format (argument ”H” gives the first\n'
        'instance and ”L” the last instance)',
    'energy_analysis # Plots the energy flows across certain\n'
        'important surfaces in B2.5.',
    'energy_analysis_fht # Plots the total energy flows across\n'
        'certain important surfaces in B2.5.',
    'energy_analysis_total # Plots the total energy flows\n'
        'across certain important surfaces in B2.5.',
    'energy_balance # Plots the energy balance.',
    'energy_balance_core # Plots the energy balance for\n'
        'the core plasma.',
    'energy_balance_core_extended # Plots an extended version\n'
        'including volumetric sources of the energy balance'
        'for the core plasma.',
    'energy_balance_extended # Plots an extended version\n'
        'including volumetric sources of the energy balance.',
    'fhexreg # Plots the electron energy flow across important\n'
        'x-directed surfaces in B2.5.',
    'fheyreg # Plots the electron energy flow across important\n'
        'y-directed surfaces in B2.5.',
    'fhixreg # Plots the ion energy flow across important\n'
        'x-directed surfaces in B2.5.',
    'fhiyreg # Plots the ion energy flow across important\n'
        'y-directed surfaces in B2.5.',
    'fhmxreg # Plots the parallel kinetic energy flow across\n'
        'important x-directed surfaces in B2.5.',
    'fhmyreg # Plots the parallel kinetic energy flow across\n'
        'important y-directed surfaces in B2.5.',
    'fhpxreg # Plots the ionization energy flow across\n'
        'important x-directed surfaces in B2.5.',
    'fhpyreg # Plots the ionization energy flow across\n'
        'important y-directed surfaces in B2.5.',
    'fhjxreg # Plots the electrostatic energy flow acros',
    'fhjyreg # Plots the electrostatic energy flow across\n'
        'important y-directed surfaces in B2.5.',
    'fhtxreg # Plots the total energy flow across important\n'
        'x-directed surfaces in B2.5.',
    'fhtyreg # Plots the total energy flow across important\n'
        'y-directed surfaces in B2.5.',
    'fluid_fluxes #1 #2 Plots the sum of fluid fluxes for\n'
        'species numbers varying from #1 to #2 (respective\n'
        'defaults are 0 and 1). Also exists as a Python script.\n'
        'Fluxes into the domain are shown as negative values,\n'
        'fluxes out of the domain as positive values.',
    'fluxt #1 Gives the recycling fluxes for the first #1\n'
        'Eirene strata. The default value is all the strata,\n'
        'as read from the b2.neutrals.parameters file, or if\n'
        'not present, the $SOLPSTOP/modules/B2.5/src/include.\n'
        'local/file, if not present, the\n'
        '$SOLPSTOP/modules/B2.5/src/include/DIMENSIONS.F file.',
    'internal_energy_balance # Outputs the energy balance\n'
        'tallies.',
    'internal_energy_balance # coupled Outputs the energy\n'
        'balance tallies for a coupled run.',
    'joule_heating # Plots the amount of Joule heating\n'
        'per region.',
    'mtv_3d # Plots the time evolution of a CDF quantity\n'
        '(Appendix E) profile.',
    'mtv_3d_f # Plots the time evolution of the profile of the\n'
        'flux of a CDF quantity (Appendix E) along the targets.',
    'mtv_3d_nf Plots the time evolution of the profile of a CDF\n'
        'quantity (Appendix E) along both targets side by side.',
    'mtv_3d_t # Plots the time evolution of the profile of the\n'
        'CDF quantity (Appendix E) along the targets.',
    'nareg #1 Shows averaged density per region for species #1.',
    'nareg_species #1 Shows averaged density per species for\n'
        'region #1.',
    'nereg # Shows averaged electron density per region.',
    'nesepm_feedback # Plots in feedback.ps the parameters\n'
        'of the nesepm sol feedback scheme.',
    'nesepm_feedback_by_core # Plots in feedback.ps the\n'
        'parameters of the nesepm feedback scheme.',
    'nesepm_feedback_by_pfr # Plots in feedback.ps the\n'
        'parameters of the nesepm pfr feedback scheme.',
    'nesepm_feedback fluid # Plots in feedback.ps the\n'
        'parameters of the nesepm sol feedback scheme for\n'
        'fluid runs.',
    'nireg # Shows averaged total ion density per region.',
    'printspecies # Prints the list of species included in\n'
        'the run.',
    'reflection # Shows reflected particle fluxes (for B2.5\n'
        'standalone runs).',
    'reflection_energy # Shows reflected energy fluxes\n'
        '(for B2.5 standalone runs).',
    'sputter # Shows sputtering particle fluxes\n'
        '(for B2.5 standalone runs).',
    'sputter_energy # Shows sputtering energy fluxes\n'
        '(for B2.5 standalone runs).',
    'sputter_RES # Shows RES sputtering particle fluxes\n'
        '(for B2.5 standalone runs).',
    'sputter_RES_energy # Shows RES sputtering energy fluxes\n'
        '(for B2.5 standalone runs).',
    'sputter_chemical # Shows chemical sputtering particle\n'
        'fluxes (for B2.5 standalone runs).',
    'sputter_chemical_energy # Shows chemical sputtering\n'
        'energy fluxes (for B2.5 standalone runs).',
    'sputter_physical # Shows physical sputtering particle\n'
        'fluxes (for B2.5 standalone runs).",',
    'sputter_physical_energy # Shows physical sputtering\n'
        'energy fluxes (for B2.5 standalone runs).',
    'thermal_evaporation # Shows thermal evaporation particle\n'
        'fluxes (for B2.5 standalone runs).',
    'thermal_evaporation_energy # Shows thermal evaporation\n'
        'energy fluxes (for B2.5 standalone runs).',
    'tereg # Shows averaged electron temperature per region.',
    'time # dep Script to obtain time traces of many useful\n'
        'quantities.',
    'tireg # Shows averaged ion temperature per region.',
    'viscous # heating Shows the viscous heating term\n'
        'per region.',
    'zeffreg # Shows Zeff per region.'
]


# TODO(mprotic): Add plot description after each # by looking into solps.pdf
_tcsh_solps_scripts_detected = [
    "2d # ",
    "2da # ",
    "2d_plots # ",
    "2dt # ",
    "2dt_jdl # ",
    "plot_mesh # ",
    "b2plot # ",
    "b2stbc_sch_reg_region # ",
    "b2stbc_she_reg_region # ",
    "b2stbc_shi_reg_region # ",
    "b2stbc_smo_reg # ",
    "b2stbc_smo_reg_region # ",
    "b2stbc_sna_reg # ",
    "b2stbc_sna_reg_region # ",
    "b2stbc_sne_reg_region # ",
    "b2stbm_sch_reg_region # ",
    "b2stbm_she_reg_region # ",
    "b2stbm_shi_reg_region # ",
    "b2stbm_smo_reg # ",
    "b2stbm_smo_reg_region # ",
    "b2stbm_sna_reg # ",
    "b2stbm_sna_reg_region # ",
    "b2stbm_sne_reg_region # ",
    "b2stbr_sch_reg_region # ",
    "b2stbr_she_reg_region # ",
    "b2stbr_shi_reg_region # ",
    "b2stbr_smo_reg # ",
    "b2stbr_smo_reg_region # ",
    "b2stbr_sna_reg # ",
    "b2stbr_sna_reg_region # ",
    "b2stbr_sne_reg_region # ",
    "D0_fluid_fluxes # ",
    "D_coupled_conservation # ",
    "D_coupled_conservation_core # ",
    "delta # ",
    "density # ",
    "D_fluid_conservation # ",
    "D_fluid_conservation_core # ",
    "D_fluid_fluxes # ",
    "D+_fluid_fluxes # ",
    "energy_analysis # ",
    "energy_analysis_fht # ",
    "energy_analysis_total # ",
    "energy_balance # ",
    "energy_balance_core # ",
    "energy_balance_core_extended # ",
    "energy_balance_extended # ",
    "fhexreg # ",
    "fheyreg # ",
    "fhixreg # ",
    "fhiyreg # ",
    "fhjxreg # ",
    "fhjyreg # ",
    "fhmxreg # ",
    "fhmyreg # ",
    "fhpxreg # ",
    "fhtxreg # ",
    "fhtyreg # ",
    "fluid_fluxes # ",
    "fluxt # ",
    "He_coupled_conservation_core # ",
    "He_fluid_conservation # ",
    "He_fluid_fluxes # ",
    "joule_heating # ",
    "mtv_3d # ",
    "mtv_3d_f # ",
    "mtv_3d_nf # ",
    "mtv_3d_t # ",
    "na_feedback_actuator # ",
    "na_feedback_actuator_all # ",
    "na_feedback_rescale # ",
    "na_feedback_rescale_all # ",
    "nareg # ",
    "nareg_species # ",
    "nereg # ",
    "nesepm_feedback # ",
    "nesepm_feedback_by_core # ",
    "nesepm_feedback_by_pfr # ",
    "nesepm_feedback_fluid # ",
    "nireg # ",
    "plot # ",
    "plot_cps # ",
    "plot_it # ",
    "plot_mesh # ",
    "plot_png # ",
    "plot_ps # ",
    "plot_set # ",
    "rcxhireg # ",
    "rcxhireg_region # ",
    "rcxnareg # ",
    "rcxnareg_region # ",
    "reflection # ",
    "reflection_energy # ",
    "resall_D # ",
    "resall_D+D # ",
    "resall_D+_only # ",
    "resall_D+T # ",
    "resall_H # ",
    "resave_mds # ",
    "resco # ",
    "resco_D+C # ",
    "resco_D+C+He # ",
    "resco_D+O # ",
    "resco_reg # ",
    "resco_reg_region # ",
    "res_D+C # ",
    "res_D+C+Ar+Ne+He # ",
    "res_D+C+He # ",
    "res_D+O # ",
    "reshe_reg # ",
    "reshi_reg # ",
    "resmo # ",
    "resmo_D+C # ",
    "resmo_D+C+He # ",
    "resmo_D+O # ",
    "resmo_reg # ",
    "resmo_reg_region # ",
    "resmt_reg # ",
    "respo # ",
    "respo_num # ",
    "respo_reg # ",
    "resrest # ",
    "rqahereg # ",
    "rqahereg_region # ",
    "rqbrmreg # ",
    "rqradreg # ",
    "rqradreg_region # ",
    "rrahireg # ",
    "rrahireg_region # ",
    "rranareg # ",
    "rranareg_region # ",
    "rsahireg # ",
    "rsahireg_region # ",
    "rsanareg # ",
    "rsanareg_region # ",
    "save_mds # ",
    "sputter # ",
    "sputter_chemical # ",
    "sputter_chemical_energy # ",
    "sputter_energy # ",
    "sputter_physical # ",
    "sputter_physical_energy # ",
    "sputter_RES # ",
    "sputter_RES_energy # ",
    "summarize_run # ",
    "tereg # ",
    "thermal_evaporation # ",
    "thermal_evaporation_energy # ",
    "tireg # ",
    "triang # ",
    "viscous_heating # ",
    "xlyplot # ",
    "xlyplot2 # ",
    "xlyplot3 # ",
    "xlyplot4 # ",
    "xlyplot5 # ",
    "xlyplot6 # ",
    "xlyplot7 # ",
    "xlyplot8 # ",
    "xlyplot9 # ",
    "xyplot # ",
    "xyplot2 # ",
    "xyplot3 # ",
    "xyplot4 # ",
    "xyplot5 # ",
    "xyplot6 # ",
    "xyplot7 # ",
    "xyplot8 # ",
    "xyplot9 # ",
    "zeffreg # ",
]


if __name__ == "__main__":

    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = SolpsPlots()
    window.show()
    sys.exit(app.exec_())


