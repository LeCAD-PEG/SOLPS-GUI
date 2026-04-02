#!/usr/bin/env python3

from PySide6.QtCore import Slot, QProcess, QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QPlainTextEdit, QLineEdit, QLabel, QMessageBox


class SqueueActor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.read_output)

        self.cancelProcess = QProcess(self)
        self.cancelProcess.setProcessChannelMode(QProcess.MergedChannels)
        self.cancelProcess.readyReadStandardOutput.connect(self.read_cancel_output)

        self.timer = QTimer(self)
        self.timer.setInterval(3000)
        self.timer.timeout.connect(self.run_once)
        self.monitor_enabled = False

        self.prepareUserInterface()

    def prepareUserInterface(self):
        layout = QVBoxLayout(self)

        buttonLayout = QHBoxLayout()
        self.startButton = QPushButton("Start")
        self.stopButton = QPushButton("Stop")

        self.startButton.clicked.connect(self.start_monitor)
        self.stopButton.clicked.connect(self.stop_monitor)

        buttonLayout.addWidget(self.startButton)
        buttonLayout.addWidget(self.stopButton)

        cancelLayout = QHBoxLayout()
        cancelLayout.addWidget(QLabel("Job ID:"))
        self.lineEditJobId = QLineEdit()
        self.cancelButton = QPushButton("scancel")
        self.cancelButton.clicked.connect(self.cancel_job)

        cancelLayout.addWidget(self.lineEditJobId)
        cancelLayout.addWidget(self.cancelButton)

        self.textDisplay = QPlainTextEdit()
        self.textDisplay.setReadOnly(True)
        self.textDisplay.setLineWrapMode(QPlainTextEdit.NoWrap)

        layout.addLayout(buttonLayout)
        layout.addLayout(cancelLayout)
        layout.addWidget(self.textDisplay)
        
    def showEvent(self, event):
        super().showEvent(event)
        if self.monitor_enabled:
            self.run_once()
            self.timer.start()

    def hideEvent(self, event):
        super().hideEvent(event)
        self.timer.stop()

    @Slot()
    def start_monitor(self):
        self.monitor_enabled = True
        self.run_once()
        self.timer.start()

    @Slot()
    def stop_monitor(self):
        self.monitor_enabled = False
        self.timer.stop()

    @Slot()
    def run_once(self):
        if self.process.state() == QProcess.NotRunning:
            self.process.start(
                "bash",
                ["-lc", 'squeue -u $USER -o "%.18i %.9P %.20j %.8u %.8T %.10M %.6D %R"']
            )

    @Slot()
    def read_output(self):
        data = self.process.readAllStandardOutput()
        text = bytes(data).decode("utf-8", errors="replace")
        self.textDisplay.setPlainText(text.rstrip())

    @Slot()
    def cancel_job(self):
        job_id = self.lineEditJobId.text().strip()
        if not job_id:
            QMessageBox.warning(self, "Missing job id", "Please enter a job id.")
            return

        self.cancelProcess.start(
            "bash",
            ["-lc", f"scancel {job_id} && echo Cancelled {job_id}"]
        )

    @Slot()
    def read_cancel_output(self):
        data = self.cancelProcess.readAllStandardOutput()
        text = bytes(data).decode("utf-8", errors="replace")
        if text.strip():
            QMessageBox.information(self, "scancel", text.strip())
        self.run_once()