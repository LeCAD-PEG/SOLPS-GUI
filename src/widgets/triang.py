#!/usr/bin/env python3
""" A PyQt widget for Triang process.
"""

from PyQt5.QtWidgets import (QPlainTextEdit, QVBoxLayout, QGridLayout,
                             QInputDialog, QSpacerItem, QSizePolicy,
                             QPushButton, QGroupBox, QCheckBox, QMessageBox)
from PyQt5.QtCore import pyqtSlot, QSettings, Qt, QDateTime
from PyQt5.QtGui import QTextCursor
from tcsh_process import TcshProcess
import logging
import os
import sys
import glob

TIME = QDateTime()
TIME_FORMAT = "ddd MMM d t yyyy"


class TriangVars:
    NumOfVars = 9

    Uinp, uinp, b2ag, eirene, tria, triaGeom, store, outTemp, gridTemp = \
        range(NumOfVars)

    Name = {0: 'Uinp(U)', 1: 'Uinp(u)', 2: 'B2ag', 3: 'Eirene', 4: 'Tria',
            5: 'triaGeom', 6: 'Store', 7: 'Conv2Out (c)', 8: 'Conv2Grid (C)'}

    command = {0: 'U', 1: 'u', 2: 'b', 3: 'e', 4: 't', 5: 'g', 6: 's', 7: 'c',
               8: 'C'}

    Values = {'Uinp(U)': 0, 'Uinp(u)': 1, 'B2ag': 2, 'Eirene': 3, 'Tria': 4,
              'triaGeom': 5, 'Store': 6, 'Conv2Out (c)': 7, 'Conv2Grid (C)': 8}

    Default = {i: 0 for i in range(NumOfVars)}


class TriangState:
    notRunning, starting, waiting, stepRunning = range(4)


class StepPush(QPushButton):
    def __init__(self, parent=None, value=None):
        super(StepPush, self).__init__(parent)
        self.value = value


