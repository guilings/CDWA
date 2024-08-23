import sys
import csv
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFormLayout, QMessageBox
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor

class RegistrationForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('CDWA服务端账号注册工具')
        self.setFixedSize(400, 300)
        self.setWindowIcon(QIcon('icon.png'))  # 设置窗口图标

        # 设置背景颜色
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        self.setPalette(palette)

        # 设置布局
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # 创建字体
        font = QFont('Arial', 12)

        # 创建控件
        self.username_label = QLabel('用户名:')
        self.username_label.setFont(font)
        self.username_input = QLineEdit()
        self.username_input.setFont(font)
        
        self.password_label = QLabel('密码:')
        self.password_label.setFont(font)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(font)
        
        self.confirm_password_label = QLabel('确认密码:')
        self.confirm_password_label.setFont(font)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setFont(font)
        
        self.confirm_code_label = QLabel('确认码:')
        self.confirm_code_label.setFont(font)
        self.confirm_code_input = QLineEdit()
        self.confirm_code_input.setFont(font)
        
        self.submit_button = QPushButton('提交')
        self.submit_button.setFont(font)
        self.submit_button.clicked.connect(self.submit_form)
        
        # 添加控件到表单布局
        form_layout.addRow(self.username_label, self.username_input)
        form_layout.addRow(self.password_label, self.password_input)
        form_layout.addRow(self.confirm_password_label, self.confirm_password_input)
        form_layout.addRow(self.confirm_code_label, self.confirm_code_input)
        
        # 添加表单布局到主布局
        layout.addLayout(form_layout)
        layout.addWidget(self.submit_button)
        
        # 设置主布局
        self.setLayout(layout)

    def submit_form(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        confirm_code = self.confirm_code_input.text()

        if not username or not password or not confirm_password or not confirm_code:
            QMessageBox.warning(self, '错误', '请填写所有字段')
        elif password != confirm_password:
            QMessageBox.warning(self, '错误', '两次输入的密码不同，请重新输入')
            self.password_input.clear()
            self.confirm_password_input.clear()
        elif confirm_code != '注册':
            QMessageBox.warning(self, '错误', '未通过人机检验，请在确认码处填写确认')
        else:
            if self.check_username_exists(username):
                QMessageBox.warning(self, '错误', '用户名已存在，注册失败')
            else:
                try:
                    self.register_user(username, password)
                    QMessageBox.information(self, '成功', '注册成功！')
                except PermissionError:
                    QMessageBox.critical(self, '错误', '当前已经通过其他程序打开了此文件，请关闭其他程序后再做尝试')

    def check_username_exists(self, username):
        try:
            with open('users.csv', mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == username:
                        return True
        except FileNotFoundError:
            return False
        return False

    def register_user(self, username, password):
        # 使用绝对路径
        file_path = os.path.abspath('users.csv')
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, password])

def main():
    app = QApplication(sys.argv)
    window = RegistrationForm()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
