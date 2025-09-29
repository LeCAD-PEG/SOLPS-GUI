#!/usr/bin/env python3
""":class:``initialize_run.InitializeRun`` initializes a populated ``baserun``
directory.
"""
from PySide6.QtWidgets import (QVBoxLayout, QGridLayout, QGroupBox, QComboBox,
                             QFormLayout, QLabel, QSpacerItem, QSizePolicy,
                             QPushButton, QPlainTextEdit, QFileDialog,
                             QMessageBox, QInputDialog, QCheckBox)
from PySide6.QtGui import QTextCursor
from PySide6.QtCore import Slot, QSettings, Qt, QProcess
from tcsh_process import TcshProcess
import os


class InitializeRun(TcshProcess):
    """This widget is used to initialize ``baserun`` directory.
    """

    def __init__(self, parent=None):
        super(InitializeRun, self).__init__(parent)

        self.prepareUserInterface()
        self.tcsh.setTcshPath('/usr/bin/tcsh')
        self.tcsh.stdOutput.connect(self.updateText)
        self.tcsh.stdErrOutput.connect(self.updateText)
        self.completedSuccessfully = False

    def prepareUserInterface(self):
        """This prepares the user interface for the
        :meth:`initialize_run.InitializeRun` class. The widget is split into
        upper and lower half.

        The upper half contains a combobox for either selecting a run directory
        or creating a new one.

        The lower half contains buttons for starting ``setup_eirene_links`` and
        ``b2run b2mn``.

        Attributes:
            runDirCombo (QComboBox): Contains the list of directories other
                than baserun directory
            textDisplay (QPlainTextEdit): Displays the output of
                :class:`tcsh_process.Tcsh`
        """
        mainLayout = QVBoxLayout()

        # mainLayout.setSpacing(0)
        # mainLayout.setContentsMargins(0, 0, 0, 0)

        upperGridLayout = QGridLayout()
        lowerGridLayout = QGridLayout()
        mainLayout.addLayout(upperGridLayout)
        mainLayout.addLayout(lowerGridLayout)
        self.setLayout(mainLayout)

        #############
        # Group Box 1
        groupBox1 = QGroupBox()
        groupBox1.setTitle('Select/Create run directory')
        self.runDirCombo = QComboBox()
        self.runDirCombo.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,
                                                   QSizePolicy.Fixed))
        groupLayout = QGridLayout()
        groupLayout.setSpacing(0)
        groupLayout.setContentsMargins(0, 0, 0, 0)
        groupLayout.addWidget(QLabel('Select run dir:'), 0, 0)
        groupLayout.addWidget(self.runDirCombo, 0, 1, -1, 1)
        push = QPushButton('Create directory')
        push.clicked.connect(self.createRunDirectory)
        groupLayout.addWidget(push, 0, 3)
        groupBox1.setLayout(groupLayout)
        # Group Box 1
        #############

        upperGridLayout.addWidget(groupBox1)
        upperGridLayout.addItem(QSpacerItem(40, 20,
                                            hData=QSizePolicy.Expanding),
                                0, 2)

        #############
        # Group Box 2
        groupBox2 = QGroupBox()
        groupBox2.setTitle('Commands')
        groupLayout = QVBoxLayout()
        groupLayout.setSpacing(0)
        groupLayout.setContentsMargins(0, 0, 0, 0)

        setupEireneLinks = QPushButton('setup_baserun_eirene_links')
        setupEireneLinks.clicked.connect(self.setupEireneLinks)
        groupLayout.addWidget(setupEireneLinks)

        b2mn = QPushButton('b2mn')
        b2mn.clicked.connect(self.b2mn)

        clearLog = QPushButton('Clear log')
        clearLog.clicked.connect(self.clearLog)

        saveToIDS = QPushButton('Save to IDS')
        saveToIDS.clicked.connect(self.saveToIDS)

        stopB2mn = QPushButton('Stop run')
        stopB2mn.clicked.connect(self.stopB2mn)

        groupLayout.addWidget(b2mn)
        groupLayout.addWidget(saveToIDS)
        groupLayout.addWidget(clearLog)
        groupLayout.addWidget(stopB2mn)

        groupLayout.addItem(QSpacerItem(40, 20, vData=QSizePolicy.Expanding))
        groupBox2.setLayout(groupLayout)
        # Group Box 2
        #############

        lowerGridLayout.addWidget(groupBox2, 0, 0)

        #############
        # Group Box 3
        groupBox3 = QGroupBox()
        groupBox3.setTitle('Log window')

        groupLayout = QGridLayout()
        groupLayout.setSpacing(0)
        groupLayout.setContentsMargins(0, 0, 0, 0)
        groupBox3.setLayout(groupLayout)

        self.textDisplay = QPlainTextEdit()
        self.textDisplay.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.textDisplay.setReadOnly(True)
        groupLayout.addWidget(self.textDisplay, 0, 0, 1, -1)

        groupLayout.addItem(QSpacerItem(40, 20, hData=QSizePolicy.Expanding),
                            1, 0)
        manualInput = QPushButton('Terminal input')
        manualInput.clicked.connect(self.manualInput)
        groupLayout.addWidget(manualInput, 1, 1)
        # Group Box 3
        #############

        lowerGridLayout.addWidget(groupBox3, 0, 1)

        mainLayout.setSpacing(0)
        mainLayout.setContentsMargins(0, 0, 0, 0)

    @Slot()
    def createRunDirectory(self):
        """Spawns a QFileDialog with filter for directories. The browser can
        create a new run directory.
        """
        baserunDir = self.getRunDir()
        if not baserunDir or not baserunDir.endswith('baserun'):
            QMessageBox.information(self, 'Error',
                                    'No baserun directory selected!')
            return

        newDir = QFileDialog.getExistingDirectory(self,
                                                  'Create a run directory',
                                                  baserunDir.rstrip('baserun'))
        if newDir:
            self.updateFolderComboBox(os.path.basename(newDir))

    def updateFolderComboBox(self, focus=''):
        """Updated the QComboBox :attr:`self.runDirCombo` with a new list of
        run directories, excluding the ``baserun`` directory.

        Arguments:
            focus (str): Name of the directory that the user just created. If
                there is no focus, then just update the list.
        """
        baserunDir = self.getRunDir()
        # Get a list from next(os.walk(DIR_PATH))[1]
        listOfDirs = next(os.walk(baserunDir.rstrip('baserundir')))[1]
        self.runDirCombo.clear()
        [self.runDirCombo.addItem(_) if _ != 'baserun' else None for _ in
         listOfDirs]
        if focus:
            i = self.runDirCombo.findText(focus)
            if i >= 0:
                self.runDirCombo.setCurrentIndex(i)

    def enterRunDirectory(self):
        """Checks whether the run directory specified in the QComboBox
        :attr:`InitializeRun.runDirCombo` exists.
        """

        baserunDir = self.getRunDir()
        runDir = baserunDir.rstrip('baserun') + \
            self.runDirCombo.currentText()
        if not runDir:
            self.textDisplay.appendPlainText('No run directory specified!')
            return ''

        if not os.path.exists(runDir):
            self.textDisplay.appendPlainText('Run directory: ' + runDir +
                                             ' does not exist!')
            return ''

        return runDir

    def executeCommand(self, info, cmd):
        if self.tcsh.state() != QProcess.ProcessState.NotRunning:
            runDirectory = self.enterRunDirectory()
            if not runDirectory:
                return
            baseRunDirectory = os.path.basename(runDirectory)
            self.textDisplay.appendPlainText('In %s :' % baseRunDirectory +
                                             info)
            self.tcsh.write('cd ' + runDirectory + '\n')
            self.tcsh.write(cmd)

    @Slot()
    def setupEireneLinks(self):
        """Runs the ``setup_baserun_eirene_links`` inside the run directory.
        """
        info = "Running - setup_baserun_eirene_links"
        cmd = 'setup_baserun_eirene_links && echo Done performing ' \
              'setup_baserun_eirene_links\n'
        self.executeCommand(info, cmd)

    @Slot()
    def b2mn(self):
        """Runs ``b2run b2mn`` if the TCSH terminal is running in run directory
        """
        info = "Running - b2run b2mn"
        cmd = "b2run b2mn && echo Done running b2run b2mn\n"
        self.executeCommand(info, cmd)

    def saveToIDS(self):
        """If the QCheckBox :attr:`saveToIDS` is checked, run the fortran
        routine.
        """

        info = "Running - Saving data to IDS"
        cmd = 'b2run b2_ual_write\n'
        # Get SHOT, RUN, USERNAME, VERSION, DEVICE
        SHOT, RUN, USER, VERSION, DEVICE = self.readRunID()
        if not (SHOT and RUN and USER and VERSION and DEVICE):
            self.textDisplay.appendPlainText('Missing IDS id settings:')
            if not SHOT:
                self.textDisplay.appendPlainText('    shot')
            if not RUN:
                self.textDisplay.appendPlainText('    run')
            if not USER:
                self.textDisplay.appendPlainText('    user')
            if not VERSION:
                self.textDisplay.appendPlainText('    version')
            if not DEVICE:
                self.textDisplay.appendPlainText('    device')

            self.textDisplay.appendPlainText('Fill the required id settings in'
                                             ' either b2mn.dat or b2md.dat')
            return
        self.textDisplay.appendPlainText(cmd)
        self.executeCommand(info, cmd)

    def readRunID(self):
        runDirectory = self.enterRunDirectory()

        # Read b2mn.dat for:
        # - b2mndr_run_number
        # - b2mndr_shot_number
        # - b2mndr_device
        # - b2mndr_user
        VERSION = '3'
        SHOT, RUN, USER, DEVICE = 4 * (None,)

        if os.access(runDirectory + '/b2mn.dat', os.F_OK | os.R_OK):
            with open(runDirectory + '/b2mn.dat', 'r') as f:
                for line in f:
                    if 'b2mndr_run_number' in line:
                        RUN = line.split()[-1].strip("'")

                    elif 'b2mndr_shot_number' in line:
                        SHOT = line.split()[-1].strip("'")

                    elif 'b2mndr_device' in line:
                        DEVICE = line.split()[-1].strip("'")

                    elif 'b2mndr_user' in line:
                        USER = line.split()[-1].strip("'")



        return SHOT, RUN, USER, VERSION, DEVICE

    @Slot()
    def manualInput(self):
        """Spawns an input dialog in which the user writes the commands for
        a TCSH terminal or the expected input the ``carre`` scripts expect from
        the user.
        """
        if self.tcsh.state() == QProcess.ProcessState.NotRunning:
            return

        runDirectory = self.enterRunDirectory()
        if not runDirectory:
            return

        msg, ok = QInputDialog.getMultiLineText(self, 'Input dialog',
                                                'Command:')
        if ok:
            self.tcsh.write('cd ' + runDirectory + '\n')
            self.tcsh.write(msg + '\n')
            self.insertTextAtBottom(msg)

    def insertTextAtBottom(self, msg):
        """Inserts text to the bottom of :attr:`InitializeRun.textDisplay`
        without creating a new newline.

        Arguments:
            msg (str): Message to append to the
                :attr:`InitializeRun.textDisplay`
        """
        self.textDisplay.moveCursor(QTextCursor.End)
        self.textDisplay.insertPlainText('\n' + msg.rstrip())
        self.textDisplay.moveCursor(QTextCursor.End)

    @Slot()
    def startTcsh(self):
        """Starts a TCSH terminal with the SOLPS-ITER environment and enters
        the run directory.
        """
        super(InitializeRun, self).startTcsh()
        env = QSettings('ITER', 'solps-gui')
        device = env.value('device_environment', 'iter')
        self.tcsh.write('setenv DEVICE ' + device + '\n')
        self.tcsh.write('echo DEVICE set to ' + device + '\n')
        self.tcsh.write('cd ' + self.getRunDir() + '\n')
        self.textDisplay.appendPlainText('Switched to directory: ' +
                                         self.getRunDir())

    @Slot(str)
    def setRunDir(self, newRunDir):
        """Overloaded function from :meth:`tcsh_process.TcshProcess.setRunDir`.
        If the directory is a baserun directory, start the TCSH terminal if
        it isn't already started.If it is started, then check if ``SOLPS-ITER``
        changed.

        In the end switch to the new baserun directory
        """
        oldBaserunDir = self.getRunDir()
        if not newRunDir.endswith('baserun'):
            self.textDisplay.appendPlainText('Directory ' + newRunDir + ' is '
                                             'not a baserun directory!')
            return

        # TCSH terminal is running
        RUN = 1
        if self.tcsh.state() != QProcess.ProcessState.NotRunning:
            oldSOLPSTOP = self.tcsh.findSolpsTop(oldBaserunDir)
            newSOLPSTOP = self.tcsh.findSolpsTop(newRunDir)
            if oldSOLPSTOP == newSOLPSTOP:
                self.tcsh.write('cd ' + newRunDir + '\n')
                self.textDisplay.appendPlainText('Switched to baserun ' +
                                                 'directory: ' + newRunDir)
                RUN = 0
            else:
                self.tcsh.terminate()
                self.tcsh.close()
                RUN = 1
        super(InitializeRun, self).setRunDir(newRunDir)
        self.updateFolderComboBox()
        if RUN:
            self.startTcsh()

    def updateText(self, msg):
        """Shows text in the QPlainTextEdit :attr:`textDisplay`.

        Arguments:
            msg (str): Message to show
        """
        self.textDisplay.appendPlainText(msg)

    @Slot()
    def clearLog(self):
        """Clears the QPlainTextEdit :attr:`textDisplay`
        """
        self.textDisplay.clear()

    @Slot()
    def stopB2mn(self):
        """Stops the :meth:`tcsh_process.Tcsh` and restarts it.
        """
        if self.tcsh.state() != QProcess.ProcessState.NotRunning:
            self.tcsh.kill()
            self.tcsh.terminate()
        self.textDisplay.appendPlainText('Stoped TCSH')
        self.startTcsh()

if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication, QMainWindow
    import sys

    app = QApplication(sys.argv)
    main = QMainWindow()
    w = InitializeRun()
    w.setRunDir('/home/ivasileska/solps-iter/runs/examples/ITER_2298_Honly_20MW/baserun')
    main.setCentralWidget(w)
    main.show()

    sys.exit(app.exec())
