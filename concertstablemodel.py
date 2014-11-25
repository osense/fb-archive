# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class ConcertsTableModel(QAbstractTableModel):
    def __init__(self, parent, headerdata):
        super(QAbstractTableModel, self).__init__()
        self.parent = parent
        self.headerdata = headerdata
        self.data = []

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return QVariant(self.data[index.row()][index.column()])
        return QVariant()

    def headerData(self, col, orientation, role):
        # horizontal
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        else:
            return QVariant()

    def rowCount(self, parent=QModelIndex()):
        return len(self.data)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headerdata)

# End of concertstablemodel.py