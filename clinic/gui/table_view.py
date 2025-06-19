import sys
from datetime import datetime
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        value = self._data[index.row()][index.column()]

        if role == Qt.ItemDataRole.DisplayRole:

            if isinstance(value, int):
                return "%d" % value

            if isinstance(value, str):
                return '%s' % value

            return value

    def rowCount(self, index):

        return len(self._data)

    def columnCount(self, index):

        return len(self._data[0])


