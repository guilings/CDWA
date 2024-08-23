import asyncio
import websockets
import csv
import json
import logging
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MESSAGE_FILE = './history/chat_history.txt'  # 聊天记录存储文件
CSV_FILE = 'users.csv'  # 用户数据存储文件

connected_clients = {}
file_last_modified = None

async def load_users():
    users = {}
    try:
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users[row['username']] = row['password']
        logging.info("用户数据加载完成。")
        return users
    except Exception as e:
        logging.error("加载用户数据时发生错误：%s", e)
        return None

async def authenticate(websocket, path, users):
    try:
        auth_data = await websocket.recv()
        auth_data = json.loads(auth_data)
        username = auth_data.get('username')
        password = auth_data.get('password')

        if username in users and users[username] == password:
            connected_clients[websocket] = username
            await websocket.send(json.dumps({'status': 'authenticated'}))
            logging.info(f"用户 {username} 已通过验证。")
        else:
            await websocket.send(json.dumps({'status': 'unauthorized'}))
            await websocket.close()
            logging.warning(f"用户 {username} 验证失败。")
    except Exception as e:
        logging.error("认证过程中出错：%s", e)
        await websocket.send(json.dumps({'status': 'error', 'message': str(e)}))
        await websocket.close()

def store_message(username, message):
    with open(MESSAGE_FILE, 'a') as file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file.write(f"{timestamp} - {username}: {message}\n")

async def send_history(websocket):
    try:
        with open(MESSAGE_FILE, 'r') as file:
            history = file.readlines()
            await websocket.send(json.dumps({'type': 'history', 'messages': history}))
    except FileNotFoundError:
        logging.warning("消息历史文件未找到。")

async def chat_handler(websocket, path):
    users = await load_users()
    if not users:
        logging.error("用户数据未加载，无法启动聊天处理器。")
        return

    await authenticate(websocket, path, users)
    username = connected_clients.get(websocket)
    if not username:
        await websocket.close()
        return

    await send_history(websocket)

    try:
        async for message in websocket:
            if message == 'get_history':
                await send_history(websocket)
            else:
                message_data = json.loads(message)
                user = message_data.get('username')
                content = message_data.get('message')
                store_message(user, content)
                logging.info(f"收到来自 {user} 的消息：{content}")
                for client in connected_clients.keys():
                    if client != websocket:
                        await client.send(f"{user}: {content}")
    except websockets.exceptions.ConnectionClosed:
        logging.info(f"用户 {username} 已断开连接。")
    finally:
        if websocket in connected_clients:
            del connected_clients[websocket]

async def file_watcher():
    global file_last_modified
    while True:
        if os.path.exists(MESSAGE_FILE):
            modified_time = os.path.getmtime(MESSAGE_FILE)
            if file_last_modified is None or modified_time > file_last_modified:
                file_last_modified = modified_time
                logging.info("检测到消息历史文件更新，通知所有客户端。")
                for websocket in connected_clients.keys():
                    await send_history(websocket)
        await asyncio.sleep(1)

start_server = websockets.serve(chat_handler, "0.0.0.0", 55668)  # 监听所有网络接口

async def main():
    await asyncio.gather(start_server, file_watcher())

asyncio.get_event_loop().run_until_complete(main())
logging.info("服务器已启动，监听在 ws://0.0.0.0:55668")
asyncio.get_event_loop().run_forever()
