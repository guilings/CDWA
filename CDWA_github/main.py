import sys
import asyncio
import websockets
import json
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel, QLineEdit, QPushButton, QGraphicsBlurEffect
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap, QFont
from subprocess import Popen

class LoginWorker(QThread):
    authenticated = pyqtSignal(bool, str)
    error = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.server_url = ''
        self.username = ''
        self.password = ''
    
    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.login())

    async def login(self):
        try:
            async with websockets.connect(self.server_url) as websocket:
                auth_data = json.dumps({'username': self.username, 'password': self.password})
                await websocket.send(auth_data)
                response = await websocket.recv()
                response_json = json.loads(response)
                if response_json.get('status') == 'authenticated':
                    self.authenticated.emit(True, '登录成功')
                else:
                    self.authenticated.emit(False, '登录失败：用户名或密码错误')
        except Exception as e:
            self.error.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.set_background_image('./img/back.png')
        
        # 创建模糊效果
        self.blur_effect = QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(15)
        
        # 安装事件过滤器
        self.installEventFilter(self)

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1048, 677)
        self.setFixedSize(1048, 677)  # 锁定窗体大小
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        
        # 设置背景图
        self.background_label = QLabel(self.centralwidget)
        self.background_label.setGeometry(QtCore.QRect(0, 0, self.width(), self.height()))
        self.background_label.setPixmap(QPixmap('./img/back.png').scaled(self.size(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation))
        self.background_label.lower()

        # 设置控件
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(730, 300, 231, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setStyleSheet("border-radius: 15px; background-color: white; font-size: 14px; font-family: '微软雅黑';")

        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(730, 360, 231, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setStyleSheet("border-radius: 15px; background-color: white; font-size: 14px; font-family: '微软雅黑';")

        self.lineEdit_3 = QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(730, 420, 231, 31))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setStyleSheet("border-radius: 15px; background-color: white; font-size: 14px; font-family: '微软雅黑';")

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(660, 500, 301, 61))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet("border-radius: 15px; background-color: white; font-size: 14px; font-family: '微软雅黑';")

        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(660, 300, 51, 31))
        self.label.setObjectName("label")
        self.label.setStyleSheet("color: white; font-size: 14px; font-family: '微软雅黑';")

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(660, 360, 51, 31))
        self.label_2.setObjectName("label_2")
        self.label_2.setStyleSheet("color: white; font-size: 14px; font-family: '微软雅黑';")

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(660, 420, 51, 31))
        self.label_3.setObjectName("label_3")
        self.label_3.setStyleSheet("color: white; font-size: 14px; font-family: '微软雅黑';")

        # 设置分隔线透明
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(600, 0, 20, 641))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setStyleSheet("background: transparent;")
        self.line.setObjectName("line")

        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1048, 23))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        self.pushButton.clicked.connect(self.on_login)  # 连接登录按钮事件

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", ""))
        self.lineEdit.setText(_translate("MainWindow", ""))
        self.lineEdit_2.setText(_translate("MainWindow", ""))
        self.lineEdit_3.setText(_translate("MainWindow", "ws://your_server_ip:55668"))
        self.pushButton.setText(_translate("MainWindow", "登录"))
        self.label.setText(_translate("MainWindow", "账号："))
        self.label_2.setText(_translate("MainWindow", "密码："))
        self.label_3.setText(_translate("MainWindow", "服务链接"))

    def set_background_image(self, image_path):
        # 设置背景图片
        self.background_image = QPixmap(image_path)
        self.background_image = self.background_image.scaled(self.size(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
        
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(0, 0, self.background_image)
        super().paintEvent(event)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.FocusIn and isinstance(obj, QLineEdit):
            # 如果点击的是 QLineEdit，应用模糊效果
            self.apply_blur_effect()
        elif event.type() == QtCore.QEvent.MouseButtonPress and not isinstance(obj, QLineEdit):
            # 如果点击的是其它地方，移除模糊效果
            self.remove_blur_effect()
        return super().eventFilter(obj, event)

    def apply_blur_effect(self):
        # 将模糊效果应用到所有控件
        for widget in self.centralWidget().findChildren(QtWidgets.QWidget):
            if widget not in [self.lineEdit, self.lineEdit_2, self.lineEdit_3]:
                widget.setGraphicsEffect(self.blur_effect)

    def remove_blur_effect(self):
        # 移除所有控件的模糊效果
        for widget in self.centralWidget().findChildren(QtWidgets.QWidget):
            widget.setGraphicsEffect(None)

    def on_login(self):
        server_url = self.lineEdit_3.text()
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        self.worker = LoginWorker()
        self.worker.server_url = server_url
        self.worker.username = username
        self.worker.password = password
        self.worker.authenticated.connect(self.on_authenticated)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    @pyqtSlot(bool, str)
    def on_authenticated(self, success, message):
        if success:
            QMessageBox.information(self, '登录成功', message)
            self.openChatWindow()
        else:
            QMessageBox.warning(self, '登录失败', message)

    @pyqtSlot(str)
    def on_error(self, message):
        QMessageBox.critical(self, '登录异常', message)

    def openChatWindow(self):
        server_url = self.lineEdit_3.text()
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        try:
            Popen([sys.executable, 'chat.py', server_url, username, password])
        except Exception as e:
            QMessageBox.critical(self, '启动失败', f'无法启动聊天窗口: {e}')
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
