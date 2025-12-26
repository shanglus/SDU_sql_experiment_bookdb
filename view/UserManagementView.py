from PySide6.QtWidgets import QTableView, QPushButton, QListWidget, QHeaderView, QMessageBox
from connector import Connector
from model.UserModel import UserModel
from share import SI


class UserInfoView(QTableView):
    """
    用户信息视图：展示当前用户信息（复用原来的样式）并提供“查看分配任务”按钮，
    展示当前用户（司机）被分配的 transport_tasks 的 client_name 列表。
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__showTaskWidget = None
        self.verticalHeader().setVisible(False)
        self.__model = UserModel()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.setModel(self.__model)
        # 将按钮放在第一行第6列（匹配原 UI 布局）
        try:
            show_button = QPushButton('查看分配任务')
            self.setIndexWidget(self.__model.index(0, 4), show_button)  # 将按钮放在 role 列后
            show_button.setStyleSheet('min-width: 100px; max-width: 100px;')
            show_button.clicked.connect(self.showAssignedTasks)
        except Exception:
            # 如果模型没有那么多列或索引不存在，忽略（防止界面崩溃）
            pass

    def showAssignedTasks(self):
        if SI.userId is None:
            QMessageBox.information(self, '提示', '未登录用户')
            return
        cursor = Connector.get_cursor()
        if cursor is None:
            QMessageBox.critical(self, '错误', '数据库游标不可用')
            return
        sql = """
            SELECT client_name
            FROM transport_tasks
            WHERE driver_id = %s
        """
        cursor.execute(sql, (SI.userId,))
        result = cursor.fetchall()
        self.__showTaskWidget = QListWidget()
        self.__showTaskWidget.setWindowTitle('分配给我的运输任务')
        for item in result:
            self.__showTaskWidget.addItem(item[0])
        self.__showTaskWidget.show()

    def updateData(self):
        self.__model.update()