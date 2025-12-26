from PySide6.QtWidgets import QTableView, QPushButton, QMessageBox, QHeaderView
from share import SI
from connector import Connector
from model.TransportTaskModel import TransportTaskModel


class ManagerTaskView(QTableView):
    """
    管理员视图：展示 transport_tasks 表（复用原来的  名称以匹配 UI）
    提供删除任务的按钮。
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.verticalHeader().setVisible(False)
        self.__model = TransportTaskModel.getInstance()
        self.setModel(self.__model)
        self.__model.update()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        # 为每一行添加删除任务按钮（最后一列）
        for i in range(self.__model.rowCount()):
            delete_button = QPushButton('删除')
            delete_button.setStyleSheet('background-color: red; color: white')
            delete_button.setWhatsThis(str(i))
            delete_button.clicked.connect(self.deleteTask)
            # 将按钮放到最后一列
            self.setIndexWidget(self.__model.index(i, self.__model.columnCount() - 1), delete_button)

    def deleteTask(self):
        ret = QMessageBox.question(self, '确认删除', '确认删除这个运输任务吗？')
        if ret != QMessageBox.StandardButton.Yes:
            return
        row_index = int(self.sender().whatsThis())
        task_id = self.__model.index(row_index, 0).data()  # TransportTaskModel 第一列是 ID
        cursor = Connector.get_cursor()
        if cursor is None:
            QMessageBox.critical(self, '错误', '数据库游标不可用')
            return
        try:
            sql = 'DELETE FROM transport_tasks WHERE id = %s'
            cursor.execute(sql, (task_id,))
            conn = Connector.get_connection()
            if conn is not None:
                conn.commit()
            QMessageBox.information(self, '删除成功', '已删除运输任务')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'删除失败: {e}')
        self.updateData()

    def updateData(self):
        self.__model.update()
        # 重新为每行添加按钮（模型重置后索引变化）
        for i in range(self.__model.rowCount()):
            delete_button = QPushButton('删除')
            delete_button.setStyleSheet('background-color: red; color: white')
            delete_button.setWhatsThis(str(i))
            delete_button.clicked.connect(self.deleteTask)
            self.setIndexWidget(self.__model.index(i, self.__model.columnCount() - 1), delete_button)