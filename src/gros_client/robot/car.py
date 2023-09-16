from enum import Enum
from typing import Callable, Dict, Any

import requests

from .robot_base import RobotBase


class Mod(Enum):
    """ 对应car set_mode函数的参数 """

    MOD_4_WHEEL = "WHEEL_4"
    MOD_3_WHEEL = "WHEEL_3"
    MOD_2_WHEEL = "WHEEL_2"

    _MOD_HOME = 'HOME'
    _MOD_FIX = 'FIX'
    _MOD_ACTION = 'ACTION'


class Car(RobotBase):
    """
    Car对象

    在你需要连接Car的时候，你可以创建一个Car()对象！ 这将会在后台连接到控制系统，并提供对应的控制函数和状态监听！

    Args:

        ssl(bool):  是否开启ssl认证。默认 False
        host(str):  car的网络IP
        port(int):  car的控制服务的PORT
        on_connected(Callable):  该监听将会在car连接成功时触发
        on_message(Callable): 该监听将会在car发送系统状态时候触发，你可能需要监听该回掉处理你的逻辑
        on_close(Callable): 该监听将会在car连接关闭时触发
        on_error(Callable): 该监听将会在car发生错误时触发
    """
    
    def __init__(self, ssl: bool = False, host: str = '127.0.0.1', port: int = 8001, on_connected: Callable = None,
                 on_message: Callable = None, on_close: Callable = None, on_error: Callable = None):
        super().__init__(ssl, host, port, on_connected, on_message, on_close, on_error)
        self._mod = None

    def set_mode(self, mod: Mod) -> Dict[str, Any]:
        """
        设置小车的模式

        完成后小车将在对应模式下运动，包括 4轮 3轮 2轮

        Args:

            mod(Mod): 模式对象定义

        Returns:

            Dict: 返回数据包含以下字段:

            - `code` (int): 状态码，0 表示正常，-1 表示异常
            - `msg` (str): 状态信息，"ok" 表示正常
        """
        self._mod: Mod = mod
        data = {'mod_val': mod}
        response = requests.post(f'{self._baseurl}/robot/mode', data)
        return response.json()

    def move(self, angle: float, speed: float):
        """
        控制Car行走

        ``该请求维持了长链接的方式进行发送``

        Args:

             angle(float): 角度 控制方向，取值范围为正负45度。向左为正，向右为负！(浮点数8位)
             speed(float): 速度 控制前后，取值范围为正负500。向前为正，向后为负！(浮点数8位)
        """
        angle = self._cover_param(angle, 'angle', -45, 45)
        speed = self._cover_param(speed, 'speed', -500, 500)
        self._send_websocket_msg({
            'command': 'move',
            'data': {
                'angle': angle,
                'speed': speed
            }
        })
