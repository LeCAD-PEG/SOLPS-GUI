#!/usr/bin/env python3
""" A PyQt custom widget for Qt Designer that receives selected run and
    passes is forward though passthrough signal unconditionally. If the
    checkbox is checked is passess the signal through checked too.
"""

from PySide6.QtCore import (QSize, Signal,
                          QSettings, Slot, Property)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QCheckBox, QFrame


class Director(QCheckBox):
    """ Director(QCheckbox)

        The purpose of this widget is to emit received selected run
        to all interested widgets. It will not emit checked it the
        checkbox is not checked.

        Attributes:
            passthrough(str): Signal emits received run_selected.
            checked(str): Signal emits received run_selected if checkbox
                checked.
            passtrigger(): Signal is emited without checking.
            checktrigger(): Signal is emited if checked.
    """

    rundir_passthrough = Signal(str)
    rundir_checked = Signal(str)
    rundir_passtrigger = Signal()
    rundir_checktrigger = Signal()

    b2_user = Signal(str)
    b2_run_number = Signal(str)
    b2_shot_number = Signal(str)
    b2_device = Signal(str)

    def __init__(self, parent=None):
        super(Director, self).__init__(parent)

    @Slot(str)
    def setRundir(self, rundir):
        self.rundir_passthrough.emit(rundir)
        self.rundir_passtrigger.emit()
        if self.checkState():
            self.rundir_checked.emit(rundir)
            self.rundir_checktrigger.emit()
