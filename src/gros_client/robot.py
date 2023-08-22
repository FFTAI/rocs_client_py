# todo : import 的 约定是这样： 
#
# import系统库
# 然后空一行
# import 第三方
# 然后空一行
# import 自己的库

from typing import Callable
import asyncio

import websockets

# todo : 文件名 和 类名 不匹配。
# todo : 需要 pydantic 吗？

class WebSocketClient:
    def __init__(self, ssl: bool = False, host: str = '192.168.12.1', port: int = 8001, on_open: Callable = None,
                 on_message: Callable = None, on_close: Callable = None, on_error: Callable = None):
        if ssl:
            self.url = f'wss://{host}:{port}/ws'
            self.baseurl = f'https://{host}:{port}'
        else:
            self.url = f'ws://{host}:{port}/ws'
            self.baseurl = f'http://{host}:{port}'

        self.on_open = on_open
        self.on_message = on_message
        self.on_close = on_close
        self.on_error = on_error
        self.websocket = None
        asyncio.get_event_loop().run_until_complete(self._connect())

    async def _connect(self):
        self.websocket = await websockets.connect(self.url)
        if self.on_open:
            await self.on_open(self.websocket)

        while True:
            try:
                message = await self.websocket.recv()
                if self.on_message:
                    await self.on_message(self.websocket, message)
            except websockets.ConnectionClosed:
                if self.on_close:
                    await self.on_close(self.websocket)
                break
            except Exception as e:
                if self.on_error:
                    await self.on_error(self.websocket, e)
                break

    async def send_message(self, message: str):
        if self.websocket:
            await self.websocket.send(message)

    async def close(self):
        if self.websocket:
            await self.websocket.close()


