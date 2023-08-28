from typing import Any, Dict, Callable

import requests

from ..robot_base import RobotBase


class Human(RobotBase):

    def __init__(self, ssl: bool = False, host: str = '127.0.0.1', port: int = 8001, on_open: Callable = None,
                 on_message: Callable = None, on_close: Callable = None, on_error: Callable = None):
        super().__init__(ssl, host, port, on_open, on_message, on_close, on_error)

    def stand(self) -> Dict[str, Any]:
        response = requests.post(f'{self._baseurl}/robot/stand')
        return response.json()

    def get_joint_limit(self) -> Dict[str, Any]:
        response = requests.get(f'{self._baseurl}/robot/joint_limit')
        return response.json()

    def get_joint_states(self) -> Dict[str, Any]:
        response = requests.get(f'{self._baseurl}/robot/joint_states')
        return response.json()

    def enable_debug_state(self, frequence: int = 1):
        response = requests.get(f'{self._baseurl}/robot/enable_states_listen')
        return response.json()

    def disable_debug_state(self):
        response = requests.get(f'{self._baseurl}/robot/disable_states_listen')
        return response.json()

    def walk(self, angle: float, speed: float):
        angle = self._cover_param(angle, 'angle', -45, 45)
        speed = self._cover_param(speed, 'speed', -0.8, 0.8)
        self._send_websocket_msg({
            'command': 'move',
            'data': {
                'angle': angle,
                'speed': speed
            }
        })

    def head(self, roll: float, pitch: float, yaw: float):
        self._send_websocket_msg({
            'command': 'head',
            'data': {
                'roll': roll,
                'pitch': pitch,
                'yaw': yaw
            }
        })
