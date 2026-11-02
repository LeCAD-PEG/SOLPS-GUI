#!/usr/bin/env python3
"""UQ Runs actor: creates one SOLPS run directory per sample, submits them
to Slurm, follows their state and creates b2fplasmf. Emits
runsFinished(studyDir) once every run has finished with a b2fplasmf.
"""

import glob
import json
import os
import shutil
import subprocess

from PySide6.QtCore import Slot, Signal, Property, QProcess, QSettings, QSize, QTimer
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import (QGridLayout, QGroupBox, QPushButton, QVBoxLayout,
                               QHBoxLayout, QMessageBox, QTableWidgetItem, QSpinBox,
                               QLineEdit, QFormLayout, QLabel, QCheckBox,
                               QProgressBar, QTableWidget)

from tcsh_process import TcshProcess
from uq_common import (PARTITIONS, FILES_TO_COPY, SAMPLES_FILE, readSetup, updateSetup,
                       readCsv, inputNames, runDirs, setNamelistValue, newTable,
                       newCombo, UQWorkerMixin)


STATE_COLORS = {
    'finished': '#c8e6c9', 'failed': '#ffcdd2',
    'running/pending': '#fff9c4', 'not submitted': '#eeeeee', 'missing': '#eeeeee',
}

# Check run states every 2 minutes when "Watch" is checked.
WATCH_INTERVAL_MS = 120000


