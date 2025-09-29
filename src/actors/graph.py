from itertools import filterfalse
from PySide6.QtCore import (Qt, QSize, Property, Slot, Signal, QObject, QRunnable, QThreadPool,
                            QEvent, QTimer)
from PySide6.QtWidgets import (QWidget, QGridLayout, QSlider, QCheckBox, QGroupBox,
                               QHBoxLayout, QVBoxLayout, QGraphicsPathItem, QPushButton, QLineEdit,
                               QGraphicsProxyWidget, QLabel, QFileDialog)
from PySide6.QtGui import (QPalette, QBrush, QColor, QDoubleValidator)

import pyqtgraph as pg
pg.setConfigOptions(antialias=True)

import numpy as np
from math import sin, cos, pi
import re
import imas
import os, sys
import queue
from copy import deepcopy
import getpass
import xml.etree.ElementTree as ET
from xml.dom import minidom
from xml.dom.minidom import Node


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


class MyViewBox(pg.ViewBox):
    def __init__(self, parent=None, invert_x_axis=False, invert_y_axis=False):
        super().__init__(parent=parent)
        self.setMouseMode(pg.ViewBox.RectMode)
        self.setAutoVisible(x=True, y=True)
        if invert_x_axis:
            self.invertX(True)
        if invert_y_axis:
            self.invertY(True)


