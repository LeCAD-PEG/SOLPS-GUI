from typing import Tuple, List
from PySide6.QtCore import (Qt, QSize, Property, Slot, Signal, QObject, QEvent, 
                            QRunnable, QThreadPool)
from PySide6.QtGui import QShowEvent, QStandardItemModel, QIcon, QAction
from PySide6.QtWidgets import (QFileDialog, QMessageBox, QVBoxLayout, QFrame, 
                                QLabel, QStyle)

import numpy as np
import os
import json
import getpass

import imas

from iplotlib.core import SignalXY, Canvas, PlotXY
from iplotlib.impl.matplotlib.qt.qtMatplotlibCanvas import QtMatplotlibCanvas
from iplotlib.qt.gui.iplotQtCanvas import IplotQtCanvas
from iplotlib.qt.gui.iplotQtPreferencesWindow import IplotQtPreferencesWindow, \
    QWidget
from iplotlib.qt.models.plotting import CanvasItem
#from iplotDataAccess.dataAccess import DataAccess, DataSource
#from imasAccess import IMASDataAccess
from iplotlib.interface import AccessHelper, IplotSignalAdapter, StatusInfo
from iplotlib.core.axis import Axis, LinearAxis
from iplotProcessing.core import BufferObject
from iplottoolbar import IPlotToolbar

from xml.dom.minidom import parseString
import xml.etree.ElementTree as ET

import queue