class UQRunsActor(UQWorkerMixin, TcshProcess):
    """ UQRunsActor(TcshProcess)

        Runs the SOLPS cases of a UQ study on Slurm.

        Attributes:
            runDirsCreated(str): Signal emits the study directory when all
                sample run directories are created.
            jobsSubmitted(int): Signal emits the number of submitted jobs.
            statusChanged(str): Signal emits a short summary of run states.
            runsFinished(str): Signal emits the study directory when all
                runs are finished and have b2fplasmf.
            busy(bool): Signal emits True when a task starts, False at end.
            logMessage(str): Signal emits progress and error messages.
    """
    icon = ''

    runDirsCreated = Signal(str)
    jobsSubmitted = Signal(int)
    statusChanged = Signal(str)
    runsFinished = Signal(str)
    busy = Signal(bool)
    logMessage = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.studyDirectory_ = ''
        self.setup = {}
        self.samples = None
        self.finishedEmitted = False

        self.watchTimer = QTimer(self)
        self.watchTimer.setInterval(WATCH_INTERVAL_MS)
        self.watchTimer.timeout.connect(self.checkStatus)

        self.prepareUserInterface()
        self.updateButtons()

        self.tcsh.stdOutput.connect(self.tcshOutput)
        self.tcsh.stdErrOutput.connect(self.tcshOutput)

    def sizeHint(self):
        return QSize(520, 420)

    def prepareUserInterface(self):
        layout = QGridLayout(self)

        self.studyLabel = QLabel('Study: none (waiting for samplesReady)', self)
        layout.addWidget(self.studyLabel, 0, 0, 1, 2)

        slurmBox = QGroupBox('Slurm', self)
        form = QFormLayout(slurmBox)
        self.partitionCombo = newCombo(PARTITIONS, 'all', slurmBox)
        form.addRow('Partition', self.partitionCombo)
        self.timeEdit = QLineEdit('06:00:00', slurmBox)
        form.addRow('Time limit', self.timeEdit)
        self.memEdit = QLineEdit('8G', slurmBox)
        form.addRow('Memory', self.memEdit)
        self.ntasksSpin = QSpinBox(slurmBox, minimum=1, maximum=28, value=1)
        form.addRow('MPI tasks per run', self.ntasksSpin)
        layout.addWidget(slurmBox, 1, 0)

        commandBox = QGroupBox('Commands', self)
        commands = QVBoxLayout(commandBox)
        self.buttons = {}
        for key, label, slot, tip in [
                ('create', 'Create run dirs', self.createRunDirs,
                 'Copy the base run and write the sample values.'),
                ('submit', 'Submit to Slurm', self.submitRuns,
                 'Submit every sample run with sbatch.'),
                ('status', 'Check status', self.checkStatus,
                 'Update the run table.'),
                ('plasmf', 'Create b2fplasmf', self.postProcessRuns,
                 'Run b2uf in every finished run.')]:
            button = QPushButton(label, commandBox)
            button.setToolTip(tip)
            button.clicked.connect(slot)
            commands.addWidget(button)
            self.buttons[key] = button
        self.watchCheck = QCheckBox('Watch (every 2 min)', commandBox)
        self.watchCheck.toggled.connect(self.setWatching)
        commands.addWidget(self.watchCheck)
        layout.addWidget(commandBox, 1, 1)

        runsBox = QGroupBox('Runs', self)
        runsLayout = QVBoxLayout(runsBox)
        self.summaryLabel = QLabel('', runsBox)
        runsLayout.addWidget(self.summaryLabel)
        self.runsTable = newTable(['Run', 'State', 'b2fplasmf'], runsBox)
        self.runsTable.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.runsTable.verticalHeader().setVisible(False)
        runsLayout.addWidget(self.runsTable)
        self.progressBar = QProgressBar(runsBox)
        self.progressBar.setRange(0, 0)
        self.progressBar.setMaximumHeight(10)
        self.progressBar.setTextVisible(False)
        runsLayout.addWidget(self.progressBar)
        layout.addWidget(runsBox, 2, 0, 1, 2)
        layout.setRowStretch(2, 1)

    def updateButtons(self):
        running = self.isBusy()
        haveSamples = self.samples is not None
        haveScripts = haveSamples and any(
            os.path.isfile(os.path.join(d, 'submit.sh')) for d in self.runDirs())
        state = {'create': haveSamples, 'submit': haveScripts,
                 'status': haveSamples, 'plasmf': haveScripts}
        for key, enabled in state.items():
            self.buttons[key].setEnabled(enabled and not running)
        self.progressBar.setVisible(running)

    @Slot(str)
    def log(self, text):
        self.logMessage.emit(f'[UQ Runs] {text.rstrip()}')

    # ------------------------------------------------------------------
    # Slots and properties
    # ------------------------------------------------------------------
    @Slot(str)
    def setStudy(self, studyDir):
        """Load uq_setup.json and uq_samples.csv of the study."""
        self.studyDirectory_ = studyDir
        self.setup = readSetup(studyDir)
        samplesPath = os.path.join(studyDir, SAMPLES_FILE)
        self.samples = readCsv(samplesPath)[2] if os.path.isfile(samplesPath) else None
        if self.setup.get('base_run'):
            self.setRunDir(self.setup['base_run'])
        slurm = self.setup.get('slurm')
        if slurm:
            self.partitionCombo.setCurrentText(slurm['partition'])
            self.timeEdit.setText(slurm['time'])
            self.memEdit.setText(slurm['mem'])
            self.ntasksSpin.setValue(slurm['ntasks'])
        count = 0 if self.samples is None else len(self.samples)
        self.studyLabel.setText(f'Study: <b>{os.path.basename(studyDir)}</b> ({count} samples)')
        self.studyLabel.setToolTip(studyDir)
        self.finishedEmitted = False
        self.checkStatus()

    def getStudy(self):
        return self.studyDirectory_

    studyDirectory = Property(str, getStudy, setStudy, doc='Directory of the UQ study')

    @Slot(bool)
    def setWatching(self, watch):
        self.watchCheck.setChecked(watch)
        if watch:
            self.watchTimer.start()
        else:
            self.watchTimer.stop()

    def getWatching(self):
        return self.watchTimer.isActive()

    watching = Property(bool, getWatching, setWatching,
                        doc='Check the run states every 2 minutes')

    @Slot(str)
    def setPartition(self, partition):
        self.partitionCombo.setCurrentText(partition)

    def getPartition(self):
        return self.partitionCombo.currentText()

    partition = Property(str, getPartition, setPartition, doc='Slurm partition')

    @Slot(str)
    def setTimeLimit(self, time):
        self.timeEdit.setText(time)

    def getTimeLimit(self):
        return self.timeEdit.text()

    timeLimit = Property(str, getTimeLimit, setTimeLimit, doc='Slurm time limit')

    @Slot(str)
    def setMemory(self, memory):
        self.memEdit.setText(memory)

    def getMemory(self):
        return self.memEdit.text()

    memory = Property(str, getMemory, setMemory, doc='Slurm memory per job')

    @Slot(int)
    def setTasks(self, ntasks):
        self.ntasksSpin.setValue(ntasks)

    def getTasks(self):
        return self.ntasksSpin.value()

    tasks = Property(int, getTasks, setTasks, doc='MPI tasks per run')

    # ------------------------------------------------------------------
    # Run directories and Slurm
    # ------------------------------------------------------------------
    def runDirs(self):
        if self.samples is None:
            return []
        return runDirs(self.studyDirectory_, self.setup.get('prefix', 'sample_'),
                       len(self.samples))

    def slurmSettings(self):
        return {'partition': self.partitionCombo.currentText(),
                'time': self.timeEdit.text().strip(),
                'mem': self.memEdit.text().strip(),
                'ntasks': self.ntasksSpin.value()}

    @Slot()
    def createRunDirs(self):
        if self.samples is None or not self.runDir:
            QMessageBox.warning(self, 'UQ', 'No samples. Generate samples first.')
            return
        dirs = self.runDirs()
        existing = [d for d in dirs if os.path.exists(d)]
        if existing:
            answer = QMessageBox.question(
                self, 'UQ', f'{len(existing)} run directories already exist in\n'
                f'{self.studyDirectory_}\nDelete and recreate them?')
            if answer != QMessageBox.StandardButton.Yes:
                return
        slurm = self.slurmSettings()
        self.setup = updateSetup(self.studyDirectory_, slurm=slurm)
        baseDir = self.runDir
        baserun = os.path.join(baseDir, 'baserun')
        if not os.path.exists(baserun):
            baserun = os.path.join(os.path.dirname(os.path.normpath(baseDir)), 'baserun')
        baserun = os.path.realpath(baserun) if os.path.exists(baserun) else None
        if baserun is None:
            QMessageBox.warning(self, 'UQ', 'No baserun found next to or inside the base '
                                'run. The SOLPS Makefile needs it for b2fgmtry.')
            return
        # The SOLPS Makefile reads the grid from ../baserun of every run.
        studyBaserun = os.path.join(self.studyDirectory_, 'baserun')
        if os.path.islink(studyBaserun):
            os.remove(studyBaserun)
        if not os.path.exists(studyBaserun):
            os.symlink(baserun, studyBaserun)
        solpsTop = (self.tcsh.findSolpsTop(baseDir) or os.environ.get('SOLPSTOP', '')).strip()
        if not solpsTop:
            QMessageBox.warning(self, 'UQ', 'SOLPSTOP not found for the base run.')
            return
        inputs = self.setup['inputs']
        names = inputNames(inputs)
        samples = self.samples

        def work(log):
            for runDir, sample in zip(dirs, samples):
                if os.path.exists(runDir):
                    shutil.rmtree(runDir)
                os.makedirs(runDir)
                for fileName in FILES_TO_COPY:
                    source = os.path.join(baseDir, fileName)
                    if os.path.exists(source):
                        shutil.copy(source, runDir)
                for cf in sorted(glob.glob(os.path.join(baseDir, 'cf*.dat'))):
                    os.symlink(os.path.realpath(cf),
                               os.path.join(runDir, os.path.basename(cf)))
                os.symlink(baserun, os.path.join(runDir, 'baserun'))

                params = {}
                for entry, name, value in zip(inputs, names, sample):
                    path = os.path.join(runDir, entry['file'])
                    with open(path, 'r', errors='ignore') as f:
                        text = f.read()
                    text = setNamelistValue(text, entry['variable'], entry['index'], value)
                    with open(path, 'w') as f:
                        f.write(text)
                    params[name] = float(value)
                with open(os.path.join(runDir, 'params.json'), 'w') as f:
                    json.dump(params, f, indent=2)
                self.writeSubmitScript(runDir, slurm, solpsTop)
                log(f'{os.path.basename(runDir)}: ' +
                    ', '.join(f'{k}={v:.4g}' for k, v in params.items()))
            log(f'{len(dirs)} run directories created in {self.studyDirectory_}')

        def done(_):
            self.checkStatus()
            self.runDirsCreated.emit(self.studyDirectory_)

        self.startWorker(work, done)

    def writeSubmitScript(self, runDir, slurm, solpsTop):
        """The job loads the SOLPS-ITER environment with setup.csh, like the
        GUI tcsh session, so it does not depend on the environment of the
        program that runs sbatch.
        """
        settings = QSettings('ITER', 'solps-gui')
        device = settings.value('device_environment', 'iter')
        compiler = settings.value('compiler_environment', 'ifort64')
        ntasks = int(slurm['ntasks'])
        if ntasks > 1:
            b2run = 'b2run -m \\"srun -n $SLURM_NTASKS\\" b2mn >& run.log'
        else:
            b2run = 'b2run b2mn >& run.log'
        run = (f'tcsh -c "setenv DEVICE {device}; cd {solpsTop} && '
               f'source setup.csh {compiler} >& /dev/null; '
               f'cd {runDir} && {b2run}"')
        script = f"""#!/bin/bash
#SBATCH --job-name=uq_{os.path.basename(runDir)}
#SBATCH --partition={slurm['partition']}
#SBATCH --nodes=1
#SBATCH --ntasks={ntasks}
#SBATCH --cpus-per-task=1
#SBATCH --time={slurm['time']}
#SBATCH --mem={slurm['mem']}
#SBATCH --output={runDir}/job.out
#SBATCH --error={runDir}/job.err
#SBATCH --no-requeue

export SOLPSTOP={solpsTop}
export PATH=$SOLPSTOP/bin:$PATH
cd {runDir} || exit 1
echo "Running on $(hostname), started at $(date)"

{run}
status=$?
# b2run can return 0 although b2mn never ran (e.g. a Makefile error).
if [ $status -eq 0 ] && [ ! -s {runDir}/b2fstate ]; then
    echo "b2fstate was not written, see run.log" >&2
    status=99
fi

echo "DONE exit=$status" > {runDir}/FINISHED
echo "Finished at $(date) with exit code $status"
"""
        path = os.path.join(runDir, 'submit.sh')
        with open(path, 'w') as f:
            f.write(script)
        os.chmod(path, 0o755)

    @Slot()
    def submitRuns(self):
        dirs = [d for d in self.runDirs() if os.path.isfile(os.path.join(d, 'submit.sh'))]
        if not dirs:
            QMessageBox.warning(self, 'UQ', 'No submit.sh found. Create run dirs first.')
            return
        if len(dirs) > 100:
            QMessageBox.warning(self, 'UQ', 'More than 100 runs exceed the Slurm limit '
                                'of active jobs per user.')
            return
        answer = QMessageBox.question(
            self, 'UQ', f'Submit {len(dirs)} jobs to partition '
            f"'{self.partitionCombo.currentText()}' "
            f'(time {self.timeEdit.text()}, mem {self.memEdit.text()})?')
        if answer != QMessageBox.StandardButton.Yes:
            return
        studyDir = self.studyDirectory_

        def work(log):
            jobIds = []
            for runDir in dirs:
                for name in ('FINISHED', 'FAILED', 'run.log', 'b2mn.prt',
                             'job.out', 'job.err'):
                    path = os.path.join(runDir, name)
                    if os.path.exists(path):
                        os.remove(path)
                result = subprocess.run(['sbatch', os.path.join(runDir, 'submit.sh')],
                                        capture_output=True, text=True)
                if result.returncode == 0:
                    jobIds.append(result.stdout.strip().split()[-1])
                    log(f'{os.path.basename(runDir)}: job {jobIds[-1]}')
                else:
                    log(f'{os.path.basename(runDir)}: sbatch FAILED {result.stderr.strip()}')
            with open(os.path.join(studyDir, 'uq_job_ids.txt'), 'w') as f:
                f.write('\n'.join(jobIds) + '\n')
            log(f'{len(jobIds)}/{len(dirs)} jobs submitted.')
            return len(jobIds)

        def done(count):
            self.finishedEmitted = False
            self.checkStatus()
            self.jobsSubmitted.emit(count)

        self.startWorker(work, done)

    @staticmethod
    def runState(runDir):
        finished = os.path.join(runDir, 'FINISHED')
        if os.path.isfile(finished):
            with open(finished) as f:
                text = f.read()
            if 'exit=' in text and 'exit=0' not in text:
                return 'failed'
            return 'finished'
        if os.path.isfile(os.path.join(runDir, 'job.out')):
            return 'running/pending'
        if os.path.isfile(os.path.join(runDir, 'submit.sh')):
            return 'not submitted'
        return 'missing'

    @Slot()
    def checkStatus(self):
        dirs = self.runDirs()
        self.runsTable.setRowCount(len(dirs))
        counts = {}
        plasmf = 0
        for row, runDir in enumerate(dirs):
            state = self.runState(runDir)
            hasPlasmf = os.path.isfile(os.path.join(runDir, 'b2fplasmf'))
            counts[state] = counts.get(state, 0) + 1
            plasmf += hasPlasmf
            color = QBrush(QColor(STATE_COLORS[state]))
            for column, text in enumerate([os.path.basename(runDir), state,
                                           'yes' if hasPlasmf else '']):
                item = QTableWidgetItem(text)
                item.setBackground(color)
                self.runsTable.setItem(row, column, item)
        summary = ', '.join(f'{key}: {value}' for key, value in sorted(counts.items()))
        if dirs:
            summary += f' | b2fplasmf: {plasmf}/{len(dirs)}'
        self.summaryLabel.setText(summary)
        self.updateButtons()
        self.statusChanged.emit(summary)
        if dirs and plasmf == len(dirs) and not self.finishedEmitted:
            self.finishedEmitted = True
            self.log(f'All {len(dirs)} runs finished with b2fplasmf.')
            self.runsFinished.emit(self.studyDirectory_)

    @Slot()
    def postProcessRuns(self):
        """Create b2fplasmf in every finished run with the SOLPS tcsh session,
        the same command as 'Create b2fplasmf' in the Optimization tab.
        """
        if not self.runDir:
            return
        self.tcsh.setRunDir(self.runDir)
        self.tcsh.setTcshPath(self.getTcshPath())
        if self.tcsh.state() == QProcess.ProcessState.NotRunning:
            self.tcsh.start()
        if self.tcsh.state() == QProcess.ProcessState.NotRunning:
            self.log('Failed to start tcsh process.')
            return
        prefix = self.setup.get('prefix', 'sample_')
        self.log('Creating b2fplasmf in finished runs...')
        self.tcsh.write(
            f'cd {self.studyDirectory_}\n'
            f'foreach d ({prefix}*)\n'
            'if ( -e $d/FINISHED && ! -e $d/b2fplasmf ) then\n'
            'echo "b2fplasmf: $d"\n'
            '(cd $d; gmake -f $SOLPSTOP/runs/Makefile b2uf.prt >& b2uf_post.log)\n'
            'endif\n'
            'end\n'
            'echo "UQ post-processing done"\n')

    @Slot(str)
    def tcshOutput(self, text):
        for line in text.splitlines():
            if 'no access to tty' in line or 'Inappropriate ioctl' in line \
                    or 'job control' in line or 'TCSH READY' in line or not line.strip():
                continue
            self.log(line)
            if 'UQ post-processing done' in line:
                self.checkStatus()


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = UQRunsActor()
    widget.logMessage.connect(print)
    if len(sys.argv) > 1:
        widget.setStudy(sys.argv[1])
    widget.show()
    sys.exit(app.exec())
