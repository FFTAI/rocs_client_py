import asyncio
import json

import websockets

from src.gros_client.robot import WebSocketClient

# 使用示例
if __name__ == "__main__":
    send = None

    async def on_open(websocket: websockets.WebSocketClientProtocol):
        print("WebSocket opened")


    async def on_message(websocket: websockets.WebSocketClientProtocol, message: str):
        print("Received message:", message)


    async def on_close(websocket: websockets.WebSocketClientProtocol):
        print("WebSocket closed")


    async def on_error(websocket: websockets.WebSocketClientProtocol, error: Exception):
        print("WebSocket error:", error)


    # 创建WebSocketClient并指定WebSocket服务器的URL和回调函数
    client = WebSocketClient(host='127.0.0.1',
                             on_open=on_open,
                             on_message=on_message,
                             on_close=on_close,
                             on_error=on_error)

    loop = asyncio.get_event_loop()
    send = loop.create_task(client.send_message(json.dumps({"command": "states", "data": {"frequence": 1}})))

    asyncio.get_event_loop().run_until_complete(client.close())
