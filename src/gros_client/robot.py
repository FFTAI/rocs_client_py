import asyncio
import json
import threading
from typing import Any, Dict, Callable

import requests
import websocket
from websocket import *

from .mod import Mod
from .robot_type import RobotType

'''
# todo: 前端实际上需要大致还原出后端的类结构：

FFTAI
    L robotics
        L Robot
            L Human
            L Car
            L Dog
        L Common
            L Cammera
            L Slam
            L Speaker
    L system
        L 

        
在使用的时候：


import * from FFTAI
robot = robotics.Robot.Human()
robot.start()


前端的SDK结构，OpenAI做的不错，可以作为我们的示例。

'''


class Robot:

    def __init__(self, ssl: bool = False, host: str = '127.0.0.1',
                 on_open: Callable = None, on_message: Callable = None,
                 on_close: Callable = None, on_error: Callable = None):
        self.on_open = on_open
        self.on_message = on_message
        self.on_close = on_close
        self.on_error = on_error
        self.type: str = ''
        self.mod = Mod.MOD_ORIGINAL

        if ssl:
            self.baseurl = f'https://{host}:8001'
            self.ws_url = f'wss://{host}:8001/ws'
        else:
            self.baseurl = f'http://{host}:8001'
            self.ws_url = f'ws://{host}:8001/ws'

        self.ws: WebSocket = create_connection(self.ws_url)
        if self.on_open:
            asyncio.run(self.on_open(self.ws))

        self.type: str = self.get_type()['data']
        self.receive_thread = threading.Thread(target=self._receive_loop)
        self.receive_thread.start()

    def _receive_loop(self):
        while True:
            try:
                message = self.ws.recv()
                if self.on_message:
                    asyncio.run(self.on_message(self.ws, message))
            except websocket.WebSocketConnectionClosedException as e:
                if self.on_close:
                    asyncio.run(self.on_close(self.ws))
            except websocket.WebSocketException as e:
                if self.on_close:
                    asyncio.run(self.on_error(self.ws, e))

    def get_type(self) -> Dict[str, Any]:
        response = requests.get(f'{self.baseurl}/robot/type')
        return response.json()

    def get_video_status(self) -> Dict[str, Any]:
        response = requests.get(f'{self.baseurl}/control/camera_status')
        return response.json()

    def get_video_stream_url(self) -> str:
        return f'{self.baseurl}/control/camera'

    def set_mode(self, mod: Mod) -> Dict[str, Any]:
        if self.type == RobotType.CAR.value:
            self.mod = mod.value
            data = {'mod_val': mod}
            response = requests.post(f'{self.baseurl}/robot/mode', data)
            return response.json()
        print('robot type not allow this command! The current function is only applicable to car')

    def get_joint_limit(self) -> Dict[str, Any]:
        if self.type == RobotType.HUMAN.value:
            response = requests.get(f'{self.baseurl}/robot/joint_limit')
            return response.json()
        print('robot type not allow this command! The current function is only applicable to humans')

    def get_joint_states(self) -> Dict[str, Any]:
        if self.type == RobotType.HUMAN.value:
            response = requests.get(f'{self.baseurl}/robot/joint_states')
            return response.json()
        print('robot type not allow this command! The current function is only applicable to humans')

    def enable_debug_state(self, frequence: int = 1):
        if self.type == RobotType.HUMAN.value:
            self._send_websocket_msg({
                'command': 'states',
                'data': {
                    'frequence': frequence
                }
            })
            print('The debug state is enabled successfully! '
                  'please listen to the data with the on_message function processing function as "SonnieGetStates"')
        else:
            print('robot type not allow this command! The current function is only applicable to humans')

    def disable_debug_state(self):
        if self.type == RobotType.HUMAN.value:
            self._send_websocket_msg({
                'command': 'states',
                'data': {
                    'switch': False
                }
            })
            print('The debug state is enabled successfully! '
                  'please listen to the data with the on_message function processing function as "SonnieGetStates"')
        else:
            print('robot type not allow this command! The current function is only applicable to humans')

    def stand(self) -> Dict[str, Any]:
        if self.type == RobotType.HUMAN.value:
            response = requests.post(f'{self.baseurl}/robot/stand')
            return response.json()
        print('robot type not allow this command! The current function is only applicable to human')

    def move(self, angle: float, speed: float):
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

    def close_websocket(self):
        self.ws.close()

    def _send_websocket_msg(self, message: json):
        self.ws.send(json.dumps(message))

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
