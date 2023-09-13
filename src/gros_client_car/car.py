import asyncio
import json
import threading
from enum import Enum
from typing import Callable, Dict, Any

import requests
import websocket
from websocket import *


class Mod(Enum):
    """ 对应car set_mode函数的参数 """
    _HOME = 590338
    _STOP = 131331

    MOD_4_WHEEL = 592385
    MOD_3_WHEEL = 592386
    MOD_2_WHEEL = 592387


class Car:
    """
    Car对象

    在你需要连接Car的时候，你可以创建一个Car()对象！ 这将会在后台连接到控制系统，并提供对应的控制函数和状态监听！

    Args:
        ssl(bool):  是否开启ssl认证。默认 False
        host(str):  car的网络IP
        port(int):  car的控制服务的PORT
        on_connected(Callable):  该监听将会在car连接成功时触发
        on_message(Callable): 该监听将会在car发送系统状态时候触发，你可能需要监听该事件处理你的逻辑
        on_close(Callable): 该监听将会在car连接关闭时触发
        on_error(Callable): 该监听将会在car发生错误时触发
    """
    video_stream_url: str
    _mod: Mod

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
        self.video_stream_url = f'{self._baseurl}/control/camera'

        if self._ws:
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

    def _cover_param(self, param: float, value: str, min_threshold: float, max_threshold: float) -> float:
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

    def exit(self):
        """ 断开Robot链接 """
        self._ws.close()

    def video_status(self):
        """ 获取设备视频状态 """
        response = requests.get(f'{self._baseurl}/control/camera_status')
        return response.json()

    def start(self):
        """ 小车启动 """
        response = requests.post(f'{self._baseurl}/control/car/mode', json={"mode": Mod._HOME.value,
                                                                            "host": '127.0.0.1',
                                                                            "port": 4197
                                                                            })
        return response.json()

    def stop(self):
        """ 小车急停

        ``该命令优先于其他命令! 会掉电停止。请在紧急情况下触发``
        """
        response = requests.post(f'{self._baseurl}/control/car/mode',
                                 json={"mode": Mod._STOP.value, "host": '127.0.0.1', "port": 4197})
        return response.json()

    def set_mode(self, mod: Mod):
        """
        设置小车的运动模式

        完成后小车将在对应模式下运动，包括 4轮 3轮 2轮 （请确认电机限位等因素）

        Args:
            mod(Mod): 模式对象定义
        """
        self._mod: Mod = mod
        response = requests.post(f'{self._baseurl}/control/car/mode',
                                 json={"mode": mod.value, "host": '127.0.0.1', "port": 4197})
        return response.json()

    def move(self, velocity: float, direction: float):
        """
        控制Car行走

        ``该请求维持了长链接的方式进行发送``

        Args:
            direction(float): 方向/角度 控制方向，取值范围为正负45度。向左为正，向右为负！(浮点数8位)
            velocity(float): 速度 控制前后，取值范围为正负500。向前为正，向后为负！(浮点数8位)
        """
        velocity = self._cover_param(velocity, 'velocity', -500, 500)
        direction = self._cover_param(direction, 'direction', -45, 45)
        self._send_websocket_msg({
            "host": '127.0.0.1',
            "port": 4197,
            "type": 'command',
            "client_type": "car",
            'command': 'operate',
            'velocity': velocity,
            'direction': direction
        })