class Triang(TcshProcess):

    def __init__(self, parent=None):
        super(Triang, self).__init__(parent)

        # Creating QPlainTextEdit
        self.vars = TriangVars.Default
        self.prepareUserInterface()

        self.tcsh.readyReadStandardOutput.connect(self.tcsh.readStdOut)
        settings = QSettings('ITER', 'solps-gui')
        self.tcsh.setTcshPath(settings.value('tcsh_path', '/usr/bin/tcsh'))
        self.tcsh.prcStateChanged.connect(self.updateText)
        self.tcsh.prcFinished.connect(self.updateText)
        self.tcsh.prcError.connect(self.updateError)
        self.tcsh.stdOutput.connect(self.updateText)
        self.tcsh.stdErrOutput.connect(self.updateError)

        self.currentRunDir = ''
        self.STATE = TriangState.notRunning

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
        for i in range(TriangVars.NumOfVars // _n):
            for j in range(_n):
                # Creating checkboxes for
                x = QCheckBox(TriangVars.Name[i * _n + j])
                x.setCheckState(0)
                x.stateChanged.connect(self.setVarsFromClickedGroup)
                groupLayout.addWidget(x, j, i)
        leftOver = TriangVars.NumOfVars - (TriangVars.NumOfVars // _n) * _n
        if leftOver > 0:
            for k in range(leftOver):
                x = QCheckBox(TriangVars.Name[(i + 1) * _n + k])
                x.setCheckState(0)
                x.stateChanged.connect(self.setVarsFromClickedGroup)
                groupLayout.addWidget(x, k, i + 1)
        groupBox1.setLayout(groupLayout)
        # Group Box 1
        #############

        upperGridLayout.addWidget(groupBox1, 0, 0)

        upperGridLayout.addItem(QSpacerItem(20, 40,
                                            hPolicy=QSizePolicy.Expanding),
                                0, 2)

        #############
        # Group Box 2
        groupBox2 = QGroupBox()
        groupBox2.setTitle('Steps')
        groupLayout = QVBoxLayout()
        groupLayout.setSpacing(0)
        groupLayout.setContentsMargins(0, 0, 0, 0)

        start = QPushButton('Start Triang')
        start.clicked.connect(self.startTriang)
        groupLayout.addWidget(start)
        for i in range(TriangVars.NumOfVars):
            x = StepPush(value=TriangVars.command[i])
            x.clicked.connect(self.runStep)
            x.setText(TriangVars.Name[i])
            groupLayout.addWidget(x)
        groupLayout.addItem(QSpacerItem(40, 20, vPolicy=QSizePolicy.Expanding))
        groupBox2.setLayout(groupLayout)
        # Group Box 2
        #############

        lowerGridLayout.addWidget(groupBox2, 0, 0)

        #############
        # Group Box 3
        groupBox3 = QGroupBox()
        groupBox3.setTitle('Log window')

        self.textDisplay = QPlainTextEdit()
        self.textDisplay.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.textDisplay.setReadOnly(True)

        groupLayout = QGridLayout()
        groupLayout.setContentsMargins(0, 0, 0, 0)
        groupLayout.setSpacing(0)
        groupLayout.addWidget(self.textDisplay, 0, 0, 1, -1)

        groupLayout.addItem(QSpacerItem(40, 20, hPolicy=QSizePolicy.Expanding),
                            1, 0)
        editB2ag = QPushButton('Edit b2ag.dat')
        editB2ag.clicked.connect(self.editB2ag)

        groupLayout.addWidget(editB2ag, 1, 1)

        manualInput = QPushButton('Terminal input')
        manualInput.clicked.connect(self.manualInput)

        groupLayout.addWidget(manualInput, 1, 2)

        yes = StepPush(value='y')
        yes.setText('Yes')
        yes.clicked.connect(self.runStep)

        no = StepPush(value='n')
        no.setText('No')
        no.clicked.connect(self.runStep)

        groupLayout.addWidget(yes, 1, 3)
        groupLayout.addWidget(no, 1, 4)
        groupBox3.setLayout(groupLayout)
        # Group Box 3
        #############

        lowerGridLayout.addWidget(groupBox3, 0, 1)

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
            statusFile (array): text of status without the Triang block.
            mark (int): Where Triang block is inserted into .status file.
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
        TriangBlocks = 0
        with open(file, 'r') as f:
            for i, line in enumerate(f):
                if reading and line.startswith('&'):
                    reading = 0

                if reading:
                    try:
                        sline = line.split()
                        name, val = sline[0], sline[1]
                        self.vars[TriangVars.Values[name]] = int(val) if \
                            val.isdigit else val
                    except KeyError as e:
                        logging.error('Uknown key ' + name)
                    except ValueError as e:
                        logging.error("Wrong value for: " + name)
                    except IndexError as e:
                        logging.error("Not enough arguments on line: " + line)

                if line.startswith('&Triang'):
                    reading = 1 # We are reading the block
                    TriangBlocks += 1
                    if TriangBlocks > 1:
                        logging.error("Multiple Triang block in .status file "
                                      "in baserun: " + baserunDir)
                        break
        self.setClickedGroupFromVars()

    def storeStatusFile(self, baserunDir):
        variables = self.vars
        if not baserunDir:
            return
        if not baserunDir.endswith('baserun'):
            return
        logging.info('Storing .status in baserun ' + baserunDir)
        file = baserunDir + '/.status'
        triangLines = [TriangVars.Name[i] + ' ' + str(variables[i]) for i
                      in range(len(variables))]
        if os.access(file, os.F_OK):
            if os.access(file, os.W_OK):
                logging.info(".status file exists in baserun " + baserunDir)
                with open(file, 'r') as f:
                    text = f.read()

                if "&Triang" in text:
                    logging.info("Triang block found in .status file!")
                    left, right = text.split("&Triang", 1)
                    center, right = right.split("&", 1)

                    text = left + "&Triang\n" +'\n'.join(triangLines) + \
                           "\n&" + right

                else:
                    logging.info("No Triang block found in .status file!")
                    text = '&Triang\n' + '\n'.join(triangLines) + '\n&' + text

                with open(file, 'w') as f:
                    f.write(text)
                logging.info("Triang Written to .status file.")

            else:
                logging.error("No writing permission to .status file!")

        else:
            logging.info("No .status file exists in baserun " + baserunDir)
            with open(file, 'w') as f:
                text = '&Triang\n'
                text += '\n'.join(triangLines)
                text += '\n&'
                f.write(text)
            logging.info(".status file created for triang block!")

    def appendToStatus(self, msg):
        baserunDir = self.runDir
        if not baserunDir:
            return
        path = baserunDir + '/.status'
        if os.access(path, os.W_OK | os.F_OK):
            with open(path, 'a') as f:
                time = TIME.currentDateTime().toString(TIME_FORMAT)
                f.write('\nRan Triang step ' + msg + ' at ' + time)

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
    def editB2ag(self):
        """Read b2ag.dat if it exists and prompts the user with a
        QInputDialog.getMultiLineText to edit the file and then writes back
        to the file.
        """
        file = self.getRunDir() + '/b2ag.dat'

        # Get .sno file
        env = QSettings('ITER', 'solps-gui')
        device = env.value('device_environment', 'iter')

        solpstop = self.tcsh.findSolpsTop(self.getRunDir())
        if solpstop:
            # Directory to Divgeo/device/$device

            deviceDir = solpstop + '/modules/DivGeo/device/' + device

            snoFile = self.findLatestFile(deviceDir, '*.sno')

        else:
            deviceDir = ''
            snoFile = ''

        snoFile = os.path.basename(snoFile)

        if os.access(file, os.F_OK | os.W_OK | os.R_OK):
            with open(file, 'r') as f:
                text = f.read()
            text += '\n! Latest SNO file in ' + 'DivGeo/device/' + device + \
                    ': ' + snoFile
            text += '\n! Change the b2agfs_geometry value with: ' + device
            text += '\n! Change The first value of *param from -2 to -1'
            msg, ok = QInputDialog.getMultiLineText(self, 'Input dialog',
                                                    'Edit b2ag.dat',
                                                    text)
            if ok:
                with open(file, 'w') as f:
                    f.write(msg)
        else:
            QMessageBox.information(self, 'Information', 'File b2ag.dat in ' +
                                    self.getRunDir() + ' either does not exist'
                                    ' or you do not have permission to wrie/'
                                    'read!')

    @pyqtSlot()
    def runStep(self):
        """Custom PushButtons emits signal to this function. They contain
        attribute value which is then passed to tcsh if it is running.
        """
        if not self.tcsh.state():
            return
        if self.STATE == TriangState.waiting:
            sender = self.sender()
            self.appendToStatus(sender.text())
            msg = sender.value + '\n'
            self.tcsh.write(msg)

    def processText(self, text):
        default = "Help, Uinp, B2ag, Eirene, Tria, triaGeom, Plot, View, " \
                  "Store, Convert, List, Remove, reMap, Inquire, Quit ?"
        if default in text:
            self.STATE = TriangState.waiting

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
            self.readStatusFile(runDir)
            self.stopTriang()
        super(Triang, self).setRunDir(runDir)

    @pyqtSlot(str)
    def updateText(self, text):
        """Read the output given from Triang, and when input is expected, spawn
        input dialogs to get input from the user and then pass it back to
        Triang.
        """
        #self.insertTextAtBottom(text)
        # self.processText(text)  # Triang script outputs via StdError...
        if self.STATE >= TriangState.waiting:
            self.insertTextAtBottom(text)

    @pyqtSlot(str)
    def updateError(self, text):
        # color_pref = '<font color=red>'
        # color_post = '</font>'
        # self.textDisplay.appendHtml('<b>' + color_pref + text + color_post +
        #                             '</b>')
        if self.STATE >= TriangState.starting:
            self.processText(text)
        if self.STATE >= TriangState.waiting:
            self.insertTextAtBottom(text)

    @pyqtSlot()
    def startTriang(self):
        self.textDisplay.clear()
        if not self.getRunDir():
            self.textDisplay.appendPlainText('No baserun selected.')
            return

        runDir = self.getRunDir()
        if self.getRunDir() != self.currentRunDir:
            msg = 'Baserun changed'
            if self.STATE != TriangState.notRunning:
                msg += '. But current triang run hasn\'t finished yet!'
                logging.warning(msg)
                self.insertTextAtBottom(msg)
                return

            msg += '. Running triang in directory ' + self.currentRunDir + '.'
            logging.info(msg)
            self.currentRunDir = runDir

        if not self.tcsh.state():
            # Get DG model from combo box

            self.startTcsh()
            self.tcsh.waitForStarted()

            env = QSettings('ITER', 'solps-gui')
            device = env.value('device_environment', 'iter')
            cmd = 'setenv DEVICE ' + device + '\n'
            cmd += 'cd ' + runDir + '\n'
            self.textDisplay.appendPlainText('Sourcing setup.csh. It will '
                                             'take a while.')
            self.tcsh.write(cmd)
        else:
            logging.info('TCSH for triang is aready running.')

        self.STATE = TriangState.starting
        Triang = 'triang\n'
        cmd = Triang + '\n'
        # self.tcsh.write(cmd)
        self.tcsh.write(cmd)

    def stopTriang(self):
        if self.tcsh.state():
            self.textDisplay.clear()
            self.tcsh.terminate()
            self.tcsh.close()
            self.STATE = TriangState.notRunning
            msg = "Switched to another baserun, therefore stopped carre."
            self.textDisplay.appendPlainText(msg)

    def findLatestFile(self, directory, suffix):
        files = glob.glob(directory + '/' + suffix)
        if files:
            return max(files, key=os.path.getctime)
        else:
            return ''


if __name__ == '__main__':
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget)
    env = QSettings('ITER', 'solps-gui')
    env.setValue('device_environment', 'cmod')
    app = QApplication(sys.argv)
    main = QMainWindow()
    triangM = Triang()
    triangM.activateDebugging()
    triangM.setTcshPath('/bin/tcsh')
    path = os.path.expanduser('~/solps-iter/runs/test_run/baserun')
    triangM.setRunDir(path)

    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(triangM)

    window = QWidget()
    window.setLayout(layout)

    main.setCentralWidget(window)
    main.show()

    res = app.exec_()
    app.quit()
    sys.exit(res)
