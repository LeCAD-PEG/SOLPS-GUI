from PySide6.QtCore import  Slot, Signal, QTimer, QThread
from PySide6.QtWidgets import QLCDNumber

class LongOperation(QThread):
    result = Signal(object) #: Signal(object): |Signal| for emitting result object.
    def run(self):
        print('Running in LongOperation(QThread)')
        print(f'QThread.currentThread = {QThread.currentThread()}')
        self.sleep(3)
        self.result.emit(2)
        print('run() finished')


class Counter(QLCDNumber):
    """ Graphical actor
    """

    finished = Signal() #: Signal(): |Signal| for indicating that a process has finished. 
    next_step = Signal() #: Signal(): |Signal| for a next step.
    checkpoint = Signal(float) #: Signal(float): |Signal| for emitting checkpoint. 

    def __init__(self, parent=None):
        super().__init__(parent)

        self.myop = LongOperation()
        self.myop.result.connect(self.recurring_timer_increment)
        self.myop.finished.connect(self.log_finished)
        self.myop.started.connect(self.log_started)

        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.recurring_timer)       

    @Slot()
    def compute(self):
        """ |Slot| that starts LongOperation if not already running."""
        print(f'QThread.idealThreadCount = {QThread.idealThreadCount()}')
        if self.myop.isRunning():
            print(f'LongOperation already running in loopLevel {self.myop.loopLevel()}')
        else:
            self.myop.start()

    @Slot()
    def start(self):
        """ |Slot| that reads interval from dynamic property and starts timer."""
        if interval := self.property('interval'):
            self.timer.setInterval(interval)
        self.timer.start()

    @Slot()
    def stop(self):
        """ |Slot| that stops timer."""
        self.timer.stop()

    @Slot()
    def reset(self):
        """ |Slot| that resets timer display."""
        self.display(0)

    @Slot()
    def log_started(self):
        """ |Slot| that logs the start of operation."""
        print('LongOperation started')

    @Slot()
    def log_finished(self):
        """ |Slot| that logs the end of operation."""
        print('LongOperation finished')

    @Slot()
    def step(self):
        """ |Slot| that does one step in the counter. Counter goes up by one until max_steps value is reached. """
        if max_steps := self.property('max_steps'):
            if self.intValue() > max_steps:
                self.finished.emit()
                return

        self.display(self.intValue()+1)
        self.next_step.emit()

        if checkpoint_interval := self.property('checkpoint_interval'):
            if self.intValue() % checkpoint_interval == 0:
                self.checkpoint.emit(float(self.intValue()+1))

    def recurring_timer(self):
        """After timer finishes, counter goes up by one or stops if max steps reached."""
        if max_steps := self.property('max_steps'):
            if self.intValue() > max_steps:
                print(max_steps)
                return

        self.display(self.intValue()+1)

    def recurring_timer_increment(self, value):
        """After result signal is emmited, counter goes up by that value. 

        Args:
            value(int): value to add to counter."""
        self.display(self.intValue()+value)

if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    from PySide6.QtUiTools import loadUiType

    uiclass, baseclass = loadUiType("counter.ui")

    class MainWindow(uiclass, baseclass):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)



    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())