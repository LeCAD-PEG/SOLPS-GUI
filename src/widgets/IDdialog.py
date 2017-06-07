from PyQt5.QtCore import (QDateTime, pyqtSlot, QModelIndex, Qt, QSettings,
                          pyqtSignal, QThread, QAbstractItemModel, QVariant,
                          QSortFilterProxyModel, QRegExp, QObject, QRect,
                          QSize, QProcess)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox, QDialog,
                             QFileDialog, QStyle, QStyledItemDelegate,
                             QLineEdit, QToolButton, QGridLayout, QLabel,
                             QDialogButtonBox, QInputDialog, QPushButton)
from PyQt5.QtGui import QIntValidator
import os
import sys

N = 4

class Row:
    shot, run, user, machine = range(N)
    names = ['shot', 'run', 'user', 'machine']

class GetDialog(QDialog):
    """Dialog Demanding the shot, run, name and device for getting the data
    from IDS.
    """
    def __init__(self, parent=None):
        super(GetDialog, self).__init__(parent)
        self.setModal(True)
        self.main_layout = QGridLayout(self)
        self.setWindowTitle('Get IDS')

        self.main_layout.addWidget(QLabel('SHOT'), 0, 0, Qt.AlignLeft)
        shot = QLineEdit('1001')
        shot.setValidator(QIntValidator())
        self.main_layout.addWidget(shot, 0, 1, Qt.AlignCenter)

        self.main_layout.addWidget(QLabel('RUN'), 1, 0, Qt.AlignLeft)
        run = QLineEdit('1001')
        run.setValidator(QIntValidator())
        self.main_layout.addWidget(run, 1, 1, Qt.AlignCenter)

        self.main_layout.addWidget(QLabel('USER'), 2, 0, Qt.AlignLeft)
        self.main_layout.addWidget(QLineEdit(os.getenv('USER')), 2, 1,
                                   Qt.AlignCenter)

        self.main_layout.addWidget(QLabel('MACHINE'), 3, 0, Qt.AlignLeft)
        self.main_layout.addWidget(QLineEdit('solps-iter'),
                                   3, 1, Qt.AlignCenter)

        self.main_layout.addWidget(QLabel('VERSION'), 4, 0, Qt.AlignLeft)
        self.main_layout.addWidget(QLineEdit('3'), 4, 1, Qt.AlignCenter)

        self.main_layout.addWidget(QLabel('Run name'), 5, 0, Qt.AlignLeft)
        self.main_layout.addWidget(QLineEdit('new_run', ), 5, 1,
                                   Qt.AlignCenter)

        # Adding the Ok and Cancel button.
        dialog_button_box = QDialogButtonBox()
        dialog_button_box.setStandardButtons(QDialogButtonBox.Ok|
                                             QDialogButtonBox.Cancel)
        dialog_button_box.accepted.connect(self.accept)
        dialog_button_box.rejected.connect(self.reject)
        self.main_layout.addWidget(dialog_button_box, 6, 1)

    def sizeHint(self):
        return QSize(100,100)

    def on_close(self):
        # Returning the values
        # SHOT, RUN, USER, MACINE, VERSION, run_name exclusively.
        try:
            SHOT = int(self.main_layout.itemAt(1).widget().text())
            RUN = int(self.main_layout.itemAt(3).widget().text())
        except ValueError as e:
            SHOT = -1
            RUN = -1

        USER = self.main_layout.itemAt(5).widget().text()
        MACHINE = self.main_layout.itemAt(7).widget().text()
        VERSION = self.main_layout.itemAt(9).widget().text()
        RUN_NAME = self.main_layout.itemAt(11).widget().text()

        return SHOT, RUN, USER, MACHINE, VERSION, RUN_NAME
if __name__ == '__main__':
    app = QApplication(sys.argv)
    class MainWindow(QMainWindow):
        def __init__(self, parent=None):
            super(MainWindow, self).__init__(parent)
            push_button = QPushButton()
            self.setCentralWidget(push_button)
            push_button.clicked.connect(self.click_dialog)

        @pyqtSlot()
        def click_dialog(self):
            dialog = GetDialog()

            if dialog.exec_():
                print(dialog.on_close())

    main = MainWindow()
    main.show()

    sys.exit(app.exec_())
