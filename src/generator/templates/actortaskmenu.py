from actor import Actor

from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout
from PySide6.QtDesigner import (QExtensionFactory, QPyDesignerTaskMenuExtension)


class ActorDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self._actor = Actor(self)
        layout.addWidget(self._actor)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok
                                      | QDialogButtonBox.Cancel
                                      | QDialogButtonBox.Reset)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        reset_button = button_box.button(QDialogButtonBox.Reset)
        reset_button.clicked.connect(self._actor.clear_board)
        layout.addWidget(button_box)

    def set_state(self, new_state):
        self._actor.setState(new_state)

    def state(self):
        return self._actor.state


class ActorTaskMenu(QPyDesignerTaskMenuExtension):
    def __init__(self, actor, parent):
        super().__init__(parent)
        self._actor = actor
        self._edit_state_action = QAction('Edit State...', None)
        self._edit_state_action.triggered.connect(self._edit_state)

    def taskActions(self):
        return [self._edit_state_action]

    def preferredEditAction(self):
        return self._edit_state_action

    @Slot()
    def _edit_state(self):
        dialog = ActorDialog(self._actor)
        dialog.set_state(self._actor.state)
        if dialog.exec() == QDialog.Accepted:
            self._actor.state = dialog.state()


class ActorTaskMenuFactory(QExtensionFactory):
    def __init__(self, extension_manager):
        super().__init__(extension_manager)

    @staticmethod
    def task_menu_iid():
        return 'org.qt-project.Qt.Designer.TaskMenu'

    def createExtension(self, object, iid, parent):
        if iid != ActorTaskMenuFactory.task_menu_iid():
            return None
        if object.__class__.__name__ != 'Actor':
            return None
        return ActorTaskMenu(object, parent)
