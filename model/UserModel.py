from typing import Any
from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex
from PySide6.QtCore import Qt
from connector import Connector
from share import SI
class UserModel(QAbstractTableModel):

    s_instance = None

    @staticmethod
    def getInstance():
        if UserModel.s_instance is None:
            UserModel.s_instance = UserModel()
        return UserModel.s_instance

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__userList = []
        self.__headerList = ['ID', '用户名', '密码', '姓名', '角色']
        SI.g_userModel = self
        self.update()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if 0 <= section < len(self.__headerList):
                return self.__headerList[section]
        return super().headerData(section, orientation, role)

    def rowCount(self, parent: [QModelIndex, QPersistentModelIndex] = ...) -> int:
        return len(self.__userList)

    def columnCount(self, parent: [QModelIndex, QPersistentModelIndex] = ...) -> int:
        return len(self.__headerList)

    def data(self, index: [QModelIndex, QPersistentModelIndex], role: int = ...) -> Any:
        if not index.isValid():
            return None
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if 0 <= index.column() < len(self.__headerList) and 0 <= index.row() < len(self.__userList):
            return self.__userList[index.row()][index.column()]
        return None

    def sort(self, column: int, order: Qt.SortOrder = ...) -> None:
        self.__userList.sort(key=lambda row: row[column], reverse=order == Qt.SortOrder.DescendingOrder)
        self.dataChanged.emit(self.index(0, 0), self.index(len(self.__userList) - 1, len(self.__headerList) - 1))

    def update(self):
        self.beginResetModel()
        cursor = Connector.get_cursor()
        sql = '''
        SELECT id, username, password, name, role 
        FROM users
        '''
        cursor.execute(sql)
        result = cursor.fetchall()
        self.__userList = []
        for row in result:
            self.__userList.append([
                row[0],
                row[1],
                row[2],
                row[3],
                row[4]
            ])
        self.endResetModel()