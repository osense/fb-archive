# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from constants import *


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
            if index.column() in [COLUMN_DATE_FROM, COLUMN_DATE_TO]:
                return QVariant(self.data[index.row()][index.column()].strftime('%d.%m.%Y'))
            # Show multiline note as one line with 3 dots
            elif index.column() == COLUMN_NOTE:
                text = self.data[index.row()][index.column()]
                if (text != None) and (text.count('\n') > 0):
                    text = text[:text.find('\n')] + '...'
                return QVariant(text)
            else:
                return QVariant(self.data[index.row()][index.column()])
        if role == Qt.ToolTipRole:
            if index.column() in [COLUMN_WORKS, COLUMN_SOLOISTS, COLUMN_DIRIGENTS, COLUMN_CHOIRS]:
                text = self.data[index.row()][index.column()]
                if text != None:
                    QToolTip.showText(self.parent.cursor().pos(), text.replace(', ', '\n'))
            elif index.column() == COLUMN_NOTE:
                text = self.data[index.row()][index.column()]
                if text != None:
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