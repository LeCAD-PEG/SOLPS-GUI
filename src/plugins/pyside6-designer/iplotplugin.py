from iplot import IPlot
from iplotlib.impl.matplotlib.qt.qtMatplotlibCanvas import QtMatplotlibCanvas

# Dialog menu 

from PySide6.QtGui import QAction, QIcon 
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, \
    QTableWidget, QTableWidgetItem, QHeaderView, QWidget, QSizePolicy
from PySide6.QtDesigner import (QExtensionManager, QExtensionFactory, 
    QPyDesignerTaskMenuExtension, QDesignerFormWindowInterface)
from PySide6.QtCore import QEvent, Slot, Signal, QSize
import pdsicons


class IPlotTaskMenu(QPyDesignerTaskMenuExtension):

    def __init__(self, actor, parent):
        super().__init__(parent)
        self._actor = actor
        self._edit_state_action = QAction('Edit IPlot Canvas...', None)
        self._edit_state_action.triggered.connect(self._edit_state)
        # Right click on the widget will connect dynamic properties and canvas redraw
        form = QDesignerFormWindowInterface.findFormWindow(actor)
        form.changed.connect(actor.create_canvas)
        

    def taskActions(self):
        return [self._edit_state_action]

    def preferredEditAction(self):
        return self._edit_state_action

    @Slot()
    def _edit_state(self):
        from PySide6.QtUiTools import loadUiType    
        import os
        for dir in os.getenv('PYSIDE_DESIGNER_PLUGINS').split(':'):
            file = os.path.join(dir, 'iplot-menu.ui')
            if os.path.exists(file):
                uiclass, baseclass = loadUiType(file)
                break
        
        class DialogWindow(uiclass, baseclass):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.setupUi(self)

            def setupVars(self, actor):

                ## Read the information from Dynamic Properties section
                ## and update the Dialog window accordingly

                # Update pulse information
                if actor.property('pulse'):
                    (shot, run, occurrence, username, database, backend) = \
                                            eval(actor.property('pulse'))
                    self.lineEdit_shot.setText(str(shot))
                    self.lineEdit_run.setText(str(run))
                    self.lineEdit_occurrence.setText(str(occurrence))
                    self.lineEdit_username.setText(str(username))
                    self.lineEdit_database.setText(database)
                    for i in range(self.comboBox_backend.count()):
                        if backend == self.comboBox_backend.itemText(i):
                            self.comboBox_backend.setCurrentIndex(i)
                            break
                else:
                    self.lineEdit_shot.setText('')
                    self.lineEdit_shot.setEnabled(False)
                    self.lineEdit_run.setText('')
                    self.lineEdit_run.setEnabled(False)
                    self.lineEdit_occurrence.setText('')
                    self.lineEdit_occurrence.setEnabled(False)
                    self.lineEdit_username.setText('')
                    self.lineEdit_username.setEnabled(False)
                    self.lineEdit_database.setText('')
                    self.lineEdit_database.setEnabled(False)
                    self.comboBox_backend.setEnabled(False)
                
                # Update rows and columns of the plot window
                self.spinBox_rows.setValue(actor.property('rows') or 1)
                self.spinBox_cols.setValue(actor.property('cols') or 1)

                # Update plot signal names and plotting info
                ids_signals = actor.property('ids_signals')
                ids_signals = ids_signals.split('\n')
                for i,signal in enumerate(ids_signals):
                    # remove trailing spaces or tabs
                    ids_signals[i] = ids_signals[i].strip(" \t")
                # remove empty entries 
                ids_signals = [x for x in ids_signals if x!='']
                nsig = len(ids_signals)
                self.tableWidget.setRowCount(nsig)
                for i in range(nsig):
                     ids_info = ids_signals[i].split(',')
                     for j in range(4):
                        newItem = QTableWidgetItem()
                        newItem.setText(ids_info[j].strip())
                        self.tableWidget.setItem(i, j, newItem)

                # Set proper tableWidget size
                header = self.tableWidget.horizontalHeader()
                header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
                header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
                header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
                header.setSectionResizeMode(3, QHeaderView.Stretch)

                self.pushButton.clicked.connect(self.insert_row)

            def insert_row(self):
                row = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row)

        dialog = DialogWindow()
        dialog.setupVars(self._actor)

        if dialog.exec() == QDialog.Accepted:
            # Everything here activates when button "Apply" is clicked.
            # For changes on window creation, see setupVars of DialogWindow 
            form = QDesignerFormWindowInterface.findFormWindow(self._actor)
            # Update dynamic properties with values in window
            if self._actor.property('pulse'):
                shot = int(dialog.lineEdit_shot.text())
                run = int(dialog.lineEdit_run.text())
                occurrence = int(dialog.lineEdit_occurrence.text())
                username = dialog.lineEdit_username.text()
                database = dialog.lineEdit_database.text()
                backend = dialog.comboBox_backend.currentText()
                pulse = (shot, run, occurrence, username, database, backend)
                form.cursor().setProperty('pulse', f'{pulse}')
            
            form.cursor().setProperty('rows', dialog.spinBox_rows.value())
            form.cursor().setProperty('cols', dialog.spinBox_cols.value())

            # compute total rows and columns from table
            tot_rows = 0
            tot_cols = 0
            for row in range(dialog.tableWidget.rowCount()):
                # Empty or incomplete rows will be discarded
                try:
                    stack = dialog.tableWidget.item(row,1).text()
                    col = int(stack.split('.')[0])
                    row = int(stack.split('.')[1])
                    rs = int(dialog.tableWidget.item(row,3).text())
                    tot_rows = max([tot_rows, row+rs-1])
                    cs = int(dialog.tableWidget.item(row,2).text())
                    tot_cols = max([tot_cols, col+cs-1])
                except: pass

            # update dynamic properties of rows and columns
            form.cursor().setProperty('rows', max([tot_rows, self._actor.property('rows')]))
            form.cursor().setProperty('cols', max([tot_cols, self._actor.property('cols')]))
            # create the complex dynamic property for signals, as csv string
            ids_signals = []
            for row in range(dialog.tableWidget.rowCount()):
                # Empty or incomplete rows will be discarded
                try:
                    newline = []
                    for col in range(dialog.tableWidget.columnCount()):
                        value = dialog.tableWidget.item(row,col).text()
                        if value != '':
                            newline.append(value)
                        else:
                            break
                    if len(newline):
                        ids_signals.append(newline)
                except: pass
            property_ids_signals = f'{ids_signals}'
            property_ids_signals = property_ids_signals.replace('[[' , '')
            property_ids_signals = property_ids_signals.replace("['" , '')
            property_ids_signals = property_ids_signals.replace('], ', '\n')
            property_ids_signals = property_ids_signals.replace("'"  , '')
            property_ids_signals = property_ids_signals.replace(']]' , '')
            form.cursor().setProperty('ids_signals', f'{property_ids_signals}')

            form.emitSelectionChanged()


