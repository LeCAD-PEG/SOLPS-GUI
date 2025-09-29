# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

"""QUiLoader example, showing how to dynamically load a Qt Designer form
   from a UI file."""

from argparse import ArgumentParser, RawTextHelpFormatter
import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import loadUiType

if __name__ == '__main__':
    arg_parser = ArgumentParser(description="QUiLoader example",
                                formatter_class=RawTextHelpFormatter)
    arg_parser.add_argument('file', type=str, help='UI file')
    args = arg_parser.parse_args()
    ui_file_name = args.file

    app = QApplication(sys.argv)
    uiclass, baseclass = loadUiType(ui_file_name)

    class MainWindow(uiclass, baseclass):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())