from typing import Any
from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex
from PySide6.QtCore import Qt
from connector import Connector
from share import SI

class TransportTaskModel(QAbstractTableModel):

    s_instance = None

    @staticmethod
    def getInstance():
        if TransportTaskModel.s_instance is None:
            TransportTaskModel.s_instance = TransportTaskModel()
        return TransportTaskModel.s_instance

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__taskList = []
        self.__headerList = [
            'ID', '客户名称', '需要车型', '需要数量', '计划里程', '计划开始时间', '计划结束时间',
            '安排车号', '安排司机', '实际开始时间', '实际结束时间', '实际里程', '实际耗油量', '状态'
        ]
        SI.g_transportTaskModel = self
        self.update()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if 0 <= section < len(self.__headerList):
                return self.__headerList[section]
        return super().headerData(section, orientation, role)

    def rowCount(self, parent: [QModelIndex, QPersistentModelIndex] = ...) -> int:
        return len(self.__taskList)

    def columnCount(self, parent: [QModelIndex, QPersistentModelIndex] = ...) -> int:
        return len(self.__headerList)

    def data(self, index: [QModelIndex, QPersistentModelIndex], role: int = ...) -> Any:
        if not index.isValid():
            return None
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if 0 <= index.column() < len(self.__headerList) and 0 <= index.row() < len(self.__taskList):
            return self.__taskList[index.row()][index.column()]
        return None

    def sort(self, column: int, order: Qt.SortOrder = ...) -> None:
        self.__taskList.sort(key=lambda row: row[column], reverse=order == Qt.SortOrder.DescendingOrder)
        self.dataChanged.emit(self.index(0, 0), self.index(len(self.__taskList) - 1, len(self.__headerList) - 1))

    def update(self):
        self.beginResetModel()
        cursor = Connector.get_cursor()
        sql = '''
        SELECT 
            id, client_name, need_vehicle_type, need_count, plan_mileage, plan_start_time, plan_end_time,
            vehicle_id, driver_id, real_start_time, real_end_time, real_mileage, fuel_used, status 
        FROM transport_tasks
        '''
        cursor.execute(sql)
        result = cursor.fetchall()
        self.__taskList = []
        for row in result:
            self.__taskList.append([
                row[0],  # ID
                row[1],  # 客户名称
                row[2],  # 需要车型
                row[3],  # 需要数量
                row[4],  # 计划里程
                row[5].strftime('%Y-%m-%d %H:%M:%S') if row[5] else '',  # 计划开始时间
                row[6].strftime('%Y-%m-%d %H:%M:%S') if row[6] else '',  # 计划结束时间
                row[7],  # 安排车号
                row[8],  # 安排司机
                row[9].strftime('%Y-%m-%d %H:%M:%S') if row[9] else '',  # 实际开始时间
                row[10].strftime('%Y-%m-%d %H:%M:%S') if row[10] else '',  # 实际结束时间
                row[11],  # 实际里程
                row[12],  # 实际耗油量
                row[13]   # 状态
            ])
        self.endResetModel()
