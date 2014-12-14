
## This file is part of fb-archive.

## fb-archive is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.

## fb-archive is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with fb-archive.  If not, see <http://www.gnu.org/licenses/>.


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


