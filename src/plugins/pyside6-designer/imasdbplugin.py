from imasdb import IMASDB, Backend

from PySide6.QtGui import QAction, QIcon
from PySide6.QtDesigner import (QExtensionManager, QExtensionFactory, 
    QPyDesignerTaskMenuExtension, QDesignerFormWindowInterface)
from PySide6.QtCore import QObject, QEvent, Slot
from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtUiTools import loadUiType 
import imas
import pdsicons
from shiboken6 import re

class IMASDBTaskMenu(QPyDesignerTaskMenuExtension):
    def __init__(self, actor, parent):
        super().__init__(parent)
        self._actor = actor
        self._edit_state_action = QAction('Edit IMASDB properties...', parent)
        self._edit_state_action.triggered.connect(self._edit_state)
    def taskActions(self):
        return [self._edit_state_action]

    def preferredEditAction(self):
        return self._edit_state_action

    @Slot()
    def _edit_state(self):  
        import os
        for dir in os.getenv('PYSIDE_DESIGNER_PLUGINS').split(':'):
            file = os.path.join(dir, 'imasdb-menu.ui')
            if os.path.exists(file):
                uiclass, baseclass = loadUiType(file)
                break
        
        class DialogWindow(uiclass, baseclass):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.setupUi(self)

            def setupVars(self, actor):
                if pulse := actor.property('pulse'):
                    (shot, run, occurrence, username, database, backend, data_version) = eval(pulse)
                    self.lineEdit_shot.setText(str(shot))
                    self.lineEdit_shot.textChanged.connect(self.update_uri)
                    self.lineEdit_run.setText(str(run))
                    self.lineEdit_run.textChanged.connect(self.update_uri)
                    self.lineEdit_occurrence.setText(str(occurrence))
                    self.lineEdit_username.setText(str(username))
                    self.lineEdit_username.textChanged.connect(self.update_uri)
                    self.lineEdit_database.setText(str(database))
                    self.lineEdit_database.textChanged.connect(self.update_uri)
                    self.lineEdit_data_version.setText(data_version)
                    self.lineEdit_data_version.textChanged.connect(self.update_uri)
                    backend_name = Backend(backend).name
                    for i in range(self.comboBox_backend.count()):
                        if backend_name == self.comboBox_backend.itemText(i):
                            self.comboBox_backend.setCurrentIndex(i)
                            break
                    self.comboBox_backend.currentIndexChanged.connect(self.update_uri)
                    if actor.property('uri'):
                        self.plainTextEdit_uri.setPlainText(actor.property('uri'))

            @Slot()
            def update_uri(self):
                pulse = dialog.lineEdit_shot.text()
                run = dialog.lineEdit_run.text()
                user = dialog.lineEdit_username.text()
                database = dialog.lineEdit_database.text()
                backend = dialog.comboBox_backend.currentText().lower()
                version = dialog.lineEdit_data_version.text()
                uri = f'imas:{backend}?user={user};pulse={pulse};run={run};database={database};version={version}'
                print('Updated URI', uri)
                self.plainTextEdit_uri.setPlainText(uri)



        dialog = DialogWindow()
        dialog.setupVars(self._actor)


        if dialog.exec() == QDialog.Accepted:
            if self._actor.property('pulse'):
                shot = int(dialog.lineEdit_shot.text())
                run = int(dialog.lineEdit_run.text())
                occurrence = int(dialog.lineEdit_occurrence.text())
                username = dialog.lineEdit_username.text()
                database = dialog.lineEdit_database.text()
                backend = dialog.comboBox_backend.currentText()
                data_version = dialog.lineEdit_data_version.text()
                backend = Backend[backend].value
                pulse = (shot, run, occurrence, username, database, backend, data_version)
                uri = dialog.plainTextEdit_uri.toPlainText()
                form = QDesignerFormWindowInterface.findFormWindow(self._actor)
                form.cursor().setProperty('pulse', f'{pulse}')
                form.cursor().setProperty('uri', uri)
                self._actor.setProperty('pulse', f'{pulse}')
                self._actor._set_pulse_layout(self._actor._eval_pulse_property())
                self._actor.setProperty('uri', uri)
                self._actor._uri.setPlainText(uri)
                form.emitSelectionChanged()



