#!/usr/bin/env python3
""" A PyQt widget for Carre process.
"""

from PySide6.QtWidgets import (QPlainTextEdit, QVBoxLayout, QPushButton,
                             QGridLayout, QInputDialog, QComboBox, QSpacerItem,
                             QSizePolicy, QGroupBox, QCheckBox)
from PySide6.QtCore import Slot, QSettings, Qt, QDateTime
from PySide6.QtGui import QTextCursor
from tcsh_process import TcshProcess
import logging
import glob
import os
import sys

TIME = QDateTime()
TIME_FORMAT = "ddd MMM d t yyyy"


class CarreVars:
    """Variables for Carre for automation.

    Variables it includes are Carre steps performed for the selected baserun,
    the name of the dgModel and if the lns command has been called for the
    dgModel.

    NumOfVars tells us how many variables are there.

    It should be noted that this is used for ease of creating widgets for
    steps and that the steps should be written in proper order and that there
    are only NumOfVars-2 steps since the last to are reserved for which
    dgModel has been used and if lns was called.

    Attributes:
        NumOfVars (int): This tells us the number of values in
            :class:`CarreVars`
        Name (dict): Holds the string representation of the enumerated value
        command (dict): Holds the command of the enumerated value
        Values (dict): Holds the enumerated value for the string representation
        Default (dict): Default values for the values

        prepare (int): The **prepare** step for ``carre`` script
        grid (int): The **grid** step for ``carre`` script
        convert (int): The **convert** step for ``carre`` script
        save (int): The **save** step for ``carre`` script
        store (int): The **store** step for ``carre`` script
        lns (int): Is the value that tells the widget if the linking command
            ``lns`` has been run against the selected DivGeo model
        dgModel (int): String name of the DivGeo model to use for Carre
    """
    NumOfVars = 7
    prepare, grid, convert, save, store, lns, dgModel = range(NumOfVars)
    Name = {0: 'Prepare', 1: 'Grid', 2: 'SaveChoice', 3: 'Convert',
            4: 'Store', 5: 'lns', 6: 'dgModel'}
    command = {0: 'p', 1: 'g', 2: 's', 3: 'c', 4: 't'}

    Values = {'Prepare': 0, 'Grid': 1, 'SaveChoice': 2, 'Convert': 3,
              'Store': 4, 'lns': 5, 'dgModel': 6}

    Default = {i: 0 for i in range(NumOfVars - 1)}
    Default[NumOfVars - 1] = ''


class CarreState:
    """This class contains the enumerator values for state of the TCSH
    terminal.

    Attributes:
        notRunning (int): Means that the TCSH terminal is not running
        starting (int): Means that the TCSH terminal is starting, sourcing
            the SOLPS-ITER environment
        waiting (int): Means that we can run the steps of ``carre`` script
        stepRunning (int): Means that a step from ``carre`` script is running
    """
    notRunning, starting, waiting, stepRunning = range(4)


class StepPush(QPushButton):
    """Modified :class:`QtWidgets.QPushButton` that contains the command for
    the step it represents, i.e., if the :class:`StepPush` represents the
    **store** step of carre script, the value stored in :attr:`StepPush.value`
    corresponds to the command to run the step: ``t``.
    """
    def __init__(self, parent=None, value=None):
        super(StepPush, self).__init__(parent)
        self.value = value


