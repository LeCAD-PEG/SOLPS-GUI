#!/usr/bin/env python3

"""

A PyQt custom widget with embedded list of SOLPS scripts.

"""

from PyQt5.QtCore import Qt, QProcess, QSize, pyqtSlot, pyqtProperty
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QComboBox


class SolpsTcshPlots(QComboBox):
    """SolpsTcshPlots(QComboBox)
    
    Provides a custom widget that holds all SOLPS Gnuplot script names
    for combining them with
    """
    
    def __init__(self, parent=None):
        super(SolpsTcshPlots, self).__init__(parent)
        self.setEditable(True)
        self.addItems(_tcsh_solps_scripts)

    @pyqtSlot()
    def triggerTextChanged(self):
        """ Connector that receives a signal and re-emits the current text.
        """
        self.editTextChanged.emit(self.currentText())
        self.currentTextChanged.emit(self.currentText())

# List of TCSH plot scripts in solps-iter/scripts obtained by
# grep -H plot * | grep -v .py | \
#  sed 's/\([a-zA-Z0-9_+-]*\):.*/    \"\1 # \",/' | sort | uniq
# TODO(mprotic): Add plot description after each # by looking into solps.pdf
_tcsh_solps_scripts = [
    "sin(x)",
    "sin(3*x)/x",
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
    window = SolpsTcshPlots()
    window.show()
    sys.exit(app.exec_())


