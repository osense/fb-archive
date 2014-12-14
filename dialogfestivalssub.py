#!/usr/bin/env python
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
from dialogfestivals import Ui_DialogFestivals
from dialogeditsub import DialogEditSub


class DialogFestivalsSub(QDialog, Ui_DialogFestivals):
    """
    Dialog to manage festivals
    """
    def __init__(self, parent):
        super(QDialog, self).__init__()
        self.parent = parent
        self.setupUi(self)
        self.show_all_festivals()

    def show_all_festivals(self):
        """
        Loads all festivals to listwidget
        """
        data = self.parent.dbjobs.get_all_festivals()
        for row in data:
            item = QListWidgetItem(row[1])
            item.setData(Qt.UserRole, row[0])
            self.lw_festivals.addItem(item)

    @pyqtSlot()
    def on_btn_festivals_add_clicked(self):
        d = DialogEditSub(self.parent, festivals=True, caption=self.tr('Zadejte název festivalu'))
        if d.exec_() == QDialog.Accepted:
            id = self.parent.dbjobs.add_festival(d.dataFestival)
            item = QListWidgetItem(d.dataFestival)
            item.setData(Qt.UserRole, id)
            self.lw_festivals.addItem(item)

    @pyqtSlot()
    def on_btn_festivals_remove_clicked(self):
        if len(self.lw_festivals.selectedItems()) > 0:
            id = self.lw_festivals.takeItem(self.lw_festivals.currentIndex().row()).data(Qt.UserRole)
            self.parent.dbjobs.remove_festival(id)

# End of dialogconcertssub.py
