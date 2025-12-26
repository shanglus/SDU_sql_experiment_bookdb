from PySide6.QtWidgets import QStackedWidget
from share import SI
from widget.uiMainWindow import Ui_MainWindow

class MainWindow(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        SI.mainWindow = self
        # 连接 UI 按钮（UI 中已经把各个 Widget 实例放到 QStackedWidget 中）
        self.__ui.m_readerLoginButton.clicked.connect(lambda:
                                                      self.setCurrentWidget(self.__ui.m_readerLoginWidget))
        self.__ui.m_administerLoginButton.clicked.connect(lambda:
                                                            self.setCurrentWidget(self.__ui.m_administerLoginWidget))

    def updateBorrowWidget(self):
        # BorrowWidget 中会刷新 bookInfo 和 userInfo
        self.__ui.m_borrowWidget.updateData()

    def updateAdminWidget(self):
        # AdminWidget 中刷新 admin 页面的信息
        self.__ui.m_adminWidget.updateData()