class GlobalQueue(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.queue = queue.Queue()
        self.threadpool = QThreadPool.globalInstance()

    def addTask(self, task):
        self.queue.put(task)
        if not self.threadpool.activeThreadCount():
            self.startWorker()

    def startWorker(self):
        self.worker = QueueWorker(self.queue)
        self.threadpool.start(self.worker)

class QueueWorker(QRunnable):
    def __init__(self, queue, parent=None):
        super().__init__(parent)
        self.queue = queue

    def run(self):
        while True:
            try:
                task = self.queue.get(block=False)
            except queue.Empty:
                break
            if task:
                task()
            self.queue.task_done()


class IPlot(QtMatplotlibCanvas):

    icon = ":/iter.org/pds/icons/gnuplot-icon.png"
    """The icon to be used by IPlot actor inside PDS Designer 
       and Study Explorer actor.
    """
    finished = Signal() 
    """Signal(): |Signal| for indicating that drawing the canvas has finished. 
    """
    log = Signal(str)
    _allowDynamicPropertyChange = False # Attribute to block drawing canvas 
                                        # during typing in Designer
    _trigger_canvas = False # Attribute to trigger canvas drawing when typing 
                            # in Designer finished
    _enabled = True 

    def __init__(self, parent=None):
        """ 
        IPlot widget based on the :class:`iplotlib` plotting library.

        """
        super().__init__(parent)

        self._model = QStandardItemModel(parent=self) # Model object used to 
        # extract information from Canvas
        self._parentItem = self._model.invisibleRootItem()
        self._cols = 1 # Initial number or columns in the plot array. 
        self._sample_signals = [] 
        """ list(iplotlib.core.SignalXY): List of sample plot signals."""
        self._sample_plots = []   
        """ list(list(iplotlib.core.PlotXY)): Array of plot objects created 
        from sample signals.  """    
        self._IDS_signals = []
        """ list(iplotlib.core.IplotSignalAdapter): List of IDS plot signals."""
        self._IDS_plots = []   
        """ list(list(iplotlib.core.PlotXY)): Array of IDS plot objects created 
        from IDS signals.  """
        self._pulse = None 
        """ tuple: Pulse information in the form of 
        *(shot, run, username, database, backend)*."""
        self._pulse_old = None # Control variable to check if pulse information 
                               # has changed.
        self._da = None #  DataAccess object.
        self.dbentry = None 
        """imas.DBEntry: Database object."""
        self._DBcreated = False # If MEMORY_BACKEND is not used
        self._pulseSignal = False # If pulse information was received from a 
                                  # signal
        self._canvas = None # the main IPlot canvas
        canvasItem = CanvasItem('IPlot Canvas')
        canvasItem.setEditable(False)
        self._parentItem.appendRow(canvasItem)
        self._signal_tag = '' # Any tag that can be appended to a signal
        self.slice_ids = False
        self.received_ids_name = ''
        self.isPlotting = False
        self.slice_idx = 0
        self.queue = GlobalQueue()
        
        

    def minimumSizeHint(self):
        return QSize(200, 200)

    def sizeHint(self):
        return QSize(200, 200)

    def set_canvas_data(self):
        """
        Refreshes model links for Preferences window.
        """
        idx = 0
        self._model.item(idx, 0).removeRows(0, \
                                        self._model.item(idx, 0).rowCount())
        self._model.item(idx, 0).setData(self._canvas, Qt.UserRole)
    
    @Slot()
    def preferences(self):
        """
        |Slot| for opening Preferences window.
        """
        self.set_canvas_data() # refresh model links for preferences
        self._prefWindow = IplotQtPreferencesWindow(self._model, parent=self)
        self._prefWindow.setWindowTitle('IPlot Preferences')
        root_index = self._prefWindow.treeView.rootIndex()
        self._prefWindow.treeView.expandRecursively(root_index)
        self._prefWindow.onApply.connect(self.update_canvas_preferences)
        self._prefWindow.onReset.connect(self.update_canvas_preferences)
        self._prefWindow.show()

    @Slot(QWidget)
    def toolbar(self, toolBar: IPlotToolbar):
        """
        |Slot| for connecting Toolbar widget to IPlot widget.
        
        Args:
            toolBar (IPlotToolbar): Toolbar widget to be connected.
        """
        toolBar.undoAction.triggered.connect(self.undo)
        toolBar.redoAction.triggered.connect(self.redo)
        toolBar.toolActivated.connect(lambda tool_name:
                [self.set_mouse_mode(tool_name)])
        #toolBar.redrawAction.triggered.connect(self.unfocus)
        #toolBar.detachAction.triggered.connect(self.detach)
        toolBar.removeAction(toolBar.detachAction)
        toolBar.removeAction(toolBar.redrawAction)
        toolBar.configureAction.triggered.connect(self.preferences)
        toolBar.exportAction.setText("Export Canvas")
        toolBar.importAction.setText("Import Canvas")
        toolBar.exportAction.triggered.connect(self.export_canvas)
        toolBar.importAction.triggered.connect(self.import_canvas)
        clearIcon = self.style().standardIcon(getattr(QStyle, 'SP_DialogDiscardButton'))
        clearAction = QAction(clearIcon, "Clear Canvas")
        toolBar.insertAction(toolBar.configureAction, clearAction)
        clearAction.triggered.connect(self.clear_plots)
        imageIcon = self.style().standardIcon(getattr(QStyle, 'SP_ArrowDown'))
        imageAction = QAction(imageIcon, "Export as image")
        toolBar.insertAction(toolBar.configureAction, imageAction)
        imageAction.triggered.connect(self._export_image)



    def export_json(self, file_path: os.PathLike):
        """
        Saves workspace in ``json`` file.
        
        Args:
            file_path (os.PathLike): Path to ``json`` file.
        """
        # self.statusBar().showMessage(f"Exporting {file_path} ..")
        try:
            with open(file_path, mode='w') as f:
                f.write(json.dumps(self.export_dict()))
        except Exception as e:
            box = QMessageBox()
            box.setIcon(QMessageBox.Critical)
            box.setText(
                f"Error {str(e)}: cannot export workspace to file: {file_path}")
            #logger.exception(e)
            box.exec_()
            #self.indicateReady()
            return

    def get_state(self) -> ET.Element:
        """ Gets the current state of the widget, e.g. for saving the state 
            into the study file.
        """
        _state = ET.Element(self.objectName()) # ElementTree.Element containing the state of the actor
        _canvas_ET = self.canvas_to_ET()
        if _canvas_ET:
            _state.append(_canvas_ET)
        return _state
        
        
    def set_state(self, _state: ET.Element):
        """ Sets the state of the widget, e.g. after loading the state 
            from the study file.

            Args: state (Element) – XML study file
        """
        self._canvas = self.ET_to_canvas(_state)
        self._allowDynamicPropertyChange = True
        if self._canvas:
            self._restore_vars()
            self.set_canvas(self._canvas)
        else:
            self._canvas = None


    def _restore_vars(self):
        # Restore internal variables
        self._IDS_plots = self._canvas.plots
        self.list_of_plot_id = []
        for i,col in enumerate(self._IDS_plots):
            for j,row in enumerate(col):
                for stack in row.signals.values():
                    for signal in stack:
                        self._IDS_signals.append(signal)
                self.list_of_plot_id.append(str(i+1)+'.'+str(j+1))        
            
    def export_xml(self, file_path: os.PathLike) -> None:
        """
        Saves workspace in ``xml`` file.
        
        Args:
            file_path (os.PathLike): Path to ``xml`` file.
        """
        _canvas_ET = self.canvas_to_ET()
        _xml = ET.tostring(_canvas_ET, encoding='unicode')
        _canvas_dom = parseString(_xml)
        xml = _canvas_dom.toprettyxml()
        try:
            with open(file_path, mode='w') as f:
                f.write(xml)
        except Exception as e:
            box = QMessageBox()
            box.setIcon(QMessageBox.Critical)
            box.setText(
                f"Error {str(e)}: cannot export canvas to file: {file_path}")
            box.exec_()
            return

    @Slot()
    def export_canvas(self):
        """ |Slot| for saving Canvas as XML.
        """
        file = QFileDialog.getSaveFileName(
            #self, "Save workspace as ..", filter='*.json') # dir=self._data_dir
            self, "Save workspace as ..", filter='*.xml') 
        if file and file[0]:
            #if not file[0].endswith('.json'):
            if not file[0].endswith('.xml'):
                #file_name = file[0] + '.json'
                file_name = file[0] + '.xml'
            else:
                file_name = file[0]
            #self.export_json(file_name)
            self.export_xml(file_name)
            self._data_dir = os.path.dirname(file_name)


    def _export_image(self):
        """ |Slot| for exporting Canvas as image.
        """
        file_name = QFileDialog.getSaveFileName(self,
            ("Export to image"), os.getcwd(), ("Files (*.png *.pdf *.svg)"))[0]
        if file_name:
            self._parser.figure.savefig(file_name)


    def import_json(self, json: object):
        """ Loads workspace from ``json`` file.
        
        Args:
            json (object): ``json`` file.
        """
        self.set_canvas(Canvas.from_json(json))

    def import_xml(self, xml: str):
        """ Loads workspace from ``xml`` file.
        
        Args:
            xml (str): ``xml`` file content.
        """
        _state = ET.parse(xml).getroot()
        self._canvas = self.ET_to_canvas(_state)
        self.set_canvas(self._canvas)
        self._restore_vars()


    @Slot()
    def import_canvas(self):
        """ Loads canvas from XML file.
        """
        file = QFileDialog.getOpenFileName(
            self, "Open a workspace ..", filter='*.xml') 
        if file and file[0]:
            self._data_dir = os.path.dirname(file[0])
            #self.import_json(file[0])
            self.import_xml(file[0])


    def update_canvas_preferences(self):
        """  Updates canvas preferences.
        """
        w = self #.currentWidget()
        with w.view_retainer():
            w.refresh()
        self._reset_axes('stack')
        self._prefWindow.postApplied()

    @Slot(str)
    def _add_tag_to_signal(self, tag: str):
        """A string to be appended to signal labels.
        """
        self._signal_tag = '-'+tag

    @Slot()
    def compute(self):
        """ Draws canvas and emits finished.
        """
        self.create_canvas()
        self.finished.emit()


    def create_sample_signal(self, i:int) -> SignalXY:
        """ Creates sample plot signal.

        Args:
            i (int): ID of sample signal

        Returns:
            Plot signal object.
        """
        x = np.linspace(0.0, 1.2, 50)
        y = (1 - x ** i) + 100 * (2 - x ** i) ** i
        s = SignalXY(label='signal_'+str(i), x_data=x, y_data=y)
        return s


    def create_sample_plots(self):
        """ Creates and populates :class:`PlotXY` object with 
        sample plot signals.
        """
        rows = self.property('rows') or 1
        cols = self.property('cols') or 1
        signals_available = len(self._sample_signals)
        if  signals_available < 2*rows*cols:
            for i in range(signals_available, 2*rows*cols):
                self._sample_signals.append(self.create_sample_signal(i))
        if len(self._sample_plots) < rows*cols or self._cols != cols:
            self._sample_plots = []
            for j in range(cols): 
                self._sample_plots.append([])
                for i in range(rows):                        
                    plot=PlotXY(col_span=2 if i==0 and j==0 and cols>1 else 1)
                    signal=self._sample_signals[2*(i+j*rows)]
                    plot.add_signal(signal, stack=i+1 if (i+j)%2 else i)
                    if cols > 1 or rows > 1: 
                        signal2=self._sample_signals[2*(i+j*rows)+1]
                        plot.add_signal(signal2, stack=i)
                    if i==0 and j==1 and cols>1:
                        self._sample_plots[j].append([])
                    else:
                        self._sample_plots[j].append(plot)

    def _empty_plots(self):
        """ Creates list of empty :class:`PlotXY` objects.
        """
        rows = self.property('rows') or 1
        cols = self.property('cols') or 1
        if cols<1: cols = 1
        try:
            ids_signals = self.property('ids_signals').split('\n')
            ids_signals = [ i.replace(' ','') for i in ids_signals ]
            ids_signals = [sig for sig in ids_signals if sig] # remove empty lines from count
            ids_signals = [ i.split(',') for i in ids_signals ]
        except: 
            ids_signals = [['signal', '1.1', '1', '1']]
        nrows = len(ids_signals)

        plots = [ [] for _ in range(cols) ]
        for i in range(cols): 
            for j in range(nrows):
                plots[i].append([])
        for i in range(nrows):
            plot_id = ids_signals[i][1].split('.')
            try: 
                stack_id = int(plot_id[2])
            except: 
                stack_id = 1            
            col = int(plot_id[0])-1
            row = int(plot_id[1])-1
            colspan = int(ids_signals[i][2])
            rowspan = int(ids_signals[i][3]) 
            plot = PlotXY(col_span=colspan,row_span=rowspan,
                        title=self.property(f'title({i+1})') or None)
            signal= SignalXY(label='_none', x_data=[0], y_data=[0])
            plot.add_signal(signal, stack=stack_id)
            plots[col][row] = plot

        return plots


    # def connect_pulse_to_imas_uda_database(self):
    #     """ Connects to DB on persistent storage or in memory 
    #         backend. It uses information from :class:`_pulse` described as 
    #         string tuple of ``(shot, run, username, database, backend)``.
    #     """
    #     (shot, run, occurrence, username, database, backend) = self._pulse
    #     if backend == imas.imasdef.MEMORY_BACKEND:
    #         backend = 'MEMORY'
    #         self._pulse = (shot, run, occurrence, username, database, backend)
    #     if username == '$USER' : username = getpass.getuser()
    #     self.pulse = f"{shot}/{run}" # used for loading signals
    #     self._da = DataAccess()
    #     AccessHelper.da = self._da
    #     self._dataS = DataSource(name='imas')
    #     self._dataS.dtype = 'IMAS_UDA'
    #     self._da.addDataSource(dataS=self._dataS)
    #     self._dataS.setConnectionString(f'database={database},path={username},backend={backend}')
    #     if not self._dataS.connected: 
    #         self._dataS.connect()
    #     self._pulse_old = self._pulse
    #     print('IMAS UDA connected')


    def connect_pulse_to_imas_database(self):
        """ Connects to DB on persistent storage or in memory backend.
        """
        if not self._da:
            (shot, run, occurrence, username, database, backend) = self._pulse
            if backend == imas.imasdef.MDSPLUS_BACKEND:
                backend = 'MDSPLUS'
            elif backend == imas.imasdef.MEMORY_BACKEND:
                backend = 'MEMORY'
            elif backend == imas.imasdef.HDF5_BACKEND:
                backend = 'HDF5'

            self.pulse = f"{shot}/{run}" # used for loading signals
            self._da = IMASDataAccess()
            connectionString=f"database={database},path={username},"+\
                             f"backend={backend},pulseIdent={self.pulse}"
            self._da.connectSource(connectionString=connectionString) 
            AccessHelper.da = self._da
        elif not self._da.isconnected():
            self._da.connect()
            

    def create_imas_memory_database(self) -> int:
        """ Creates database in memory using information from :class:`_pulse`.
        """
        shot = id(self) % 100000 # To get unique DB in memory  for our use
        run = 1
        occurrence = 0
        username = getpass.getuser()
        database = 'iter_memory'
        backend = imas.imasdef.MEMORY_BACKEND
        status = -1
        self.dbentry = imas.DBEntry(backend, database, shot, run, username)
        try:
            status, self.idx = self.dbentry.create()
        except Exception as e:
            #print('========= memory db WAS NOT created ===============')
            print(f'{e}')
        if status == 0:
            #print('memory db created')
            self._pulse = (shot, run, occurrence, username, database, backend)
        return status


    def load_signals(self, signals:List[str]) -> List[IplotSignalAdapter]:
        """ Creates :class:`IplotSignalAdapter` objects from list
            of signal names. Also, it initiates connection to database.

            Args:
                signals (list(str)): Signal names  
                    extracted from IPlot widget dynamic property *ids_signals*.

            Returns:
                List of signals to be shown by :class:`create_canvas()`.
        """
        if self._DBcreated == False: #if the MEMORY_BACKEND is not used
            if self.property('pulse') and self._pulseSignal == False:
                self._pulse = eval(self.property('pulse'))
        if self._pulse != self._pulse_old or not self._da.isconnected():
            self.connect_pulse_to_imas_database()
    
        sigs = []
        for i in range(len(signals)):  
            #print("Loading: ",signals[i])
            try: color = tuple([float(i)/255 for i in \
                list(self.property('color('+str(i+1)+')').toTuple())])
            except: color = None
            signal = IplotSignalAdapter(
                        # data_source=self._dataS.name, 
                        data_source=None, 
                        name=signals[i], 
                        label = self.property('label('+str(i+1)+')') or None,
                        line_style = self.property('line_style('+str(i+1)+')') or None,
                        line_size  = self.property('line_size('+str(i+1)+')') or None,
                        marker = self.property('marker('+str(i+1)+')') or None,
                        marker_size = self.property('marker_size('+str(i+1)+')') or None,
                        color =  color,
                        ts_start = self.property('ts_start('+str(i+1)+')') or None, 
                        ts_end = self.property('ts_end('+str(i+1)+')') or None,
                        pulse_nb = self.pulse, 
                        processing_enabled = True,
                        data_access_enabled = True)#,
                        #plot_type=PlotXY)
            #signal._fetch_data()
            sigs.append(signal)
        return sigs


    def create_IDS_plots(self):
        """ Creates the IDS plot array to be used by 
            :class:`iplotlib.core.Canvas`. It places
            each element of the list returned by :class:`load_signals` into the 
            corresponding row and column supplied by the IPlot widget dynamic 
            property *ids_signals*.
        """
        cols = self.property('cols') or 1
        if cols<1: cols = 1
        try:
                ids_signals = self.property('ids_signals').split('\n')
                ids_signals = [ i.replace(' ','') for i in ids_signals ]
                ids_signals = [sig for sig in ids_signals if sig] # remove empty lines from count
                ids_signals = [ i.split(',') for i in ids_signals ]
        except: ids_signals = []
        nrows = len(ids_signals)

        if len(self._IDS_signals)==0 or not self._DBcreated  or self.slice_ids:
            # update nrows from ids_signals
            new_nrows = 0
            for i in range(nrows):
                rows_ids = int(ids_signals[i][1].split('.')[1])
                new_nrows = max([new_nrows,rows_ids])
            # create the plots and stacks
            self.list_of_plot_id = []
            self._IDS_plots = [ [] for _ in range(cols) ]
            for i in range(cols): 
                for j in range(new_nrows):
                    self._IDS_plots[i].append([])

        # load the signals:
        sig_names_avail = []
        sig_names = [ ids_signals[i][0] for i in range(nrows) ]

        if self._DBcreated == True: # if memory backend is being used
                # load only the signals for which the ids has been put into memory DB
                idx = [i for i,x in enumerate(sig_names) \
                       if x.split('/')[0] == self.received_ids_name]
                sig_names_avail = [sig_names[x] for x in idx]
        else:
            idx = [i for i,x in enumerate(sig_names)]
            sig_names_avail = sig_names

        if len(sig_names_avail) > 0:
            _IDS_signals = self.load_signals(sig_names_avail)
            self._pulse_old = self._pulse
            if self._DBcreated: 
                # if memory backend, append sender into name and other tag
                for signal in _IDS_signals:
                    signal.label = signal.label+'-'+str(self._sender)+self._signal_tag

            if self._DBcreated and not self.slice_ids: 
                for x in _IDS_signals:
                    self._IDS_signals.append(x)
            else:
                self._IDS_signals = _IDS_signals

            labels = [x.label for x in self._IDS_signals]

            # check if the signal properties have changed in designer
            for i in range(len(self._IDS_signals)):
                try: 
                    color = self.property('color('+str(i+1)+')').toTuple()
                    color = list(color)
                    color = [float(i)/255 for i in color]
                    color = tuple(color)
                except: color = None
                self._IDS_signals[i].color = color
                self._IDS_signals[i].line_style = self.property('line_style('+str(i+1)+')') or None
                self._IDS_signals[i].line_size = self.property('line_size('+str(i+1)+')') or None
                self._IDS_signals[i].marker = self.property('marker('+str(i+1)+')') or None
                self._IDS_signals[i].marker_size = self.property('marker_size('+str(i+1)+')') or None
            
            for j in range(len(_IDS_signals)):
                i = idx[j]
                plot_id = ids_signals[i][1].split('.')
                try: stack_id = int(plot_id[2])
                except: stack_id = 1            
                col = int(plot_id[0])-1
                row = int(plot_id[1])-1
                plot_id = plot_id[0]+'.'+plot_id[1]
                colspan = int(ids_signals[i][2])
                rowspan = int(ids_signals[i][3]) 
                if plot_id not in self.list_of_plot_id:
                    self.list_of_plot_id.append(plot_id)
                    new_plot = PlotXY(col_span=colspan,row_span=rowspan,
                        title=self.property(f'title({i+1})') or None)
                    self._IDS_plots[col][row] = new_plot
                self._IDS_plots[col][row].add_signal(_IDS_signals[j], stack=stack_id)

    @Slot()
    def clear_plots(self):
        """Removes all signals from plots.
        """
        self._IDS_signals = []
        self._IDS_plots = []
        if self._canvas is None:
            self.create_canvas()
        self._canvas.plots = self._empty_plots()
        self._canvas.legend = False
        self.set_canvas(self._canvas)


    @Slot(str)
    def plot_pulse(self, pulse:str):
        """ |Slot| for receiving pulse information and for initiating plotting.

            Args: 
                pulse (str): Pulse information in the form of 
                    *(shot, run, username, database, backend)*.
                    If ``username`` is ``$USER`` then current user's database
                    is used.
        """
        if self._DBcreated == False:
            (shot, run, occurrence, username, database, backend) = eval(pulse)
            if backend == imas.imasdef.MDSPLUS_BACKEND:
                backend = 'MDSPLUS'
            self._pulse = (shot, run, occurrence, username, database, backend)
            self._IDS_signals = []
            self._pulseSignal = True
            self.create_canvas()


    @Slot(object)
    def plot_ids(self, ids:object):
        """ |Slot| for receiving IDS object (in memory). Creates 
            or opens database, writes IDS into database and initializes plotting.
            
            Args:
                ids (object): IDS object, e.g. the result of a simulation code.
        """
        if not self._enabled:
            return
        if ids is None:
            return
        self.received_ids_name = ids.__name__
        if self._DBcreated == False:
            statusdb = self.create_imas_memory_database()
            if statusdb == 0:
                self._DBcreated = True
                self.connect_pulse_to_imas_database()
                self._pulseSignal = False 
                self._IDS_signals = []

        if self._DBcreated == True:
            self._sender = self.sender().objectName()
            # Save ids only if it exists in the list of signals to be plotted
            ids_signals = self.property('ids_signals').split('\n')
            ids_signals = [ i.replace(' ','') for i in ids_signals ]
            ids_signals = [sig for sig in ids_signals if sig] # remove empty lines from count
            ids_names = [ i.split(',')[0].split('/')[0] for i in ids_signals ]
            if ids.__name__ in ids_names:
                if len(ids.time) == 1:
                    self.slice_ids = True
                    self.dbentry.put_slice(ids)
                    if self._IDS_plots is None:
                        self.create_canvas()
                    if self.slice_idx == 10:
                        #self.queue.addTask(self.plot_ids_task) # plot using threaded queue
                        #self.queue.addTask(self.ids_streamer) # freezes completely
                        self.ids_streamer() # run in main thread, optimizes memory
                        self.slice_idx = 0
                    self.slice_idx += 1

                else:
                    self.dbentry.put(ids)
                    self.slice_ids = False
                    self.plot_ids_task() # blocking, with labels

        


    def ids_streamer(self):
   
        # load the signals:
        ids_signals = self.property('ids_signals').split('\n')
        ids_signals = [ i.replace(' ','') for i in ids_signals ]
        ids_signals = [sig for sig in ids_signals if sig] # remove empty lines from count
        ids_signals = [ i.split(',') for i in ids_signals ]
        nrows = len(ids_signals)
        sig_names_avail = []
        sig_names = [ ids_signals[i][0] for i in range(nrows) ]
        if self._DBcreated == True: # if memory backend is being used
            # load only the signals for which the ids has been put into memory DB
            idx = [i for i,x in enumerate(sig_names) \
                   if x.split('/')[0] == self.received_ids_name]
            sig_names_avail = [sig_names[x] for x in idx]

        if len(sig_names_avail) > 0:
            loaded_signals = self.load_signals(sig_names_avail)

        for dobj in loaded_signals:
            data = dobj.get_data()
            dobj.set_data(data)
            if len(data[1])>0:
                for signal in self._IDS_signals:
                    if (hasattr(signal, 'inject_external')
                        and signal.name == dobj.name):
                        result = dict(alias_map={
                                    'time': {'idx': 0, 'independent': True},
                                    'data': {'idx': 1}
                                    },
                                  d0=dobj.x_data,
                                  d1=dobj.y_data,
                                  d2=dobj.z_data,
                                  d0_unit=dobj.x_data.unit,
                                  d1_unit=dobj.y_data.unit,
                                  d2_unit=dobj.z_data.unit)
                        signal.inject_external(append=True, **result)
            signal.data_access_enabled = False
        self._reset_axes()
        self.set_canvas(self._canvas)
        self.dbentry.delete_data(self.received_ids_name)


    def handle_output(self, text):
        # Emit the captured output
        if isinstance(text, bytes):
            text = text.decode('utf-8')
        self.log.emit(text)

    def plot_ids_task(self):
        """
        """
        self.create_canvas()
        # prevent current signals to be overwritten by future signals
        for sig in self._IDS_signals:
            sig.data_access_enabled = False
        self._reset_axes()    
        

    def _reset_axes(self, axes='xy'):       
        for col in self._canvas.plots:
            for row in col:
                if hasattr(row,'__dict__'):
                    x_axis = row.__dict__['axes'][0]
                    y_axis = row.__dict__['axes'][1]
                    if 'x' in axes:
                        x_axis.begin = None
                        x_axis.end = None
                    if 'y' in axes:
                        y_axis.begin = None
                        y_axis.end = None
                    if axes=='stack':
                        if len(row.signals.values())>1:
                            y_axis.begin = None
                            y_axis.end = None

    @Slot()
    def create_canvas(self):
        """ |Slot| for refreshing plot signals, creating canvas and plotting.            
        """
        #print('create_canvas')
        # awk -F '[:=]|, ' '{for(i=1;i<NF;i+=3)print $i"=self.property('"'"'"$i"""'"'"') or"$(i+2)","}' header.txt
        # Determine plot type 
        if self._pulse or self.property('pulse'):
            self.create_IDS_plots()            
        else:
            self._IDS_plots = None
            if self.property('start_empty') and self.property('start_empty')==True:
                self._sample_plots = self._empty_plots()
            else:
                self.create_sample_plots()
            plrows = []
            plcols = []
            
        # Determine max of rows and cols from created IDS plots
        if self._IDS_plots is not None:
            plrows = 0
            try:
                plcols = len(self._IDS_plots)
            except:
                plcols = []
            try:
                for i in self._IDS_plots:
                    plrows = max([plrows,len(i)])
                if isinstance(self.property('rows'),int):
                    plrows = max([plrows,self.property('rows')])
            except:
                plrows = []
        
        self._canvas = Canvas(
            rows=plrows or self.property('rows') or 1,
            cols=plcols or self.property('cols') or 1,
            title=self.property('title') or None,
            font_size=self.property('font_size') or None,
            font_color=self.property('font_color') or None,
            line_style=self.property('line_style') or None,
            line_size=self.property('line_size') or None,
            marker=self.property('marker') or None,
            marker_size=self.property('marker_size') or None,
            step=self.property('step') or None,
            hi_precision_data=self.property('hi_precision_data') or False,
            dec_samples=self.property('dec_samples') or 1000,
            legend=self.property('legend') or True, 
            grid=self.property('grid') or False,
            mouse_mode=self.property('mouse_mode') or 'MM_SELECT',
            plots=self._IDS_plots or self._sample_plots,
            crosshair_enabled=self.property('crosshair_enabled') or False,
            crosshair_color=self.property('crosshair_color') or 'red',
            crosshair_line_width=self.property('crosshair_line_width') or 1,
            crosshair_horizontal=self.property('crosshair_horizontal') or True,
            crosshair_vertical=self.property('crosshair_vertical') or True,
            crosshair_per_plot=self.property('crosshair_per_plot') or False,
            streaming=self.property('streaming') or False,
            shared_x_axis=self.property('shared_x_axis') or False,
            autoscale=self.property('autoscale') or True,
            auto_refresh=self.property('auto_refresh') or 0,
            _type=self.property('_type') or None
            )
        self._mpl_renderer.toolbar = None
        if self._sample_plots == self._empty_plots():
            self._canvas.legend = False
        self._canvas.grid = True
        try:
            self.set_canvas(self._canvas)
        except:
            pass
        
        # To prevent creating canvas on showEvent if plot signal
        # has been received before showEvent. It would result in double-plot.
        self._allowDynamicPropertyChange = True
    
    def dict_to_ET(self, tag: str, d):
        """Converts dictionary object to ElementTree object.

        Args:
                tag (str): Character string to be used as tag for the 
                            newly created ElementTree object.
                d: The dictionary object to be converted into ElementTree or a list of objects.
        """
        elem= ET.Element(tag,{})
        if isinstance(d,list):
            if all(isinstance(x, (int, float)) for x in d):
                        # if list is a 1D array of values (e.g. datapoints), 
                        # return array instead of separate elements
                        elem.text = str(d)
            else:
                for item in d:
                    elem.append(self.dict_to_ET('item',item))
                elem.set('type','list')
        else:
            for key, val in d.items():
                if key.isnumeric():
                    key = 'n'+key
                if isinstance(val,list):
                    child = self.dict_to_ET(key,val)
                    child.set('type','list')
                elif isinstance(val,dict):
                    child = self.dict_to_ET(key, val)
                    child.set('type','dict')
                else:
                    child= ET.Element(key, {'type':type(val).__name__})
                    child.text= str(val)
                elem.append(child)
        return elem



    def canvas_to_ET(self) -> ET.Element:
        """ Converts Canvas object to ET
        """
        try:
            canvas_json = json.loads(json.dumps(self._canvas, default=lambda x: x.__dict__))
        except:
            return None
        if canvas_json:
            canvas_ET = self.dict_to_ET('Canvas', canvas_json)
            # Find the IplotSignalAdapter entries to inject the datapoints
            idx_checked = []
            parents = list(canvas_ET.iter(tag='item'))
            for parent in parents:
                child = parent.find('label')
                if ET.iselement(child):
                    # Match the ET entry with the IplotSignalAdapter object
                    for i,sig in enumerate(self._IDS_signals):
                        if sig.label == child.text and i not in idx_checked:
                            data_json = json.loads(json.dumps(sig.data_store, cls=_NumpyEncoder))
                            data_ET = self.dict_to_ET('data_store', data_json)
                            data_ET.set('type','list')
                            parent.append(data_ET)
                            idx_checked.append(i)
                            break
            return canvas_ET
        else:
            return None
            
        
    def etree_to_dict(self, t):
        """Converts ElementTree object to dictionary object.

        Args:
                t : The ElementTree object to be converted into dictionary object.
        """
        if type(t) is ET.ElementTree: 
            return self.etree_to_dict(t.getroot())
        if 'type' in t.attrib and t.attrib['type']=='list': # if Element is a list:
            t_list = []
            for e in t:
                t_list.append(self.etree_to_dict(e))
            if len(t_list)==0 and t.text:
                t_list = eval(t.text)
            parent_dict = t_list
        elif t.tag=='item' and t.text.strip('\n\t') != '': # array of values
            t_list = []
            if all(isinstance(e, (int, float)) for e in eval(t.text.strip('\n\t'))):
                # if list is a 1D array of values (e.g. datapoints), 
                # return array instead of separate elements
                t_list = eval(t.text)
                parent_dict = t_list
        else:
            # if all elements in tree have different tag:
            # Warning: if child elements do not have different tag,
            # they will be overwritten
            child_dict = {}
            for e in t:
                child_dict[e.tag] = self.etree_to_dict(e)
            if isinstance(t.text, str):
                t.text = t.text.strip('\n\t')
            parent_dict = {**t.attrib, '#text': t.text, **child_dict}
        return parent_dict


    def ET_to_canvas(self, _state: ET.Element) -> object:
        """ Creates and returns Canvas class object from ElementTree
        """
        def _process_value(v): 
            # Process any value, cast to type. Returns any type.
            if isinstance(v, dict):
                value = v['#text']
                if '_type'in v.keys():
                    nv = cast_dict(v) # class object
                elif 'type' in v.keys():
                    vtype = v['type']
                    if vtype=='bool' and value == 'True':
                        nv = True
                    elif vtype=='bool' and value == 'False':
                        nv = False
                    elif vtype=='NoneType' and value == 'None':
                        nv = None
                    elif vtype=='str':
                        if value == 'None':
                            nv = ''
                        else:
                            nv = value
                    elif vtype=='dict':
                        nv = cast_dict(v)
                    else:
                        nv = eval(v['type']+'('+value+')')
                else: 
                    if len(v.keys())==1 and '#text' in v.keys(): # array in text
                        if value == '[]':
                            nv = []
                        else:
                            nv = eval(v)
                    else: # still a dictionary
                        nv = cast_dict(v) 
            elif isinstance(v,list):
                if all(isinstance(x, (int, float)) for x in v):
                    # if list is a 1D array of values (e.g. datapoints), 
                    # return array instead of separate elements
                    nv = v 
                else:
                    nv = []
                    for item in v:
                        nv.append(_process_value(item))
            return nv

        def cast_dict(some_dict: dict) -> object:                
            # Process dictionary recursively. 
            # Returns re-casted and filtered new dictionary or class object
            new_dict = {} # the new dictionary to be returned
            if 'type' in some_dict.keys() and some_dict['type']=='dict': 
                del some_dict['type'] # it has no value, remove
            if '#text' in some_dict.keys():
                del some_dict['#text'] # it has no value, remove
            for k,v in some_dict.items():
                # numeric keys were appended with "n" during XML-isation
                if k[0]=='n' and k[1:].isnumeric(): 
                    k = k[1:] # removing "n"
                new_dict[k] = _process_value(v)
            # color key must be recast as tuple
            if 'color' in new_dict.keys() and isinstance(new_dict['color'],list):
                new_dict['color'] = tuple(new_dict['color'])
            # StatusInfo class detected as dictionary instead of class,
            # fixing and returnig object of class
            if 'stage' in new_dict.keys(): 
                del new_dict['sep'] # inherited, key not needed
                #del new_dict['#text'] # it has no value, remove
                class_object = StatusInfo(**new_dict)
                return class_object
            if '_type' in new_dict.keys(): # if the dictionary entry is a class, return object of class
                class_name = new_dict['_type']
                class_object = eval(class_name.split('.')[-1]+'()')
                class_object_items = class_object.__dict__.items()
                if 'IplotSignalAdapter' in class_name:
                    del some_dict['data_store'] # duplicate, free memory
                    data_store = new_dict.pop('data_store') # not accepted during init(), injected later
                    # inherited parameters not accepted by __init__() are removed
                    del new_dict['_data']
                    del new_dict['_alias_map']
                    del new_dict['_local_env']
                    # # x,y,z_data members hold unit information
                    # # will be added after object construction
                    x_data = new_dict.pop('x_data')
                    y_data = new_dict.pop('y_data')
                    z_data = new_dict.pop('z_data')
                    del new_dict['_access_md5sum']
                if len(class_object_items) >= len(new_dict): # if class parameters are sufficient
                    class_object = eval(class_name.split('.')[-1]+'(**new_dict)') # create class object
                    # Reset axis limits otherwise all stacked plots will have the same Y-axis limits
                    # Same issue identified in IPlotToolbar.
                    if 'LinearAxis' in class_name:
                        for k in new_dict.keys():
                            if 'begin'in k or 'end' in k:
                                exec('class_object.'+k+'= None')
                    if 'IplotSignalAdapter' in class_name:
                        # Prepare the datapoints 
                        xx_data = BufferObject(np.asarray(data_store[0]))
                        yy_data = BufferObject(np.asarray(data_store[1]))
                        zz_data = BufferObject(np.asarray(data_store[2]))
                        # Add the units
                        xx_data.unit = x_data['unit']
                        yy_data.unit = y_data['unit']
                        zz_data.unit = z_data['unit']
                        # Finally, inject the datapoints
                        class_object.data_store[0] = xx_data
                        class_object.data_store[1] = yy_data
                        class_object.data_store[2] = zz_data
                        # Reasign the StatusInfo object which was defaulted during creation 
                        # of IplotSignalAdapter object
                        class_object.status_info = new_dict['status_info']
                        # To prevent requesting data with AccessHelper
                        class_object.data_access_enabled = False
                else:
                    print("ERROR: class object [", class_name ,"] parameter mismatch")
                    print("ERROR: expected ", len(class_object_items) ," members,")
                    print(class_object_items)
                    print("ERROR: received ", len(some_dict) ," members.")
                    print(some_dict.keys())
                return class_object
            else:
                return new_dict
        canvas_dict = self.etree_to_dict(_state)
        if 'Canvas' in canvas_dict.keys():
            if canvas_dict['Canvas']['_type']['#text'] == 'iplotlib.core.canvas.Canvas':
                canvas_dict = canvas_dict['Canvas']
        elif '_type' in canvas_dict.keys():
            pass
        else:
            # print('Error: xml not valid canvas')
            pass
        return cast_dict(canvas_dict)


    def event(self, event: QEvent):
        """Overloaded event.
        """
        if event.type() == QEvent.Show: 
            if self._allowDynamicPropertyChange == False:
                self.create_canvas()
        return super().event(event)


class _NumpyEncoder(json.JSONEncoder):
    # Subclassed JSON encoder to serialize complex types, e.g. numpy types.
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    from PySide6.QtUiTools import loadUiType

    uiclass, baseclass = loadUiType("../designer/iplot.ui")

    class MainWindow(uiclass, baseclass):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
