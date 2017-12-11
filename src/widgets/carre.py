#!/usr/bin/env python3
""" A PyQt widget for Carre process.
"""

from PyQt5.QtWidgets import (QPlainTextEdit, QVBoxLayout, QPushButton,
                             QGridLayout, QInputDialog, QComboBox, QSpacerItem,
                             QSizePolicy, QGroupBox, QCheckBox)
from PyQt5.QtCore import pyqtSlot, QSettings, Qt, QDateTime
from PyQt5.QtGui import QTextCursor
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
    notRunning, starting, waiting, stepRunning = range(4)


class StepPush(QPushButton):
    def __init__(self, parent=None, value=None):
        super(StepPush, self).__init__(parent)
        self.value = value


class Carre(TcshProcess):
    """ Widget for the grid generation tool Carre.
    Its layout will look:
    #-VericalBox layout-#
    |----------------------------------------------|
    | #-GridBox layout-#                           |
    |                                              |
    | #################     #############          |
    | #Status GroupBox#     #DG groupbox#          |
    | #               #     #           #          |
    | #               #     #           #          |
    | #################     #############          |
    |----------------------------------------------|
    |#-GridBox layout-#                            |
    |                                              |
    | #################    ####################    |
    | #PushButton for #    # Display output of#    |
    | #steps          #    # current step     #    |
    | #               #    ####################    |
    | #               #    # Default response #    |
    | #               #    # buttons          #    |
    | #################    ####################    |
    |----------------------------------------------|

    Widget creates a .status file in baserun directory that contains
    information about which steps have been performed for which DG model and
    if the initial lns linking for the DG model has been ran.
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
                x.setCheckState(0)
                x.stateChanged.connect(self.setVarsFromClickedGroup)
                groupLayout.addWidget(x, j, i)
        _N = CarreVars.NumOfVars - 1
        leftOver = _N - (_N // _n) * _n
        if leftOver > 0:
            for k in range(leftOver):
                x = QCheckBox(CarreVars.Name[(i + 1) * _n + k])
                x.setCheckState(0)
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
        upperGridLayout.addItem(QSpacerItem(20, 40,
                                            hPolicy=QSizePolicy.Expanding),
                                0, 2)

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
        groupLayout.addItem(QSpacerItem(40, 20, vPolicy=QSizePolicy.Expanding))
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

        groupLayout.addItem(QSpacerItem(40, 20, hPolicy=QSizePolicy.Expanding),
                            1, 0)
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
        layout = self.clickedGroup.layout()
        for i in range(layout.count()):
            item = layout.itemAt(i).widget()

            item.stateChanged.disconnect()

            if self.vars[i]:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)

            item.stateChanged.connect(self.setVarsFromClickedGroup)

    @pyqtSlot()
    def setVarsFromClickedGroup(self):
        layout = self.clickedGroup.layout()
        for i in range(layout.count()):
            item = layout.itemAt(i).widget()
            if item.isChecked():
                self.vars[i] = 1
            else:
                self.vars[i] = 0

    def resetCheckBox(self):
        layout = self.clickedGroup.layout()
        for i in range(layout.count()):
            layout.itemAt(i).widget().setCheckState(Qt.Unchecked)

    def readStatusFile(self, baserunDir):
        """Read the .status file in baserun.

        Variables:
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
        baserunDir = self.runDir
        if not baserunDir:
            return
        path = baserunDir + '/.status'
        if os.access(path, os.W_OK | os.F_OK):
            with open(path, 'a') as f:
                time = TIME.currentDateTime().toString(TIME_FORMAT)
                f.write('\nRan Carre step ' + msg + ' at ' + time)

    @pyqtSlot()
    def manualInput(self):
        if not self.tcsh.state():
            return

        msg, ok = QInputDialog.getMultiLineText(self, 'Input dialog',
                                                'Command:')
        if ok:
            self.tcsh.write(msg + '\n')
            self.insertTextAtBottom(msg)

    @pyqtSlot()
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
        default = "Help, Prepare, Grid, Save, Convert, sTore, Next, " \
                  "Remove, Input, Output, Quit ?"
        if default in text:
            self.STATE = CarreState.waiting

    def insertTextAtBottom(self, msg):
        self.textDisplay.moveCursor(QTextCursor.End)
        if msg.endswith('\n'):
            msg = msg[:-1]
        self.textDisplay.insertPlainText('\n' + msg)
        self.textDisplay.moveCursor(QTextCursor.End)

    # Overloaded
    @pyqtSlot(str)
    def setRunDir(self, runDir):
        if runDir != self.runDir:
            self.storeStatusFile(self.runDir)
        if runDir.endswith('baserun'):
            # Update QMainWindow status bar.
            self.updateDivGeoModel(runDir)
            self.readStatusFile(runDir)
            self.stopCarre()
        super(Carre, self).setRunDir(runDir)

    @pyqtSlot(str)
    @pyqtSlot()
    def updateDivGeoModel(self, runDir=None):
        """Gives the user a list of all .dg files in baserun
        """
        if not runDir:
            if not self.getRunDir():
                return
            runDir = self.getRunDir()

        self.selectDgModel.clear()
        self.selectDgModel.addItem('')
        [self.selectDgModel.addItem(os.path.basename(_)) for _ in
         glob.glob(runDir + '/*.dg')]

    @pyqtSlot(str)
    def updateText(self, text):
        """Read the output given from carre, and when input is expected, spawn
        input dialogs to get input from the user and then pass it back to
        Carre.
        """
        if self.STATE >= CarreState.starting:
            self.processText(text)
        if self.STATE >= CarreState.waiting:
            self.insertTextAtBottom(text)

    @pyqtSlot(str)
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

    @pyqtSlot()
    def startCarre(self):

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

            env = QSettings('ITER', 'solps-gui')
            device = env.value('device_environment', 'iter')
            cmd = 'module load libpng\n'
            cmd += 'setenv DEVICE ' + device + '\n'
            cmd += 'cd ' + runDir + '\n'
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
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget)
    env = QSettings('ITER', 'solps-gui')
    env.setValue('device_environment', 'cmod')
    app = QApplication(sys.argv)
    main = QMainWindow()
    carreM = Carre()
    logging.getLogger().setLevel(logging.DEBUG)
    carreM.activateDebugging()
    carreM.setTcshPath('/bin/tcsh')
    path = os.path.expanduser('~/solps-iter/runs/test_run/baserun')
    carreM.setRunDir(path)

    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(carreM)

    window = QWidget()
    window.setLayout(layout)

    main.setCentralWidget(window)
    main.show()

    res = app.exec_()
    app.quit()
    sys.exit(res)
