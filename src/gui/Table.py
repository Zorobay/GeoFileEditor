import typing

from PyQt6.QtCore import QAbstractTableModel, QSortFilterProxyModel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QTableView
from geopandas import GeoDataFrame


class GeoDataFrameTableModel(QAbstractTableModel):

    def __init__(self, data: GeoDataFrame, schema: dict):
        super().__init__()
        self._feature_index = 0
        self._data = data
        self._schema = schema['properties']
        self._keys = list(self._schema.keys())
        self.headers = ['Attribute', 'Value', 'Type']
        self._editable_columns = [1]

    def data(self, index, role):
        key = self._keys[index.row()]
        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            if index.column() == 0:
                return key
            elif index.column() == 2:
                dtype = self._schema[key]
                if dtype == object:
                    return '?'
                else:
                    return str(dtype)
            else:
                val = self._data.iloc[self._feature_index].loc[key]
                if val is None:
                    return ''
                else:
                    return str(val)

        if role == Qt.ItemDataRole.ForegroundRole:
            value = self._data.iloc[self._feature_index].loc[key]
            if isinstance(value, bool):
                if value:
                    return QColor('green')
                if not value:
                    return QColor('red')

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
            self._data.loc[self._feature_index, key] = self._cast_to_dtype(key, value)
            return True

    def _cast_to_dtype(self, key: str, value) -> typing.Any:
        dtype = self._schema[key]
        if value == '':
            return None
        return value

    def setFeatureIndex(self, index: int):
        self._feature_index = index


class Table(QTableView):

    def __init__(self):
        super().__init__()
        self.model = None
        self.source_model = None
        self.setSortingEnabled(True)

    def setData(self, data: GeoDataFrame, schema: dict):
        self.model = QSortFilterProxyModel()
        self.source_model = GeoDataFrameTableModel(data, schema)
        self.model.setSourceModel(self.source_model)
        self.setModel(self.model)

    def setFeatureIndex(self, index: int):
        self.source_model.setFeatureIndex(index)

    def filter(self, text: str):
        self.model.setFilterFixedString(text)
