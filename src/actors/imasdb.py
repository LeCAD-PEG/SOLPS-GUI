"""IMAS Database reader and writer"""
from PySide6.QtCore import  (QObject, QSize, Property, Slot, Signal, 
    QMetaMethod, QRunnable, QThreadPool, QTimer, QRect, Qt, QEvent, QSignalBlocker)
from PySide6.QtWidgets import (QWidget,QVBoxLayout, QPushButton, QPlainTextEdit,
    QComboBox, QGridLayout, QGroupBox, QLabel, QLineEdit, QSplitter, QFrame,
    QCheckBox, QApplication, QScrollArea)
from PySide6.QtUiTools import loadUiType 
from PySide6.QtGui import QIntValidator, QDoubleValidator, QFont

import getpass
import multiprocessing
import traceback
import sys
import enum
import xml.etree.ElementTree as ET
import numpy as np

try:
    import imas
    class Backend(enum.Enum):
        MDSPLUS = imas.ids_defs.MDSPLUS_BACKEND
        HDF5    = imas.ids_defs.HDF5_BACKEND
        MEMORY  = imas.ids_defs.MEMORY_BACKEND
        UDA     = imas.ids_defs.UDA_BACKEND
    # Backend["MDSPLUS"].value
    # Backend(imas.ids_defs.MDSPLUS_BACKEND).name
except ImportError:
    print('IMAS not available!')
    class Backend(enum.Enum):
        NO = 0
        @classmethod
        def _missing_(cls, value):
            """Return default when value is not found"""
            return cls.NO 

    IDS_NAMES = ['amns_data', 'barometry', 'b_field_non_axisymmetric', 'bolometer', 'bremsstrahlung_visible', 'calorimetry',
            'camera_ir', 'camera_visible', 'camera_x_rays', 'charge_exchange', 'coils_non_axisymmetric', 'controllers',
            'core_instant_changes', 'core_profiles', 'core_sources', 'core_transport', 'cryostat', 'dataset_description',
            'dataset_fair', 'disruption', 'distribution_sources', 'distributions', 'divertors', 'ec_launchers', 'ece', 'edge_profiles',
            'edge_sources', 'edge_transport', 'em_coupling', 'equilibrium', 'ferritic', 'focs', 'gas_injection', 'gas_pumping',
            'gyrokinetics_local', 'hard_x_rays', 'ic_antennas', 'interferometer', 'iron_core', 'langmuir_probes', 'lh_antennas',
            'magnetics', 'operational_instrumentation', 'mhd', 'mhd_linear', 'mse', 'nbi', 'neutron_diagnostic', 'ntms',
            'pellets', 'pf_active', 'pf_passive', 'pf_plasma', 'plasma_initiation', 'plasma_profiles', 'plasma_sources',
            'plasma_transport', 'polarimeter', 'pulse_schedule', 'radiation', 'real_time_data', 'reflectometer_profile',
            'reflectometer_fluctuation', 'refractometer', 'runaway_electrons', 'sawteeth', 'soft_x_rays', 'spectrometer_mass',
            'spectrometer_uv', 'spectrometer_visible', 'spectrometer_x_ray_crystal', 'spi', 'summary', 'temporary', 'thomson_scattering',
            'tf', 'transport_solver_numerics', 'turbulence', 'wall', 'waves', 'workflow']



class StdRedirector:
    """Redirects stdout to a custom output stream.
    """
    def __init__(self, target):
        self.target = target    
    def write(self, text):
        self.target(text)
    def flush(self):
        pass

class WorkerSignals(QObject):
    def __init__(self, parent=None) -> None:
        """ Defines the signals available from a running worker thread.
        """  
        super().__init__(parent)

    finished = Signal() 
    """ Signal(): |Signal| for indicating that the worker finished."""
    error = Signal(tuple)  
    """ Signal(tuple): |Signal| for emitting worker error message 
       in the form of *tuple(exctype, value, traceback.format_exc())*."""
    result = Signal(object) 
    """ Signal(object): |Signal| for emitting worker computational result."""
    progress = Signal(int)
    """ Signal(int): |Signal| for emitting worker progress. """
    log = Signal(str)
    """ Signal(int): |Signal| for emitting worker log. """


