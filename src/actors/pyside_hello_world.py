from PySide6.QtWidgets import QApplication, QLabel
import sys

app = QApplication()

w = QLabel("test")
w.show()

sys.exit(app.exec_())
