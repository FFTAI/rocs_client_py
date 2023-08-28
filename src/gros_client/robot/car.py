from enum import Enum
from typing import Callable, Dict, Any

import requests

from ..robot_base import RobotBase
from ..robot_type import RobotType


class Mod(Enum):
    MOD_4_WHEEL = "WHEEL_4",
    MOD_3_WHEEL = "WHEEL_3",
    MOD_2_WHEEL = "WHEEL_2",

    _MOD_HOME = 'HOME',
    _MOD_FIX = 'FIX',
    _MOD_ACTION = 'ACTION',


class Car(RobotBase):
    def __init__(self, ssl: bool = False, host: str = '127.0.0.1', port: int = 8001, on_open: Callable = None,
                 on_message: Callable = None, on_close: Callable = None, on_error: Callable = None):
        super().__init__(ssl, host, port, on_open, on_message, on_close, on_error)
        self._mod = None
        self._type: RobotType = RobotType.CAR

    def set_mode(self, mod: Mod) -> Dict[str, Any]:
        self._mod: Mod = mod
        data = {'mod_val': mod}
        response = requests.post(f'{self._baseurl}/robot/mode', data)
        return response.json()

    def move(self, angle: float, speed: float):
        angle = self._cover_param(angle, 'angle', -45, 45)
        speed = self._cover_param(speed, 'speed', -500, 500)
        self._send_websocket_msg({
            'command': 'move',
            'data': {
                'angle': angle,
                'speed': speed
            }
        })