class Graph(QWidget):

    log = Signal(str)
    """ Signal(int): |Signal| for emitting worker log. """
    slice_four_points = Signal(list)
    """ Signal(list): |Signal| for emitting positions of the four points for plasma shaping. """
    remove_slice = Signal(tuple)
    insert_slice = Signal(float)
    index_time = Signal(tuple)
    equilibrium = Signal(object) # IDS created from XML
    scenplint_xml = Signal(str) # Signal for emitting updated Scenplint input XML 
    connect_to_pulse_editor = Signal(object) # Signal for emitting self to connect to pulse editor widget


    def __init__(self, parent=None):
        """ Initialize layout, canvas and figure.
        """
        super().__init__(parent)

        ## Switch to using transparent background and black foreground
        pg.setConfigOption('background', 'w') # or (r,g,b,alpha)
        pg.setConfigOption('foreground', 'k')

        self._viewBox = MyViewBox()
        self._plotWidget = pg.PlotWidget(viewBox=self._viewBox)

        self.plotItem = self._plotWidget.plotItem # convenience variable
        self.plotItem.setTitle(" ")
        self.plotItems = None

        self._layout = QVBoxLayout(self)
        self._layout.setSpacing(2)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._plotWidget)
        
        self._shotrun = 202200125
        self._name = ''
        self._column_name = "IP"

        axis_pen = pg.mkPen(color='#333')
        self._units = 'A'
        self._unitPrefix = 'k'
        self._XLabel = 'Time'
        self._XUnits = 's'
        self._XUnitPrefix = ''
        ait = pg.AxisItem('top', showValues=False, pen=axis_pen)
        air = pg.AxisItem('right', showValues=False, pen=axis_pen)
        ail = pg.AxisItem('left',  showValues=True, pen=axis_pen)
        aib = pg.AxisItem('bottom', showValues=True, pen=axis_pen,
                text=self._XLabel, units=self._XUnits,
                unitPrefix=self._XUnitPrefix)
        aib.showLabel(True)
        text_pen = pg.mkPen(color='k')
        aib.setTextPen(text_pen)
        ail.setTextPen(text_pen)

        self.plotItem.setAxisItems(axisItems={'top': ait, 'right': air,
                                              'left': ail, 'bottom': aib})
        if len(self._name):
            self.plotItem.setLabel('left', text=self._name,
                    units=self._units, unitPrefix=self._unitPrefix)
        else:
            self.plotItem.setLabel('left', text=self._column_name,
                    units=self._units, unitPrefix=self._unitPrefix)

        self.plots= {'equilibrium':[], 'wall':[], 'pf_active':[], 'pf_passive':[]}
        self.plots['shaping'] = [] # plots for plasma shaping
        
        self.idslist = {}
        self._plot_init = True
        self._show_legend = True
        self._line_colors = [[55,126,184], # blue
                             [255,127,0],  # orange
                             [228,26,28],  # red
                             [77,175,74],  # green
                             [152,78,163], # purple
                             [200,200,51], # yellow
                             [166,86,40],[247,129,191]]
        self._ylabels = None
        self._xlabels = None
        self._link_xaxis = False
        self._add_vertical_line = False
        self._selected_point = None
        self._default_brush = pg.mkBrush(150, 150, 170) # grey
        self._select_brush = pg.mkBrush(250,100,100) # orange
        self._mode = QLabel(text='select')
        self.legend = None
        self._old_table = None # ElementTree object containing initial waveforms from input XML
        self._new_table = None # ElementTree object containing modified waveforms from GraphItem
        self.sig_names = None # list of signal names to be plotted

        self.imas_dd_units = imas.dd_units.DataDictionaryUnits()

        self.queue = GlobalQueue()

        self.root_scenplint = None # ElementTree object from Scenplint input XML
        self.root_transmak = None # ElementTree object from Transmak input XML

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.prepare_xml)

        self._connected = False # Control variable, if self is connected to other widget

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(-1, -1)
        self.slider.setVisible(False)
        self._layout.addWidget(self.slider)






    def connectNotify(self, signal):
        """When the signal is connected we need to emit the object the linking
        request back to the widget that requested axis linking."""
        if hasattr(self, '_plotWidget'):
            if self._plotWidget is not None:
                self._plotWidget.connectNotify(signal)
                if signal.name() == 'link':
                    self.link.emit(self._plotWidget)

    def minimumSizeHint(self):
        return QSize(50, 50)

    def sizeHint(self):
        return QSize(50, 50)

    def _set_plot_name(self):
        """Sets plot to plot_name if specified, otherwise to column name """
        if self._name:
            self.plotItem.setLabel('left', text=self._name,
                                   units=self._units,
                                   unitPrefix=self._unitPrefix)
        else:
            self.plotItem.setLabel('left', text=self._column_name,
                                   units=self._units,
                                   unitPrefix=self._unitPrefix)
    def setName(self, new_name):
        """Sets the name of the plot to new_name.

        Args:
            new_name (str): string plot name."""
        self._name = new_name
        self._set_plot_name()

    def getName(self):
        return self._name

    def setShotRun(self, new_shotrun):
        self._shotrun = new_shotrun

    def getShotRun(self):
        return self._shotrun

    def setColumnName(self, new_column):
        self._column_name = new_column
        self._viewBox.register(new_column) # Axis link
        self._set_plot_name()

    def getColumnName(self):
        return self._column_name

    def setUnits(self, units):
        self._units = units
        self._set_plot_name()

    def getUnits(self):
        return self._units

    def setUnitPrefix(self, unit_prefix):
        self._unitPrefix = unit_prefix
        self._set_plot_name()
        # TODO inert bug in setting unitPrefix
        # https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/plotitem.html#pyqtgraph.PlotItem.setLabel

    def getUnitPrefix(self):
        return self._unitPrefix

    def _setXlabel(self):
        self.plotItem.setLabel('bottom', text=self._XLabel,
                               units=self._XUnits, unitPrefix=self._XUnitPrefix)

    def setXLabel(self, new_label):
        self._XLabel = new_label
        self._setXlabel()

    def getXLabel(self):
        return self._XLabel

    def setXUnits(self, units):
        self._XUnits = units
        self._setXlabel()

    def getXUnits(self):
        return self._XUnits

    def setXUnitPrefix(self, unit_prefix):
        self._XUnitPrefix = unit_prefix
        self._setXlabel()

    def getXUnitPrefix(self):
        return self._XUnitPrefix

    @Slot()
    def plot_sample_signal(self):
        self._plotWidget.plot([1,2,3,4,5,6,7,8,9,10], [30,32,34,32,33,31,29,32,35,45],
                  pen=pg.mkPen('k', width=2))
        self.finished.emit()

    @Slot()
    def replot(self):
        fn = self.property('dat_input_filename')
        if fn[-5:] == 'v.dat':
            data = np.genfromtxt(fn, names=True, skip_footer=True) # footer ?
        elif fn[-5:] == 'j.dat':
            data = np.genfromtxt(fn, names=True)
        x = data['times']
        y = data[self._column_name]
        if self._unitPrefix == 'k':  # PyQtGraph bug in handling unitPrefix
            y *= 1000
        self._plotWidget.plot(x, y, pen=pg.mkPen('b', width=2))


    @Slot()
    def plot_function(self):
        x = np.linspace(0, 2 * np.pi, 200)
        y = eval(self.property('plot_function'))
        self._plotWidget.plot(x, y, pen=pg.mkPen('r', width=2))


    @Slot(object)
    def plot_four_points_boundary(self, ids:imas.equilibrium, idx:int=-1):
        """Plot the plasma boundary and the four points used for 
           the shaping of the plasma boundary.

           Args:
                ids(object): Equilibrium IDS for shaping of plasma boundary.
                idx(int): Index of IDS slice to plot. If -1, all slices are plotted."""

        if not self._plot_init: # i.e. execute after canvas initialization
            self.log.emit("Received "+ids.__name__+" IDS for plasma boundary shaping.")
            
            tag = "shaping"

            if not tag in self._checkboxes.keys():
                qw = self.create_toolbar_shape()
                self._layout.insertWidget(2,qw)

                self.plots[tag] = []
                self._checkboxes[tag] = QCheckBox(tag)
                self._checkboxes[tag].setChecked(True)
                self._checkboxes[tag].stateChanged.connect(self.replot_slice)
                self.gridLayout.addWidget(self._checkboxes[tag],3,0,1,1)
                

            self.idslist[tag] = ids   

            if len(ids.time) > 1:
                for plot in self.plots[tag]:
                    self.plotItem.removeItem(plot)
                self.plots[tag] = []
                idx = -1

            for k in range(len(ids.time)):

                brush = pg.mkBrush(0,0,0,15) # R, G, B, Alpha%
                pen = pg.mkPen('k',width=0.01)

                eq_ts = ids.time_slice[k]
                sep = eq_ts.boundary_separatrix # convenience variable
                
                if eq_ts.boundary.type > 0 or sep.type > 0:
                    LOutlineR = []
                    LOutlineZ = []                
                    nsep = len(sep.outline.r)
                    for i in range(nsep):
                        if (sep.outline.z[i] >= sep.x_point[0].z):
                            LOutlineR.append(sep.outline.r[i])
                            LOutlineZ.append(sep.outline.z[i])
                else:
                    LOutlineR = list(eq_ts.boundary.outline.r)
                    LOutlineZ = list(eq_ts.boundary.outline.z)

                r = np.array(LOutlineR)
                z = np.array(LOutlineZ)

                qpath = pg.arrayToQPath(r,z,connect='all')
                qpathitem = QGraphicsPathItem(qpath)
                qpathitem.setBrush(brush)
                qpathitem.setPen(pen)
                qpathitem.setZValue(0.1)

                four_points = GraphItem(mode=QLabel(text='move'))
                four_points.positions.connect(self.emit_four_points)
                four_points.index_values.connect(self.show_point_coord)
                four_points.scatter.sigClicked.connect(self.set_current_shaping_point)
                pos = np.array([[np.min(r), z[np.argmin(r)]], 
                                [r[np.argmin(z)], np.min(z)], 
                                [np.max(r), z[np.argmax(r)]],
                                [r[np.argmax(z)], np.max(z)]], dtype=float)
                symbols = ['o','o','o','o']
                four_points.setData(pos=pos, symbol=symbols, pxMode=True, size=10, zValue=100)

                label = 't = %.3f s, Ip = N/A'%(ids.time[k])

                if idx > -1 and idx < int(len(self.plots[tag])/2):
                    # replace
                    self.plotItem.removeItem(self.plots[tag][idx*2])
                    self.plotItem.removeItem(self.plots[tag][idx*2+1])
                    self.plots[tag][idx*2] = qpathitem
                    self.plots[tag][idx*2+1] = four_points
                    self._fallback_title[idx] = label
                    slider_value = idx
                    
                else:
                    # add
                    self.plots[tag].append(qpathitem)
                    self.plots[tag].append(four_points)
                    self._fallback_title.append(label) 
                    if self.slider.maximum() < int(len(self.plots[tag])/2)-1:
                        self.slider.setMaximum(self.slider.maximum()+1)
                    slider_value = self.slider.maximum()

                if self.slider.maximum() == 0:
                    self.slider.setMinimum(0)

                self.plotItem.addItem(qpathitem)
                self.plotItem.addItem(four_points)                      

            if idx == -1:
                slider_value = self.slider.value()

            if self.slider.value() == slider_value:
                self.slider.valueChanged.emit(slider_value)
            else:
                self.slider.setValue(slider_value)
              
        else:
            print("graph.py: Error, IDS received before calling _plot_init().")


    def emit_four_points(self, pos):
        """Emit the positions of the four points together with the index of the slice.

        Args:
            pos: Positions of the four points."""

        index = self.slider.value()
        self.slice_four_points.emit(tuple([index, pos]))


    @Slot(object)
    def plot_IDS_2D(self, ids, index:int=-1):
        """Plots contours of magnetic fluxes.

            Args:
                ids: 
        """
        if ids != None:
            if ids.__name__ in ['equilibrium', 'wall', 'pf_active','pf_passive']:
                self.log.emit("Received "+ids.__name__+" IDS.")

                if ids.__name__ == "equilibrium" and ids.code.name == "Nova":
                    for ts in ids.time_slice:
                        ts.boundary.outline.r = ts.boundary_separatrix.outline.r
                        ts.boundary.outline.z = ts.boundary_separatrix.outline.z

                if (ids.__name__ == "equilibrium" and len(ids.time)==1 and index > -1):
                    if "equilibrium" not in self.idslist.keys(): 
                         eq_ids = imas.equilibrium()
                         eq_ids.ids_properties.homogeneous_time = 1
                         eq_ids.time = np.repeat(-1, index+1)
                         eq_ids.time_slice.resize(index+1)
                         self.idslist["equilibrium"] = eq_ids
                    eq_ids = self.idslist["equilibrium"]
                    if index < len(eq_ids.time):
                        # replace old slice with new
                        eq_ids.time[index] = ids.time[0]
                        eq_ids.time_slice[index] = ids.time_slice[0]
                        slider_value = index
                    else: # append slice
                        empty_ids = imas.equilibrium()
                        empty_ids.ids_properties.homogeneous_time = 1
                        empty_ids.time.resize(1)
                        empty_ids.time_slice.resize(1)
                        empty_slice = empty_ids.time_slice[0]
                        for i in range(index-len(eq_ids.time)):
                            # fill up intermediate indexes with empty data
                            eq_ids.time = np.append(eq_ids.time, -1)
                            eq_ids.time_slice = np.append(eq_ids.time_slice, empty_slice)
                        eq_ids.time = np.append(eq_ids.time, ids.time[0])
                        eq_ids.time_slice = np.append(eq_ids.time_slice, ids.time_slice[0])
                        self.slider.setMaximum(len(eq_ids.time)-1)
                        slider_value = index
                     
                    if self.slider.value() == slider_value:
                        self.slider.valueChanged.emit(slider_value)
                    else:
                        self.slider.setValue(slider_value)
                        
                else:
                    if ids.__name__ == 'equilibrium':
                        self.slider.setRange(0, max([len(ids.time)-1, self.slider.maximum()]))
                    self.idslist[ids.__name__] = deepcopy(ids)
                    self.plot_contour()

                
    @Slot(object)
    def stream_slices(self, ids):
        """Plot contours of magnetic fluxes, wall contour and contours of passive and active elements 
           of the latest received time slice. 

                Args:
                    ids: wall, pf_active, pf_passive IDS or slice of equilibrium IDS.
           """
        if ids != None:
            if ids.__name__ in ['equilibrium', 'wall', 'pf_active','pf_passive']:
                self.log.emit("Received "+ids.__name__+" IDS.")
                self.idslist[ids.__name__] = ids
                if ids.__name__ == 'equilibrium':
                    self.slider.setValue(0)
                    self.slider.valueChanged.emit(0)
                else:
                    self.plot_contour()


    def plot_contour(self):
        """Plot contours of magnetic fluxes, wall contour and contours of passive and active elements
           at a specified time slice selected by the slider..
        """
        if self._plot_init:  
            self.slider.valueChanged.connect(self.replot_slice) # only for contour plots          
            groupBox_ids = QGroupBox()       
            gridLayout = QGridLayout(groupBox_ids)
            self.gridLayout = gridLayout
            gridLayout.setVerticalSpacing(2)
            gridLayout.setContentsMargins(0, 0, 0, 0);
            gridLayout.setContentsMargins(0, 0, 0, 0);

            self._checkboxes = {}
            ncols = 3
            for i,cb in enumerate(['pf_active','pf_passive','wall',
                                    'psi_outside','psi_inside','boundary',
                                    'separatrix','separatrix2','limiter']):
                self._checkboxes[cb] = QCheckBox(cb)
                # a matter of preference for initial view:
                if cb in ['pf_passive','separatrix2']:
                    self._checkboxes[cb].setChecked(False)
                else:
                    self._checkboxes[cb].setChecked(True)
                self._checkboxes[cb].stateChanged.connect(self.replot_slice)
                gridLayout.addWidget(self._checkboxes[cb],i/ncols,i%ncols,1,1)
            self._layout.addWidget(groupBox_ids)

            self._viewBox.setAspectLocked()

            # create title
            self.title_label = 't = 0.0 s, Ip = N/A'
            self.plotItem.setTitle(self.title_label)
            # create axis labels
            self.plotItem.setLabel('left', text="Z", units="")
            self.plotItem.setLabel('bottom', text="R", units="")
            # create legend
            self.legend = pg.LegendItem(offset=[-1,25])
            self.legend.setParentItem(self.plotItem)

            # Create empty plots
            # closest point to the wall
            self.n_levels = 7
            self.n_levels_max = 100
            s = pg.PlotDataItem([0],[0],symbol='x',
                                pen=pg.mkPen('k', width=2), zValue=20)
            s.setVisible(False)
            self.plotItem.addItem(s)
            self.plots['equilibrium'].append(s)
            
            # psi outside
            pen = pg.mkPen([166,189,219], width=1)
            for i in range(3*self.n_levels_max):
                c = pg.IsocurveItem(pen=pen)
                c.setZValue(1)
                c.setVisible(False)
                self.plotItem.addItem(c)
                self.plots['equilibrium'].append(c)
            # psi inside
            pen = pg.mkPen([251,106,74], width=1)
            for i in range(self.n_levels):
                c = pg.IsocurveItem(pen=pen)
                c.setZValue(1)
                c.setVisible(False)
                self.plotItem.addItem(c)
                self.plots['equilibrium'].append(c)
            # boundaries
            colorsb = [[253,141,60],[203,24,29],[140,107,177]]
            for i in range(3):
                pen = pg.mkPen(colorsb[i], width=2)
                c = pg.IsocurveItem(pen=pen)
                c.setZValue(1)
                c.setVisible(False)
                self.plotItem.addItem(c)
                self.plots['equilibrium'].append(c)
            # legend entries
            # self.legend_labels = ['boundary, psi=0.0 Wb',
            #                       'separatrix, psi=0.0 Wb',
            #                       'separatrix2, psi=0.0 Wb']
            self.legend_labels = ['boundary', 'separatrix', 'separatrix2']
            # pg.IsocurveItem not compatible with legend, create dummy
            for i in range(3):
                pen = pg.mkPen(colorsb[i], width=2)
                dummy = pg.PlotDataItem(pen=pen)
                self.legend.addItem(dummy, self.legend_labels[i])
                self.plots['equilibrium'].append(dummy)  

            self.units = None
            self._fallback_title = []

            self._plot_init = False

        if not self.idslist: # IDS not received through slot
            self.idslist = self.read_IDS(SingleSlice=False)

        # draw magnetic field
        if 'equilibrium' in self.idslist.keys():
            for cb in ['boundary','separatrix','separatrix2','limiter',
                        'psi_outside','psi_inside']:
                self._checkboxes[cb].setDisabled(False)

            if self.units == None:
                xunit = self.imas_dd_units.get_units('equilibrium', 
                    'time_slice/boundary_separatrix/outline/r')
                yunit = self.imas_dd_units.get_units('equilibrium', 
                    'time_slice/boundary_separatrix/outline/z')
                self.units = [xunit, yunit]

            self.replot_slice()

        else:
            for cb in ['boundary','separatrix','separatrix2','limiter',
                        'psi_outside','psi_inside']:
                self._checkboxes[cb].setDisabled(True)

                
        # draw wall
        if len(self.plots['wall']) == 0:
            if 'wall' in self.idslist.keys():
                self._checkboxes['wall'].setDisabled(False)
                wall_units = self.idslist['wall'].description_2d[0].limiter.unit
                for wall_unit in wall_units:
                    wall_r = wall_unit.outline.r
                    wall_z = wall_unit.outline.z
                    c = pg.PlotDataItem(wall_r, wall_z, pen=pg.mkPen('k', width=2), zValue=10)
                    self.plotItem.addItem(c)
                    self.plots['wall'].append(c)
                for plot in self.plots['wall']:
                    plot.setVisible(self._checkboxes['wall'].isChecked())
                if self.units == None:
                    xunit = self.imas_dd_units.get_units('wall', 
                                        'description_2d/limiter/unit/outline/r')
                    yunit = self.imas_dd_units.get_units('wall', 
                                        'description_2d/limiter/unit/outline/z')
                    self.units = [xunit, yunit]

            else:
                self._checkboxes['wall'].setDisabled(True)
                self._checkboxes['wall'].setChecked(False)
                
        # Draw Coils
        if len(self.plots['pf_active'])==0:
            if 'pf_active' in self.idslist.keys(): 
                color = [115,115,155]
                pen = pg.mkPen(color, width=2)
                brush = pg.mkBrush(color)
                self._checkboxes['pf_active'].setDisabled(False)
                for coil in self.idslist['pf_active'].coil:
                    for element in coil.element:
                        if element.geometry.geometry_type == 2: # rectangle
                            rect = element.geometry.rectangle
                            dx = rect.width/2
                            dy = rect.height/2
                            x = [rect.r-dx, rect.r+dx, rect.r+dx, rect.r-dx, rect.r-dx]
                            y = [rect.z-dy, rect.z-dy, rect.z+dy, rect.z+dy, rect.z-dy]
                            c = pg.PlotDataItem(x, y, pen=pen, zValue=1)
                            self.plotItem.addItem(c)
                            self.plots['pf_active'].append(c)
                            center = pg.PlotDataItem([rect.r], [rect.z],symbol='o', symbolSize=0.1,
                                                    pen=pen, symbolPen=pen, symbolBrush=brush,
                                                    zValue=1, pxMode=False)
                            self.plotItem.addItem(center)
                            self.plots['pf_active'].append(center)
                for plot in self.plots['pf_active']:
                    plot.setVisible(self._checkboxes['pf_active'].isChecked())
                if self.units == None:
                    xunit = self.imas_dd_units.get_units('pf_active', 
                        'coil/element/geometry/rectangle/width')
                    yunit = self.imas_dd_units.get_units('pf_active', 
                        'coil/element/geometry/rectangle/height')
                    self.units = [xunit, yunit]
            else:
                self._checkboxes['pf_active'].setDisabled(True)
                self._checkboxes['pf_active'].setChecked(False)
                
        # Draw Passive
        if len(self.plots['pf_passive'])==0: 
            if 'pf_passive' in self.idslist.keys():
                self._checkboxes['pf_passive'].setDisabled(False)
                for loop in self.idslist['pf_passive'].loop:
                    for element in loop.element:
                        if element.geometry.geometry_type == 2: # rectangle
                            rectangle = element.geometry.rectangle
                            r1 = rectangle.r - rectangle.width/2
                            z1 = rectangle.z - rectangle.height/2
                            r2 = rectangle.r + rectangle.width/2
                            z2 = z1
                            r3 = r2
                            z3 = rectangle.z + rectangle.height/2
                            r4 = r1
                            z4 = z3
                            x = [r1, r2, r3, r4, r1]
                            y = [z1, z2, z3, z4, z1]                            

                        elif element.geometry.geometry_type == 3: # oblique
                            # parallelogram
                            oblique = element.geometry.oblique 
                            # Major radius of the reference point (from which the alpha and beta angles are defined, 
                            # marked by a + on the diagram) [m] 
                            # file:///opt/pkg/ITER/imas/core/IMAS/3.39.0-4.11.5-foss-2022b/share/doc/imas/utilities/parallelogram.svg
                            r = oblique.r 
                            # Height of the reference point (from which the alpha and beta angles are defined, 
                            # marked by a + on the diagram) [m]
                            z = oblique.z 
                            # length of the parallelogram side inclined with 
                            # angle alpha with respect to the major radius axis
                            la = oblique.length_alpha 
                            # length of the parallelogram side inclined with 
                            # angle beta with respect to the height axis
                            lb = oblique.length_beta
                            # inclination of first angle measured counter-clockwise 
                            # from horizontal outwardly directed radial vector (grad R).
                            a = oblique.alpha
                            # inclination of second angle measured counter-clockwise from 
                            # vertically upwards directed vector (grad Z). If both alpha 
                            # and beta are zero (rectangle) then the simpler rectangular 
                            # elements description should be used.
                            b = oblique.beta
                            # calculating the position of parallelogram corners
                            # counting counter-clockwise, from the bottom: 1,2,3,4
                            
                            # this should have been the correct calculation based on the diagram
                            # r1 = r # the reference point
                            # z1 = z # the reference point
                            # r2 = r + la*cos(a)
                            # z2 = z + la*sin(a)
                            # r3 = r2 + lb*sin(b)
                            # z3 = z2 + lb*cos(b)
                            # r4 = r + lb*sin(b)
                            # z4 = z + lb*cos(b)

                            # taken from ids_util and switched order of points
                            r1 = r # the reference point
                            z1 = z # the reference point
                            r2 = r + la*cos(a)
                            z2 = z + la*sin(a)
                            r3 = r2 - lb*sin(b)
                            z3 = z2 + lb*cos(b)
                            r4 = r - lb*sin(b)
                            z4 = z + lb*cos(b)

                            x = [r1, r2, r3, r4, r1]
                            y = [z1, z2, z3, z4, z1]

                        else:
                            print("graph.py: element of type", element.geometry.geometry_type, "not drawn.") 

                        c = pg.PlotDataItem(x, y, pen=pg.mkPen(color=(200, 200, 200), width=2), zValue=0)
                        self.plotItem.addItem(c)
                        self.plots['pf_passive'].append(c)  

                for plot in self.plots['pf_passive']:
                    plot.setVisible(self._checkboxes['pf_passive'].isChecked())
                if self.units == None:
                    xunit = self.imas_dd_units.get_units('pf_passive', 
                        'loop/element/geometry/oblique/r')
                    yunit = self.imas_dd_units.get_units('pf_passive', 
                        'loop/element/geometry/oblique/z')
                    self.units = [xunit, yunit]
            else:
                self._checkboxes['pf_passive'].setDisabled(True)
                self._checkboxes['pf_passive'].setChecked(False)
                
        if self.units != None:
            self.plotItem.setLabel('left', text="Z", units=self.units[1])
            self.plotItem.setLabel('bottom', text="R", units=self.units[0])


    def replot_slice(self, state=None):
        """
        """

        for cb in ['wall','pf_passive','pf_active']:
            for plot in self.plots[cb]:
                plot.setVisible(self._checkboxes[cb].isChecked())
        
        if self.idslist:
            index = self.slider.value()
            if index == -1: index = 0
            if 'equilibrium' in self.idslist.keys():
                eq_ids = self.idslist['equilibrium']
                if index < len(eq_ids.time) and eq_ids.time[index] > -1:
                    self.queue.addTask(self.plot_slice)
                    # the following actions cannot be done in a thread
                    time = eq_ids.time[index]
                    ip = eq_ids.time_slice[index].global_quantities.ip
                    if np.abs(ip) < 1e20: 
                        self.title_label = 't = %.3f s, Ip = %.3f MA'%(time,ip*1.e-6)
                    else: # undefined value
                        self.title_label = 't = %.3f s, Ip = N/A'%(time)
                    self.plotItem.setTitle(self.title_label)
                else:
                    self.clear_contour()    
                    self.plotItem.setTitle(self._fallback_title[index]) 

            tag = 'shaping'
            if tag in self.idslist.keys():
                for item in self.plots[tag]:
                    if item != None:
                        item.setVisible(False)
                if self._checkboxes[tag].isChecked():
                    if (index+1)*2 <= len(self.plots[tag]):
                        if self.plots[tag][index*2] != None:
                            self.plots[tag][index*2].setVisible(True) # plasma shape
                        if self.plots[tag][index*2+1] != None:
                            self.plots[tag][index*2+1].setVisible(True) # four-points
                        if 'equilibrium' in self.idslist.keys():
                            if index >= len(self.idslist['equilibrium'].time): # update title
                                self.plotItem.setTitle(self._fallback_title[index])
                        else:
                            self.plotItem.setTitle(self._fallback_title[index])

            if (self._checkboxes['pf_active'].isChecked() == False and 
                self._checkboxes['pf_passive'].isChecked() == False):
                self.plotItem.autoRange(items=self.plots['wall'])

            self.plotItem.update()


    def plot_slice(self):
        """
        """

        index = self.slider.value()

        plots = self.plots['equilibrium']

        eq_ts = self.idslist['equilibrium'].time_slice[index]
        
        iplot = 0 # the internal index of the plots       
        
        if not len(eq_ts.profiles_2d):
            return

        psi2d = eq_ts.profiles_2d[0].psi
        x = eq_ts.profiles_2d[0].grid.dim1
        y = eq_ts.profiles_2d[0].grid.dim2
        psi_axis = eq_ts.global_quantities.psi_axis
        psi_sep = eq_ts.boundary_separatrix.psi
        psi_bnd = eq_ts.boundary.psi
        psi_sep2 = eq_ts.boundary_secondary_separatrix.psi
        if psi_bnd == -9e40: psi_bnd = eq_ts.global_quantities.psi_boundary
        if psi_sep2 == -9e40: psi_sep2 = psi_sep

        limr = eq_ts.boundary.active_limiter_point.r
        if limr == -9e40:
            limr = eq_ts.boundary_separatrix.active_limiter_point.r
        limz = eq_ts.boundary.active_limiter_point.z
        if limz == -9e40:
            limz = eq_ts.boundary_separatrix.active_limiter_point.z

        ymin, ymax = 0, 0
        if self.idslist['equilibrium'].code.name == "Nova":
            outline_z = eq_ts.boundary_separatrix.outline.z
        else:
            outline_z = eq_ts.boundary.outline.z
                
        if not len(outline_z):
            return

        ymax = np.max(outline_z)
        ymin = np.min(outline_z)

        if (psi_axis > psi_bnd):
            psi2d = -psi2d
            psi_axis = -psi_axis
            psi_bnd = -psi_bnd
            psi_sep = -psi_sep
            psi_sep2 = -psi_sep2

        psi_max = np.amax(psi2d)

        if self._checkboxes['limiter'].isChecked() and (limr > 0):
            plots[iplot].setData([limr],[limz])
            plots[iplot].setVisible(True) 
        else:
            plots[iplot].setVisible(False) 
        iplot += 1      
                
        dpsi = (psi_bnd - psi_axis)/self.n_levels

        i_ymax = -1
        i_ymin = -1

        for i in range(len(y)):
            if (y[i] < ymin):
                i_ymin = i
            if (y[i] < ymax):
                i_ymax = i

        if self._checkboxes['psi_outside'].isChecked():
            # DrawPsiOutside

            vmax = psi_max
            vmin = psi_bnd + dpsi

            if vmax>=vmin and dpsi>0:
                levels = np.arange(vmin, vmax, dpsi)
                # psi_ax_out0
                data = psi2d
                for i in range(len(levels)):
                    c = plots[i+iplot]
                    c.setData(data)
                    c.setLevel(levels[i])
                    c.setX(x.min())
                    c.setY(y.min())
                    c.setScale((y.max()-y.min())/np.shape(psi2d)[1])   
                    c.setVisible(True)    
                for i in range(len(levels),self.n_levels_max):
                    c = plots[i+iplot]
                    c.setData(np.zeros((1,2)))
                    c.setVisible(False)
              
            vmax = psi_bnd
            vmin = psi_axis

            if vmax>=vmin and dpsi>0:
                levels = np.arange(vmin, vmax, dpsi)

                # psi_ax_out1
                data = psi2d[:,0:i_ymin]
                for i in range(len(levels)):
                    c = plots[i+iplot+self.n_levels_max]
                    c.setData(data)
                    c.setLevel(levels[i])
                    c.setX(x.min())
                    c.setY(y[0:i_ymin].min())
                    c.setScale((y.max()-y.min())/np.shape(psi2d)[1])  
                    c.setVisible(True)  
                for i in range(len(levels),self.n_levels_max):
                    c = plots[i+iplot+self.n_levels_max]
                    c.setData(np.zeros((1,2)))
                    c.setVisible(False)

                # psi_ax_out2
                data = psi2d[:,i_ymax:]
                for i in range(len(levels)):
                    c = plots[i+iplot+2*self.n_levels_max]
                    c.setData(data)
                    c.setLevel(levels[i])
                    c.setX(x.min())
                    c.setY(y[i_ymax:].min())
                    c.setScale((y.max()-y.min())/np.shape(psi2d)[1])
                    c.setVisible(True)  
                for i in range(len(levels),self.n_levels_max):
                    c = plots[i+iplot+2*self.n_levels_max]
                    c.setData(np.zeros((1,2)))
                    c.setVisible(False)
        else:
            for i in range(3*self.n_levels_max):
                plots[i+iplot].setData(np.zeros((1,2)))
                plots[i+iplot].setVisible(False)

        iplot += 3*self.n_levels_max

        if self._checkboxes['psi_inside'].isChecked():
            # DrawPsiInside
            vmax = psi_bnd
            vmin = psi_axis

            if vmax>=vmin and dpsi>0:
                #levels = np.arange(vmin, vmax, dpsi)
                levels = np.linspace(vmin, vmax, self.n_levels)
                data = psi2d[:,i_ymin:i_ymax]

                for i in range(self.n_levels):
                    c = plots[i+iplot]
                    c.setData(data)
                    c.setLevel(levels[i])
                    c.setScale((y.max()-y.min())/np.shape(psi2d)[1])
                    c.setX(x.min())
                    c.setY(y[i_ymin:i_ymax].min())                   
                    c.setVisible(True)  
        else:
            for i in range(self.n_levels):
                plots[i+iplot].setData(np.zeros((1,2)))
                plots[i+iplot].setVisible(False)

        iplot += self.n_levels

        # draw boundaries
        if psi_bnd <= psi_sep and psi_sep <= psi_sep2:
            # self.legend_labels = ['boundary, psi=' + "{:.2f}".format(psi_bnd) + " Wb",
            #                  'separatrix, psi=' + "{:.2f}".format(psi_sep) + " Wb",
            #                  'separatrix2, psi=' + "{:.2f}".format(psi_sep2) + " Wb" ]
            levels=[psi_bnd, psi_sep, psi_sep2]
            for i,cb in enumerate(['boundary','separatrix','separatrix2']):
                c = plots[i+iplot]
                if self._checkboxes[cb].isChecked():
                    c.setData(psi2d)
                    c.setLevel(levels[i])
                    c.setX(x.min())
                    c.setY(y.min())
                    c.setScale((y.max()-y.min())/np.shape(psi2d)[1])
                    c.setVisible(True)
                else:
                    c.setData(np.zeros((1,2)))
                    c.setVisible(False)
        else:
            for cb in ['boundary','separatrix','separatrix2']:
                self._checkboxes['psi_inside'].setDisabled(True)
                self._checkboxes['psi_inside'].setChecked(False)
                
        iplot += 3 


    @Slot(bool)
    def setSliderVisible(self, value:bool):
        """|Slot| to enable/disable slider visibility. 
        If received ``True``, the slider is visible.
        If received ``False``, the slider is not visible.

        Args:
            value(bool): Boolean to enable/disable slider visibility.
        """
        self.slider.setVisible(value)


    def read_IDS(self, SingleSlice=True):
        import imas # UAL library

        shot = 135011
        run = 7
        user = "public"
        database = "iter"
        
        time = 300.0
        interp = 1
        
        imas_entry_init = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND, database, shot, run, user, data_version = '3')
        imas_entry_init.open() 

        idslist = {}
        
        if (SingleSlice):
          idslist['equilibrium'] = imas_entry_init.get_slice('equilibrium', time, interp)
          idslist['wall'] = imas_entry_init.get_slice('wall', time, interp)
          idslist['pf_active'] = imas_entry_init.get_slice('pf_active', time, interp)
          idslist['pf_passive'] = imas_entry_init.get_slice('pf_passive', time, interp)
          idslist['core_profiles'] = imas_entry_init.get_slice('core_profiles', time, interp)
          idslist['core_sources'] = imas_entry_init.get_slice('core_sources', time, interp)
          idslist['summary'] = imas_entry_init.get_slice('summary', time, interp)
        else:
          #idslist['equilibrium'] = imas_entry_init.get('equilibrium')
          #idslist['wall'] = imas_entry_init.get('wall')
          idslist['pf_active'] = imas_entry_init.get('pf_active')
          idslist['pf_passive'] = imas_entry_init.get('pf_passive')
          idslist['core_profiles'] = imas_entry_init.get('core_profiles')
          idslist['core_sources'] = imas_entry_init.get('core_sources')
          idslist['summary'] = imas_entry_init.get('summary')
        
        imas_entry_init.close()

        return idslist


    def extract_units(self, ht:int, sig:str):
        """Extract units of signal.

           Args:
                ht(int): Homogenous time value of IDS.
                sig: Path of signal in IDS.
        """
        idsp0 = sig.split('/')[0]
        idsp1 = '/'.join(sig.split('/')[1:])
        idsp1=re.sub("([\(\[]).*?([\)\]])", "", idsp1)
        yunit = self.imas_dd_units.get_units(idsp0, idsp1)
        if ht == 0:
            idsp1 = '/'.join(sig.split('/')[:-1])+'/time'
        elif ht == 1:
            if 'profiles_1d' in sig:
                idsp1 = sig.split('profiles_1d')[0]+'profiles_1d/psi'
            else:
                idsp1 = 'time'
        xunit = self.imas_dd_units.get_units(idsp0, idsp1)
        return (xunit, yunit)


    def init_layout(self):
        """Prepare new layout.
        """
        # clear plot items
        pi = self.plotItem
        for k in pi.axes:
            i = pi.axes[k]['item']
            i.close()
        pi.axes = None
        pi.scene().removeItem(pi.vb)
        pi.clear()
        self.plotItem = None
        # remove default PlotWidget
        self._layout.removeWidget(self._plotWidget)
        self._plotWidget = None
        # add new plot widget
        self._glw = pg.GraphicsLayoutWidget()
        self._layout.addWidget(self._glw)
        self.plotItems = []
        
        
    def _set_line_colors(self, colors:list):
        """Setter of attribute _line_colors
        """
        self._line_colors = colors   

    def _set_xlabels(self, labels:list):
        """Setter of attribute _xlabels
        """
        self._xlabels = labels 

    def _set_ylabels(self, labels:list):
        """Setter of attribute _ylabels
        """
        self._ylabels = labels

    def _set_link_xaxis(self, link:bool):
        """Setter of attribute _link_xaxis
        """
        self._link_xaxis = link

    def _set_add_vertical_line(self, add_line:bool):
        """Setter of attribute _add_vertical_line
        """
        self._add_vertical_line = add_line

    def _update_vertical_line_position(self, value:float):
        """Set the x-coordinate of vertical lines at value"""
        if self._add_vertical_line:
            for line in self._infinite_lines:
                self.queue.addTask(line.setValue(value))


    @Slot(object)
    def stream(self, ids):
        """|Slot| for appending data from IDS slice to plot.

        Args:
            ids(object): IDS slice or chunk of slices to be appended to the plot.
        """
        if ids is None:
            return

        if len(ids.time) == 1:
            self.plot_line(ids, update=True, width=2)
        else:
            dbentry = imas.DBEntry(imas.imasdef.MEMORY_BACKEND, 'tmp0', 12, 23, 
                              getpass.getuser(), data_version = '3')
            dbentry.create()
            dbentry.put(ids)

            for t in ids.time.tolist():
                ids_slice = dbentry.get_slice(ids_name=ids.__name__, 
                    time_requested=t, interpolation_method=1)
                self.plot_line(ids_slice, update=True, width=2)

            dbentry.close()
            




    @Slot(object)
    def profile(self, ids, **kwds):
        """Plot profile."""
        if self._plot_init == False:
            self.reset()
            # Recreate list of signal names in case number of slices changes
            # and signal name is of the form ids.time_slice[i].quantity.value
            try:
                ids_signals = self.property('ids_signals').split('\n')
                ids_signals = [ i.replace(' ','') for i in ids_signals ]
                ids_signals = [sig for sig in ids_signals if sig] # remove empty lines from count
                ids_signals = [ i.split(',') for i in ids_signals ]
            except: 
                ids_signals = []
            nsignals = len(ids_signals)
            
            self.sig_names = [ ids_signals[i][0] for i in range(nsignals) ]

            self.plotItems = []
            for i,sig in enumerate(self.sig_names):
                row = int(ids_signals[i][1].split('.')[1])-1
                col = int(ids_signals[i][1].split('.')[0])-1
                if self._editable:              
                    row += 1
                if self.property("title") is not None:     
                    row += 1
                self.plotItems.append(self._glw.getItem(row,col))

        self.plot_line(ids, **kwds)



    @Slot(object)
    def waveform(self, ids, **kwds):
        """Plot waveform."""
        self.plot_line(ids, **kwds)


    def plot_line(self, ids, **kwds):
        """Plot line."""

        if ids==None:
            return

        if self.property('shared_x_axis') in [True, False]:
            self._link_xaxis = self.property('shared_x_axis')

        colors = None
        if self.property('colors'):
            colors = eval('['+self.property('colors')+']')
        if colors is not None:
            self._line_colors = colors 

        repeat_colors = True # repeat colors in separate plot frames
        if self.property('repeat_colors') in [True, False]:
            repeat_colors = self.property('repeat_colors')

        invert_x_axis = False
        if self.property('invert_x_axis') in [True, False]:
            invert_x_axis = self.property('invert_x_axis')

        invert_y_axis = False
        if self.property('invert_y_axis') in [True, False]:
            invert_y_axis = self.property('invert_y_axis')

        update = False    
        if 'update' in kwds.keys():
            update = kwds.pop('update')
        if self.property('update') == True:
            update = True

        editable = False    
        if 'editable' in kwds.keys():
            editable = kwds.pop('editable')
        if self.property('editable') == True:
            editable = True
        if editable:
            self._link_xaxis = True
        self._editable = editable

        self._show_legend = True    
        if 'legend' in kwds.keys():
            self._show_legend = kwds.pop('legend')
        if self.property('legend') in [True, False]:
            self._show_legend = self.property('legend')

        names = self.property('names')
        if isinstance(names,str) and ',' in names:
            names = self.property('names').split(',')
            names = [x.strip() for x in names]

        hoverable = False
        if self.property('hoverable') in [True, False]:
            hoverable = self.property('hoverable')

        slice_index = None
        if 'slice_index' in kwds.keys():
            slice_index = kwds.pop('slice_index')

        if self._plot_init:
            # prepare new layout
            self.init_layout()

            cols = self.property('cols') or 1
            rows = self.property('rows') or 1
            if cols<1: cols = 1
            if rows<1: rows = 1
            try:
                ids_signals = self.property('ids_signals').split('\n')
                ids_signals = [ i.replace(' ','') for i in ids_signals ]
                ids_signals = [sig for sig in ids_signals if sig] # remove empty lines from count
                ids_signals = [ i.split(',') for i in ids_signals ]
            except: 
                ids_signals = []
            nsignals = len(ids_signals)

            # update rows and cols from ids_signals
            for i in range(nsignals):
                rows_sig = int(ids_signals[i][1].split('.')[1])
                cols_sig = int(ids_signals[i][1].split('.')[0])
                rows = max([rows,rows_sig])
                cols = max([cols,cols_sig])

            title_row = -1
            if editable: # Add toolbar
                proxy = self.create_toolbar()
                self._glw.addItem(proxy, row=0, col=0)
                title_row = 1
            else:
                title_row = 0

            if self._link_xaxis:
                self._glw.ci.setSpacing(-2) 

            #Update title
            title = self.property("title")
            if title != None:
                self._glw.addLabel(text=title, 
                                   row=title_row, col=0, colspan=cols,
                                   color='k', bold=True)    

            self.sig_names = [ ids_signals[i][0] for i in range(nsignals) ]
            
            self._infinite_lines = []

            _xlabels = []
            _ylabels = []

            j = -1

            for i,sig in enumerate(self.sig_names):

                path = sig.split('/')
                path = 'ids.'+'.'.join(path[1:])

                row = int(ids_signals[i][1].split('.')[1])-1
                if editable:              row += 1
                if title is not None:     row += 1
                col = int(ids_signals[i][1].split('.')[0])-1
                rowspan = int(ids_signals[i][3])
                colspan = int(ids_signals[i][2])
                
                # prepare the canvas
                if  self._glw.getItem(row,col) == None:
                    self._glw.addPlot(row=row, col=col, rowspan=rowspan, colspan=colspan, 
                                      viewBox=MyViewBox(invert_x_axis=invert_x_axis,
                                                        invert_y_axis= invert_y_axis))
                    if self._add_vertical_line:
                        self._infinite_lines.append(self._glw.getItem(row,col).addLine(x=0, 
                                                            pen=pg.mkPen(color=[0,0,0,70], width=2)))
                    j += 1

                if self._xlabels == None:
                    if 'profiles_1d' in path:
                        _xlabels.append('psi')
                    else:
                        _xlabels.append('time')
                else:
                    _xlabels.append(self._xlabels[j])
                if self._ylabels == None:
                    _ylabels.append('')
                else:
                    _ylabels.append(self._ylabels[j])
                plotItem = self._glw.getItem(row,col)    
                self.plotItems.append(plotItem)        
                plotItem.showAxes(True)
                plotItem.addLegend(offset=(-1,1))
                if (self._link_xaxis and j>0 and 
                    plotItem != self.plotItems[0]):
                    plotItem.setXLink(self.plotItems[0])

                ht = ids.ids_properties.homogeneous_time
                xunit, yunit = self.extract_units(ht, sig)
                
                plotItem.setLabel('left', text=_ylabels[i], units=yunit)
                if self._link_xaxis and row != rows + title_row:
                    plotItem.setLabel('bottom', text=None, units=None)
                    plotItem.showAxes(selection=True, showValues=(True,False,False,False))
                else:
                    plotItem.setLabel('bottom', text=_xlabels[i], units=xunit)

            self.plots = []
            self._index_mask = []

            self._plot_init = False

        for i,sig in enumerate(self.sig_names):

            path = sig.split('/')

            if ids.__name__ == path[0]: 
                value_path = 'ids.'+'.'.join(path[1:])
                value, time = [], []

                # # Read data from IDS
                # for waveforms
                if 'time_slice[:]' in value_path:
                    splitpath = value_path.split('[:]')
                    nvalues = eval('len('+splitpath[0]+')')
                    for j in range(nvalues):
                        value.append(eval(splitpath[0]+'['+str(j)+']'+
                                          splitpath[1]))
                        if ids.ids_properties.homogeneous_time == 0:
                            time.append(eval(splitpath[0]+'['+str(j)+'].'+
                                          '.'.join(splitpath[1].split('.')[:-1])))
                        elif ids.ids_properties.homogeneous_time == 1:
                            time.append(eval('ids.time['+str(j)+']'))
                else:
                    if ids.ids_properties.homogeneous_time == 0:
                        time_path =  'ids.'+'.'.join(path[1:-1])+'.time'
                        value, time = eval('('+value_path+','+time_path+')')
                    elif ids.ids_properties.homogeneous_time == 1:
                        value, time = eval('('+value_path+', ids.time)')

                # for profiles
                if 'time_slice[' in value_path and 'profiles_1d' in value_path:
                    ind = value_path.split('time_slice[')[1]
                    ind = ind.split(']')[0]
                    if ind.isnumeric():
                        time_path = value_path.split('profiles_1d')[0]+'profiles_1d.psi'
                        value, time = eval('('+value_path+','+time_path+')')

                # set custom legend name
                try: 
                    name = names[i]
                except:
                    name = None

                # # Create empty line objects
                if editable:
                    plot = GraphItem(mode=self._mode)
                    plot.scatter.sigClicked.connect(self.set_current_point)
                    # update all lines in same plot window with new x value
                    plot.index_values.connect(self.update_point_editable)

                    pos, adj = [], []
                    for pt in np.arange(len(time)):
                        pos.append([time[pt],value[pt]]) # positions of nodes in graphs
                        if pt < len(time)-1: 
                            adj.append([pt, pt+1]) # neighbours connected to each node
                    pos, adj = np.asarray(pos), np.asarray(adj)
                    self.queue.addTask(plot.setData(pos=pos, adj=adj, name=name, 
                                                    symbolBrush=[self._default_brush]*len(pos))) 

                else:

                    nlines = len(self.plotItems[i].listDataItems())
                    if self._add_vertical_line:
                        nlines = nlines-len(self._infinite_lines)
                    if repeat_colors:
                        ci = nlines%len(self._line_colors) # color index
                    else:
                        ci = i
                    if 'width' not in kwds.keys():
                        kwds['width'] = 2

                    if update and i<len(self.plots):
                        plot = self.plots[i]
                        xdata, ydata = plot.getData()
                        if len(time) == 1:
                            if slice_index in self._index_mask: 
                                # existing point found, update
                                idx = self._index_mask.index(slice_index)
                                if xdata is not None and ydata is not None:
                                    xdata[idx] = time[0]
                                    ydata[idx] = value[0]
                                    value, time = ydata, xdata
                            else: # append point to line
                                if xdata is not None and ydata is not None:
                                    xdata = np.append(xdata, time[0])
                                    ydata = np.append(ydata, value[0])
                                    sortx = xdata.argsort()
                                    xdata, ydata = xdata[sortx], ydata[sortx]
                                    value, time = ydata, xdata
                                if slice_index is not None and i == len(self.sig_names)-1: 
                                    # only once, it applies to all signals
                                    self._index_mask.append(slice_index)
                                    self._index_mask = np.array(self._index_mask)[sortx].tolist()
                        elif xdata is not None and ydata is not None:
                            value, time = ydata, xdata
                            self._index_mask = list(range(len(time)))

                        pen = pg.mkPen(self._line_colors[ci], width=kwds['width'])
                        plot.setPen(pen)
                        plot.curve.default_pen = pen
                        
                    else:
                        if i == len(self.sig_names)-1:
                            if slice_index is not None:
                                self._index_mask.append(slice_index)
                            else:
                                self._index_mask = list(range(len(time)))

                        pen = pg.mkPen(self._line_colors[ci], width=kwds['width'])
                        if hoverable:
                            plot = HoverablePlotDataItem(parent=self.plotItems[i],
                                                         pen=pen, zValue=1, name=name, **kwds)
                            self.plotItems[i].addItem(plot.curve.hover_info)
                        else:
                            plot = pg.PlotDataItem(pen=pen, zValue=1, name=name, **kwds)                     
                        
                    self.queue.addTask(plot.setData(time,value))

                    if slice_index is not None and i == len(self.sig_names)-1:  
                        self.queue.addTask(self._update_vertical_line_position(time[0]))

                if editable or not (update and i<len(self.plots)):
                    self.plots.append(plot)
                    self.plotItems[i].addItem(plot)
                    if name is None:
                        if editable:
                            self.plotItems[i].legend.addItem(plot.scatter, sig)
                        else:
                            self.plotItems[i].legend.addItem(plot, sig)

                self.plotItems[i].legend.setVisible(self._show_legend)




    def update_point_editable(self, index_values:tuple):
        """Update value of editable point at given index for all linked lines when point moved.

        Args:
            index_values(tuple): A tuple containing an integer index and a float point value tuple (x, y)."""

        self.index_time.emit((index_values[0], index_values[1][0]))
        sender = self.sender()
        for plot in self.plots:
            if plot != sender and plot.isVisible():
                plot.updateNodeX(index_values)
        self._lineEdits[0].setText(str(index_values[1][0]))
        self._lineEdits[1].setText(str(index_values[1][1]))
        self._lineEdits[0].setCursorPosition(0)
        self._lineEdits[1].setCursorPosition(0)
        self.timer.start(1000)


    def show_point_coord(self, index_values:tuple):
        """Display the coordinates of plasma-shaping point.

        Args:
            index_values(tuple): A tuple containing an integer index and a 
                                 float point value tuple (x, y)."""

        self._lineEdits_shape[0].setText(str(index_values[1][0]))
        self._lineEdits_shape[1].setText(str(index_values[1][1]))
        self._lineEdits_shape[0].setCursorPosition(0)
        self._lineEdits_shape[1].setCursorPosition(0)
        


    def show_profile(self, index:int):
        """Show only profile of given index.

        Args:
            index(int): index of profile."""
        if self._plot_init:
            return

        if not len(self.plots):
            return

        if index*2+1 >= len(self.plots):
            return

        for plot in self.plots:
            plot.setVisible(False)

        self.plots[index*2].setVisible(True)
        self.plots[index*2+1].setVisible(True)
       
        for plotItem in self.plotItems:
            plotItem.autoRange()


    @Slot()
    def reset(self):
        """Remove all plots."""
        # waveforms, editable waveforms, profiles, editable profiles
        if isinstance(self.plots, list):
            self.plots = []
            self._index_mask = []
            self._infinite_lines = []
            for plotItem in self._glw.ci.items: # scan the layout
                if isinstance(plotItem, pg.PlotItem):
                    plotItem.clear()
                    plotItem.legend.clear()
                    # put back vertical lines if present
                    if self._add_vertical_line:
                        self._infinite_lines.append(plotItem.addLine(x=0, 
                                                    pen=pg.mkPen(color=[0,0,0,70], width=2))) 
                    plotItem.update() 
            self.slider.setValue(0)                          

        # equilibrium, contours
        elif isinstance(self.plots, dict):
            self.clear_contour()
            if 'shaping' in self.plots.keys():
                for plot in self.plots['shaping']:
                    self.plotItem.removeItem(plot)
                self.plots['shaping'] = []
                self._fallback_title = []
            if 'equilibrium' in self.idslist.keys():
                self.idslist.pop("equilibrium")
            if self.legend is not None:
                self.legend.clear()
            self.plotItem.update()
            self.slider.setRange(-1,-1)
        


    def clear_contour(self):
        """Clear contour plots."""
        if 'equilibrium' in self.plots.keys():
            for line in self.plots['equilibrium']:
                line.setData(np.zeros((1,2)))
            self.plotItem.update()
        

    def create_toolbar(self):
        """Create group of buttons and inputs for selecting, moving, adding and
           removing points in an editable graph."""

        gb = QGroupBox()
        lw = QHBoxLayout(gb)
        lw.setContentsMargins(0, 0, 0, 0)

        pushButton0 = QPushButton("Sel.")
        pushButton1 = QPushButton("Move")
        pushButton2 = QPushButton("Del.")
        pushButton3 = QPushButton("Add")
        

        self._pushButtons = [pushButton0, pushButton1, pushButton2, pushButton3]

        for pushButton in self._pushButtons:
            pushButton.setMaximumHeight(15)
            pushButton.setMaximumWidth(50)
            pushButton.clicked.connect(self.buttonClicked)

        labelx = QLabel()
        labelx.setText(" x:")
        
        lineEditx = QLineEdit()
        lineEditx.setMaximumHeight(15)
        lineEditx.setValidator(QDoubleValidator())
        lineEditx.returnPressed.connect(self.update_value_x)
    
        labely = QLabel()        
        labely.setText(" y:")        

        lineEdity = QLineEdit()
        lineEdity.setMaximumHeight(15)
        lineEdity.setValidator(QDoubleValidator())
        lineEdity.returnPressed.connect(self.update_value_y)

        self._lineEdits = [lineEditx, lineEdity]
                
        palette = QPalette()
        brush = QBrush(QColor(239, 239, 239, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush)

        paletteGreen = QPalette()
        brush = QBrush(QColor(100, 255, 100, 0))
        brush.setStyle(Qt.SolidPattern)
        paletteGreen.setBrush(QPalette.Active, QPalette.Button, brush)
        paletteGreen.setBrush(QPalette.Inactive, QPalette.Button, brush)
        paletteGreen.setBrush(QPalette.Disabled, QPalette.Button, brush)
        
        self._palettes = [palette, paletteGreen]

        pushButton0.setPalette(paletteGreen)

        lw.addWidget(pushButton0)
        lw.addWidget(pushButton1)
        lw.addWidget(pushButton2)
        lw.addWidget(pushButton3)
        lw.addWidget(labelx)
        lw.addWidget(lineEditx)
        lw.addWidget(labely)      
        lw.addWidget(lineEdity)
        
        proxy = QGraphicsProxyWidget()
        proxy.setWidget(gb)

        return proxy

    def create_toolbar_shape(self):
        """Create inputs for moving the four plasma-shaping points."""

        gb = QGroupBox()
        lw = QHBoxLayout(gb)
        lw.setContentsMargins(0, 0, 0, 0)

        labelx = QLabel()
        labelx.setText(" x:")
        
        lineEditx = QLineEdit()
        lineEditx.setMaximumHeight(15)
        lineEditx.setValidator(QDoubleValidator())
        lineEditx.returnPressed.connect(self.update_xy_shaping)
    
        labely = QLabel()        
        labely.setText(" y:")        

        lineEdity = QLineEdit()
        lineEdity.setMaximumHeight(15)
        lineEdity.setValidator(QDoubleValidator())
        lineEdity.returnPressed.connect(self.update_xy_shaping)

        self._lineEdits_shape = [lineEditx, lineEdity]
                
        lw.addWidget(labelx)
        lw.addWidget(lineEditx)
        lw.addWidget(labely)      
        lw.addWidget(lineEdity)
        
        qw = QWidget()
        qw.setLayout(lw)
        return qw


    def buttonClicked(self):
        for i,pushButton in enumerate(self._pushButtons):
            if self.sender()==pushButton:
                if i==0: # select
                    self._pushButtons[0].setPalette(self._palettes[1])
                    self._pushButtons[1].setPalette(self._palettes[0])
                    self._pushButtons[2].setEnabled(True)
                    #self._pushButtons[3].setEnabled(True)
                    self._mode.setText('select')
                elif i==1: # move
                    self._pushButtons[0].setPalette(self._palettes[0])
                    self._pushButtons[1].setPalette(self._palettes[1])
                    self._pushButtons[2].setEnabled(False)
                    self._mode.setText('move')
                elif i==2: # remove point
                    self.remove_point_from_editable_lines()
                elif i==3: # add point
                    self.add_point_to_editable_lines()                
                break


    def add_point_to_editable_lines(self):
        """Add point in editable graph."""
        if self._selected_point is None:
            return
        if not self._lineEdits[0].text() or not self._lineEdits[1].text():
            return
        x = float(self._lineEdits[0].text())
        y = float(self._lineEdits[1].text())
        line = self._selected_point._plot
        if line is not None:
            pos, adj = self.add_point_editable(line, (x, y))
            graph = line.parent()
            graph.setData(pos=pos, adj=adj)

            # add point to linked plots
            for plot in self.plots:
                if plot != graph and plot.isVisible():
                    pos, adj = self.add_point_editable(plot.scatter, (x, None))
                    plot.setData(pos=pos, adj=adj)
            xdata = line.getData()[0]
            idx = np.where(xdata==x)[0][0]
            self.insert_slice.emit(x)

            self.timer.start(1000)

    
    def add_point_editable(self, line, point):
        """Add point to specified line.

        Args:
            line(tuple): A tuple of two coordinates (x, y) that specifies a line.
            point(tuple): A tuple containing the coordinates (x, y) of a point."""
        x,y = point
        xdata, ydata = line.getData()
        # if point exists, update
        idx = np.argmin(np.abs(xdata-x))
        if np.abs(xdata[idx]-x) < 1e-6: # data point found, update
            if y is not None:
                ydata[idx] = y
        else: # append
            if y is None: # linked plots only
                # graph is not sorted 
                if x < np.min(xdata):
                    idx0, slope = np.argmin(xdata), 0
                elif x > np.max(xdata):
                    idx0, slope = np.argmax(xdata), 0
                else:
                    # find left and right neighbours in time
                    xsorted = np.sort(xdata)
                    idx0 = np.where(x > xsorted)[0][-1]
                    idx1 = np.where(x < xsorted)[0][0]
                    slope = (ydata[idx1]-ydata[idx0])/(xdata[idx1]-xdata[idx0])
                y = ydata[idx0] + slope*(x-xdata[idx0])

            xdata = np.append(xdata, x)    
            ydata = np.append(ydata, y)

        pos, adj = [], []
        xs = np.argsort(xdata)
        for pt in np.arange(len(xdata)):
            pos.append([xdata[pt],ydata[pt]]) # positions of nodes in graphs
            if pt < len(xdata)-1: 
                adj.append([xs[pt], xs[pt+1]]) # neighbours connected to each node

        pos, adj = np.asarray(pos), np.asarray(adj)
        return pos, adj


    def remove_point_from_editable_lines(self):
        """Remove selected point from all connected editable lines."""
        if self._selected_point is None:
            return
        line = self._selected_point._plot
        
        # if waveform, keep at least 1 point in line
        if len(line.getData()[0]) < 2:
            return
        # if profile, keep at least 3 points in line (NOVA requirement)
        if ((not all([p.isVisible() for p in self.plots]) or self.slider.maximum()==0) and 
            len(line.getData()[0]) < 4):
            return

        idx = self._selected_point.index()
        for plot in self.plots:
            if plot.isVisible(): # only current slice
                pos, adj = self.remove_point_editable(plot.scatter, idx)
                self.queue.addTask(plot.setData(pos=pos, adj=adj))

        self.remove_slice.emit((idx, self._selected_point._data['x']))
        self.unset_current_point()
        self.timer.start(1000)


    def remove_point_editable(self, line, index):
        """Remove point from editable line at index.

        Args:
            line(object): Editable line object from which to remove the point at specified index.
            index(int): Index of the point to be removed.
        """
        xdata, ydata = line.getData()
        pos, adj = [], []
        for pt in np.arange(len(xdata)):
            if pt != index:
                pos.append([xdata[pt],ydata[pt]]) # positions of nodes in graphs
        for i,p in enumerate(pos):
            if i < len(pos)-1: 
                adj.append([i, i+1]) # neighbours connected to each node
        pos, adj = np.asarray(pos), np.asarray(adj)
        return pos, adj


    Slot(float)
    def remove_point_from_lines(self, time:float):
        """Remove point in all lines at given time.

        Args:
            time(float): Time of the point to be removed. """
        if not isinstance(self.plots, list):
            return
        if not len(self.plots):
            return
        
        for plot in self.plots:
            x, y = plot.getData()
            if x is None:
                continue
            axmt = np.abs(x-time)
            idx = np.argmin(axmt)
            if axmt[idx] > 1e-6:
                continue  
            x = np.delete(x, idx)
            y = np.delete(y, idx)
            self.queue.addTask(plot.setData(x, y))            


    def update_value_x(self):
        """Update X value and move selected point in editable line using value from toolbar. 
           Linked editable lines will be updated as well."""
        if self._mode.text() != 'move':
            return
        if self._selected_point is None:
            return
        xval = float(self._lineEdits[0].text())
        idx = self._selected_point.index()
        for plot in self.plots:
            plot.updateNodeX((idx,[xval, 0])) # Y value will be ignored
        self._selected_point.setBrush(self._select_brush)
        self.index_time.emit((idx,xval))
        self.unset_current_point()
        self.timer.start(1000)


    def update_time(self, index_time:tuple):
        """Update points at index with new time for all uneditable waveforms.

        Args:
            index_time(tuple): A tuple of index value and new time value of the points to be updated.
        """
        if not isinstance(self.plots, list):
            return
        if not len(self.plots):
            return
        index, time = index_time # index and time of the moved point
        if index not in self._index_mask:
            return

        ci = self._index_mask.index(index)
        for i,plot in enumerate(self.plots):
            x, y = plot.getData()
            if x is None:
                continue
            x[ci] = time
            if not i:
                sortx = np.argsort(x)
                self._index_mask = np.array(self._index_mask)[sortx].tolist()
            plot.setData(x[sortx],y[sortx])

        self._update_vertical_line_position(time)


    def update_slice_time(self, index_time:tuple):
        """Update time of |IDS| slice at index with new time.

            Args:
                index_time(tuple): A tuple of index value and new time value of the |IDS| slice to be updated. """
        
        index, time = index_time # index and time
        if ('equilibrium' in self.idslist.keys() and 
            index < len(self.idslist['equilibrium'].time)):
            self.idslist['equilibrium'].time[index] = time
        title = self.title_label.split(',')
        title0 = 't = %.3f s'%(time)
        self.title_label = title0+','+title[1]
        self._fallback_title[index] = title0+', Ip = N/A'
        self.plotItem.setTitle(self.title_label)


    def update_value_y(self):
        """Update Y value of selected point in editable line."""
        if self._mode.text() != 'move':
            return
        if self._selected_point is None:
            return
        yval = float(self._lineEdits[1].text())
        idx = self._selected_point.index()
        line = self._selected_point._plot
        line.parent().updateNodeY((idx,[0, yval])) # X value will be ignored
        self._selected_point.setBrush(self._select_brush)
        self.timer.start(1000)


    def set_current_shaping_point(self, line, point):
        """Set current point for plasma-shaping.

        Args:
            point(tuple): A tuple containing the coordinates (x, y) of a point."""
        if not len(point):
            return
        self._selected_point_shape = point[0]
        x = self._selected_point_shape.viewPos().x()
        y = self._selected_point_shape.viewPos().y()
        self._lineEdits_shape[0].setText(str(x))
        self._lineEdits_shape[1].setText(str(y))
        self._lineEdits_shape[0].setCursorPosition(0)
        self._lineEdits_shape[1].setCursorPosition(0)


    def update_xy_shaping(self):
        """Update X, Y values of selected plasma-shaping point."""
        if self._selected_point_shape is None:
            return
        xval = float(self._lineEdits_shape[0].text())
        yval = float(self._lineEdits_shape[1].text())
        idx = self._selected_point_shape.index()
        line = self._selected_point_shape._plot
        line.parent().updateNodeXY((idx,[xval,yval])) # Y value will be ignored
        

    def set_current_point(self, line, point):
        """Set current point for editing.

        Args:
            point(tuple): A tuple containing the coordinates (x, y) of a point."""
        if point[0] == self._selected_point:
            self.unset_current_point()
        else:
            self._selected_point = point[0]
            for plot in self.plots:
                for point in plot.scatter.points():
                    point.setBrush(self._default_brush)
            self._selected_point.setBrush(self._select_brush)
            x = self._selected_point.viewPos().x()
            y = self._selected_point.viewPos().y()
            self._lineEdits[0].setText(str(x))
            self._lineEdits[1].setText(str(y))
            self._lineEdits[0].setCursorPosition(0)
            self._lineEdits[1].setCursorPosition(0)
            self.index_time.emit((self._selected_point.index(),x))


    def unset_current_point(self):
        """Deselect current point."""
        self._selected_point.setBrush(self._default_brush)
        self._selected_point = None   
        self._lineEdits[0].setText("")
        self._lineEdits[1].setText("")


    def _remove_slice(self, index_time:tuple):
        """Remove plots at slice index"""
        index, time = index_time
        index_show = index
        # remove profiles
        if self.plotItems is not None:
            self.plotItems[index*2].removeItem(self.plots[index*2])
            self.plotItems[index*2+1].removeItem(self.plots[index*2+1])
            self.plots.pop(index*2)
            # after the first pop, index*2+1 becomes index*2
            self.plots.pop(index*2) 
            if index > int(len(self.plots)/2-1):
                index_show = index-1
            self.show_profile(index_show)
        # remove equilibrium
        if self.plotItem is not None:
            self.plotItem.removeItem(self.plots['shaping'][index*2]) # 4-points
            self.plotItem.removeItem(self.plots['shaping'][index*2+1]) # patch
            self.plots['shaping'].pop(index*2)
            self.plots['shaping'].pop(index*2) # idx*2+1 becomes idx*2 after the first pop
            self._fallback_title.pop(index)
            eq = self.idslist['equilibrium']
            eq.time_slice = np.delete(eq.time_slice, index)
            eq.time = np.delete(eq.time, index)
            
            self.slider.setMaximum(self.slider.maximum()-1)
            if index > len(eq.time)-1:
                index_show = index-1
            if self.slider.value() == index_show:
                self.slider.valueChanged.emit(index_show)
            else:
                self.slider.setValue(index_show)                


    def _insert_slice(self, index:int, time:float):
        """Copy contours or profile plots from index and append.

            Args:
                index(int): Index of slice to copy contours or profile from.
                time(float: Time value of the slice.)"""

        if self.plotItems is not None:
            # profiles
            idxs = [index*2, index*2+1]
            for idx in idxs:
                graph = self.plots[idx]
                pos = deepcopy(graph.pos)
                adj = deepcopy(graph.adjacency)
                opts = graph.scatter.opts
                new_graph = GraphItem(mode=self._mode)
                new_graph.setData(pos=pos, adj=adj, **opts)
                new_graph.scatter.sigClicked.connect(self.set_current_point)
                new_graph.index_values.connect(self.update_point_editable)
                self.plotItems.append(self.plotItems[idx])
                self.plotItems[-1].addItem(new_graph)
                self.plots.append(new_graph)
            self.show_profile(int(len(self.plots)/2)-1)

        if self.plotItem is not None:
            # contours
            if 'equilibrium' in self.idslist.keys():
                eq_ids = self.idslist['equilibrium']
                eq_ids.time = np.append(eq_ids.time, time)
                new_slice = deepcopy(eq_ids.time_slice[index]) 
                eq_ids.time_slice = np.append(eq_ids.time_slice, new_slice)
                ids_slice = imas.equilibrium()
                ids_slice.ids_properties.homogeneous_time = 1
                ids_slice.time.resize(1)
                ids_slice.time_slice.resize(1)
                ids_slice.time[0] = time
                ids_slice.time_slice[0] = new_slice
                self.slider.setMaximum(len(eq_ids.time)-1)
                self.plot_four_points_boundary(ids_slice, self.slider.maximum())

                slider_value = index
                     
                if self.slider.value() == slider_value:
                    self.slider.valueChanged.emit(slider_value)
                else:
                    self.slider.setValue(slider_value)


    @Slot(str)
    def XML2IDS(self, xml:str):
        """Create and return |IDS| from code |XML|.

        Args:
            xml (str): ``xml`` file content."""
        # remove spaces and indentations
        # https://stackoverflow.com/a/16919069
        def remove_blanks(node):
            for x in node.childNodes:
                if x.nodeType == Node.TEXT_NODE:
                    if x.nodeValue:
                        x.nodeValue = x.nodeValue.strip()
                elif x.nodeType == Node.ELEMENT_NODE:
                    remove_blanks(x)

        xmldom = minidom.parseString(xml)
        remove_blanks(xmldom)
        xmldom.normalize()
        xml_new = xmldom.toxml()

        root = ET.fromstring(xml_new)
        if 'Scenplint' in root.tag:
            self.root_scenplint = root
        else:
            return

        f6 = root.find("f6")
        
        if f6 is None:
            # received XML is incomplete
            return

        if self._old_table is None:
            # first time execution
            self.emit_xml() # passthrough

            table = f6.find("Table")
            self._old_table = table # prevent loading initial table again

            waveforms = {}
            for elem in table:
                arr_ET = table.find(elem.tag)
                waveforms[elem.tag] = [float(item.text) for item in arr_ET]
            ids = imas.equilibrium()
            ids.ids_properties.homogeneous_time = 1
            ids.time = np.array(waveforms['t'])
            ids.time_slice.resize(len(ids.time))
            for i,ts in enumerate(ids.time_slice):
                ts.boundary.type = 0
                ts.boundary.minor_radius = waveforms['a'][i]
                ts.boundary.geometric_axis.r = waveforms['R'][i]
                ts.boundary.geometric_axis.z = 0.0
                ts.boundary.elongation = waveforms['K'][i]
                ts.global_quantities.v_external = waveforms['Uext'][i]
            self.equilibrium.emit(ids)

        else:
            # add modified waveforms to modified XML parameters
            self.emit_xml()


    def prepare_xml(self):
        """Convert graph data into |XML| format and emit code input |XML|."""
        if self.sig_names is None:
            return
        if len(self.sig_names) != len(self.plots): # not waveforms
            return

        waveforms = {}
        for i,plot in enumerate(self.plots):
            sig = self.sig_names[i]
            if "boundary/minor_radius" in sig:
                waveforms['t'] = plot.scatter.getData()[0]
                waveforms['a'] = plot.scatter.getData()[1]
            elif "boundary/geometric_axis/r" in sig:
                waveforms['R'] = plot.scatter.getData()[1]
            elif "boundary/elongation" in sig:
                waveforms['K'] = plot.scatter.getData()[1]
            elif "global_quantities/v_external" in sig:
                waveforms['Uext'] = plot.scatter.getData()[1]

        if len(waveforms):
            # after moving the points, points are not sorted by time
            # sort by time
            time_sort = np.argsort(waveforms['t'])
            for key,val in waveforms.items():
                waveforms[key] = val[time_sort]

            # create ET from datapoints
            self._new_table = ET.Element("Table")
            for key,vals in waveforms.items():
                elem = ET.SubElement(self._new_table, key)
                for i,val in enumerate(vals.tolist()):
                    subelem = ET.SubElement(elem, key)
                    subelem.set('name', 'value#'+str(i))
                    subelem.text = str(val)
            self.emit_xml()
        

    # @Slot()
    # def export_xml(self):
    #     """Save code input |XML|s to disk."""

    #     xmls = self.prepare_xml()
    #     filenames = ['scenplint_input.xml', 'transmak_input.xml']

    #     #Open dialog window:
    #     savedir = QFileDialog.getExistingDirectory(self, "Save input files in directory:")
    #     if savedir=='':
    #         return

    #     for i,filename in enumerate(filenames):
    #         if xmls[i] is None:
    #             continue
    #         with open(os.path.abspath(os.path.join(savedir,filename)), mode='w') as f:
    #             f.write(xmls[i])


    def emit_xml(self):
        """Update and emit |XML| as string. """
        # remove old table and replace with modified one
        root = self.root_scenplint
        if self._new_table is not None:
            f6 = root.find("f6")
            old_table = f6.find("Table")
            f6.remove(old_table)
            f6.insert(0, self._new_table)
        xml = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
        self.scenplint_xml.emit(xml)
        self.finished.emit()


    @Slot(QObject)
    def linkXAxis(self, sender):
        self._plotWidget.setXLink(sender)


    def event(self, event: QEvent) -> None:
        """ Overloaded event.
        """
        if event.type() == QEvent.PolishRequest:
            if not self._connected:
                self.connect_to_pulse_editor.emit(self)
                self._connected = True
                return True
        return super().event(event)


    column_name = Property(str, getColumnName, setColumnName)
    plot_name = Property(str, getName, setName)
    shotrun = Property(int, getShotRun, setShotRun)
    units = Property(str, getUnits, setUnits)
    unitPrefix = Property(str, getUnitPrefix, setUnitPrefix)
    XLabel = Property(str, getXLabel, setXLabel)
    XUnits = Property(str, getXUnits, setXUnits)
    XUnitPrefix = Property(str, getXUnitPrefix, setXUnitPrefix)
    finished = Signal()
    """Signal(): |Signal| for indicating that a process in graph has finished. 
    """
    link = Signal(QObject)


class HoverablePlotDataItem(pg.PlotDataItem):
    """Custom pyqtgraph.PlotDataItem class to include custom curve."""
    
    def __init__(self, parent=None, *args, **kwargs):
        super(HoverablePlotDataItem, self).__init__(parent=parent,*args, **kwargs)
        self.setParent(parent)
        self.curve = HoverablePlotCurveItem(parent=self,*args, **kwargs)
        self.curve.setParentItem(self)
        # default super() init
        self.curve.sigClicked.connect(self.curveClicked)
        self.setCurveClickable(kwargs.get('clickable', False))
        self.setData(*args, **kwargs)
        

class HoverablePlotCurveItem(pg.PlotCurveItem):
    """Custom pyqtgraph.PlotCurveItem class to include hover events."""

    def __init__(self, parent=None, hoverable=True, *args, **kwargs):
        super(HoverablePlotCurveItem, self).__init__(parent=parent, *args, **kwargs)
        self.setParent(parent)
        self.hoverable = hoverable
        self.setAcceptHoverEvents(True)
        self.default_pen = self.opts['pen']
        
        if 'name' in kwargs.keys():
            name = kwargs['name']
        else:
            name = ''
        self.hover_info = pg.TextItem(text=name, color='k', border=pg.mkPen('k'), 
                                           fill=pg.mkBrush(color=(250, 250, 200)))
        self.hover_info.setZValue(10)
        self.hover_info.setVisible(False)
        self.vb = self.parent().parent().getViewBox()
        
        
    def hoverEvent(self, ev):
        if self.hoverable:
            if (hasattr(ev, '_scenePos') and 
                self.mouseShape().contains(ev.pos())):

                self.parent().setZValue(5) # set above all
                self.setPen(pg.mkPen('orange', width=2))
                self.hover_info.setVisible(True)

                r = self.hover_info.textItem.boundingRect()
                pts = self.vb.mapSceneToView(r).toList()
                yoffset = pts[1].y()-pts[2].y()
                x,y = ev.pos().toTuple()
                self.hover_info.setPos(x,y+yoffset)
                
            else:
                self.parent().setZValue(1)
                self.setPen(self.default_pen)
                self.hover_info.setVisible(False)


class GraphItem(pg.GraphItem):
    """From pyqtgraph/examples/CustomGraphItem.py"""

    positions = Signal(object)
    index_values = Signal(tuple)

    def __init__(self, mode=None, hoverable=False):
        self.dragPoint = None
        self.dragOffset = None
        self.textItems = []
        self.mode = mode
        pg.GraphItem.__init__(self, hoverable=hoverable)
        self.scatter.setParent(self)
        
    def setData(self, **kwds):
        self.text = kwds.pop('text', [])
        self.data = kwds
        if 'pos' in self.data:
            npts = self.data['pos'].shape[0]
            self.data['data'] = np.empty(npts, dtype=[('index', int)])
            self.data['data']['index'] = np.arange(npts)
        self.setTexts(self.text)
        self.updateGraph()
        
    def setTexts(self, text):
        for i in self.textItems:
            i.scene().removeItem(i)
        self.textItems = []
        for t in text:
            item = pg.TextItem(t)
            self.textItems.append(item)
            item.setParentItem(self)

    def updateGraph(self):
        for i,item in enumerate(self.textItems):
            item.setPos(*self.data['pos'][i])

        if 'symbolBrush' in self.data.keys():
            if len(self.scatter.points()):
                self.data['symbolBrush'] = [pt.brush() for pt in self.scatter.points()]

        if 'adj' in self.data.keys():
            # update node connections so that nodes look sorted by X values
            nodex = np.asarray([ [i, self.data['pos'][i][0]] for i in range(len(self.data['pos'])) ])
            nodex = nodex[nodex[:, 1].argsort()]
            self.data['adj'] = np.asarray([ [int(nodex[i,0]), int(nodex[i+1,0])] for i in range(len(nodex[:,0])-1) ])

        pg.GraphItem.setData(self, **self.data)

    def updateBrush(self, index, brush):
        """Update brush of point at index."""
        self.data['symbolBrush'][index] = brush

    def updateNodeX(self, index_values:tuple):
        """Tuple containing index and new X value of node."""
        ind, vals = index_values
        self.data['pos'][ind][0]= vals[0]
        self.updateGraph()

    def updateNodeY(self, index_values:tuple):
        """Tuple containing index and new Y value of node."""
        ind, vals = index_values
        self.data['pos'][ind][1]= vals[1]
        self.updateGraph()

    def updateNodeXY(self, index_values:tuple):
        """Tuple containing index and new X and Y values of node."""
        ind, vals = index_values
        self.data['pos'][ind][0], self.data['pos'][ind][1]= vals[0], vals[1]
        self.updateGraph()
        self.emit_positions(self.data['pos'])

    def emit_positions(self, pos):
        self.positions.emit(pos)

    def mouseDragEvent(self, ev):
        if ev.button() != Qt.MouseButton.LeftButton:
            ev.ignore()
            return
    
        if self.mode.text() != 'move':
            return
        
        if ev.isStart():
            # We are already one step into the drag.
            # Find the point(s) at the mouse cursor when the button was first 
            # pressed:
            pos = ev.buttonDownPos()
            pts = self.scatter.pointsAt(pos)
            if len(pts) == 0:
                ev.ignore()
                return
            self.dragPoint = pts[0]
            ind = pts[0].data()[0]
            self.dragOffset = self.data['pos'][ind] - pos

        elif ev.isFinish():
            # emit new positions of all nodes
            self.emit_positions(self.data['pos'])
            self.dragPoint = None
            return
        else:
            if self.dragPoint is None:
                ev.ignore()
                return

        # update position
        ind = self.dragPoint.data()[0]
        self.data['pos'][ind] = ev.pos() + self.dragOffset

        # emit index and new position of current node
        self.index_values.emit(tuple([ind, self.data['pos'][ind]]))

        self.updateGraph()
        ev.accept()


    

if __name__ == '__main__':
    import sys
    #from PySide6.QtWidgets import QApplication
    from PySide6.QtUiTools import loadUiType
    from pyqtgraph.Qt import mkQApp

    uiclass, baseclass = loadUiType("../plugins/pyside6-designer/graph.ui")

    class MainWindow(uiclass, baseclass):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)

    app = QApplication(sys.argv)
    # https://pyqtgraph.readthedocs.io/en/latest/getting_started/how_to_use.html#hidpi-displays
    #app = mkQApp(sys.argv)

    window = MainWindow()
    #window.graph.setXLink(window.graph_2)
    window.show()
    sys.exit(app.exec())