class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        """ Worker thread

        Inherits from QRunnable to handler worker thread setup, signals and 
        wrap-up.

        Args:
            fn: The function callback to run on this worker thread. Supplied 
                args and kwargs will be passed through to the runner.
            args: Arguments to pass to the callback function
            kwargs: Keywords to pass to the callback function
        """
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def add_callback(self):
        """ Add the callback to our kwargs."""
        self.kwargs['progress_callback'] = self.signals.progress
        self.kwargs['log_callback'] = self.signals.log

    def handle_output(self, text):
        """Emit the captured output.
        
        Args:
            text(string): captured text output.
        """
        if isinstance(text, bytes):
            text = text.decode('utf-8')
        self.signals.log.emit(text) 

    @Slot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """

        # Retrieve args/kwargs here; and fire processing using them
        old_stderr = sys.stderr
        old_stdout = sys.stdout
        try:
            sys.stderr = StdRedirector(self.handle_output)
            sys.stdout = StdRedirector(self.handle_output)
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of 
                                              # the processing
        finally:
            sys.stderr = old_stderr
            sys.stdout = old_stdout
            self.signals.finished.emit()  # Done


def put_ids_process(uri: str, occurrence: int,  mode: str, ids_queue: multiprocessing.Queue):
    """ Creates empty database, waits for IDSs to populate. 
        :class:`IMASDB.ids_queue` writes all IDSs from the queue into the 
        database until ``None`` is received in the queue, closes the database.

    Args:
        uri (str): Name IMAS database.
        occurence (int): occurence type.
        mode (str): IMAS open mode {'x', 'a', 'w', 'r'}
        ids_queue (multiprocessing.Queue): Queue of IDS objects to be put into
                                           database.
    """
    print(f"Creating IMAS {uri} database {'with occurrence ' + str(occurrence) if occurrence else ''}")


    try:
        dbentry = imas.DBEntry(uri=uri, mode=mode)
    except Exception as e:
        print(f'ERROR in put_ids_process: {e}')

    received_ids_types_occurrences = set()
    while True:
        (ids, occurrence) = ids_queue.get()
        if ids is None or occurrence is None: 
            break
        if (type(ids), occurrence) in received_ids_types_occurrences:
            dbentry.put_slice(ids, occurrence=occurrence)
        else:
            dbentry.put(ids, occurrence=occurrence)
            received_ids_types_occurrences.add((type(ids), occurrence))

    print(f"Closing IMAS {uri}")
    dbentry.close()


class IMASDB(QWidget):
    icon = ":/iter.org/pds/icons/imas.png"
    started = Signal()  
    """Signal(): |Signal| for indicating that :class:`get` started."""
    finished = Signal()
    """ Signal(): |Signal| for indicating that :class:`get` or :class:`put` 
    has finished. """
    emit_pulse = Signal(str)
    """ Signal(str): |Signal| for sending pulse information in the form of
    *(shot, run, occurrence, username, database, backend)* to :class:`iplot.IPlot`."""
    _running_state = 0 # 0=not started, 1=started, 2=finished

    def add_signal(self, name:str, *args):
        """ Creates a new class which is identical to this one, but which has a 
        new Signal class attribute called of the given *name*.

        See https://stackoverflow.com/questions/50294652 for possible problems

        Args:
            name (str): Name of the class and Signal to be created for emitting.
            args: Arguments to be passed when creating the Signal attribute.

        """
        # Get the class of this instance.
        cls = self.__class__

        # Create a new class which is identical to this one,
        # but which has a new Signal class attribute called of the given name.
        new_cls = type(
            cls.__name__, cls.__bases__,
            {**cls.__dict__, name: Signal(object)},
        )
        # Update this instance's class with the newly created one.
        self.__class__ = new_cls  # noqa


    def __init__(self, parent=None):
        """  IMAS Database reader and writer. The appearance of the 
        actor is configurable with dynamic properties.

        Dynamic properties:
         - pulse(str): pulse tuple
         - tille(str): Start button title
         - show_pulse(bool=True): Show pulse dialog
         - show_uri(bool=True): Show URI text edit
         - show_counter(bool)=False): starts counter on the button
         - show_log(bool=True): Show log window
         - show_button(bool=True): Show start button
        """
        super().__init__(parent)
        self.superclass = super()
        self._ids_names = []
        try:
            for name in imas.IDSFactory():
                self.add_signal(name, [object])
                self._ids_names.append(name)
        except:
            self._ids_names = IDS_NAMES
            for name in IDS_NAMES:
                self.add_signal(name, [object])  
        self._layout = QVBoxLayout(self) #: Sample vertical layout 
        self._layout.setSpacing(2)
        self._checkbox_enable = QCheckBox("Enable")
        self._checkbox_enable.setChecked(True)
        self._title = QLabel()
        self._title.setFrameStyle(QFrame.Box|QFrame.Sunken)
        self._title.setAlignment(Qt.AlignCenter)
        self._layout.addWidget(self._title)
        self._pulse_layout = self._create_pulse_layout() 
        self._layout.addWidget(self._pulse_layout)
        self._uri = QPlainTextEdit()
        self._uri.setMinimumHeight(100)
        self._uri.setPlaceholderText("This is IMAS URI")
        self._log = QPlainTextEdit()
        self._log.setMinimumHeight(100)
        self._log.setPlaceholderText("This is IMASDB log.")
        _vlayout = QVBoxLayout()
        _vlayout.setSpacing(2)
        _vlayout.setContentsMargins(0,0,0,0)
        _vlayout.addWidget(self._pulse_layout)
        _vlayout.addWidget(self._uri)
        _vlayout.addWidget(self._log)
        _qwidget = QWidget()
        _qwidget.setLayout(_vlayout)
        _scrollArea = QScrollArea()
        _scrollArea.setWidgetResizable(True)
        _scrollArea.setWidget(_qwidget)
        _scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        _scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self._layout.addWidget(_scrollArea)
        self._checkbox_enable.stateChanged.connect( \
                 lambda i: self.enable_self(True) if i else self.enable_self(False))
        self._checkbox_enable.hide()
        self._layout.addWidget(self._checkbox_enable)
        self._start_button = QPushButton("Start")
        self._layout.addWidget(self._start_button)
        self._start_button.clicked.connect(self.compute) 

        self._default_pulse: tuple = None
        """ tuple: Pulse default information in the form of 
        *(shot, run, occurrence, username, database, backend, data_version)* """
        self.dbentry = None
        """ imas.DBEntry: Database object."""
        self.put_ids_process = None
        self.ids_queue = None 
        """multiprocessing.Queue: IDS queue to put IDS objects."""
        self.occurrence = 0  #: IDS occurence for put.
        self.signal_names = [] 
        """list (str): List of signal names as a queue for emitting."""
        self._threads = [] # List hold thread objects

        self.counter = 0
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.recurring_timer)
        #self._start_button.clicked.connect(self.timer.start)

        QThreadPool.globalInstance().setExpiryTimeout(-1)

    @Slot(bool)
    def enable_self(self, b: bool) -> None:
        """|Slot| to enable/disable actor. 
        If received ``True``, the actor is enabled.
        If received ``False``, the actor is disabled.
        
        Args:
            b: Boolean to enable/disable self.
        """
        self._checkbox_enable.setChecked(b)
        self._start_button.setFlat(not b)
        for item in self._pulse_layout.children():
            item.setEnabled(b)
        self._log.setEnabled(b)
        self.blockSignals(not b)
        self._title.setAutoFillBackground(not b)
        

    def _show_or_hide(self, dynamic_property_name: str, widget: QWidget) -> bool:
        """ Depending on the dynamic_property_name the widget is shown or
            hiden.

            Args:
            dynamic_property_name: name of the dynamic property
            widget: widget to be shown or hiddenn
        """
        property = self.property(dynamic_property_name)
        if property is None:
            return None
        if property:
            widget.show()
            return True
        else:
            widget.hide()
        return False


    def event(self, received: QEvent) -> bool:
        if received.type() == QEvent.DynamicPropertyChange:
            name = bytes(received.propertyName()).decode()
            if name == 'title':
                self._title.setText(self.property('title'))
                return True
            if name == 'pulse':
                if not self._default_pulse:
                    self._default_pulse = self._eval_pulse_property()
                    self._set_pulse_layout(self._default_pulse)
                else:
                    self._set_pulse_layout(self._eval_pulse_property())
                return True
            if name == 'uri':
                self._uri.setPlainText(self.property('uri'))
                return True ### TODO            
            if name == 'button':
                self._start_button.setText(self.property('button'))
                return True
            if name == 'show_title':
                self._show_or_hide(name, self._title)
                return True
            if name == 'show_pulse':
                self._show_or_hide(name, self._pulse_layout)
                return True
            if name == 'show_uri':
                self._show_or_hide(name, self._uri)
                return True
            if name == 'show_log':
                self._show_or_hide(name, self._log)
                return True
            if name == 'show_button':
                self._show_or_hide(name, self._start_button)
                return True
            if name == 'show_enable':
                self._show_or_hide(name, self._checkbox_enable)
                return True              
        return self.superclass.event(received)


    def _create_pulse_layout(self):
        """Creates initial QGroupBox for pulse entry"""  

        groupBox_pulse = QGroupBox()
        
        gridLayout = QGridLayout(groupBox_pulse)
        gridLayout.setVerticalSpacing(1)
        gridLayout.setContentsMargins(0, 0, 0, 0)

        label_1 = QLabel(groupBox_pulse)
        label_1.setText("Shot")
        label_1.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        gridLayout.addWidget(label_1, 0, 0, 1, 1)
        lineEdit_shot = QLineEdit(groupBox_pulse)
        lineEdit_shot.setObjectName(u"lineEdit_shot")
        lineEdit_shot.setValidator(QIntValidator(1,99999999))
        lineEdit_shot.textEdited.connect(self._update_pulse_and_uri_property)
        gridLayout.addWidget(lineEdit_shot, 0, 1, 1, 1)

        label_2 = QLabel(groupBox_pulse)
        label_2.setText("Run")
        label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        gridLayout.addWidget(label_2, 1, 0, 1, 1)
        lineEdit_run = QLineEdit(groupBox_pulse)
        lineEdit_run.setObjectName(u"lineEdit_run")
        lineEdit_run.setValidator(QIntValidator(1,99999999))
        lineEdit_run.textEdited.connect(self._update_pulse_and_uri_property)
        gridLayout.addWidget(lineEdit_run, 1, 1, 1, 1)
        
        label_3 = QLabel(groupBox_pulse)
        label_3.setText("Occurrence")
        label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        gridLayout.addWidget(label_3, 2, 0, 1, 1)
        lineEdit_occurrence = QLineEdit(groupBox_pulse)
        lineEdit_occurrence.setObjectName(u"lineEdit_occurrence")
        lineEdit_occurrence.setValidator(QIntValidator(0,20))
        lineEdit_occurrence.textEdited.connect(self._update_pulse_and_uri_property)
        gridLayout.addWidget(lineEdit_occurrence, 2, 1, 1, 1)

        label_4 = QLabel(groupBox_pulse)
        label_4.setText("Username")
        label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        gridLayout.addWidget(label_4, 3, 0, 1, 1)
        lineEdit_username = QLineEdit(groupBox_pulse)
        lineEdit_username.setObjectName(u"lineEdit_username")
        lineEdit_username.textEdited.connect(self._update_pulse_and_uri_property)
        gridLayout.addWidget(lineEdit_username, 3, 1, 1, 1)

        label_5 = QLabel(groupBox_pulse)
        label_5.setText("Database")
        label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        gridLayout.addWidget(label_5, 4, 0, 1, 1)
        lineEdit_database = QLineEdit(groupBox_pulse)
        lineEdit_database.setObjectName(u"lineEdit_database")
        lineEdit_database.textEdited.connect(self._update_pulse_and_uri_property)
        gridLayout.addWidget(lineEdit_database, 4, 1, 1, 1)

        label_6 = QLabel(groupBox_pulse)
        label_6.setText("Backend")
        label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        gridLayout.addWidget(label_6, 5, 0, 1, 1)
        comboBox_backend = QComboBox(groupBox_pulse)
        comboBox_backend.setObjectName(u"comboBox_backend")
        try:
            for member in Backend:
                comboBox_backend.addItem(member.name)
            comboBox_backend.currentIndexChanged.connect(self._update_pulse_and_uri_property)
        except NameError:
            pass
        gridLayout.addWidget(comboBox_backend, 5, 1, 1, 1)

        label_7 = QLabel(groupBox_pulse)
        label_7.setText("Data Version")
        label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        gridLayout.addWidget(label_7, 6, 0, 1, 1)
        lineEdit_data_version = QLineEdit(groupBox_pulse)
        lineEdit_data_version.setObjectName(u"lineEdit_data_version")
        lineEdit_data_version.textEdited.connect(self._update_pulse_and_uri_property)
        gridLayout.addWidget(lineEdit_data_version, 6, 1, 1, 1)

        font_size = 9
        height = font_size+7
        font = QFont("Arial",font_size)
        for child in groupBox_pulse.children():
            try:
                child.setFont(font)
            except:
                pass
            try:
                child.setMaximumHeight(height)
            except:
                pass

        box_height = height*7
        groupBox_pulse.setGeometry(QRect(0, 0, 150, box_height))

        return groupBox_pulse


    def _set_pulse_layout(self, pulse: tuple):
        """Update pulse layout widgets from pulse tuple provided"""
        (shot, run, occurrence, username, database, backend, data_version) = pulse
        (shot2, run2, occurrence2, username2, database2, backend2, data_version2) = self._default_pulse
        for child in self._pulse_layout.children():
            with QSignalBlocker(child): # This won't re-emit signals such as currentIndexChanged()
                if child.objectName() == 'lineEdit_shot':    
                    if shot==shot2:
                        child.clear()
                        child.setPlaceholderText(str(shot2))
                    else:
                        child.setText(str(shot))
                elif child.objectName() == 'lineEdit_run':    
                    if run==run2:
                        child.clear()
                        child.setPlaceholderText(str(run2))
                    else:
                        child.setText(str(run))
                elif child.objectName() == 'lineEdit_occurrence':    
                    if occurrence==occurrence2:
                        child.clear()
                        child.setPlaceholderText(str(occurrence2))
                    else:
                        child.setText(str(occurrence))
                elif child.objectName() == 'lineEdit_username':  
                    if username==username2:
                        child.clear()
                        child.setPlaceholderText(username2)                     
                    else:
                        child.setText(username)
                elif child.objectName() == 'lineEdit_database': 
                    if database==database2:
                        child.clear()
                        child.setPlaceholderText(database2)                     
                    else:
                        child.setText(database)
                elif child.objectName() == 'comboBox_backend':
                    backend_name = Backend(backend).name
                    for i in range(child.count()):
                        if backend_name == child.itemText(i):
                            child.setCurrentIndex(i)
                            if backend_name == backend2:
                                child.setStyleSheet("color: grey;  background-color: white")                    
                            else:
                                child.setStyleSheet("color: black;  background-color: white")
                            break
                elif child.objectName() == 'lineEdit_data_version': 
                    if data_version == data_version2:
                        child.clear()
                        child.setPlaceholderText(data_version2)                     
                    else:
                        child.setText(data_version)

    def _update_pulse_and_uri_property(self):
        """Update pulse property from pulse layout widgets"""
        for child in self._pulse_layout.children():
            if child.objectName() == 'lineEdit_shot': 
                if child.text() != '':
                    shot = int(child.text()) 
                else: 
                    shot = int(child.placeholderText()) 
            elif child.objectName() == 'lineEdit_run':    
                if child.text() != '':
                    run = int(child.text()) 
                else: 
                    run = int(child.placeholderText()) 
            elif child.objectName() == 'lineEdit_occurrence':    
                if child.text() != '':
                    occurrence = int(child.text()) 
                else: 
                    occurrence = int(child.placeholderText()) 
            elif child.objectName() == 'lineEdit_username':  
                if child.text() != '':
                    username = child.text()
                else: 
                    username = child.placeholderText()
            elif child.objectName() == 'lineEdit_database': 
                if child.text() != '':
                    database = child.text()
                else: 
                    database = child.placeholderText()
            elif child.objectName() == 'comboBox_backend': 
                backend = Backend[child.currentText()].value
            elif child.objectName() == 'lineEdit_data_version':
                if child.text() != '':
                    data_version = child.text()
                else: 
                    data_version = child.placeholderText()

        _pulse = (shot, run, occurrence, username, database, backend, data_version)
        #self._set_pulse_layout(_pulse)
       
        with QSignalBlocker(self):
            self.setProperty('pulse', f'{str(_pulse)}')
            backend_name = Backend(backend).name.lower()
            uri = f'imas:{backend_name}?user={username};pulse={shot};run={run};database={database};version={data_version}'
            self._uri.setPlainText(uri)
            self.setProperty('uri', uri)


        
    def _eval_pulse_property(self) -> tuple:
        """Evaluate pulse property and return tuple."""
        (shot, run, occurrence, username, database, backend, data_version) = eval(self.property('pulse'))
        try:  # Convert name (e.g. 'HDF5' back to number
            backend = Backend[backend].value
        except:
            pass          
        return (shot, run, occurrence, username, database, backend, data_version)

    def get_state(self) -> ET.Element:
        """ Gets the current state of the widget, e.g. for saving the state 
            into the study file.
        """
        _state = ET.Element(self.objectName())
        _state.text = str(self._eval_pulse_property())
        return _state
        

    def set_state(self, _state: ET.Element):
        """ Sets the state of the widget, e.g. after loading the state 
            from the study file.

            Args:
                state(Element): |XML| study file
        """       
        (shot, run, occurrence, username, database, backend, data_version) = eval(_state.text)
        _pulse = (shot, run, occurrence, username, database, backend, data_version)
        self.setProperty('pulse', f'{_pulse}')
        self._set_pulse_layout(_pulse)
        self._log.appendPlainText(f'State loaded.')
        

    def minimumSizeHint(self):
        """ This property holds the recommended minimum size for the widget
        """
        return QSize(50, 50)

    def sizeHint(self):
        """ This property holds the recommended size for the widget
        """
        h = 270
        if not self.property('show_pulse'): 
            h -= 160
        return QSize(200, h)


    @Slot()
    def compute(self):
        """ |Slot| that starts processing by opening and reading database."""
        if self._checkbox_enable.isChecked():
            if not self.dbentry: 
                self.opendb()
                if self.property('start_counter'): 
                    self.timer.start()
                self.started.emit()
                if self.property('time_requested'):
                    self.get_slice()
                else:
                    self.get()

    @Slot()
    def opendb(self):
        """ |Slot| for opening existing IMAS database using :class:`_pulse` and 
        creating :class:`dbentry` for reading the database.
        """
        if self._checkbox_enable.isChecked():
            #_pulse = self._eval_pulse_property()
            #(shot, run, occurrence, username, database, backend, data_version) = _pulse
            #if username == '$USER' : username = getpass.getuser()
            #uri = imas.DBEntry.build_uri_from_legacy_parameters(backend,shot,run,database,username,data_version)
            uri = self.property('uri')
            try:
                self.dbentry = imas.DBEntry(uri, "r")
                self._status = 0
            except Exception as e:
                self._status = -2
                self._log.appendPlainText(f'Error: Opening pulse {e}')
            self._log.appendPlainText(f'Opening {uri}')

    def createdb(self):
        """ |Slot| for calling :class:`imasdb.put_ids_process` in a separate 
        process.
        """

        uri = self.property('uri')
        username = getpass.getuser()
        uri = uri.replace('$USER', username)

        #if not self.occurrence:
        #    (shot, run, occurrence, username, database, backend, data_version) = eval(self.property('pulse'))
        #    self.occurrence = occurrence

        self.ids_queue = multiprocessing.Queue()
        self.put_ids_process = multiprocessing.Process(target=put_ids_process,   
            args=(uri, self.occurrence, 'w', self.ids_queue))
        self.put_ids_process.start()
        self._log.appendPlainText(f'Creating {uri}:{self.occurrence}')
        

    def _append_log(self):
        msg = self._msg_queue.get()
        self._log.appendPlainText(msg)


    @Slot()
    def get(self):
        """ Prepares the list of names of all connected IDS signals and 
        initiates reading the corresponding IDSs from database.
        """
        if self._checkbox_enable.isChecked():
            self._title.setAutoFillBackground(True)
            self._title.setStyleSheet("background-color:rgb(255,255,150)")
            self._running_state = 1
            if not self.dbentry:
                self.opendb()
            if self._status < 0:
                self._title.setStyleSheet("")
                self._title.setAutoFillBackground(False)
                self._log.appendPlainText("\nError opening pulse.")
                self._running_state = 2
            else:
                metaObj = self.metaObject()
                for i in range(metaObj.methodCount()):      
                    meta_method = metaObj.method(i)
                    if meta_method.methodType() == QMetaMethod.Signal:         
                        signal_name = meta_method.name().data().decode('utf8')
                        if signal_name in self._ids_names:
                            if self.isSignalConnected(meta_method):
                                 self.signal_names.append(signal_name)
                self.pop_get() # Start get with first IDS in a list, if any
    
    def pop_get(self):
        """ Creates worker thread for reading IDS from database, for each 
        connected IDS signal, and closes the database when :class:`signal_names` 
        becomes ``empty``.
        """
        if len(self.signal_names):
            if self.property('time_requested'):
                time_requested = float(self.property('time_requested')) or 0
                interpolation_method = self.property('interpolation_method') or 1
                worker = Worker(self.dbentry.get_slice,self.signal_names.pop(0), time_requested, interpolation_method)
            else:
                worker = Worker(self.dbentry.get,self.signal_names.pop(0)) 
                # Any other args, kwargs are passed to the run function
            worker.signals.result.connect(self.emit_ids)
            # Execute
            self._threads.append(worker)
            QThreadPool.globalInstance().start(worker)
        else:
            if self.dbentry:
                self.dbentry.close()
                self.dbentry = None
                self._log.appendPlainText(f'Reading complete')
                self._title.setStyleSheet("")
                self._title.setAutoFillBackground(False)
            self.finished.emit()
            self._running_state = 2


    @Slot(object)
    def emit_ids(self, ids: object):
        """ |Slot| for receiving IDS object from worker thread and for emitting 
        IDS signal from main thread.
        
        Args:
            ids (object): IDS object to be emitted by the worker thread.
        """
        signal = getattr(self, ids.metadata.name)
        if self.property('time_requested'):
            if len(ids.time):
                self._log.appendPlainText(f'Emitting {ids.metadata.name}'+' slice at time= '+
                                     str(ids.time[0]))
            else:
                self._log.appendPlainText(f'Emitting {ids.metadata.name}'+' slice')     
        else:
            self._log.appendPlainText(f'Emitting {ids.metadata.name}')
        signal.emit(ids)
        self.pop_get()

    @Slot(float)
    @Slot(str)
    def _update_slice_time(self, value):
        self.setProperty('time_requested',float(value))

    @Slot(float)
    def set_time_requested(self, time_requested: float):
        """Setter for dynamic property time_requested."""
        self.setProperty("time_requested", time_requested)

    @Slot(int)
    def set_interpolation_method(self, interpolation_method: float):
        """Setter for dynamic property interpolation_method."""
        self.setProperty("interpolation_method", interpolation_method)

    @Slot()
    def get_slice(self):
        """ Emits all connected IDSs at given ``time_requested`` 
            and ``interpolation_method`` actor dynamic properties.
        """
        self.get()


    def partial_get(self, ids_name: str, data_path: str, occurrence: int = 0):
        """ Get partial IDS.

        Args:
            ids_name (str): Name of IDS to be read.
            data_path (str): Path of the IDS.
            occurrence (int): Occurrence of the IDS.
        """
        metaObj = self.metaObject()
        for i in range(metaObj.methodCount()):      
            meta_method = metaObj.method(i)
            #if meta_method.methodType() == QMetaMethod.Signal:         
            #    if meta_method.name().data().decode('utf8') == signal_name:
            #       print(self.isSignalConnected(meta_method))

    @Slot(int)
    def set_occurrence(self, occurrence:int):
        """Before put() IDS occurrence can be changed.

        Args: 
            occurrence: IDS occurence number (e.g. 0, 1, 2, ...)
        """
        self.occurrence = occurrence
        self.appendPlainText(f'Changed {occurrence =}')


    @Slot(object)
    def put(self, ids:object):
        """ |Slot| for puting received IDS into :class:`ids_queue`.

        Args:
            ids (object): IDS object to be put into Queue.
        """
        if self._checkbox_enable.isChecked():
            self._title.setAutoFillBackground(True)
            self._title.setStyleSheet("background-color:rgb(255,255,150)")
            self._running_state = 1
            if not self.put_ids_process:                
                self.createdb()
            self.ids_queue.put((ids, self.occurrence))
            if ids is not None:
                if hasattr(self, "time") and len(ids.time)==1:
                    self._log.appendPlainText(f"IDS {ids.metadata.name}" +
                        f"({self.occurrence}) slice at time " +
                        f"{ids.time[0]} s written.")
                else:
                    self._log.appendPlainText(f"IDS {ids.metadata.name}" +
                            f"({self.occurrence}) written.")

    @Slot()
    def closedb(self):
        """ |Slot| for closing the IMAS database in a worker thread 
             if opened by :class:`imasdb.put_ids_process`.
        """
        if not self._checkbox_enable.isChecked():
            return
        if not self.put_ids_process:
            return

        self.ids_queue.put((None, None)) # Ask child to exit

        try: # Close parent's Queue end and wait for its feeder thread to end
            self.ids_queue.close()
            self.ids_queue.cancel_join_thread()
        except Exception:
            pass

        if QApplication.platformName()=='offscreen':
            # Calling process.join() method in thread causes issues
            # with --no-gui so calling in main thread instead
            self.put_ids_process.join()
            self.emit_database_closed()
        else:
            # # multiprocess.Process in QRunnable does not
            # # return cleanly ?
            task = Worker(self.put_ids_process.join)
            task.signals.finished.connect(self.emit_database_closed)
            self._threads.append(task)
            QThreadPool.globalInstance().start(task)
            # or
            #self.put_ids_process.join()
            #self.emit_database_closed()


    @Slot()
    def emit_database_closed(self):
        """ |Slot| for destroying the Process object after database has been closed.
        Also, it emits :class:`_pulse` to be used in :class:`iplot.IPlot`.
        """
        self._title.setStyleSheet("")
        self._title.setAutoFillBackground(False)
        self.ids_queue = None
        self.put_ids_process = None
        self.emit_pulse.emit(str(self._eval_pulse_property()))
        self.finished.emit()
        self._running_state = 2

    @Slot(float)
    def time_in(self, time):
        pass

    def recurring_timer(self):
        self.counter +=1
        self._start_button.setText("Counter: %d" % self.counter)

    @Slot()
    def start_timer(self):
        if self._checkbox_enable.isChecked():
            self.timer.start()

if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    from PySide6.QtUiTools import loadUiType

    uiclass, baseclass = loadUiType("../plugins/pyside6-designer/imasdb.ui")

    class MainWindow(uiclass, baseclass):
        def __init__(self, parent=None):
            super().__init__(parent)
            try:
                self.setupUi(self)
            except AttributeError as e:
                print(f'Signal not available?: {e}')

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())