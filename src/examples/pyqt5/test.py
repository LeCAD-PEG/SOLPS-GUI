""" Tests basic functionality of PyQt5 """
from PyQt5.QtWidgets import QApplication, QWidget
import sys
app = QApplication(sys.argv)
w = QWidget()
w.show()
sys.exit(app.exec_())
