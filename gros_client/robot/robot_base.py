import asyncio
import json
import threading
from typing import Callable

import requests
import websocket
from websocket import *

from ..common.camera import Camera
from ..common.system import System


class RobotBase:
    """ Robot 基类

    实例化的时候会通过websocket连接到对应设备的控制端口！
    """

    def __init__(self, ssl: bool = False, host: str = '127.0.0.1', port: int = 8001,
                 on_connected: Callable = None, on_message: Callable = None,
                 on_close: Callable = None, on_error: Callable = None):
        if ssl:
            self._baseurl: str = f'https://{host}:{port}'
            self._ws_url = f'wss://{host}:{port}/ws'
        else:
            self._baseurl = f'http://{host}:{port}'
            self._ws_url = f'ws://{host}:{port}/ws'

        self._ws: WebSocket = create_connection(self._ws_url)
        self._on_connected = on_connected
        self._on_message = on_message
        self._on_close = on_close
        self._on_error = on_error

        self.camera = Camera(self._baseurl)
        self.system = System()

        self._receive_thread = threading.Thread(target=self._event_)
        self._receive_thread.start()

    def _event_(self):
        if self._on_connected:
            asyncio.run(self._on_connected(self._ws))
        while True:
            try:
                message = self._ws.recv()
                if self._on_message:
                    asyncio.run(self._on_message(self._ws, message))
            except websocket.WebSocketConnectionClosedException:
                if self._on_close:
                    asyncio.run(self._on_close(self._ws))
            except websocket.WebSocketException as e:
                if self._on_error:
                    asyncio.run(self._on_error(self._ws, e))

    def _send_websocket_msg(self, message: json):
        self._ws.send(json.dumps(message))

    @classmethod
    def _cover_param(cls, param: float, value: str, min_threshold: float, max_threshold: float) -> float:
        if param is None:
            print(f"Illegal parameter: {value} = {param}")
            param = 0
        if param > max_threshold:
            print(
                f"Illegal parameter: {value} = {param}, "
                f"greater than maximum, expected not to be greater than {max_threshold}, actual {param}")
            param = max_threshold
        if param < min_threshold:
            print(
                f"Illegal parameter: {value} = {param}, "
                f"greater than maximum, expected not to be less than {min_threshold}, actual {param}")
            param = min_threshold
        return param

    def start(self):
        """ 启动 : 重置/归零/对设备初始状态的校准

        当你想要控制Robot设备的时候，你的第一个指令
        """
        response = requests.post(f'{self._baseurl}/robot/start')
        return response.json()

    def stop(self):
        """ 停止

        ``该命令优先于其他命令! 会掉电停止。请在紧急情况下触发``
        """
        response = requests.post(f'{self._baseurl}/robot/stop')
        return response.json()

    def exit(self):
        """ 断开Robot链接 """
        self._ws.close()
