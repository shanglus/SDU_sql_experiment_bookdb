from typing import Any
from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex
from PySide6.QtCore import Qt
from connector import Connector
from share import SI

class DriverModel(QAbstractTableModel):

    s_instance = None

    @staticmethod
    def getInstance():
        if DriverModel.s_instance is None:
            DriverModel.s_instance = DriverModel()
        return DriverModel.s_instance

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__driverList = []
        self.__headerList = ['ID', '姓名', '电话']
        SI.g_driverModel = self
        self.update()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if 0 <= section < len(self.__headerList):
                return self.__headerList[section]
        return super().headerData(section, orientation, role)

    def rowCount(self, parent: [QModelIndex, QPersistentModelIndex] = ...) -> int:
        return len(self.__driverList)

    def columnCount(self, parent: [QModelIndex, QPersistentModelIndex] = ...) -> int:
        return len(self.__headerList)

    def data(self, index: [QModelIndex, QPersistentModelIndex], role: int = ...) -> Any:
        if not index.isValid():
            return None
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if 0 <= index.column() < len(self.__headerList) and 0 <= index.row() < len(self.__driverList):
            return self.__driverList[index.row()][index.column()]
        return None

    def sort(self, column: int, order: Qt.SortOrder = ...) -> None:
        self.__driverList.sort(key=lambda row: row[column], reverse=order == Qt.SortOrder.DescendingOrder)
        self.dataChanged.emit(self.index(0, 0), self.index(len(self.__driverList) - 1, len(self.__headerList) - 1))

    def update(self):
        self.beginResetModel()
        cursor = Connector.get_cursor()
        sql = '''
        SELECT id, name, phone 
        FROM drivers
        '''
        cursor.execute(sql)
        result = cursor.fetchall()
        self.__driverList = []
        for row in result:
            self.__driverList.append([
                row[0],
                row[1],
                row[2]
            ])
        self.endResetModel()
