import os
import time
import sys
import asyncio
import subprocess
import psutil
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget
from PyQt5.QtCore import *

file_weizhi = os.path.dirname(__file__)

def show_error_popup(message):
    app = QApplication.instance() or QApplication(sys.argv)
    QMessageBox.critical(None, "Port Error", message)

class MyWindow(QWidget):
    def show3(self):
        reply = QMessageBox.warning(self, "警告对话框", "警告对话框正文", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        print(reply)
        if reply == QMessageBox.Yes:
            reply_2 = QMessageBox.warning(self, "警告对话框", "再次确认", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply_2 == QMessageBox.Yes:

                with open("./history/chat_history.txt","w")as f:
                    f.write("")
                    print("已删除")
                    time.sleep(0.5)
                    os.system("cls")
                    
            else:
                print("取消执行操作")
                os.system("cls")
        else:
            print("取消执行操作")
            os.system("cls")

def find_process_by_port(port):
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == port:
            return conn.pid
    return None

def stop_server():
    pid = find_process_by_port(55668)
    if pid:
        try:
            process = psutil.Process(pid)
            process_name = process.name()
            msg_box = QMessageBox()
            msg_box.setWindowTitle("终止进程")
            msg_box.setText(f"端口 55668 正在被进程 {process_name} (PID: {pid}) 占用。\n是否终止该进程？")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            reply = msg_box.exec_()

            if reply == QMessageBox.Yes:
                process.terminate()  # 终止进程
                process.wait()  # 等待进程结束
                print(f"进程 {process_name} (PID: {pid}) 已终止。")
            else:
                print("取消终止进程操作。")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            print("无法访问该进程或进程不存在。")
    else:
        print("端口 55668 未被任何进程占用。")
        time.sleep(1)

async def start_server():
    process = subprocess.Popen(
        [sys.executable, os.path.join(file_weizhi, "server_1.py")],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = await asyncio.get_event_loop().run_in_executor(None, process.communicate)
    
    if "OSError: [Errno 10048]" in stderr:
        show_error_popup("端口 55668 已在使用中。请关闭其他应用程序或释放端口。")
    elif process.returncode != 0:
        print(f"Server exited with error code {process.returncode}")

def main():
    app = QApplication(sys.argv)
    window = MyWindow()

    while True:
        print("欢迎使用CDWA服务端管理系统，开发作者：coffee_dou")
        print("1.配置服务端环境（首次部署需执行）")
        print("2.注册用户")
        print("3.删除当前服务端内所有聊天记录")
        print("4.启动服务主进程")
        print("5.停止服务主进程")
        choose = str(input("请输入你的选择："))
        if choose == '1':
            os.system(os.path.join(file_weizhi, "服务端配置一键脚本.bat"))
            os.system("cls")
        elif choose == "2":
            os.system("python " + os.path.join(file_weizhi, "design.py"))
            os.system("cls")
        elif choose == '4':
            print("服务主进程启动中...")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(start_server())
            os.system("cls")
        elif choose == "5":
            stop_server()
            os.system("cls")
        elif choose == "3":
            window.show3()
        else:
            print("此功能还没被开发，敬请期待~")
            time.sleep(1)
            os.system("cls")

if __name__ == '__main__':
    main()
