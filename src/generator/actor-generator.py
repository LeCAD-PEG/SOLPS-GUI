# https://doc.qt.io/qtforpython/tutorials/basictutorial/uifiles.html#custom-widgets-in-qt-designer
import sys
import os
import pathlib
import xml.etree.ElementTree as ET
from PySide6.QtCore import  Qt, Slot, QFile, QSettings, Signal
from PySide6.QtGui import QPixmap, QStandardItemModel, QStandardItem, QIcon
from jinja2 import Environment, FileSystemLoader, Template
from PySide6.QtWidgets import (QApplication, QFileDialog, QTreeView, 
                            QDialog, QDialogButtonBox, QVBoxLayout)
from PySide6.QtUiTools import loadUiType
from numpy.core.defchararray import isspace

uiclass, baseclass = loadUiType(__file__[:-2]+'ui')

class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Warning!")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Actor already exists. Overwrite?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class MainWindow(uiclass, baseclass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.actionSave.triggered.connect(self.__save)
        self.lineEdit_actor_display_name.textChanged.connect(
            self.__actor_display_name_changed)
        self.actionLoad.triggered.connect(self.__load)
        self.actionDelete.triggered.connect(self.__delete)
        self.actionGit.triggered.connect(self.__git)
        #self.actionPreview.triggered.connect(self.__preview)  #### PART OF UNUSED PREVIEW MENU OPTION
        self._show_icon(self.lineEdit_icon_path.text())
        self.icontree.icon_path.connect(self._show_icon)
        self.actionSaveIcon.triggered.connect(self.__saveIcon)
        self.buttonActorDir.clicked.connect(self.__setActorDir)
        self.buttonPluginDir.clicked.connect(self.__setPluginDir)

        self.qsettings = QSettings('ITER', 'SOLPS')
        if self.qsettings.contains("actor directory"):
            self.lineEdit_actor_directory.setText(self.qsettings.value("actor directory"))
        if self.qsettings.contains("plugin directory"): 
            self.lineEdit_plugin_directory.setText(self.qsettings.value("plugin directory"))
        if self.qsettings.contains("new icon directory"): 
            self.new_icon_directory = self.qsettings.value("new icon directory")
        else:
            self.new_icon_directory = ""        


    @Slot(str)
    def _show_icon(self, icon_path:str):
        icon = QIcon(QPixmap(icon_path))
        self.setWindowIcon(icon)


    def __save(self):
        if not QFile.exists(self.lineEdit_actor_directory.text()) or \
           not QFile.exists(self.lineEdit_plugin_directory.text()):
            self.statusbar.showMessage(
                "Error: One of selected directories does not exists.", 2000)
            return
        if QFile.exists(os.path.join(self.lineEdit_actor_directory.text(), 
                    self.lineEdit_class_name.text().lower() + '.py')):
            dlg = CustomDialog()
            if not dlg.exec():
                return 
        
        data = {
            'class_name': self.lineEdit_class_name.text(),
            'base_class': self.comboBox_base_class.currentText(),
            'name': self.lineEdit_class_name.text().lower(),
            'display_name': self.lineEdit_actor_display_name.text(),
            'include_menu': self.checkBox_include_menu.isChecked(),
            'simple_actor': self.checkBox_simple_actor.isChecked(),
            'state': self.checkBox_state.isChecked(),
            'size_hints': self.checkBox_size_hints.isChecked(),
            'dom_xml': self.plainTextEdit_dom_xml.toPlainText(),
            'icon_path': self.lineEdit_icon_path.text(),
            'group': self.comboBox_group.currentText(),
            'toolTip': self.lineEdit_toolTip.text(),
            'whatsThis': self.plainTextEdit_whatsThis.toPlainText(),
            'designer_localPath': os.path.relpath( 
                self.lineEdit_plugin_directory.text(),self.lineEdit_actor_directory.text())
        }

        self.create_actor(data)
        self.statusbar.showMessage(
            f"Source files for the actor are saved in .../"
            f"{os.path.basename(self.lineEdit_actor_directory.text())} "
            f"and .../{os.path.basename(self.lineEdit_plugin_directory.text())}", 5000)

        self.qsettings.setValue("actor directory",
                                self.lineEdit_actor_directory.text())
        self.qsettings.setValue("plugin directory",
                                self.lineEdit_plugin_directory.text())
        return data

    #### PART OF UNUSED PREVIEW MENU OPTION
    # def __preview(self):       
    #     data = self.__save()
    #     cmd = "import sys\nsys.path.append('../designer')\n"
    #     cmd += "import sys\nsys.path.append('../actors')\n"
    #     cmd += f"key=\"{data['name']}plugin\"; delete = False\n"
    #     cmd += "for key, value in sys.modules.items():\n"
    #     cmd += "  if key in sys.modules.keys(): delete = True\n"
    #     cmd += "if delete: del sys.modules[key]\n"
    #     cmd += f"from {data['name']}plugin import {data['class_name']}Dialog\n" 
    #     cmd += f"m = {data['class_name']}Dialog(self); m.show()"
    #     exec(cmd)


    def __load(self):
        file_name = QFileDialog.getOpenFileName(self,
        "Open Image", "templates", "Image Files (*.xpm)")
        with open(file_name[0], 'r') as f:
            data = f.read()
            begin = data.find('{')+2 # skip newline too
            end = data.rfind('}')
            pixmap = data[begin:end]
            self.plainTextEdit_icon_text.setPlainText(pixmap)
            self._show_icon()

    def __delete(self):
        name = self.lineEdit_class_name.text().lower()
        output_dir = self.lineEdit_actor_directory.text()
        if os.path.exists(os.path.join(output_dir, name+'.py')):
            os.remove(os.path.join(output_dir, name+'.py'))
        output_dir = self.lineEdit_plugin_directory.text()
        if os.path.exists(os.path.join(output_dir, name+'plugin.py')):
            os.remove(os.path.join(output_dir, name+'plugin.py'))
        if os.path.exists(os.path.join(output_dir, 'register'+name+'.py')):
            os.remove(os.path.join(output_dir, 'register'+name+'.py'))
        if os.path.exists(os.path.join(output_dir, name+'.ui')):
            os.remove(os.path.join(output_dir, name+'.ui'))
        if os.path.exists(os.path.join(output_dir, name+'-menu.ui')):
            os.remove(os.path.join(output_dir, name+'-menu.ui'))
        self.statusbar.showMessage(f"Files for the actor removed in "
            f".../{os.path.basename(self.lineEdit_actor_directory.text())} "
            f"and .../{os.path.basename(self.lineEdit_plugin_directory.text())} " \
            "(if existed)", 5000)


    def __git(self):
        name = self.lineEdit_class_name.text().lower()
        output_dir = self.lineEdit_actor_directory.text()
        file_list = os.path.join(output_dir, name+'.py')
        output_dir = self.lineEdit_plugin_directory.text()
        if not self.checkBox_simple_actor.isChecked():
            file_list += ' ' + os.path.join(output_dir, name+'plugin.py')
        file_list += ' ' + os.path.join(output_dir, 'register'+name+'.py')
        file_list += ' ' + os.path.join(output_dir, name+'.ui')
        if self.checkBox_include_menu.isChecked():
            file_list += ' ' + os.path.join(output_dir, name+'-menu.ui')
        os.system('git add ' + file_list)
        self.statusbar.showMessage(f"git add {file_list}", 2000)

    def __saveIcon(self):
        input_file = self.lineEdit_icon_path.text()
        if not input_file:
            self.statusbar.showMessage(
                f"No icon selected", 2000)
            return

        #Open dialog window:
        file = QFileDialog.getSaveFileName(
            self, "Save Icon as...", self.new_icon_directory, filter='*.png') 
        if file and file[0]:
            if not file[0].endswith('.png'):
                file_name = file[0] + '.png'
            else:
                file_name = file[0]
            try:
                output_dir = os.path.split(file[0])[0]
                if QFile.exists(file_name):
                    QFile.remove(file_name)
                QFile.copy(input_file, file_name)        
                self.statusbar.showMessage(
                            f"Icon is saved in .../"
                            f"{os.path.basename(output_dir)}", 2000)
                self.qsettings.setValue("new icon directory", output_dir)
            except Exception as e:
                box = QMessageBox()
                box.setIcon(QMessageBox.Critical)
                box.setText(
                    f"Error {str(e)}: cannot save icon in {output_dir}.")
                box.exec_()


    def __setActorDir(self):
        #Open dialog window:
        file = QFileDialog.getExistingDirectory(self, 'Select Folder...', 
                                self.lineEdit_actor_directory.text())
        if not file:
            return
        self.lineEdit_actor_directory.setText(file)
        self.qsettings.setValue("actor directory",
                                self.lineEdit_actor_directory.text())


    def __setPluginDir(self):   
        #Open dialog window:
        file = QFileDialog.getExistingDirectory(self, 'Select Folder...', 
                                self.lineEdit_plugin_directory.text())
        if not file:
            return
        self.lineEdit_plugin_directory.setText(file)
        self.qsettings.setValue("plugin directory",
                                self.lineEdit_plugin_directory.text())
        


    def __actor_display_name_changed(self, value):
        value = value.replace(' ', '')
        self.lineEdit_class_name.setText(value)

    def create_actor(self, data: dict):
        generator_dir = pathlib.Path(__file__).parent.resolve()
        file_loader = FileSystemLoader(os.path.join(generator_dir,'templates'))
        env = Environment(loader=file_loader)

        # DOM_XML can contain {{ replacements }} too.
        template = Template(data['dom_xml'])
        data['dom_xml'] = template.render(data)

        name = data['name']
        output_dir = self.lineEdit_actor_directory.text()
        template = env.get_template('actor.py')
        with open(os.path.join(output_dir, name+'.py'), 'w+') as f:
            f.write(template.render(data))

        
        output_dir = self.lineEdit_plugin_directory.text()
        if not self.checkBox_simple_actor.isChecked():
            template = env.get_template('actorplugin.py')
            with open(os.path.join(output_dir, name+'plugin.py'), 'w+') as f:
                f.write(template.render(data))

        template = env.get_template('registeractor.py')
        with open(os.path.join(output_dir, 'register'+name+'.py'), 'w+') as f:
            f.write(template.render(data))

        template = env.get_template('actor.ui')
        with open(os.path.join(output_dir, name+'.ui'), 'w+') as f:
            f.write(template.render(data))
            
        if self.checkBox_include_menu.isChecked():
            template = env.get_template('menu.ui')
            with open(os.path.join(output_dir, name+'-menu.ui'), 'w+') as f:
                f.write(template.render(data))


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())


