from PySide6.QtWidgets import QTableView, QPushButton, QMessageBox, QHeaderView
from PySide6.QtCore import QDateTime
from share import SI
from connector import Connector
from model.TransportTaskModel import TransportTaskModel

class DriverTaskView(QTableView):
    """
    读者/司机视图：展示运输任务（复用原来的  名称以匹配 UI）
    提供“开始/完成”切换按钮。简单策略：
      - 如果任务状态为 '待安排'：不能直接开始（提示）
      - 如果任务状态为 '进行中' 或 '运输中'：点击则标记为已完成（更新 real_end_time, status）
      - 如果任务状态为 '待安排' 且没有司机：不能开始；如果要开始并绑定司机，需要管理员先分配
      - 如果任务状态为 '待安排' 且当前用户可作为司机（本示例将不会自动分配以避免错误）
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.verticalHeader().setVisible(False)
        self.__model = TransportTaskModel.getInstance()
        self.setModel(self.__model)
        self.__model.update()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        # 为每一行添加“开始/完成”按钮（最后一列）
        for i in range(self.__model.rowCount()):
            op_button = QPushButton('开始/完成')
            op_button.setWhatsThis(str(i))
            op_button.clicked.connect(self.toggleTaskStatus)
            self.setIndexWidget(self.__model.index(i, self.__model.columnCount() - 1), op_button)

    def toggleTaskStatus(self):
        row_index = int(self.sender().whatsThis())
        task_id = self.__model.index(row_index, 0).data()
        status = self.__model.index(row_index, self.__model.columnCount() - 1).data()  # 状态列通常在最后
        cursor = Connector.get_cursor()
        if cursor is None:
            QMessageBox.critical(self, '错误', '数据库游标不可用')
            return
        try:
            # 兼容几种状态词：'待安排', '进行中' / '运输中', '已完成'
            if status in ('已完成',):
                QMessageBox.information(self, '操作无效', '该任务已完成')
                return
            if status in ('待安排', None, ''):
                QMessageBox.information(self, '无法开始', '该任务尚未安排车辆/司机，无法开始')
                return
            # 如果处于进行中，标记为已完成并设置 real_end_time
            if status in ('进行中', '运输中'):
                sql = "UPDATE transport_tasks SET status = %s, real_end_time = %s WHERE id = %s"
                now_str = QDateTime.currentDateTime().toString('yyyy-MM-dd HH:mm:ss')
                cursor.execute(sql, ('已完成', now_str, task_id))
                conn = Connector.get_connection()
                if conn is not None:
                    conn.commit()
                QMessageBox.information(self, '完成', '任务已标记为已完成')
            else:
                # 其他未知状态，简单提示并刷新
                QMessageBox.information(self, '提示', f'当前状态：{status}')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'操作失败: {e}')
        self.updateData()

    def updateData(self):
        self.__model.update()
        for i in range(self.__model.rowCount()):
            op_button = QPushButton('开始/完成')
            op_button.setWhatsThis(str(i))
            op_button.clicked.connect(self.toggleTaskStatus)
            self.setIndexWidget(self.__model.index(i, self.__model.columnCount() - 1), op_button)