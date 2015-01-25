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
from mainformsub import *

class FileCopy(QThread):
    def __init__(self, parent, src_path, dest_path):
        QThread.__init__(self)
        self.parent = parent
        self.src = open(src_path, "rb")
        self.dest = open(dest_path, "wb")
        self.src_size = os.stat(src_path).st_size
        self.dialog = QProgressDialog('Kopirovani', 'Zrusit', 0, self.src_size)
        self.dialog.reset()
        self.dialog.setWindowModality(Qt.WindowModal);
        self.dialog.setMinimumDuration(0)
        self.dialog.open()
        
    def run(self):
        try:
            while True:
                #if self.dialog.wasCancelled():
                #    raise Exception()
                
                block = self.src.read(1); # 16384
                QThread.usleep(100)
                if not block:
                    QMessageBox.information(None, self.parent.tr('Informace'), self.parent.tr('Databáze koncertů byla úspěšne zálohována.'))
                    break
            
                self.dest.write(block);
                self.dialog.setValue(self.dest.tell())
        except:
            QMessageBox.critical(None, self.parent.tr('Chyba'), self.parent.tr('Zálohování bylo neúspěšné'))
        self.cleanup()
                
    def cleanup(self):
        self.dialog.setValue(self.dialog.maximum())
        self.src.close()
        self.dest.close()
        self.quit()