class Carre(TcshProcess):
    """ Widget for the grid generation tool Carre.

    Widget creates a .status file in baserun directory that contains
    information about which steps have been performed for which DG model and
    if the initial lns linking for the DG model has been ran.

    In :meth:`Carre.__init__` the signals from :meth:`tcsh_process.Tcsh` output
    signals are connected to the functions that process the output. Also other
    variables are instantiated.

    Attributes:
        vars (dict): This contains the enumerators for steps described in
            :class:`CarreVars` and their value
        STATE (int): This contains the enumerator value for the TCSH status.
            States are described in :class:`CarreState`
        textDisplay (QPlainTextEdit): Widget for displayin the output of
            ``carre`` script
    """

    def __init__(self, parent=None):
        super(Carre, self).__init__(parent)
        self.vars = CarreVars.Default

        self.prepareUserInterface()

        self.tcsh.setTcshPath('/usr/bin/tcsh')
        self.tcsh.prcStateChanged.connect(self.updateText)
        self.tcsh.prcFinished.connect(self.updateText)
        self.tcsh.prcError.connect(self.updateError)
        self.tcsh.stdOutput.connect(self.updateText)
        self.tcsh.stdErrOutput.connect(self.updateError)

        self.currentRunDir = ''
        self.STATE = CarreState.notRunning

    def prepareUserInterface(self):
        """This prepares the user interface for the :meth:`carre.Carre` class.
        The widget is split into upper and lower half.

        The upper half contains the self-assessment group box and a separate
        group box for choosing the DivGeo model for ``carre``.

        The lower half contains buttons for communicating with the ``carre``
        script and a log window for viewing the output of ``carre`` script.
        """
        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(0)
        mainLayout.setContentsMargins(0, 0, 0, 0)

        upperGridLayout = QGridLayout()
        lowerGridLayout = QGridLayout()

        #############
        # Group Box 1
        groupBox1 = QGroupBox()
        self.clickedGroup = groupBox1
        groupLayout = QGridLayout()
        groupBox1.setTitle('Baserun .status')
        _n = 2  # Number of widgets per column
        for i in range((CarreVars.NumOfVars - 1) // _n):
            for j in range(_n):
                # Creating checkboxes for
                x = QCheckBox(CarreVars.Name[i * _n + j])
                # LK TODO x.setCheckState(Qt.Unchecked)
                x.stateChanged.connect(self.setVarsFromClickedGroup)
                groupLayout.addWidget(x, j, i)
        _N = CarreVars.NumOfVars - 1
        leftOver = _N - (_N // _n) * _n
        if leftOver > 0:
            for k in range(leftOver):
                x = QCheckBox(CarreVars.Name[(i + 1) * _n + k])
                x.setCheckState(Qt.Unchecked)
                x.stateChanged.connect(self.setVarsFromClickedGroup)
                groupLayout.addWidget(x, k, i + 1)
        groupBox1.setLayout(groupLayout)
        # Group Box 1
        #############

        upperGridLayout.addWidget(groupBox1, 0, 0)

        #############
        # Group Box 2
        groupBox2 = QGroupBox()
        groupBox2.setTitle('DG model')
        groupLayout = QVBoxLayout()
        self.selectDgModel = QComboBox()
        self.selectDgModel.addItem('')
        self.selectDgModel.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,
                                                     QSizePolicy.Fixed))
        x = QPushButton('Update DG list')
        x.clicked.connect(self.updateDivGeoModel)
        groupLayout.addWidget(self.selectDgModel, alignment=Qt.AlignTop)
        groupLayout.addWidget(x, alignment=Qt.AlignTop)
        groupBox2.setLayout(groupLayout)
        # Group Box 2
        #############

        upperGridLayout.addWidget(groupBox2, 0, 1)
        # LK upperGridLayout.addItem(QSpacerItem(20, 40,
        #                                    hData=QSizePolicy.Expanding),
        #                        0, 2)

        #############
        # Group Box 3
        groupBox3 = QGroupBox()
        self.stepGroup = groupBox3
        groupBox3.setTitle('Steps')
        groupLayout = QVBoxLayout()
        groupLayout.setSpacing(0)
        groupLayout.setContentsMargins(0, 0, 0, 0)

        start = QPushButton('Start Carre')
        start.clicked.connect(self.startCarre)
        groupLayout.addWidget(start)
        for i in range(CarreVars.NumOfVars - 2):
            x = StepPush(value=CarreVars.command[i])
            x.clicked.connect(self.runStep)
            x.setText(CarreVars.Name[i])
            groupLayout.addWidget(x)
        # LK groupLayout.addItem(QSpacerItem(40, 20, vData=QSizePolicy.Expanding))
        groupBox3.setLayout(groupLayout)
        # Group Box 3
        #############

        lowerGridLayout.addWidget(groupBox3, 0, 0)

        #############
        # Group Box 4
        groupBox4 = QGroupBox()
        groupBox4.setTitle('Log window')

        self.textDisplay = QPlainTextEdit()
        self.textDisplay.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.textDisplay.setReadOnly(True)

        groupLayout = QGridLayout()
        groupLayout.setContentsMargins(0, 0, 0, 0)
        groupLayout.setSpacing(0)
        groupLayout.addWidget(self.textDisplay, 0, 0, 1, -1)

        # LK groupLayout.addItem(QSpacerItem(40, 20, hData=QSizePolicy.Expanding),
        #                    1, 0)
        manualInput = QPushButton('Terminal input')
        manualInput.clicked.connect(self.manualInput)

        groupLayout.addWidget(manualInput, 1, 1)

        yes = StepPush(value='y')
        yes.setText('Yes')
        yes.clicked.connect(self.runStep)

        no = StepPush(value='n')
        no.setText('No')
        no.clicked.connect(self.runStep)

        groupLayout.addWidget(yes, 1, 2)
        groupLayout.addWidget(no, 1, 3)
        groupBox4.setLayout(groupLayout)
        # Group Box 4
        #############

        lowerGridLayout.addWidget(groupBox4, 0, 1)

        mainLayout.addLayout(upperGridLayout)
        mainLayout.addLayout(lowerGridLayout)
        self.setLayout(mainLayout)

    def setClickedGroupFromVars(self):
        """Sets the QCheckBox clicked state according to the values storred in
        :attr:`Carre.vars`. If the value for a step is 0 then the
        QCheckBox is unchecked and vice versa if the value is 1.
        """
        layout = self.clickedGroup.layout()
        for i in range(layout.count()):
            item = layout.itemAt(i).widget()

            item.stateChanged.disconnect()

            if self.vars[i]:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)

            item.stateChanged.connect(self.setVarsFromClickedGroup)

    @Slot()
    def setVarsFromClickedGroup(self):
        """When you change the checked state of a QCheckBox, the values are
        updated into :attr:`Carre.vars` variable.
        """
        layout = self.clickedGroup.layout()
        for i in range(layout.count()):
            item = layout.itemAt(i).widget()
            if item.isChecked():
                self.vars[i] = 1
            else:
                self.vars[i] = 0

    def resetCheckBox(self):
        """Resets all the QCheckBox-es to unchecked state.
        """
        layout = self.clickedGroup.layout()
        for i in range(layout.count()):
            layout.itemAt(i).widget().setCheckState(Qt.Unchecked)

    def readStatusFile(self, baserunDir):
        """Read the .status file in baserun. At the end it also sets the
        checked status of the QCheckBox-es.

        Arguments:
            baserunDir (str): Absolute path to the baserun directory.

        Attributes:
            statusFile (array): text of status without the Carre block.
            mark (int): Where Carre block is inserted into .status file.
        """
        self.resetCheckBox()
        if not baserunDir:
            return

        if not baserunDir.endswith('baserun'):
            return

        file = baserunDir + '/.status'

        # Checking file permission and existance
        ok = os.access(file, os.F_OK | os.R_OK)
        if not ok:
            logging.info("No .status found in baserun " + baserunDir +
                         ", or no permission to read .status.")
            return

        reading = 0
        CarreBlocks = 0
        with open(file, 'r') as f:
            for i, line in enumerate(f):
                if reading and line.startswith('&'):
                    reading = 0

                if reading:
                    try:
                        sline = line.split()
                        name, val = sline[0], sline[1]
                        self.vars[CarreVars.Values[name]] = int(val) if \
                            val.isdigit() else val
                    except KeyError as e:
                        logging.error('Uknown key ' + name)
                    except ValueError as e:
                        logging.error("Wrong value for: " + name + ': ' + val)
                    except IndexError as e:
                        logging.error("Not enough arguments on line: " + line)
                        if CarreVars.Name[CarreVars.dgModel] in line:
                            self.vars[CarreVars.dgModel] = ''

                if line.startswith('&Carre'):
                    reading = 1 # We are reading the block
                    CarreBlocks += 1
                    if CarreBlocks > 1:
                        logging.error("Multiple Carre block in .status file "
                                      "in baserun: " + baserunDir)
                        break
        if self.vars[CarreVars.dgModel]:
            self.selectDgModel.setCurrentText(self.vars[CarreVars.dgModel])

        self.setClickedGroupFromVars()

    def storeStatusFile(self, baserunDir):
        """Stores the values of the :attr:`Carre.vars` to the .status file in
        baserun directory.

        If the status file is not created, it will create it. If the status
        file exists it will check if there is already a carre block inside and
        write the values.

        Arguments:
            baserunDir (str): absolute path to the baserun directory
        """
        variables = self.vars
        if not baserunDir:
            return
        if not baserunDir.endswith('baserun'):
            return
        logging.info('Storing .status in baserun ' + baserunDir)
        file = baserunDir + '/.status'
        carreLines = [CarreVars.Name[i] + ' ' + str(variables[i]) for i
                      in range(len(variables))]
        if os.access(file, os.F_OK):
            if os.access(file, os.W_OK):
                logging.info(".status file exists in baserun " + baserunDir)
                with open(file, 'r') as f:
                    text = f.read()

                if "&Carre" in text:
                    logging.info("Carre block found in .status file!")
                    left, right = text.split("&Carre", 1)
                    center, right = right.split("&", 1)

                    text = left + "&Carre\n" + '\n'.join(carreLines) + \
                        "\n&" + right

                else:
                    logging.info("No Carre block found in .status file!")
                    text = '&Carre\n' + '\n'.join(carreLines) + '\n&\n' + text

                with open(file, 'w') as f:
                    f.write(text)
                logging.info("Carre written to .status file.")

            else:
                logging.error("No writing permission to .status file!")

        else:
            logging.info("No .status file exists in baserun " + baserunDir)
            with open(file, 'w') as f:
                text = '&Carre\n'
                text += '\n'.join(carreLines)
                text += '\n&'
                f.write(text)
            logging.info(".status file created for carre block!")

    def appendToStatus(self, msg):
        """Stores the current step that the user ran at the end of the .status
        file in the baserun directory.

        Arguments:
            msg (str): Message to write to the end of the status file
        """
        baserunDir = self.runDir
        if not baserunDir:
            return
        path = baserunDir + '/.status'
        if os.access(path, os.W_OK | os.F_OK):
            with open(path, 'a') as f:
                time = TIME.currentDateTime().toString(TIME_FORMAT)
                f.write('\nRan Carre step ' + msg + ' at ' + time)

    @Slot()
    def manualInput(self):
        """Spawns an input dialog in which the user writes the commands for
        a TCSH terminal or the expected input the ``carre`` scripts expect from
        the user.
        """
        if not self.tcsh.state():
            return

        msg, ok = QInputDialog.getMultiLineText(self, 'Input dialog',
                                                'Command:')
        if ok:
            self.tcsh.write(msg + '\n')
            self.insertTextAtBottom(msg)

    @Slot()
    def runStep(self):
        """Custom PushButtons emits signal to this function. They contain
        attribute value which is then passed to tcsh if it is running.
        """
        if not self.tcsh.state():
            return
        if self.STATE == CarreState.waiting:
            sender = self.sender()
            self.appendToStatus(sender.text())
            msg = sender.value + '\n'
            self.tcsh.write(msg)

    def processText(self, text):
        """Process the output of the ``carre`` script so the user gets notified
        when he can start running the ``carre`` steps.

        Arguments:
            text (str): Output of the ``carre`` script.
        """
        default = "Help, Prepare, Grid, Save, Convert, sTore, Next, " \
                  "Remove, Input, Output, Quit ?"
        if default in text:
            self.STATE = CarreState.waiting

    def insertTextAtBottom(self, msg):
        """Inserts text to the bottom of :attr:`Carre.textDisplay` without
        creating a new newline.

        Arguments:
            msg (str): Message to append to the :attr:`Carre.textDisplay`
        """
        self.textDisplay.moveCursor(QTextCursor.End)
        if msg.endswith('\n'):
            msg = msg[:-1]
        self.textDisplay.insertPlainText('\n' + msg)
        self.textDisplay.moveCursor(QTextCursor.End)

    # Overloaded
    @Slot(str)
    def setRunDir(self, runDir):
        """Overloaded function of :meth:`tcsh_process.Tcsh.setRunDir`.
        Additionally to setting the new directory, it is also tested whether
        the directory is a **baserun** directory.

        If we select a new baserun directory from the ``Runs`` tab of
        ``SOLPS-GUI`` the following happens:

        1. If we left a baserun directory, then update the .status file.
        2. Stop current TCSH terminal.
        3. Read the new .status file in the new baserun directory.
        4. Start the TCSH terminal in the new baserun directory.

        Arguments:
            runDir (str): Absolute path to the run directory.
        """
        if runDir != self.runDir:
            self.storeStatusFile(self.runDir)
        if runDir.endswith('baserun'):
            # Update QMainWindow status bar.
            self.updateDivGeoModel(runDir)
            self.readStatusFile(runDir)
            self.stopCarre()
        super(Carre, self).setRunDir(runDir)

    @Slot(str)
    @Slot()
    def updateDivGeoModel(self, runDir=None):
        """Gives the user a list of all .dg files in baserun
        Attributes:
            runDir (str): Absolute path to the run directory.
        """
        if not runDir:
            if not self.getRunDir():
                return
            runDir = self.getRunDir()

        self.selectDgModel.clear()
        self.selectDgModel.addItem('')
        [self.selectDgModel.addItem(os.path.basename(_)) for _ in
         glob.glob(runDir + '/*.dg')]

    @Slot(str)
    def updateText(self, text):
        """Read the output given from carre, and when input is expected, spawn
        input dialogs to get input from the user and then pass it back to
        Carre.
        """
        if self.STATE >= CarreState.starting:
            self.processText(text)
        if self.STATE >= CarreState.waiting:
            self.insertTextAtBottom(text)

    @Slot(str)
    def updateError(self, text):
        # color_pref = '<font color=red>'
        # color_post = '</font>'
        # self.textDisplay.appendHtml('<b>' + color_pref + text + color_post +
        #                             '</b>')
        # self.insertTextAtBottom(text)
        # self.processText(text)
        if "does not exist. Create it?" in text:
            self.tcsh.write('y\n')
        pass

    @Slot()
    def startCarre(self):
        """ Starts the ``carre`` script in the baserun directory and with the
        selected device from the **Preferences** settings and with the selected
        DivGeo model.
        """

        if not self.getRunDir():
            self.textDisplay.appendPlainText('No baserun selected.')
            return

        runDir = self.getRunDir()
        if runDir != self.currentRunDir:
            msg = 'Baserun changed'
            if self.STATE != CarreState.notRunning:
                msg += '. But current carre run hasn\'t finished yet!'
                logging.warning(msg)
                self.insertTextAtBottom(msg)
                return

            msg += '. Running carre in directory ' + self.currentRunDir + '.'
            logging.info(msg)
            self.currentRunDir = runDir

        self.textDisplay.clear()

        if not self.tcsh.state():
            # Get DG model from combo box
            if self.vars[CarreVars.dgModel]:
                dgModel = self.vars[CarreVars.dgModel]
            dgModel = self.selectDgModel.currentText()
            if dgModel.endswith('.dg'):
                dgModel = dgModel[:-3]

            if not dgModel:
                logging.error('No valid dg model selected from '
                              ' baserun ' + runDir + '!')
                self.insertTextAtBottom('No valid dg model selected from '
                                        'baserun ' + runDir + '!')
                return

            self.vars[CarreVars.dgModel] = dgModel

            self.startTcsh()
            self.tcsh.waitForStarted()

            # device = env.value('device_environment', 'iter')
            # cmd = 'module load libpng\n'
            cmd = 'cd ' + runDir + '\n'
            if not self.vars[CarreVars.lns]:
                cmd += 'lns ' + dgModel + '\n'  # Link .sno DivGeo file
                self.vars[CarreVars.lns] = 1
                self.setClickedGroupFromVars()
            self.textDisplay.appendPlainText('Sourcing setup.csh. It will '
                                             'take a while.')
            self.tcsh.write(cmd)
        else:
            logging.info('TCSH for Carre is aready running.')

        Carre = 'carre -\n'

        self.STATE = CarreState.starting

        cmd = Carre + '\n'
        # self.tcsh.write(cmd)
        self.tcsh.write(cmd)

    def stopCarre(self):
        if self.tcsh.state():
            self.textDisplay.clear()
            self.tcsh.terminate()
            self.tcsh.close()
            self.STATE = CarreState.notRunning
            msg = "Switched to another baserun, therefore stopped carre."
            self.textDisplay.appendPlainText(msg)


if __name__ == '__main__':
    from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget)
    env = QSettings('ITER', 'solps-gui')
    env.setValue('device_environment', 'cmod')
    app = QApplication(sys.argv)
    main = QMainWindow()
    carreM = Carre()
    logging.getLogger().setLevel(logging.DEBUG)
    carreM.activateDebugging()
    carreM.setTcshPath('/bin/tcsh')
    path = os.path.expanduser('/solps-iter/runs/examples/ITER_2298_Honly_20MW/baserun')
    carreM.setRunDir(path)

    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(carreM)

    window = QWidget()
    window.setLayout(layout)

    main.setCentralWidget(window)
    main.show()

    res = app.exec()
    app.quit()
    sys.exit(res)
