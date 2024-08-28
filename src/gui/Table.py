import typing

from PyQt6 import QtGui
from PyQt6.QtCore import QAbstractTableModel, QSortFilterProxyModel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QTableView
from pandas import Series

from src.DtypeUtils import DtypeUtils
from src.utils.GeoData import GeoData


class GeoDataFrameTableModel(QAbstractTableModel):

    def __init__(self, data: GeoData):
        super().__init__()
        self._feature_index = 0
        self._data = data
        self._keys = list(self._data.schema().keys())
        self.headers = ['Attribute', 'Value', 'Type']
        self._editable_columns = [1]

    def _get_value(self, key: str) -> typing.Any:
        return self._data.get_value(self._feature_index, key)

    def _get_original_value(self, key: str) -> typing.Any:
        return self._data.get_original_value(self._feature_index, key)

    def resetOriginalValues(self):
        self._data.update_original_attrs()
        self.update()

    def data(self, index, role):
        key = self._keys[index.row()]
        value = self._data.get_value(self._feature_index, key)
        dtype = self._data.schema()[key]

        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            if index.column() == 0:
                return key
            elif index.column() == 1:
                return DtypeUtils.to_string(dtype, value)
            elif index.column() == 2:
                if dtype == object:
                    return '?'
                else:
                    return str(dtype)

        if role == Qt.ItemDataRole.ForegroundRole:
            if isinstance(value, bool):
                if value:
                    return QColor('green')
                if not value:
                    return QColor('red')

        # If data has been edited, but not saved, color the background
        if role == Qt.ItemDataRole.BackgroundRole:
            orig_value = self._get_original_value(key)
            if isinstance(value, Series) or isinstance(orig_value, Series):
                a = 2
            if index.column() == 1 and orig_value != value:
                return QtGui.QColor('#DBEDFF')

    def rowCount(self, index):
        return len(self._keys)

    def columnCount(self, parent) -> int:
        return len(self.headers)

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.headers[section]

    def flags(self, index):
        if index.column() in self._editable_columns:
            return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable

        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled

    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            key = self._keys[index.row()]
            self._data.set_value(self._feature_index, key, value)
            # self._data.loc[self._feature_index, key] = self._cast_to_dtype(key, value, old_val)
            return True

    def update(self):
        self.modelReset.emit()

    def setFeatureIndex(self, index: int):
        self._feature_index = index
        self.update()


class Table(QTableView):

    def __init__(self):
        super().__init__()
        self.model = None
        self.source_model = None
        self.setSortingEnabled(True)

    def setData(self, data: GeoData):
        self.model = QSortFilterProxyModel()
        self.source_model = GeoDataFrameTableModel(data)
        self.model.setSourceModel(self.source_model)
        self.setModel(self.model)

    def setFeatureIndex(self, index: int):
        self.source_model.setFeatureIndex(index)

    def filter(self, text: str):
        self.model.setFilterFixedString(text)

    def resetOriginalValues(self):
        self.source_model.resetOriginalValues()
