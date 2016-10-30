from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import (QPixmap, QImage)
import sys
from PyQt5.QtWidgets import (QLabel, QHBoxLayout, QWidget, QApplication, QMainWindow)
from PyQt5.QtCore import (QProcess, QProcessEnvironment)

import logging
from pathlib import Path
import os.path
import time

class B2Plot(QLabel):
    def __init__(self, parent=None):
        #Call base class method
        # QtCore.QProcess.__init__(self)
        super(B2Plot, self).__init__(parent)

        #To show all log above DEBUG lvl
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

        self.base = QProcess()
        self.convert = QProcess()

        self.base.started.connect(self.writeToBase)
        self.base.finished.connect(self.startProcessConvert)
        self.base.readyReadStandardOutput.connect(self.readTcshStdOutput)

        self.convert.started.connect(self.writeToConvert)

        self.startProcessBase()

    def startProcessBase(self):
        self.base.start("/bin/tcsh")

    def writeToBase(self):
        # here we first set the working directory
        self.b2plot_dir = os.path.expanduser("~/solps-iter-devel/runs/ITER_535_D+He+Ar/my_new_run")
        self.cmd_base = "cd ~/solps-iter-devel/" + "\n" \
                    + "source setup.csh" + "\n" \
                    + "cd " + self.b2plot_dir + "\n" \
                    + "setup_baserun_eirene_links" + "\n" \
                    + "setenv B2PLOT_DEV 'ps'" + "\n" \
                    + "echo phys a4p ti te m/ surf | b2plot" + "\n" \
                    + "echo b2plot_done" + "\n"

        self.base.write(bytearray(self.cmd_base, "utf8"))



    #currently we use logging. instead of QTextEdit to show standard output
    def setTcshWindowOutput(self):
        # Creating window, in this tcsh std output / progress will be shown
        self.edit = QtWidgets.QTextEdit()
        self.edit.setMinimumWidth(900)
        self.edit.setMinimumHeight(600)
        self.edit.setWindowTitle("Tcsh Standard Output ")
        self.edit.show()

    def readTcshStdOutput(self):
        if self.base.NotRunning != 1:
            self.baseOutput = str(self.base.readAllStandardOutput())

            logging.debug(self.baseOutput)

            # print(baseOutput)

            #to show tcsh std output in other window
            # self.edit.append(str(baseOutput))

            # when "rmdir b2pl.exe.dir" will be found in tcsh std output,
            # which indicates that the b2plot command finished, then end
            # the tcsh process

            # if "rmdir b2pl.exe.dir" in self.baseOutput:
            if "b2plot_done" in self.baseOutput:
                # logging.info("'rmdir b2pl.exe.dir' command found.")
                logging.info("'b2plot_done' command found.")

                self .getCurrentDirectory()

                self.exitBaseProcess()

    def exitBaseProcess(self):
        logging.info("Exiting the base. process")
        # killing the base process
        self.base.kill()

    def getCurrentDirectory(self):
        pass


    ######
    def startProcessConvert(self):
        #it doesn'y work with "$home" == /home/ITER/tomsicp/, we have to use os.path.expanduser and ~ symbol
        # b2plot_ps_file = os.path.expanduser("~/solps-iter-devel/runs/ITER_535_D+He+Ar/my_new_run/b2plot.ps")
        b2plot_ps_file = self.b2plot_dir + "/b2plot.ps"
        if os.path.isfile(b2plot_ps_file) == True:
            if self.convert.Running != 1:
                self.convert.start("/bin/tcsh")
                # print(self.convert.state())
            else:
                logging.warning("convert process is already running.")
        else:
            logging.warning("The b2plot.ps file was not generated, it doesn't exist.")

    def writeToConvert(self):
        logging.info("Writing to convert process.")
        self.cmd_convert = "cd " + self.b2plot_dir + "\n" \
                        + "convert b2plot.ps gif:- | display gif:-" + "\n" \


        self.convert.write(bytearray(self.cmd_convert, "utf8"))










if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    qProcess = B2Plot()
    # qProcess.setTcshWindowOutput()




    sys.exit(app.exec_())