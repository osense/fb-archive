#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
