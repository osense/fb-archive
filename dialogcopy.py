# -*- coding: utf-8 -*-

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
import os

class FileCopy(QObject):

    progress = pyqtSignal(int)
    finished = pyqtSignal()
    success = pyqtSignal()
    fail = pyqtSignal()

    def __init__(self, src, dest):
        QObject.__init__(self)
        self.src_path = src
        self.dest_path = dest

    def run(self):
        src = open(self.src_path, "rb")
        dest = open(self.dest_path, "wb")

        try:
            while True:
                block = src.read(1); # 16384
                QThread.usleep(300)
                if not block:
                    self.success.emit()
                    break
                dest.write(block);
                self.progress.emit(dest.tell())
        except:
            self.fail.emit()
        self.finished.emit()