class IMASDBTaskMenuFactory(QExtensionFactory):
    def __init__(self, extension_manager):
        super().__init__(extension_manager)

    @staticmethod
    def task_menu_iid():
        return 'org.qt-project.Qt.Designer.TaskMenu'

    def createExtension(self, object, iid, parent):
        if iid != IMASDBTaskMenuFactory.task_menu_iid():
            return None
        if object.__class__.__name__ != 'IMASDB':
            return None
        return IMASDBTaskMenu(object, parent)

### end menu



from PySide6.QtGui import QIcon
from PySide6.QtDesigner import (QExtensionManager,
    QDesignerCustomWidgetInterface)


DOM_XML = """
<ui language='c++' displayname='IMAS DB'>
    <widget class='IMASDB' name='imasdb'>
        <property name='geometry'>
            <rect>
                <width>200</width>
                <height>270</height>
            </rect>
        </property>
        <property name='uri'>
            <string notr='true' comment='IMAS URI for the data entry it used in DBEntry'
            extracomment='URI starts with imas:'>imas:hdf5?user=public;pulse=123347;run=1;database=ITER;version=3</string>
        </property>
        <property name='pulse'>
            <string notr='true' comment='(pulse, run, occurrence, usename, database, backend, data_version)'
            extracomment='Tuple of IDS parameters'>(123347, 1, 0, 'public', 'ITER', 13, '4')</string>
        </property>
        <property name='title'>
            <string notr='true' comment='Text for widget title.'
            extracomment='Add this to widget title'>IMAS DB</string>
        </property>
        <property name='button'>
            <string notr='true' comment='Title for Start button'
            extracomment='Add this to button'>Read IMAS DB</string>
        </property>
        <property name="start_counter">
            <bool>false</bool>
        </property>
        <property name="show_pulse">
            <bool>true</bool>
        </property>
        <property name="show_uri">
            <bool>true</bool>
        </property>
        <property name="show_log">
            <bool>true</bool>
        </property>
        <property name="show_button">
            <bool>true</bool>
        </property>
        <property name="show_title">
            <bool>true</bool>
        </property>
        <property name="show_enable">
            <bool>false</bool>
        </property>
        <property name='toolTip'>	
                <string>Opens or creates IMAS database and sends/receives QObject IDSs (get/put)</string>
        </property>
        <property name='whatsThis'>	
                <string>This actor is part of IMAS workflow</string>
        </property>
    </widget>
</ui>
"""

class IMASDBPlugin(QDesignerCustomWidgetInterface):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._form_editor = None
        self._widget = None

    def createWidget(self, parent):
        self._widget = IMASDB(parent)
        return self._widget

    def domXml(self):
        return DOM_XML

    def group(self):
        return 'IMAS'

    def icon(self):
        if self._widget:
            return QIcon(self._widget.icon)
        else:
            return QIcon()

    def includeFile(self):
        return 'imasdb'

    def initialize(self, form_editor):
        self._form_editor = form_editor
        
        manager = form_editor.extensionManager()
        iid = IMASDBTaskMenuFactory.task_menu_iid()
        manager.registerExtensions(IMASDBTaskMenuFactory(manager), iid)
        

    def isContainer(self):
        return False

    def isInitialized(self):
        return self._form_editor is not None

    def name(self):
        return 'IMASDB'

    def toolTip(self):
        return 'Opens or creates IMAS database and sends/receives QObject IDSs (get/put)'

    def whatsThis(self):
        return 'This actor is part of PDS-WF workflow'
        #return self.toolTip()



    