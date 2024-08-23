from PyQt5 import QtCore, QtGui, QtWidgets
import asyncio
import websockets
import json
import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QTextCursor, QPalette, QBrush, QPixmap
import random

class AsyncWorker(QThread):
    message_received = pyqtSignal(str)
    
    def __init__(self, server_url, username, password):
        super().__init__()
        self.server_url = server_url
        self.username = username
        self.password = password
        self.websocket = None
        self.loop = None

    async def connect_to_server(self):
        try:
            self.websocket = await websockets.connect(self.server_url)
            auth_data = json.dumps({'username': self.username, 'password': self.password})
            await self.websocket.send(auth_data)
            response = await self.websocket.recv()
            response_json = json.loads(response)
            if response_json.get('status') == 'authenticated':
                print("连接并认证成功。")
                await self.listen_for_messages()
            else:
                print("认证失败。")
        except Exception as e:
            print(f"连接服务器失败: {e}")

    async def listen_for_messages(self):
        try:
            while True:
                message = await self.websocket.recv()
                self.message_received.emit(message)
        except websockets.exceptions.ConnectionClosed:
            print("连接已关闭。")
        except Exception as e:
            print(f"监听消息时出错: {e}")

    async def send_message(self, message):
        try:
            if self.websocket and self.websocket.open:
                await self.websocket.send(message)
        except Exception as e:
            print(f"发送消息失败: {e}")

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.connect_to_server())

class ChatWindow(QtWidgets.QMainWindow):
    def __init__(self, server_url, username, password):
        super().__init__()
        self.server_url = server_url
        self.username = username
        self.password = password

        self.init_ui()

        self.setWindowTitle(f'Chat - {self.username}')
        self.setFixedSize(self.size())

        self.set_background_image("./img/back_ui.png")
        self.set_widget_styles()

        self.pushButton.setText("发送")
        self.pushButton.clicked.connect(self.send_message)
        
        # 适配回车键发送消息
        self.textEdit.keyPressEvent = self.handle_keypress

        self.worker = AsyncWorker(server_url, username, password)
        self.worker.message_received.connect(self.append_message)
        self.worker.start()

    def init_ui(self):
        self.resize(972, 600)
        self.centralwidget = QtWidgets.QWidget(self)
        
        # 将QTreeView改为QTextBrowser
        self.announcementBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.announcementBrowser.setGeometry(QtCore.QRect(0, 0, 231, 571))
        
        # 设置公告的字体和颜色
        self.set_announcement_content("欢迎使用CDWA测试版|公告：|当前客户端为0.1.0版本|目前已在GitHub开源|访问链接：https://github.com/guilings/CDWA|开发作者:coffee_dou|希望能有更多人能加入并将该项目优化|该程序禁止用于商业用途|使用其中代码必须标明原作者|请注意遵守开源社区规定")

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(240, 0, 731, 351))
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(240, 370, 731, 201))
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(880, 530, 91, 31))
        
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusbar)

    def set_announcement_content(self, content):
        # 将 | 替换为换行符
        lines = content.split('|')
        
        # 随机颜色设置
        colors = [
            '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF',
            '#800000', '#008000', '#000080', '#808000', '#800080', '#008080',
            '#C0C0C0', '#808080', '#999900', '#9900CC', '#FF6600', '#3399FF',
            '#33CC33', '#FF99CC'
        ]
        
        # 使用不同颜色和微软雅黑字体设置公告内容
        announcement_text = ""
        for line in lines:
            color = random.choice(colors)
            announcement_text += f'<p style="color:{color}; font-size:16pt; font-family:微软雅黑;">{line}</p>'
        
        self.announcementBrowser.setHtml(announcement_text)

    def set_background_image(self, image_path):
        palette = QPalette()
        pixmap = QPixmap(image_path).scaled(self.size(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
        palette.setBrush(QPalette.Background, QBrush(pixmap))
        self.setPalette(palette)

    def set_widget_styles(self):
        self.setStyleSheet("""
            QWidget {
                border-radius: 10px;
            }
            QTextBrowser, QTextEdit {
                background-color: rgba(255, 255, 255, 180);
                border-radius: 10px;
                border: 1px solid black;
            }
            QPushButton {
                background-color: white;
                border-radius: 10px;
            }
        """)

    def handle_keypress(self, event):
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            if event.modifiers() & QtCore.Qt.ShiftModifier:
                # Shift + Enter -> 新行
                self.textEdit.insertPlainText('\n')
            else:
                # Enter -> 发送消息
                self.send_message()
        else:
            QtWidgets.QTextEdit.keyPressEvent(self.textEdit, event)

    def send_message(self):
        message = self.textEdit.toPlainText().strip()
        if message:
            message_data = json.dumps({'username': self.username, 'message': message})
            asyncio.run_coroutine_threadsafe(self.worker.send_message(message_data), self.worker.loop)
            self.textEdit.clear()
            self.append_message(message_data)

    def append_message(self, message):
        try:
            message_data = json.loads(message)
            user_message = message_data.get('message')
            user_name = message_data.get('username')
            if not user_message or not user_name:
                return
            
            avatar = "./img/avatar.png"  # 默认头像路径

            if user_name == self.username:
                # 右侧显示当前用户的消息
                formatted_message = f"""
                <div align='right' style="margin: 5px;">
                    <img src="{avatar}" width="30" height="30" style="border-radius: 15px; margin-left: 5px;">
                    <b>{user_name}:</b> {user_message}
                </div>
                """
            else:
                # 左侧显示其他用户的消息
                formatted_message = f"""
                <div align='left' style="margin: 5px;">
                    <img src="{avatar}" width="30" height="30" style="border-radius: 15px; margin-right: 5px;">
                    <b>{user_name}:</b> {user_message}
                </div>
                """

            self.textBrowser.append(formatted_message)
            self.textBrowser.append('------------------------------------------------------')
        except json.JSONDecodeError:
            self.textBrowser.append(f"<div align='right'>{message}</div>")
            self.textBrowser.append('------------------------------------------------------')
        
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()

    def closeEvent(self, event):
        if self.worker.websocket:
            asyncio.run_coroutine_threadsafe(self.worker.websocket.close(), self.worker.loop)
        super().closeEvent(event)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: chat.py <server_url> <username> <password>")
        sys.exit(1)

    server_url = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    app = QtWidgets.QApplication(sys.argv)
    chat_window = ChatWindow(server_url, username, password)
    chat_window.show()  # 确保显示窗口
    sys.exit(app.exec_())
