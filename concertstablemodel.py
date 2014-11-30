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
        if role == Qt.DisplayRole:
            # Show multiline note as one line with 3 dots
            if index.column() == 9:
                text = self.data[index.row()][index.column()]
                if (text != None) and (text.count('\n') > 0):
                    text = text[:text.find('\n')] + '...'
                return QVariant(text)
            else:
                return QVariant(self.data[index.row()][index.column()])
        if role == Qt.ToolTipRole:
            if index.column() in [6, 7, 8]:
                text = self.data[index.row()][index.column()]
                if text != None:
                    QToolTip.showText(self.parent.cursor().pos(), text.replace(', ', '\n'))
            elif index.column() == 9:
                text = self.data[index.row()][index.column()]
                if (text != None) and (text.count('\n') > 0):
                    QToolTip.showText(self.parent.cursor().pos(), text)
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

    def addRow(self, row):
        self.data.append(row)

    def clear(self):
        self.beginResetModel()
        self.data = []
        self.endResetModel()

    def get_item_data(self, index, column):
        return self.data[index.row()][column]

    def removeRow(self, row, parent=QModelIndex()):
        """
        Remove just one row
        """
        self.beginRemoveRows(parent, row, row)
        self.data.pop(row)
        self.endRemoveRows()

# End of concertstablemodel.py