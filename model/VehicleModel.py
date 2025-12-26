from typing import Any
from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex
from PySide6.QtCore import Qt
from connector import Connector
from share import SI

class VehicleModel(QAbstractTableModel):

    s_instance = None

    @staticmethod
    def getInstance():
        if VehicleModel.s_instance is None:
            VehicleModel.s_instance = VehicleModel()
        return VehicleModel.s_instance

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__vehicleList = []
        self.__headerList = ['ID', '车牌号', '类型', '状态']
        SI.g_vehicleModel = self
        self.update()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if 0 <= section < len(self.__headerList):
                return self.__headerList[section]
        return super().headerData(section, orientation, role)

    def rowCount(self, parent: [QModelIndex, QPersistentModelIndex] = ...) -> int:
        return len(self.__vehicleList)

    def columnCount(self, parent: [QModelIndex, QPersistentModelIndex] = ...) -> int:
        return len(self.__headerList)

    def data(self, index: [QModelIndex, QPersistentModelIndex], role: int = ...) -> Any:
        if not index.isValid():
            return None
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if 0 <= index.column() < len(self.__headerList) and 0 <= index.row() < len(self.__vehicleList):
            return self.__vehicleList[index.row()][index.column()]
        return None

    def sort(self, column: int, order: Qt.SortOrder = ...) -> None:
        self.__vehicleList.sort(key=lambda row: row[column], reverse=order == Qt.SortOrder.DescendingOrder)
        self.dataChanged.emit(self.index(0, 0), self.index(len(self.__vehicleList) - 1, len(self.__headerList) - 1))

    def update(self):
        self.beginResetModel()
        cursor = Connector.get_cursor()
        sql = '''
        SELECT id, plate_number, type, status 
        FROM vehicles
        '''
        cursor.execute(sql)
        result = cursor.fetchall()
        self.__vehicleList = []
        for row in result:
            self.__vehicleList.append([
                row[0],
                row[1],
                row[2],
                row[3]
            ])
        self.endResetModel()