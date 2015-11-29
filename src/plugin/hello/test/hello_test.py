from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.hello import Hello

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    label = Hello()
    label.show()
    sys.exit(app.exec_())