class IPlotTaskMenuFactory(QExtensionFactory):
    def __init__(self, extension_manager):
        super().__init__(extension_manager)

    @staticmethod
    def task_menu_iid():
        return 'org.qt-project.Qt.Designer.TaskMenu'

    def createExtension(self, object, iid, parent):
        if iid != IPlotTaskMenuFactory.task_menu_iid():
            return None
        if object.__class__.__name__ != 'IPlot':
            return None
        return IPlotTaskMenu(object, parent)

### end menu



from PySide6.QtGui import QIcon
from PySide6.QtDesigner import (QExtensionManager,
    QDesignerCustomWidgetInterface)


DOM_XML = """
<ui language='c++' displayname='IPlot'>
    <widget class='IPlot' name='iplot'>
        <property name='geometry'>
            <rect>
                <x>0</x>
                <y>0</y>
                <width>500</width>
                <height>500</height>
            </rect>
        </property>
        <property name='pulse'>
            <string notr='true' comment='(shot, run, occurrence, usename, database, backend)'
            extracomment='Tuple of IDS parameters'>(130012, 2, 0, 'public', 'ITER', 'MDSPLUS')</string>
        </property>
        <property name='title'>
            <string>IDS plot</string>
        </property>
        <property name="rows">
            <number>1</number>
        </property>
        <property name="cols">
            <number>1</number>
        </property>
        <property name="ids_signals">
           <string notr='true' comment='IDS path, col.row.stack, row span, col span)'
            extracomment='CSV of ids signals describing layout of the plots'>summary/global_quantities/ip/value, 1.1, 1, 1
summary/heating_current_drive/ec[0]/power/value, 1.2.1, 1, 1
summary/heating_current_drive/nbi[0]/power/value, 1.2.1, 1, 1
summary/global_quantities/b0/value, 1.3, 1, 1
             </string>
        </property>
        <property name='legend'>
            <bool>false</bool>
        </property>
    </widget>
</ui>
"""

# By injecting the following event handler to the widget at the
# design time, right clicking the widget for dynamic properties to be
# handled is not needed as with every chance of any dynamic property
# the canvas is created. See settattr() in createWidget()

def dynamic_properties_event(self, received : QEvent):
    # To allow QEvent.DynamicPropertyChange to create canvas only after QEvent.Show
    if received.type() == QEvent.Show: 
        if self._allowDynamicPropertyChange == False:
            self.create_canvas()
        self._allowDynamicPropertyChange = True
    if received.type() == QEvent.DynamicPropertyChange and self._allowDynamicPropertyChange:
        name = bytes(received.propertyName()).decode()
        # To prevent QEvent.DynamicPropertyChange to create canvas during 
        # typing a string property value in Designer
        if isinstance(self.property(name), str) or self.property(name)==None:
            self._trigger_canvas = True
        else:
            self.create_canvas()
    # To trigger creating canvas when finished typing
    if (received.type() not in [QEvent.CursorChange, QEvent.DynamicPropertyChange] 
        and self._trigger_canvas):
        self._trigger_canvas = False
        self.create_canvas()
    return True



class IPlotPlugin(QDesignerCustomWidgetInterface):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._form_editor = None
        self._widget = None
        self.show_event_received = False

    def createWidget(self, parent):
        setattr(IPlot, 'event', dynamic_properties_event)
        self._widget = IPlot(parent)
        return self._widget

    def domXml(self):
        return DOM_XML

    def group(self):
        return 'IMAS Plot'

    def icon(self):
        if self._widget:
            return QIcon(self._widget.icon)
        else:
            return QIcon()

    def includeFile(self):
        return 'iplot'

    def initialize(self, form_editor):
        self._form_editor = form_editor 
        manager = form_editor.extensionManager()
        iid = IPlotTaskMenuFactory.task_menu_iid()
        manager.registerExtensions(IPlotTaskMenuFactory(manager), iid)  

    def isContainer(self):
        return False

    def isInitialized(self):
        return self._form_editor is not None

    def name(self):
        return 'IPlot'

    def toolTip(self):
        return 'IplotLib'

    def whatsThis(self):
        return self.toolTip()


    