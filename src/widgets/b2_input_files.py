#!/usr/bin/env python3
""" A PyQt widget for B2 input files.
"""

from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QGridLayout, QGroupBox,
                             QCheckBox, QSpacerItem, QSizePolicy,
                             QPlainTextEdit, QInputDialog)
from PyQt5.QtCore import pyqtSlot, Qt, QDateTime
from PyQt5.QtGui import QTextCursor
from tcsh_process import TcshProcess
import logging
import os

TIME = QDateTime()
TIME_FORMAT = "ddd MMM d t yyyy"


class B2Vars:
    NumOfVars = 4
    b2ai, b2ah, b2ar, b2ag = range(NumOfVars)

    Name = {0: 'b2ai', 1: 'b2ah', 2: 'b2ar', 3: 'b2ag'}
    command = Name

    Values = {'b2ai': 0, 'b2ah': 1, 'b2ar': 2, 'b2ag': 3}

    Default = {i: 0 for i in range(NumOfVars)}


class B2State:
    notRunning, starting, waiting, b2Running = range(4)


class B2Push(QPushButton):
    def __init__(self, parent=None, value=None):
        super(B2Push, self).__init__(parent)
        self.value = value


class B2InputFiles(TcshProcess):

    def __init__(self, parent=None):
        super(B2InputFiles, self).__init__(parent)
        self.vars = B2Vars.Default
        # self.activateDebugging()

        self.prepareUserInterface()

        self.tcsh.setTcshPath('/usr/bin/tcsh')
        self.tcsh.prcStateChanged.connect(self.updateText)
        self.tcsh.prcFinished.connect(self.updateText)
        self.tcsh.prcError.connect(self.updateError)
        self.tcsh.stdOutput.connect(self.updateText)
        self.tcsh.stdErrOutput.connect(self.updateError)
        self.STATE = B2State.notRunning

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
        for i in range(B2Vars.NumOfVars // _n):
            for j in range(_n):
                # Creating checkboxes for
                x = QCheckBox(B2Vars.Name[i * _n + j])
                x.setCheckState(0)
                x.stateChanged.connect(self.setVarsFromClickedGroup)
                groupLayout.addWidget(x, j, i)
        leftOver = B2Vars.NumOfVars % _n
        if leftOver > 0:
            for k in range(leftOver):
                x = QCheckBox(B2Vars.Name[(i + 1) * _n + k])
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

        for i in range(B2Vars.NumOfVars):
            x = B2Push(value=B2Vars.command[i])
            x.clicked.connect(self.runStep)
            x.setText(B2Vars.Name[i])
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

        manualInput = QPushButton('Terminal input')
        manualInput.clicked.connect(self.manualInput)

        groupLayout.addWidget(manualInput, 1, 1)

        groupBox3.setLayout(groupLayout)
        # Group Box 3
        #############

        lowerGridLayout.addWidget(groupBox3, 0, 1)

        mainLayout.addLayout(upperGridLayout)
        mainLayout.addLayout(lowerGridLayout)
        self.setLayout(mainLayout)

    @pyqtSlot()
    def setVarsFromClickedGroup(self):
        layout = self.clickedGroup.layout()
        for i in range(layout.count()):
            item = layout.itemAt(i).widget()
            if item.isChecked():
                self.vars[i] = 1
            else:
                self.vars[i] = 0

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
        B2Block = 0
        with open(file, 'r') as f:
            for i, line in enumerate(f):
                if reading and line.startswith('&'):
                    reading = 0

                if reading:
                    try:
                        sline = line.split()
                        if len(sline) == 3:
                            name = sline[0] + ' ' + sline[1]
                            val = sline[2]
                        else:
                            name, val = sline[0], sline[1]
                        self.vars[B2Vars.Values[name]] = int(val) if \
                            val.isdigit else val
                    except KeyError as e:
                        logging.error('Uknown key ' + name)
                    except ValueError as e:
                        logging.error("Wrong value for: " + name)
                    except IndexError as e:
                        logging.error("Not enough arguments on line: " + line)

                if line.startswith('&B2InputFiles'):
                    reading = 1  # We are reading the block
                    B2Block += 1
                    if B2Block > 1:
                        logging.error("Multiple b2 blocks in .status file "
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
        b2lines = [B2Vars.Name[i] + ' ' + str(variables[i]) for i
                   in range(len(variables))]
        if os.access(file, os.F_OK):
            if os.access(file, os.W_OK):
                logging.info(".status file exists in baserun " + baserunDir)
                with open(file, 'r') as f:
                    text = f.read()

                if "&B2InputFiles" in text:
                    logging.info("b2 block found in .status file!")
                    left, right = text.split("&B2InputFiles", 1)
                    center, right = right.split("&", 1)

                    text = left + "&B2InputFiles\n" + '\n'.join(b2lines) + \
                        "\n&" + right

                else:
                    logging.info("No b2 block found in .status file!")
                    text = '&B2InputFiles\n' + '\n'.join(b2lines) + \
                           '\n&\n' + text

                with open(file, 'w') as f:
                    f.write(text)
                logging.info("b2 Written to .status file.")

            else:
                logging.error("No writing permission to .status file!")

        else:
            logging.info("No .status file exists in baserun " + baserunDir)
            with open(file, 'w') as f:
                text = '&B2InputFiles\n'
                text += '\n'.join(b2lines)
                text += '\n&'
                f.write(text)
            logging.info(".status file created for b2 block!")

    def resetCheckBox(self):
        layout = self.clickedGroup.layout()
        for i in range(layout.count()):
            layout.itemAt(i).widget().setCheckState(Qt.Unchecked)

    def appendToStatus(self, msg):
        baserunDir = self.runDir
        if not baserunDir:
            return
        path = baserunDir + '/.status'
        if os.access(path, os.W_OK | os.F_OK):
            with open(path, 'a') as f:
                time = TIME.currentDateTime().toString(TIME_FORMAT)
                f.write('\nRan b2 step ' + msg + ' at ' + time)

    @pyqtSlot()
    def runStep(self):
        if not self.tcsh.state():
            return
        if self.STATE == B2State.waiting:
            sender = self.sender()
            self.appendToStatus(sender.text())
            msg = 'b2run ' + sender.value + '\n'
            self.tcsh.write(msg)

    @pyqtSlot()
    def manualInput(self):
        if not self.tcsh.state():
            return
        if not self.STATE >= B2State.waiting:
            return

        msg, ok = QInputDialog.getMultiLineText(self, 'Input dialog',
                                                'Command:')
        if ok:
            self.tcsh.write(msg + '\n')
            self.insertTextAtBottom(msg)

    def insertTextAtBottom(self, msg):
        self.textDisplay.moveCursor(QTextCursor.End)
        if msg.endswith('\n'):
            msg = msg[:-1]
        self.textDisplay.insertPlainText('\n' + msg)
        self.textDisplay.moveCursor(QTextCursor.End)

    def startTerminal(self):
        self.textDisplay.clear()
        if not self.getRunDir():
            self.textDisplay.appendPlainText('No baserun selected.')
            return

        if self.tcsh.state():
            self.tcsh.terminate()
            self.tcsh.close()

        self.startTcsh()
        self.tcsh.waitForStarted()

        cmd = 'cd ' + self.getRunDir() + '\n'
        self.textDisplay.appendPlainText('Sourcing setup.csh. It will '
                                         'take a while.')
        self.tcsh.write(cmd)

        self.STATE = B2State.starting
        cmd = 'echo B2 READY\n'
        self.tcsh.write(cmd)

    @pyqtSlot(str)
    def updateText(self, msg):
        if "B2 READY" in msg:
            self.STATE = B2State.waiting
            self.textDisplay.appendPlainText('Ready to run b2*.exe in ' +
                                             self.getRunDir())
            return

        if self.STATE >= B2State.waiting:
            self.textDisplay.appendPlainText(msg)

    @pyqtSlot(str)
    def updateError(self, msg):
        if self.STATE >= B2State.waiting:
            self.textDisplay.appendPlainText(msg)

    # Overloaded
    @pyqtSlot(str)
    def setRunDir(self, runDir):
        """ In this case we do not need to rerun the TCSH terminal as only the
        b2*.exe files are run. So first we check if SOLPSTOP has changed.

        If it has rerun the terminal, otherwise just change the directory.
        """
        oldRunDir = self.runDir
        if not runDir.endswith('baserun') and runDir != oldRunDir:
            self.textDisplay.clear()
            self.storeStatusFile(oldRunDir)
            self.textDisplay.appendPlainText('Current directory is not a '
                                             'baserun: ' + runDir)
            self.STATE = B2State.notRunning
            return

        self.storeStatusFile(oldRunDir)
        self.readStatusFile(runDir)
        oldSolpsTop = self.tcsh.findSolpsTop(oldRunDir) if oldRunDir else ''
        newSolpsTop = self.tcsh.findSolpsTop(runDir)
        super(B2InputFiles, self).setRunDir(runDir)

        if oldSolpsTop != newSolpsTop:
            self.startTerminal()
        else:
            if self.tcsh.state():
                self.STATE = B2State.notRunning
                cmd = 'cd ' + runDir + '\n'
                self.tcsh.write(cmd)
                self.STATE = B2State.waiting
                self.textDisplay.clear()
                self.textDisplay.appendPlainText('Changed to new baserun dir:'
                                                 ' ' + runDir)
            else:
                self.startTerminal()


if __name__ == '__main__':

    from PyQt5.QtWidgets import QApplication, QMainWindow
    import sys

    app = QApplication(sys.argv)

    main = QMainWindow()

    b2InputFiles = B2InputFiles()
    main.setCentralWidget(b2InputFiles)
    main.show()

    sys.exit(app.exec_())
