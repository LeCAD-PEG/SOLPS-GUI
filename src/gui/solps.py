#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" SOLPS GUI aims controlling SOLPS-ITER code suite with a framework
consisting of various tools aiming at improving the user’s experience,
to accelerate and simplify run input set-up, and to increase the scientific
us ability of the B2.5-Eirene  simulation results. GUI allows a large set of
runs  to be scanned, identifying the state they are in, and providing a
framework for in-line analysis and run re-launch, including input file editing
beforehand.

Example:
  Running the GUI requires Python3 and PySide6 to be installed::

    $ python3 solps.py

  or::

    $ ./solps.py

Notes:
    Listed Runs can receive status updates from network with single line
    UDP message with netcat utility or from the client that can broadcast
    to multiple IP destinations at once.

.. _Google Python Style Guide:
   http://google-styleguide.googlecode.com/svn/trunk/pyguide.html
   http://sphinx-doc.org/ext/example_google.html#example-google
   https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html#example-google
   http://sphinx-doc.org/ext/napoleon.html#module-sphinx.ext.napoleon
   Author: Leon Kos, University of Ljubljana
  
"""

import getopt
import logging
import os
import shutil
import sys
import time

from PySide6.QtCore import (Slot, QModelIndex, Qt, QSettings, Signal,
                            QRegularExpression, QProcess, QTimer)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox, QDialog,
                             QFileDialog, QLineEdit, QToolButton, QGridLayout,
                             QDialogButtonBox, QLabel, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QPlainTextEdit)
from PySide6.QtNetwork import QUdpSocket
from PySide6.QtNetwork import QHostAddress
from PySide6.QtUiTools import loadUiType


from addmenu import AddMenu


class Column(object):
    """Column enumeration for Runs treeview.parent

        First column `name` cannot be moved and is short name.

    Attributes:
        name : Basename of the directory
        path : Full path to the directory
        date : Last status update of the directory. Uses LC_TIME environment.
        status : Status retrieved from status & log files or via network update
        label : One line description of the run from b2mn.dat
        comment : User comment on simulation.
        device : Device name.
        shot : Number for shot.
        run : Number for run.
    """
    name, path, date, status, label, comment, device, shot, run, user = \
        range(10)
    headerData = ['Name', 'Path', 'Date', 'Status', 'Label',
                  'Comment', 'Device', 'Shot', 'Run', 'User']
    n = 10


class MyLineEdit(QLineEdit):
    def __init__(self, name, row, column):
        super(MyLineEdit, self).__init__(name)
        self.i = row
        self.j = column


class MyToolButton(QToolButton):
    def __init__(self, row, column):
        super(MyToolButton, self).__init__()
        self.i = row
        self.j = column


class RunsSettings(QDialog):
    def __init__(self, parent=None):
        super(RunsSettings, self).__init__()
        self.setModal(True)
        self.main_layout = QGridLayout(self)
        self.setWindowTitle('Runs directories')
        settings = QSettings("ITER", "solps-gui")
        settings.beginGroup("RunDirectories")

        self.alias_base = 'Alias'
        self.runDir_base = 'runDir'

        label_1 = QLabel('Runs Alias')
        label_2 = QLabel('Runs Directory')
        self.main_layout.addWidget(label_1, 0, 0, Qt.AlignCenter)
        self.main_layout.addWidget(label_2, 0, 1, Qt.AlignLeft)

        for i in range(5):
            entry_1 = MyLineEdit(settings.value('Alias' + str(i + 1)), i, 0)
            entry_1.setAlignment(Qt.AlignCenter)

            entry_2 = MyLineEdit(settings.value('runDir' + str(i + 1)), i, 1)
            entry_2.setMinimumWidth(350)

            button_1 = MyToolButton(i, 2)
            button_1.setText('...')
            button_1.clicked.connect(self.dialog_action)

            self.main_layout.addWidget(entry_1, i + 1, 0, Qt.AlignCenter)
            self.main_layout.addWidget(entry_2, i + 1, 1)
            self.main_layout.addWidget(button_1, i + 1, 2, Qt.AlignCenter)
        settings.endGroup()
        # Adding the Ok and Cancel button.
        dialog_button_box = QDialogButtonBox()
        dialog_button_box.setStandardButtons(QDialogButtonBox.Ok |
                                             QDialogButtonBox.Cancel)
        dialog_button_box.accepted.connect(self.accept)
        dialog_button_box.rejected.connect(self.reject)
        self.main_layout.addWidget(dialog_button_box, 6, 1)
        self.setLayout(self.main_layout)

    @Slot()
    def dialog_action(self):
        """ When the tool button is clicked a directory browser is opened. If
        a new directory is opened, the new value is then assigned to the
        correct alias and runDir setting.
        """
        widget = self.sender()
        i = widget.i  # row
        j = widget.j  # column
        current_dir = self.main_layout.itemAt(2+i*3+j-1).widget().text()

        if current_dir == "":
            current_dir = os.path.expanduser("~")

        new_dir = QFileDialog.getExistingDirectory(self,
                                                   "Select Directory",
                                                   current_dir,
                                                   QFileDialog.ShowDirsOnly)

        if new_dir:
            line_edit = self.main_layout.itemAt(2+i*3+j-1).widget()
            line_edit.setText(new_dir)

    def on_close(self):
        settings = QSettings('ITER', 'solps-gui')
        settings.beginGroup('RunDirectories')
        for i in range(5):
            alias_name = self.alias_base + str(i + 1)
            value = self.main_layout.itemAt(2 + i * 3).widget().text()
            settings.setValue(alias_name, value)

            runDir_name = self.runDir_base + str(i + 1)
            value = self.main_layout.itemAt(2 + i * 3 + 1).widget().text()
            settings.setValue(runDir_name, value)
        settings.endGroup()


class Preferences():
    """
    Class that holds preferences and allows reading/writing them permanently
    """

    def __init__(self, parent=None):
        super(Preferences, self).__init__()
        # Create reasonable defaults
        self.bind_address = '0.0.0.0'
        self.port = 0xCAFE + os.getuid() % 13566
        self.solps_gui_ip = '127.0.0.1'
        self.tcsh_path = '/bin/tcsh'
        self.gnuplot_path = '/usr/bin/gnuplot'
        self.convert_path = '/usr/bin/convert'
        self.browser_path = '/usr/bin/firefox'
        self.log_level = 1  # info
        self.submit_script = 'localsubmit'
        self.run_mode = ""
        self.job_name = 'SOLPS-ITER'
        self.standalone = 0
        self.use_mpi = 0
        self.mpi_options = '-np 16'
        self.use_debugger = 0
        self.debugger = 'totalview'
        self.compress_log = 0
        self.dry_run = 0
        self.use_openmp = 0
        self.threads = ''
        self.time = ''
        self.partition = ''
        self.nodes = ''
        self.memory = ''
        self.device_environment = 'ITER'
        self.compiler_environment = 'ifort64'

    def read(self):
        """  Reads Preferences from QSettings()
        """
        settings = QSettings('ITER', 'solps-gui')
        self.bind_address = settings.value('SOLPS_GUI_BIND', self.bind_address)
        self.port = int(settings.value('SOLPS_GUI_PORT', self.port))
        self.solps_gui_ip = settings.value('SOLPS_GUI_IP', self.solps_gui_ip)
        self.tcsh_path = settings.value('tcsh_path', self.tcsh_path)
        self.gnuplot_path = settings.value('gnuplot_path', self.gnuplot_path)
        self.convert_path = settings.value('convert_path', self.convert_path)
        self.browser_path = settings.value('browser_path', self.browser_path)
        self.log_level = int(settings.value('log_level', self.log_level))
        self.submit_script = settings.value('submit_script', self.submit_script)
        self.run_mode = settings.value("run_mode", "")
        self.job_name = settings.value('job_name', self.job_name)
        self.standalone = int(settings.value('standalone', self.standalone))
        self.use_mpi = int(settings.value('use_mpi', self.use_mpi))
        self.mpi_options = settings.value('mpi_options', self.mpi_options)
        self.use_debugger = int(settings.value('use_debugger', self.use_debugger))
        self.debugger = settings.value('debugger', self.debugger)
        self.compress_log = int(settings.value('compress_log', self.compress_log))
        self.dry_run = int(settings.value('dry_run', self.dry_run))
        self.use_openmp = int(settings.value('use_openmp', self.use_openmp))
        self.threads = settings.value('threads', self.threads)
        self.time = settings.value('time', self.time)
        self.partition = settings.value('partition', self.partition)
        self.nodes = settings.value('nodes', self.nodes)
        self.memory = settings.value('memory', self.memory)
        self.device_environment = settings.value('device_environment', self.device_environment)
        self.compiler_environment = settings.value('compiler_environment', self.compiler_environment)

    def write(self):
        """ Writes preference to disk
        """
        settings = QSettings('ITER', 'solps-gui')
        settings.setValue('SOLPS_GUI_BIND', self.bind_address)
        settings.setValue('SOLPS_GUI_PORT', str(self.port))
        settings.setValue('SOLPS_GUI_IP', self.solps_gui_ip)
        settings.setValue('tcsh_path', self.tcsh_path)
        settings.setValue('gnuplot_path', self.gnuplot_path)
        settings.setValue('convert_path', self.convert_path)
        settings.setValue('browser_path', self.browser_path)
        settings.setValue('log_level', str(self.log_level))
        settings.setValue('submit_script', self.submit_script)
        settings.setValue("run_mode", self.run_mode)
        settings.setValue('job_name', self.job_name)
        settings.setValue('standalone', str(self.standalone))
        settings.setValue('use_mpi', str(self.use_mpi))
        settings.setValue('mpi_options', self.mpi_options)
        settings.setValue('use_debugger', str(self.use_debugger))
        settings.setValue('debugger', self.debugger)
        settings.setValue('compress_log', self.compress_log)
        settings.setValue('dry_run', str(self.dry_run))
        settings.setValue('use_openmp', str(self.use_openmp))
        settings.setValue('threads', self.threads)
        settings.setValue('time', self.time)
        settings.setValue('partition', self.partition)
        settings.setValue('nodes', self.nodes)
        settings.setValue('memory', self.memory)
        settings.setValue('device_environment', str(self.device_environment))
        settings.setValue('compiler_environment', str(self.compiler_environment))


class PreferencesDialog(QDialog):
    """ Maps dialog into Preferences.
    """

    def __init__(self, preferences, parent=None):
        super(PreferencesDialog, self).__init__()
        prefix = os.path.dirname(os.path.abspath(__file__))
        uiclass, baseclass = loadUiType(prefix + '/preferences.ui')
        self.form = uiclass()
        self.form.setupUi(self)

        self.preferences = preferences

        self._mode_buttons = [
            self.form.radioButton_tgt,
            self.form.radioButton_adj,
            self.form.radioButton_opt_tgt,
            self.form.radioButton_opt_adj,
        ]

        for button in self._mode_buttons:
            button.setAutoExclusive(False)
            button.clicked.connect(self.on_mode_button_clicked)

        self.form.lineEdit_monitor_interface.setText(preferences.bind_address)
        self.form.lineEdit_monitor_port.setText(str(preferences.port))
        self.form.lineEdit_monitor_ip.setText(preferences.solps_gui_ip)
        self.form.lineEdit_tcsh_path.setText(preferences.tcsh_path)
        self.form.lineEdit_gnuplot_path.setText(preferences.gnuplot_path)
        self.form.lineEdit_convert_path.setText(preferences.convert_path)
        self.form.lineEdit_browser_path.setText(preferences.browser_path)
        self.form.comboBox_log_level.setCurrentIndex(preferences.log_level)
        self.form.comboBox_submit_script.setCurrentText(preferences.submit_script)

        mode = preferences.run_mode
        if mode == "tgt":
            self.form.radioButton_tgt.setChecked(True)
        elif mode == "adj":
            self.form.radioButton_adj.setChecked(True)
        elif mode == "opt_tgt":
            self.form.radioButton_opt_tgt.setChecked(True)
        elif mode == "opt_adj":
            self.form.radioButton_opt_adj.setChecked(True)

        for button in self._mode_buttons:
            button._was_checked = button.isChecked()

        self.form.lineEdit_job_name.setText(preferences.job_name)
        self.form.checkBox_standalone.setChecked(int(preferences.standalone))
        self.form.checkBox_use_mpi.setChecked(int(preferences.use_mpi))
        self.form.lineEdit_mpi_options.setText(preferences.mpi_options)
        self.form.checkBox_use_debugger.setChecked(int(preferences.use_debugger))
        self.form.lineEdit_debugger.setText(preferences.debugger)
        self.form.checkBox_compress_log.setChecked(int(preferences.compress_log))
        self.form.checkBox_dry_run.setChecked(int(preferences.dry_run))
        self.form.checkBox_use_openmp.setChecked(int(preferences.use_openmp))
        self.form.lineEdit_threads.setText(preferences.threads)
        self.form.lineEdit_time.setText(preferences.time)
        self.form.lineEdit_partition.setText(preferences.partition)
        self.form.lineEdit_nodes.setText(preferences.nodes)
        self.form.lineEdit_memory.setText(preferences.memory)
        self.form.comboBox_device_environment.setCurrentText(preferences.device_environment)
        self.form.comboBox_compiler_environment.setCurrentText(preferences.compiler_environment)

    def on_mode_button_clicked(self):
        clicked_button = self.sender()

        if getattr(clicked_button, "_was_checked", False):
            clicked_button.setChecked(False)
            clicked_button._was_checked = False
            return

        for button in self._mode_buttons:
            button.setChecked(button is clicked_button)
            button._was_checked = (button is clicked_button)

    def setPreferences(self):
        self.preferences.bind_address = self.form.lineEdit_monitor_interface.text()
        self.preferences.port = int(self.form.lineEdit_monitor_port.text())
        self.preferences.solps_gui_ip = self.form.lineEdit_monitor_ip.text()
        self.preferences.tcsh_path = self.form.lineEdit_tcsh_path.text()
        self.preferences.gnuplot_path = self.form.lineEdit_gnuplot_path.text()
        self.preferences.convert_path = self.form.lineEdit_convert_path.text()
        self.preferences.browser_path = self.form.lineEdit_browser_path.text()
        self.preferences.log_level = self.form.comboBox_log_level.currentIndex()
        self.preferences.submit_script = self.form.comboBox_submit_script.currentText()

        if self.form.radioButton_tgt.isChecked():
            self.preferences.run_mode = "tgt"
        elif self.form.radioButton_adj.isChecked():
            self.preferences.run_mode = "adj"
        elif self.form.radioButton_opt_tgt.isChecked():
            self.preferences.run_mode = "opt_tgt"
        elif self.form.radioButton_opt_adj.isChecked():
            self.preferences.run_mode = "opt_adj"
        else:
            self.preferences.run_mode = ""

        self.preferences.job_name = self.form.lineEdit_job_name.text()
        self.preferences.standalone = int(self.form.checkBox_standalone.isChecked())
        self.preferences.use_mpi = int(self.form.checkBox_use_mpi.isChecked())
        self.preferences.mpi_options = self.form.lineEdit_mpi_options.text()
        self.preferences.use_debugger = int(self.form.checkBox_use_debugger.isChecked())
        self.preferences.debugger = self.form.lineEdit_debugger.text()
        self.preferences.compress_log = int(self.form.checkBox_compress_log.isChecked())
        self.preferences.dry_run = int(self.form.checkBox_dry_run.isChecked())
        self.preferences.use_openmp = int(self.form.checkBox_use_openmp.isChecked())
        self.preferences.threads = self.form.lineEdit_threads.text()
        self.preferences.time = self.form.lineEdit_time.text()
        self.preferences.partition = self.form.lineEdit_partition.text()
        self.preferences.nodes = self.form.lineEdit_nodes.text()
        self.preferences.memory = self.form.lineEdit_memory.text()
        self.preferences.device_environment = self.form.comboBox_device_environment.currentText()
        self.preferences.compiler_environment = self.form.comboBox_compiler_environment.currentText()


    def setPreferences(self):
        # s = QSettings('ITER', 'solps-gui')
        self.preferences.bind_address = self.form.lineEdit_monitor_interface.text()
        self.preferences.port = int(self.form.lineEdit_monitor_port.text())
        self.preferences.solps_gui_ip = self.form.lineEdit_monitor_ip.text()
        self.preferences.tcsh_path = self.form.lineEdit_tcsh_path.text()
        self.preferences.gnuplot_path = self.form.lineEdit_gnuplot_path.text()
        self.preferences.convert_path = self.form.lineEdit_convert_path.text()
        self.preferences.browser_path = self.form.lineEdit_browser_path.text()
        self.preferences.log_level = self.form.comboBox_log_level.currentIndex()
        self.preferences.submit_script = self.form.comboBox_submit_script.currentText()
        if self.form.radioButton_tgt.isChecked():
            self.preferences.run_mode = "tgt"
        elif self.form.radioButton_adj.isChecked():
            self.preferences.run_mode = "adj"
        elif self.form.radioButton_opt_tgt.isChecked():
            self.preferences.run_mode = "opt_tgt"
        elif self.form.radioButton_opt_adj.isChecked():
            self.preferences.run_mode = "opt_adj"
        else:
            self.preferences.run_mode = ""
        self.preferences.job_name = self.form.lineEdit_job_name.text()
        self.preferences.standalone = int(self.form.checkBox_standalone.isChecked())
        self.preferences.use_mpi = int(self.form.checkBox_use_mpi.isChecked())
        self.preferences.mpi_options = self.form.lineEdit_mpi_options.text()
        self.preferences.use_debugger = int(self.form.checkBox_use_debugger.isChecked())
        self.preferences.debugger = self.form.lineEdit_debugger.text()
        self.preferences.compress_log = int(self.form.checkBox_compress_log.isChecked())
        self.preferences.dry_run = int(self.form.checkBox_dry_run.isChecked())
        self.preferences.use_openmp = int(self.form.checkBox_use_openmp.isChecked())
        self.preferences.threads = self.form.lineEdit_threads.text()
        self.preferences.time = self.form.lineEdit_time.text()
        self.preferences.partition = self.form.lineEdit_partition.text()
        self.preferences.nodes = self.form.lineEdit_nodes.text()
        self.preferences.memory = self.form.lineEdit_memory.text()
        self.preferences.device_environment = self.form.comboBox_device_environment.currentText()
        self.preferences.compiler_environment = self.form.comboBox_compiler_environment.currentText()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyle("windows")

    prefix = os.path.dirname(os.path.abspath(__file__))
    ui_path = prefix + '/solps.ui'
    try:
        opts, args = getopt.getopt(app.arguments()[1:],
                                   "hu:d", ["help", "ui=", "default"])
    except getopt.GetoptError:
        print('Supplied option not recognized!')
        print('For help: solps.py -h / --help')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print('Load default user interface : solps.py')
            print('Load custom user interface : solps.py '
                  '[-u / --ui] <UIfile.ui>')
            sys.exit(2)
        elif opt in ("-u", "--ui"):
            ui_path = os.path.abspath(arg)

    if os.path.exists(ui_path):
        ui_filename, ui_extension = os.path.splitext(ui_path)
        if ui_extension == '.ui':
            ui_class, widget_class = loadUiType(ui_path)
        else:
            print(ui_path + ' should have .ui extension')
            sys.exit(2)
    else:
        print(ui_path + ' not found')
        sys.exit(2)


    class SOLPS_MainWindow(ui_class, widget_class):
        """Main window of the SOLPS GUI

        Attributes:
            log_thread(QThread) : Thread for Logging facility in Log tab.
            log_receiver(LogReceiver) : Receiving messages from logging thread.
            stdout_thread(QThread) : Redirected sys.stdout to Log tab.
            stdout_receiver(LogReceiver): Receiver for stdout thread.
            b2_user (Signal(str)): Emits the string for user value
            b2_run_number (Signal(str)): Emits the string for run value
            b2_shot_number (Signal(str)): Emits the string for shot value
            b2_device (Signal(str)): Emits the string for device value
        """

        runSelected = Signal(str)
        b2_user = Signal(str)
        b2_run_number = Signal(str)
        b2_shot_number = Signal(str)
        b2_device = Signal(str)

        def __init__(self, *args):
            super().__init__(*args)
            self.setupUi(self)

            self.initialize_run.runDirCombo.currentTextChanged.connect(
                self.updateTangentRunDir)
            self.initialize_run.runDirCombo.currentTextChanged.connect(
                self.updateAdjointRunDir)
            self.initialize_run.runDirCombo.currentTextChanged.connect(
                self.updateOptimizationRunDir)

            self.setAttribute(Qt.WA_DeleteOnClose, True)

            self.addMenu = AddMenu(self.menubar)
            self.menubar.insertMenu(self.menu_Help.menuAction(), self.addMenu)
            self.addMenu.output.connect(self.solpsinput.insert_line)
            self.solpsinput.editorChanged.connect(self.addMenu.editorChanged)

            self.preferences = Preferences()
            self.preferences.read()

            self.main_tcsh = QProcess(self)  # for job submission and scripting
            self.main_tcsh.setProcessChannelMode(QProcess.MergedChannels)
            self.main_tcsh.readyReadStandardOutput.connect(self.read_main_tcsh)
            self.solps_top = None  # Current active ${SOLPSTOP} for tcsh

            self.previous_tab_index = None   # For auto saving of Edit tab
            self.input_tab_index = self.tabWidget.indexOf(self.tab_Input)

            settings = QSettings("ITER", "solps-gui")
            settings.beginGroup("MainWindow")
            geometry = settings.value("Geometry")
            if geometry:
                self.restoreGeometry(geometry)
            state = settings.value("State")
            if state:
                self.restoreState(state)
            settings.endGroup()

            self.actionAbout_Qt.triggered.connect(QApplication.instance().aboutQt)

            # TODO
            self.comboBoxRunFilterType.addItem("Regular expression",
                                               QRegularExpression)
            self.comboBoxRunFilterType.addItem("Wildcard", QRegularExpression.WildcardConversionOption)
            self.comboBoxRunFilterType.addItem("Fixed string", QRegularExpression.escape)

            self.filterCaseSensitivityCheckBox.setChecked(True)

            self.lineEditRunFilter.returnPressed.connect(self.textFilterChanged)


            # Tree view for run directories
            # self.model = self.treeViewRuns.model
            # self.proxyModel = self.treeViewRuns.proxyModel
            # Tree view for archived run directories
            # self.archiveProxyModel = self.treeViewArchive.archiveModel

            # Assign the same source model for the archive treeview.
            self.treeViewArchive.setArchiveSourceModel(self.treeViewRuns.model().sourceModel())

            # Setup input tabs
            self.solpsinput.setup_input_tabs()
            self.tab_Input.setEnabled(False)

            self.actionPreferences.triggered.connect(self.show_preferences_dialog)
            self.actionRuns.triggered.connect(self.show_runs_dialog)
            self.treeViewRuns.selectionModel().selectionChanged.connect(
                self.run_selected)
            self.treeViewArchive.selectionModel().selectionChanged.connect(
                self.enable_restore_button)

            # Configure Dashboard
            # self.gnuplot.plot("sin(3*x)/x")
            # self.runSelected.connect(self.label_7.setText)
            self.runSelected.connect(self.director.setRundir)
            self.b2_device.connect(self.director.b2_device)
            self.b2_user.connect(self.director.b2_user)
            self.b2_run_number.connect(self.director.b2_run_number)
            self.b2_shot_number.connect(self.director.b2_shot_number)

            # self.runSelected.connect(self.tcsh.setRundir)
            # self.tcsh.setTcshCommand(self.lineEdit.text())
            #  self.gnuplot.setText("Started")
            #  print(self.gnuplot.process.state())
            #  self.gnuplot1.process.finished.connect(self.gnuplot1.show_plot)

            # Activate debugging on DivGeo widget
            # self.divgeo.activateDebugging()

            # Connect id signals to put_edge_ids object (solps.ui)
            # self.b2_device.connect(self.put_edge_ids.setDevice)
            # self.b2_user.connect(self.put_edge_ids.setUser)
            # self.b2_run_number.connect(self.put_edge_ids.setRun)
            # self.b2_shot_number.connect(self.put_edge_ids.setShot)
            self.sinfoTimer = QTimer(self)
            self.sinfoTimer.setInterval(3000)

            self.squeueTimer = QTimer(self)
            self.squeueTimer.setInterval(3000)

            self.sinfoProcess = QProcess(self)
            self.squeueProcess = QProcess(self)
            self.scancelProcess = QProcess(self)

            self.sinfoProcess.setProcessChannelMode(QProcess.MergedChannels)
            self.squeueProcess.setProcessChannelMode(QProcess.MergedChannels)
            self.scancelProcess.setProcessChannelMode(QProcess.MergedChannels)

            self.pushButtonStartSinfo.clicked.connect(self.start_sinfo_monitor)
            self.pushButtonStopSinfo.clicked.connect(self.stop_sinfo_monitor)
            self.pushButtonStartSqueue.clicked.connect(self.start_squeue_monitor)
            self.pushButtonStopSqueue.clicked.connect(self.stop_squeue_monitor)
            self.pushButtonScancel.clicked.connect(self.cancel_selected_job)

            self.sinfoTimer.timeout.connect(self.run_sinfo_once)
            self.squeueTimer.timeout.connect(self.run_squeue_once)

            self.sinfoProcess.readyReadStandardOutput.connect(self.read_sinfo_output)
            self.squeueProcess.readyReadStandardOutput.connect(self.read_squeue_output)
            self.scancelProcess.readyReadStandardOutput.connect(self.read_scancel_output)

        # @Slot()
        # def on_pushButton_Archive_clicked(self):
        #     """ Selecting directory and pressing Archive will add
        #     selected directory to filtered set and will not be shown in Runs.
        #     """
        #     index = self.treeViewRuns.selectionModel().currentIndex()
        #     model = self.proxyModel
        #     index_path = model.index(index.row(), Column.path, index.parent())
        #     path = model.data(index_path, Qt.DisplayRole)

        #     # self.archive_dirs.add(path)
        #     self.archiveDirs.add(path)
        #     self.proxyModel.invalidateFilter()
        #     self.archiveProxyModel.invalidateFilter()
        #     self.updateArchiveDirSettings()

        # @Slot()
        # def on_pushButton_Restore_clicked(self):
        #     index = self.treeViewArchive.selectionModel().currentIndex()
        #     arModel = self.archiveProxyModel
        #     index_path = arModel.index(index.row(), Column.path, index.parent())
        #     path = arModel.data(index_path, Qt.DisplayRole)

        #     if path in self.proxyModel.archiveDirs:
        #         self.proxyModel.archiveDirs.remove(path)
        #         self.proxyModel.invalidateFilter()
        #         self.archiveProxyModel.invalidateFilter()
        #         self.updateArchiveDirSettings()
        #     else:
        #         msg = "Can only remove archived directories marked with icons!"
        #         QMessageBox.warning(self, 'Invalid action', msg)

        # def updateArchiveDirSettings(self):
        #     settings = QSettings("ITER", "solps-gui")
        #     settings.beginGroup("Archive")
        #     settings.beginWriteArray("dirs")
        #     for i, directory in enumerate(self.proxyModel.archiveDirs):
        #         settings.setArrayIndex(i)
        #         settings.setValue("dir", directory)
        #     settings.endArray()
        #     settings.endGroup()

        
        def updateTangentRunDir(self):
            try:
                runDir = self.initialize_run.getSelectedRunDirectory()
            except Exception:
                runDir = ''

            if not runDir:
                runDir = ''

            self.tangentActor.setSelectedRunDir(runDir)
        def updateAdjointRunDir(self):
            try:
                runDir = self.initialize_run.getSelectedRunDirectory()
            except Exception:
                runDir = ''

            if not runDir:
                runDir = ''

            self.adjointActor.setRunDir(runDir)


        def updateOptimizationRunDir(self):
            try:
                runDir = self.initialize_run.getSelectedRunDirectory()
            except Exception:
                runDir = ''

            if not runDir:
                runDir = ''

            self.optimizationActor.setRunDir(runDir)

        @Slot(int)
        def on_tabWidget_currentChanged(self, tab_index):
            """ Signal is received when tab on main window is changed.
                We check if the Edit tab lost its focus and save modified files.

                Arguments:
                     tab_index (int): current tab index selected
            """
            if tab_index != self.input_tab_index \
                    and self.previous_tab_index == self.input_tab_index:
                self.solpsinput.save_modified_input_files()
            self.previous_tab_index = tab_index

        @Slot()
        def on_pushButton_Edit_clicked(self):
            """ For selected run and Edit button pressed Input tab is focused
                with all SOLPS input files modifiable with simple text editor.
            """
            self.tabWidget.setCurrentIndex(self.input_tab_index)
            index = self.treeViewRuns.selectionModel().currentIndex()
            model = self.treeViewRuns.model()
            index_path = model.index(index.row(), Column.path, index.parent())
            path = model.data(index_path, Qt.DisplayRole)
            self.statusbar.showMessage('Editing ' + path)
            self.solpsinput.setRundir(path)
            self.solpsinput.read_input_files()
            self.solpsinput.editor_tab_changed(self.solpsinput.currentIndex())
            self.tab_Input.setEnabled(True)

        @Slot()
        def run_selected(self):
            """ Whenever an item in Runs is selected this function is run.

                Archive button is enabled and directory is emited.
            """
            valid = self.treeViewRuns.selectionModel().currentIndex().isValid()
            self.pushButton_Archive.setEnabled(valid)
            self.pushButton_Continue.setEnabled(valid)
            self.pushButton_Edit.setEnabled(valid)
            self.pushButton_Import.setEnabled(valid)
            self.pushButton_Run.setEnabled(valid)
            self.pushButton_Stop.setEnabled(valid)

            if valid:
                index = self.treeViewRuns.selectionModel().currentIndex()
                model = self.treeViewRuns.model()
                index_path = model.index(index.row(), Column.path, index.parent())
                path = model.data(index_path, Qt.DisplayRole)

                index_user = model.index(index.row(), Column.user, index.parent())
                user = model.data(index_user, Qt.DisplayRole)

                if user:
                    self.b2_user.emit(user)

                index_device = model.index(index.row(), Column.device,
                                           index.parent())
                device = model.data(index_device, Qt.DisplayRole)
                if device:
                    self.b2_device.emit(device)

                index_run = model.index(index.row(), Column.run, index.parent())
                run = model.data(index_run, Qt.DisplayRole)

                if run:
                    self.b2_run_number.emit(run)

                index_shot = model.index(index.row(), Column.shot, index.parent())
                shot = model.data(index_shot, Qt.DisplayRole)

                if shot:
                    self.b2_shot_number.emit(shot)

                self.runSelected.emit(path)
                self.updateTangentRunDir()
                self.updateAdjointRunDir()
                self.updateOptimizationRunDir()

        @Slot()
        def enable_restore_button(self):
            valid = self.treeViewArchive.selectionModel().currentIndex().isValid()
            self.pushButton_Restore.setEnabled(valid)

        def textFilterChanged(self):
            # filter_index = self.comboBoxRunFilterType.currentIndex()
            # To do, see QRegularExpression documentation for options and syntaxes.
            # filter_syntax = self.comboBoxRunFilterType.itemData(filter_index)
            # syntax = QRegExp.PatternSyntax(filter_syntax)
            # case_sense = (self.filterCaseSensitivityCheckBox.isChecked() and
                          # QRegularExpression.CaseSensitive or Qt.CaseInsensitive)
            case_sense = 0 if self.filterCaseSensitivityCheckBox.isChecked() else \
                         QRegularExpression.CaseInsensitiveOption
            text = self.lineEditRunFilter.text()
            if text == '':
                # If no filter is provided, then obviously show all.
                text = '.'
            regExp = QRegularExpression(self.lineEditRunFilter.text())#, case_sense)#, syntax)
            if self.filterCaseSensitivityCheckBox.isChecked():
                regExp.setPatternOptions(QRegularExpression.NoPatternOption)
            else:
                regExp.setPatternOptions(QRegularExpression.CaseInsensitiveOption)

            self.treeViewRuns.model().setFilterRegularExpression(regExp)

        @Slot()
        def show_runs_dialog(self):
            dialog = RunsSettings()
            if dialog.exec():
                dialog.on_close()
                model = self.treeViewRuns.model().sourceModel()
                if model.retRunsFolderInfoThread.isRunning() or \
                        model.scanDirectoriesThread.isRunning():
                    msg = "Runs layout changed in the middle of the update." \
                        "Directories cannot be changed. Try settings later."
                    QMessageBox.critical(self, "Restart required", msg)
                else:
                    self.treeViewRuns.expandOnStart = True
                    model.startThreads()
                    # Also remember which directories were open from before.
                    # model.beginResetModel()
                    # model.scanDirectoriesThread.start()
                # TODO(kosl) self.treeViewRuns.model.retRunsFolderInfoThread.quit()
                # self.treeViewRuns.model.scanDirectoriesThread.start()

        @Slot()
        def show_preferences_dialog(self):
            dialog = PreferencesDialog(self.preferences)
            if dialog.exec():
                dialog.setPreferences()
                self.preferences.write()
                model = self.treeViewRuns.model().sourceModel()
                model.statusServerThread.stop()

                address = QHostAddress(self.preferences.bind_address)
                port = self.preferences.port
                if model.statusServerThread.state() == \
                   QUdpSocket.BoundState:
                   model.statusServerThread.close()
                ok = model.statusServerThread.bind(address, port)

                # Also set the log level for LOG widget
                log_levels = [logging.DEBUG, logging.INFO, logging.WARNING,
                              logging.ERROR, logging.CRITICAL]
                log_level = log_levels[self.preferences.log_level]
                self.log.logHandler.setLevel(log_level)


                if ok:
                    # model.statusServerThread.start()
                    logging.info('statusServerThread bind on port '
                                 f'{self.preferences.port} and on address '
                                 f'{self.preferences.bind_address}')
                    pass
                else:
                    msg = "Failed to bind interface {0} to port {1}. " \
                          "Job monitoring will not start unless you " \
                          "setup a free port and restart! ".format(
                           self.preferences.bind_address, self.preferences.port)
                    QMessageBox.warning(None, "SOLPS-GUI Status server", msg,
                                        QMessageBox.Ok)

        def closeEvent(self, event):
            """ Save GUI state at exit.
            Position, size of the main windows and treview columns configuration
            is saved.
            """
            settings = QSettings("ITER", "solps-gui")

            settings.beginGroup("MainWindow")
            settings.setValue("Geometry", self.saveGeometry())
            settings.setValue("State", self.saveState())
            settings.endGroup()

            settings.beginGroup("TreeViewRuns")
            settings.setValue("ColumnWidth",
                              self.treeViewRuns.header().saveState())
            tree_view_model = self.treeViewRuns.model()
            expanded_indexes = self.treeViewRuns.model().persistentIndexList()
            expanded_paths = []
            for index in expanded_indexes:
                path_index = tree_view_model.index(index.row(), Column.path, index.parent())
                expanded_path = tree_view_model.data(path_index, Qt.DisplayRole)
                expanded_paths.append(expanded_path)
            settings.setValue("ExpandedPaths", expanded_paths)
            settings.endGroup()
            settings.beginGroup("TreeViewArchive")
            settings.setValue("ColumnWidth",
                              self.treeViewArchive.header().saveState())
            settings.endGroup()
            # TODO write settings at exit
            # self.preferences.write()

            # Kill the Log gracefully.
            try:
                self.log.finish()
            except:
                pass

            QMainWindow.closeEvent(self, event)

        def expanded(self):
            for column in range(self.treeViewRuns.model().columnCount(QModelIndex())):
                self.resizeColumnToContents(column)

        def change(self, topLeftIndex, bottomRightIndex):
            self.update(topLeftIndex)
            self.expandAll()
            self.expanded()

        @Slot()
        def on_pushButton_Filter_clicked(self):
            self.textFilterChanged()

        @Slot()
        def on_pushButton_Stop_clicked(self):
            """ Signals garceful stop inside b2mn.exe.dir with .quit file.
            """

            index = self.treeViewRuns.selectionModel().currentIndex()
            model = self.treeViewRuns.model()
            index_path = model.index(index.row(), Column.path, index.parent())
            directory = model.data(index_path, Qt.DisplayRole)
            # Is there B2 running directory?
            try:
                b2mn_exe_dir = directory + '/b2mn.exe.dir'
                if os.path.exists(b2mn_exe_dir):
                    path = b2mn_exe_dir + '/.quit'
                    msg = "Graceful stop requested on " + time.ctime()
                    with open(path, 'w') as f:
                        f.write(msg + '\n')
                    index_status = model.index(index.row(), Column.status,
                                               index.parent())
                    model.setData(index_status, msg)
                else:
                    QMessageBox.warning(None, "Invalid stop request",
                                        "No b2mn.dir.exe for graceful stop!")
            except OSError:
                QMessageBox.warning(None, "Permission problem",
                                    "Can't create " + path)

        @Slot()
        def on_pushButton_Run_clicked(self):
            try:
                actor = self.get_active_output_actor()
                if actor is not None and hasattr(actor, "clearOutput"):
                    actor.clearOutput()
            except Exception:
                pass

            index = self.treeViewRuns.selectionModel().currentIndex()
            model = self.treeViewRuns.model()
            index_path = model.index(index.row(), Column.path, index.parent())
            rundir = model.data(index_path, Qt.DisplayRole)
            self.submit(model.mapToSource(index), rundir)

        @Slot()
        def on_pushButton_Continue_clicked(self):
            """ Continues the run by firstly copying the the plasma state output
                to input (b2fstate->b2fstati)
            """
            if self.treeViewRuns.selectionModel().currentIndex().isValid():
                index = self.treeViewRuns.selectionModel().currentIndex()
                model = self.treeViewRuns.model()
                index_path = model.index(index.row(), Column.path, index.parent())
                path = model.data(index_path, Qt.DisplayRole)
                try:
                    shutil.copyfile(path + '/b2fstate', path + '/b2fstati')
                    self.on_pushButton_Run_clicked()
                except IOError:
                    QMessageBox.warning(self, 'Problem copying B2 state file!',
                                        path + '/b2fstati' + " read/write error")

        def find_solps_top(self, directory):
            """ Searches for setup.csh or SOLPSTOP file in the directory hierarchy.
                Arguments:
                    run_directory (str): run_directory
                Returns:
                    solps_top(str): if found setup.csh or SOLPSTOP file. Else None
            """
            solps_top = directory

            while solps_top:
                path = solps_top + '/setup.csh'
                if os.path.exists(path):
                    return solps_top
                path = solps_top + '/SOLPSTOP'
                if os.path.exists(path) and os.access(path, os.R_OK):
                    with open(path) as file:
                        return file.readline()
                solps_top = solps_top.rsplit('/', 1)[0]
            return None

        @Slot()
        def read_main_tcsh(self):
            data = self.main_tcsh.readAllStandardOutput()
            text = str(bytearray(data).decode('utf-8', errors='replace'))

            print(text, end='')

            try:
                actor = self.get_active_output_actor()
                if actor is not None and hasattr(actor, "appendOutput"):
                    actor.appendOutput(text)
            except Exception:
                pass

            try:
                if hasattr(self, "log"):
                    if hasattr(self.log, "appendPlainText"):
                        self.log.appendPlainText(text.rstrip())
                    elif hasattr(self.log, "append"):
                        self.log.append(text.rstrip())
                    elif hasattr(self.log, "textEdit"):
                        self.log.textEdit.append(text.rstrip())
                    elif hasattr(self.log, "plainTextEdit"):
                        self.log.plainTextEdit.appendPlainText(text.rstrip())
            except Exception:
                pass

            logging.info(text.rstrip())

        def get_active_output_actor(self):
            run_mode = self.preferences.run_mode.strip()

            if run_mode == "tgt":
                return self.tangentActor
            elif run_mode == "adj":
                return self.adjointActor
            elif run_mode == "opt_tgt" or run_mode == "opt_adj":
                return self.optimizationActor
            else:
                return self.initialize_run

        @Slot()
        def start_sinfo_monitor(self):
            self.run_sinfo_once()
            self.sinfoTimer.start()

        @Slot()
        def stop_sinfo_monitor(self):
            self.sinfoTimer.stop()

        @Slot()
        def run_sinfo_once(self):
            if self.sinfoProcess.state() == QProcess.NotRunning:
                self.sinfoProcess.start(
                    "bash",
                    ["-lc", 'sinfo -o "%20P %10a %10l %10D %10T %N"']
                )

        @Slot()
        def read_sinfo_output(self):
            data = self.sinfoProcess.readAllStandardOutput()
            text = bytes(data).decode("utf-8", errors="replace")
            self.plainTextEditSinfo.setPlainText(text.rstrip())

        @Slot()
        def start_squeue_monitor(self):
            self.run_squeue_once()
            self.squeueTimer.start()

        @Slot()
        def stop_squeue_monitor(self):
            self.squeueTimer.stop()

        @Slot()
        def run_squeue_once(self):
            if self.squeueProcess.state() == QProcess.NotRunning:
                self.squeueProcess.start(
                    "bash",
                    ["-lc", 'squeue -u $USER -o "%.18i %.9P %.20j %.8u %.8T %.10M %.6D %R"']
                )

        @Slot()
        def read_squeue_output(self):
            data = self.squeueProcess.readAllStandardOutput()
            text = bytes(data).decode("utf-8", errors="replace")
            self.plainTextEditSqueue.setPlainText(text.rstrip())

        @Slot()
        def cancel_selected_job(self):
            job_id = self.lineEditCancelJob.text().strip()
            if not job_id:
                QMessageBox.warning(self, "Missing job id", "Please enter a job id.")
                return

            self.scancelProcess.start(
                "bash",
                ["-lc", f"scancel {job_id} && echo Cancelled {job_id}"]
            )

        @Slot()
        def read_scancel_output(self):
            data = self.scancelProcess.readAllStandardOutput()
            text = bytes(data).decode("utf-8", errors="replace")
            if text.strip():
                QMessageBox.information(self, "scancel", text.strip())
            self.run_squeue_once()

        def execute_tcsh_command_in_rundir(self, tcsh_command, rundir):
            """" Executes TCSH comand in run directory (e.g. submit)

                TCSH environment is searched sourced from 'setup.csh' or pointed
                with SOLPSTOP file. SOLPSTOP is probed for runDir changes and
                if necessary resourced within a new shell. The following
                environment variables are injected for use by scripts::

                    setenv SOLPS_GUI_IP <IP address of the SOLPS GUI monitor>
                    setenv SOLPS_GUI_PORT <listening port>

                Arguments:
                    tcsh_command (str) : command or series of commands separated
                        with newline.
                    rundir (str): prepared run directory
            """
            settings = QSettings('ITER', 'solps-gui')
            tcsh_path = settings.value("tcsh_path", '/bin/tcsh')
            solps_gui_ip = settings.value('SOLPS_GUI_IP', '127.0.0.1')
            default_port = str(0xCAFE + os.getuid() % 13566)
            solps_gui_port = settings.value('SOLPS_GUI_PORT', default_port)
            settings.setValue('SOLPS_GUI_PORT', default_port)

            compiler = settings.value('compiler_environment', 'gfortran')

            rundir_solps_top = self.find_solps_top(rundir)

            if not rundir_solps_top:
                if not rundir:
                    logging.error("Empty TCSH runDir! Bailing out.")
                else:
                    logging.error("Could not find SOLPSTOP for " + rundir)
                return

            if rundir_solps_top != self.solps_top:  # we have new SOLPSTOP
                self.main_tcsh.kill()
                self.main_tcsh.waitForFinished()
                self.solps_top = rundir_solps_top

            cmd = ''
            if self.main_tcsh.state() != QProcess.Running:
                self.main_tcsh.start(tcsh_path, ['-l'])  # TODO settings for -l
                if not self.main_tcsh.waitForStarted():
                    logging.error(self.main_tcsh.program() + " not started")
                    return
                logging.info("MAIN TCSH started in " + self.solps_top)
                cmd += f'cd {self.solps_top}\nsource setup.csh {compiler}\n'
                cmd += 'echo TCSH READY\n'

            cmd += f'setenv SOLPS_GUI_IP {solps_gui_ip}\n'
            cmd += f'setenv SOLPS_GUI_PORT {solps_gui_port}\n'
            cmd += f'cd {rundir}\n'
            cmd += f'{tcsh_command}\n'
            self.main_tcsh.write(bytearray(cmd, 'utf8'))  # TODO flush stdout

        def submit(self, index, rundir):
            """Submits the job in the rundir under its $SOLPSTOP environment.

            All ``*.prt`` files are removed before submission command from
            Preferences is issued.
            """
            submit_command = self.preferences.submit_script.strip()

            cmd = ''
            opts = ''
            model = self.treeViewRuns.model().sourceModel()

            if not submit_command:
                msg = f'batch {rundir} Not submitted!'
                msg += " Empty command or no run directory for MAIN TCSH"
                model.jobStatusChanged(msg)
                logging.warning(msg)
                return

            # add run mode flag
            run_mode = self.preferences.run_mode.strip()
            if run_mode == "tgt":
                opts += ' -tgt'
            elif run_mode == "adj":
                opts += ' -adj'
            elif run_mode == "opt_tgt":
                opts += ' -opt_tgt "tao"'
            elif run_mode == "opt_adj":
                opts += ' -opt_adj "tao"'

            # add job name for batch submit scripts, but not for local run / localsubmit
            if submit_command != 'localsubmit' and submit_command != 'local run' and len(self.preferences.job_name):
                if ' ' in self.preferences.job_name:
                    opts += f' -j "{self.preferences.job_name}"'
                else:
                    opts += f' -j {self.preferences.job_name}'

            if self.preferences.standalone:
                opts += ' -s'
            if self.preferences.use_mpi:
                opts += f' -m "{self.preferences.mpi_options}"'
            if self.preferences.use_debugger:
                opts += f' -d "{self.preferences.debugger}"'
            if self.preferences.compress_log:
                opts += ' -z'
            if self.preferences.dry_run:
                opts += ' -n'
            if self.preferences.use_openmp:
                opts += f' -t "{self.preferences.threads}"'
            if self.preferences.partition:
                opts += f' -Q {self.preferences.partition}'
            if self.preferences.time:
                opts += f' -T {self.preferences.time}'
            if self.preferences.nodes:
                opts += f' -N {self.preferences.nodes}'
            if self.preferences.memory:
                opts += f' -M {self.preferences.memory}'

            cmd += 'rm -rf *.prt\n'

            if submit_command == 'local run':
                cmd += f'b2run{opts} b2mn'
                msg = f'batch {rundir} b2run{opts} b2mn'
            else:
                cmd += f'{submit_command}{opts}'
                msg = f'batch {rundir} {submit_command}{opts}'

            print("FINAL SUBMIT COMMAND:")
            print(cmd)
            logging.info(f"run_mode={self.preferences.run_mode}")
            logging.info(msg)

            self.execute_tcsh_command_in_rundir(cmd, rundir)
            model.jobStatusChanged(msg)        

        @Slot()
        def on_pushButton_Import_clicked(self):
            """ Imports the run or a tree of runs from somewhere into
                the selected tree position. If baserun is imported
                then 'correct_baserun_timestamps' is run under it.

                Files with pattern ``*.log, *.prt, .status*`` and some other
                log files are not imported.

                We need to rescan the whole model as user could possibly renamed
                or deleted some directories by right-click in file-manager.
            """
            if self.treeViewRuns.selectionModel().currentIndex().isValid():
                index = self.treeViewRuns.selectionModel().currentIndex()
                model = self.treeViewRuns.model()
                index_path = model.index(index.row(), Column.path, index.parent())
                destination_dir = model.data(index_path, Qt.DisplayRole)
                selected_dir = QFileDialog.getExistingDirectory(self,
                                                        "Select Directory",
                                                        destination_dir,
                                                       QFileDialog.ShowDirsOnly)
                if selected_dir == '':
                    return
                destination_dir += '/' + os.path.basename(selected_dir)
                try:
                    shutil.copytree(selected_dir, destination_dir, symlinks=True,
                        ignore=shutil.ignore_patterns('*.o[0-9]*', '*.log',
                                '*.e[0-9]*', '*.prt', '.status*'))
                except IOError as err:
                    QMessageBox.warning(self, 'Problem copying selected run tree!',
                        "I/O error {0}".format(err.args))  # TODO Properly format
                    return

                for directory, subdirs, files in os.walk(destination_dir):
                    if os.path.exists(directory + '/baserun'):
                        self.execute_tcsh_command_in_rundir(
                            'correct_baserun_timestamps', directory)
                        logging.info("Imported baserun for " + directory)
                    if os.path.basename(directory) != 'baserun':
                        if os.path.exists(directory + '/input.dat'):
                            cmd = 'setup_baserun_eirene_links'
                            self.execute_tcsh_command_in_rundir(cmd, directory)
                            logging.info("B2 and Eirene links set to baserun for "
                                     + directory)
                        if os.path.exists(directory + '/b2fstati'):
                            cmd = 'touch b2fstati\n'
                            self.execute_tcsh_command_in_rundir(cmd, directory)
                model.startThreads()  # rescan the model

        @Slot()
        def on_actionAbout_triggered(self):
            msg = "GUI will enable users to monitor multiple simultaneously " \
                  "running cases, which requires defining the working directory " \
                  "(folder) for each case to be separated from each other. " \
                  "Input file builder will depend on it to correctly save input " \
                  "files for multiple parameter scan cases."
            QMessageBox.about(self, 'About SOLPS-ITER GUI', msg)

        @Slot()
        def on_actionDocumentation_triggered(self):
            process = QProcess(self)
            solps_gui_home = os.getenv('SOLPS_GUI_HOME',
                                       os.path.expanduser('~/solps-gui'))
            doc_path = os.path.join(solps_gui_home, "doc/build/html/index.html")
            process.startDetached("env", ["--unset", "LD_LIBRARY_PATH",
                                          "xdg-open", doc_path])

    main_window = SOLPS_MainWindow()
    main_window.show()


    code = app.exec()
    app.quit()
    sys.exit(code)