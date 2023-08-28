from typing import Any, Dict, Callable

import requests

from ..robot_base import RobotBase
from ..robot_type import RobotType


class Human(RobotBase):

    def __init__(self, ssl: bool = False, host: str = '127.0.0.1', port: int = 8001, on_open: Callable = None,
                 on_message: Callable = None, on_close: Callable = None, on_error: Callable = None):

        super().__init__(ssl, host, port, on_open, on_message, on_close, on_error)
        self.type: RobotType = RobotType.HUMAN

    def stand(self) -> Dict[str, Any]:
        if self.type == RobotType.HUMAN.value:
            response = requests.post(f'{self._baseurl}/robot/stand')
            return response.json()
        print('robot type not allow this command! The current function is only applicable to human')

    def get_joint_limit(self) -> Dict[str, Any]:
        if self.type == RobotType.HUMAN.value:
            response = requests.get(f'{self._baseurl}/robot/joint_limit')
            return response.json()
        print('robot type not allow this command! The current function is only applicable to humans')

    def get_joint_states(self) -> Dict[str, Any]:
        if self.type == RobotType.HUMAN.value:
            response = requests.get(f'{self._baseurl}/robot/joint_states')
            return response.json()
        print('robot type not allow this command! The current function is only applicable to humans')

    def enable_debug_state(self, frequence: int = 1):
        if self.type == RobotType.HUMAN.value:
            response = requests.get(f'{self._baseurl}/robot/enable_states_listen')
            return response.json()
        print('robot type not allow this command! The current function is only applicable to humans')

    def disable_debug_state(self):
        if self.type == RobotType.HUMAN.value:
            response = requests.get(f'{self._baseurl}/robot/disable_states_listen')
            return response.json()
        print('robot type not allow this command! The current function is only applicable to humans')

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
        if self.type == RobotType.HUMAN.value:
            self._send_websocket_msg({
                'command': 'head',
                'data': {
                    'roll': roll,
                    'pitch': pitch,
                    'yaw': yaw
                }
            })
        print('robot type not allow this command! The current function is only applicable to human')
