from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from mainformsub import *

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    screen = Mainformsub()
    screen.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter, screen.size(), qApp.desktop().availableGeometry()))
    screen.show()

    sys.exit(app.exec_())


