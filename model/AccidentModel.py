from typing import Any
from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex
from PySide6.QtCore import Qt
from connector import Connector
from share import SI

class AccidentModel(QAbstractTableModel):
    s_instance = None
    @staticmethod
    def getInstance():
        if AccidentModel.s_instance is None:
            AccidentModel.s_instance = AccidentModel()
        return AccidentModel.s_instance

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__accidentList = []
        self.__headerList = [
            'ID', '事故车辆', '当事司机', '事故时间', '事故地点', '事故原因', '处理方式', '处理金额', '对方车号'
        ]
        SI.g_accidentModel = self
        self.update()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if 0 <= section < len(self.__headerList):
                return self.__headerList[section]
        return super().headerData(section, orientation, role)

    def rowCount(self, parent: [QModelIndex, QPersistentModelIndex] = ...) -> int:
        return len(self.__accidentList)

    def columnCount(self, parent: [QModelIndex, QPersistentModelIndex] = ...) -> int:
        return len(self.__headerList)

    def data(self, index: [QModelIndex, QPersistentModelIndex], role: int = ...) -> Any:
        if not index.isValid():
            return None
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if 0 <= index.column() < len(self.__headerList) and 0 <= index.row() < len(self.__accidentList):
            return self.__accidentList[index.row()][index.column()]
        return None

    def sort(self, column: int, order: Qt.SortOrder = ...) -> None:
        self.__accidentList.sort(key=lambda row: row[column], reverse=order == Qt.SortOrder.DescendingOrder)
        self.dataChanged.emit(self.index(0, 0), self.index(len(self.__accidentList) - 1, len(self.__headerList) - 1))

    def update(self):
        self.beginResetModel()
        cursor = Connector.get_cursor()
        sql = '''
        SELECT 
            id, vehicle_id, driver_id, accident_time, location, reason, handle_method, cost, other_plate 
        FROM accidents
        '''
        cursor.execute(sql)
        result = cursor.fetchall()
        self.__accidentList = []
        for row in result:
            self.__accidentList.append([
                row[0],  # ID
                row[1],  # 事故车辆
                row[2],  # 当事司机
                row[3].strftime('%Y-%m-%d %H:%M:%S'),  # 事故时间
                row[4],  # 事故地点
                row[5],  # 事故原因
                row[6],  # 处理方式
                row[7],  # 处理金额
                row[8]   # 对方车号
            ])
        self.endResetModel()