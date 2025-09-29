from {{ name }} import {{ class_name }}
{% if include_menu %}
from PySide6.QtGui import QAction
from PySide6.QtDesigner import (QExtensionManager, QExtensionFactory, 
    QPyDesignerTaskMenuExtension, QDesignerFormWindowInterface)
from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtUiTools import loadUiType 

class {{ class_name }}TaskMenu(QPyDesignerTaskMenuExtension):
    def __init__(self, actor, parent):
        super().__init__(parent)
        self._actor = actor
        self._edit_state_action = QAction('Edit {{ class_name }} properties...', None)
        self._edit_state_action.triggered.connect(self._edit_state)
    def taskActions(self):
        return [self._edit_state_action]

    def preferredEditAction(self):
        return self._edit_state_action

    @Slot()
    def _edit_state(self):  
        import os
        for dir in os.getenv('PYSIDE_DESIGNER_PLUGINS').split(':'):
            file = os.path.join(dir, '{{ name }}-menu.ui')
            if os.path.exists(file):
                uiclass, baseclass = loadUiType(file)
                break
        
        class DialogWindow(uiclass, baseclass):
            def __init__(self):
                super().__init__()
                self.setupUi(self)


            def setupVars(self, actor):
                (shot, run, username, database, backend) = eval(actor.property('pulse'))
                self.lineEdit_shot.setText(str(shot))
                self.lineEdit_run.setText(str(run))
                self.lineEdit_username.setText(str(username))
                for i in range(self.comboBox_backend.count()):
                    if backend == self.comboBox_backend.itemText(i):
                        self.comboBox_backend.setCurrentIndex(i)
                        break


        dialog = DialogWindow()
        dialog.setupVars(self._actor)

        if dialog.exec() == QDialog.Accepted:
            shot = int(dialog.lineEdit_shot.text())
            run = int(dialog.lineEdit_run.text())
            username = dialog.lineEdit_username.text()
            database = dialog.lineEdit_database.text()
            backend = dialog.comboBox_backend.currentText()
            pulse = (shot, run, username, database, backend)
            form = QDesignerFormWindowInterface.findFormWindow(self._actor)
            form.cursor().setProperty('pulse', f'{pulse}')

            form.emitSelectionChanged()
            #form.currentChanged().connect(self._actor.replot())
            #self._actor.replot()

            #for dpn in self._actor.dynamicPropertyNames():
            #    name = bytes(dpn).decode()
            #    print(name,self._actor.property(name))


class {{ class_name }}TaskMenuFactory(QExtensionFactory):
    def __init__(self, extension_manager):
        super().__init__(extension_manager)

    @staticmethod
    def task_menu_iid():
        return 'org.qt-project.Qt.Designer.TaskMenu'

    def createExtension(self, object, iid, parent):
        if iid != {{ class_name }}TaskMenuFactory.task_menu_iid():
            return None
        if object.__class__.__name__ != '{{ class_name }}':
            return None
        return {{ class_name }}TaskMenu(object, parent)

### end menu
{% endif %}


from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtDesigner import (QExtensionManager,
    QDesignerCustomWidgetInterface)
import pdsicons

DOM_XML = """
{{ dom_xml }}
"""


class {{ class_name }}Plugin(QDesignerCustomWidgetInterface):
    def __init__(self):
        super().__init__()
        self._form_editor = None
        self._widget = None

    def createWidget(self, parent):
        self._widget = {{ class_name }}(parent)
        return self._widget

    def domXml(self):
        return DOM_XML

    def group(self):
        return '{{ group }}'

    def icon(self):
        if self._widget:
            return QIcon(self._widget.icon)
        else:
            return QIcon()

    def includeFile(self):
        return '{{ name }}'

    def initialize(self, form_editor):
        self._form_editor = form_editor
        {% if include_menu %}
        manager = form_editor.extensionManager()
        iid = {{ class_name }}TaskMenuFactory.task_menu_iid()
        manager.registerExtensions({{ class_name }}TaskMenuFactory(manager), iid)
        {% endif %}

    def isContainer(self):
        return False

    def isInitialized(self):
        return self._form_editor is not None

    def name(self):
        return '{{ class_name }}'

    def toolTip(self):
        return '{{ toolTip }}'

    def whatsThis(self):
        return '{{ whatsThis }}'
        #return self.toolTip()
