import asyncio
import json
import queue
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, Callable

import requests
import websockets

from websocket import *


class Mod:
    MOD_ORIGINAL = 'ORIGINAL'
    MOD_ACTION = 'ACTION'
    MOD_HOME = 'HOME'
    MOD_FIX = 'FIX'

    MOD_4_WHEEL = 'WHEEL_4'
    MOD_3_WHEEL = 'WHEEL_3'
    MOD_2_WHEEL = 'WHEEL_2'


class RobotType:
    CAR = 'car'
    HUMAN = 'human'
    DOG = 'dog'


executor = ThreadPoolExecutor()


class Robot:

    def __init__(self, ssl: bool = False, host: str = '127.0.0.1'):

        self.mod = Mod.MOD_ORIGINAL
        self.type: str = 'human'
        self.states_queue = queue.Queue()
        self.error_queue = queue.Queue()
        if ssl:
            self.baseurl = f'https://{host}:8001'
            self.ws_url = f'wss://{host}:8001/ws'
        else:
            self.baseurl = f'http://{host}:8001'
            self.ws_url = f'ws://{host}:8001/ws'

        self.message: queue = None
        self.websocket: websockets = None
        # asyncio.get_event_loop().run_until_complete(self._connect())
        self.ws: WebSocket = create_connection(self.ws_url)
        print(self.ws_url)
        self.receive_thread = threading.Thread(target=self.receive_loop)
        self.receive_thread.start()

    def receive_loop(self):
        while True:
            result = self.ws.recv()
            result_json = json.loads(result)
            if "function" in result_json:
                print("生产：length", self.states_queue.qsize())
                if (self.states_queue.qsize() > 0):
                    print("生产:先移除，后添加")
                    self.states_queue.get()
                    self.states_queue.put(result)
                else:
                    print("生产:直接添加")
                    self.states_queue.put(result)
            else:
                self.error_queue.put(result)
            print(result)

    def get_states(self):
        if self.states_queue.qsize() > 0:
            return self.states_queue.get()
        else:
            return None

    async def connect_to_server(self):
        async with websockets.connect('ws://localhost:8001/ws') as websocket:
            self.websocket = await websockets.connect(self.ws_url)
            if self.on_open:
                await self.on_open(self.websocket)
            while True:
                message = await websocket.recv()
                print(message)

    def get_type(self) -> Dict[str, Any]:
        response = requests.get(f'{self.baseurl}/robot/type')
        return response.json()

    def set_mode(self, mod: Mod) -> Dict[str, Any]:
        if self.type == RobotType.CAR:
            self.mod = mod
            data = {'mod_val': mod}
            response = requests.post(f'{self.baseurl}/robot/mode', data)
            return response.json()
        print('robot type not allow this command! The current function is only applicable to car')

    def get_joint_limit(self) -> Dict[str, Any]:
        if self.type == RobotType.HUMAN:
            response = requests.get(f'{self.baseurl}/robot/jointLimit')
            return response.json()
        print('robot type not allow this command! The current function is only applicable to humans')

    def get_joint_states(self) -> Dict[str, Any]:
        if self.type == RobotType.HUMAN:
            response = requests.get(f'{self.baseurl}/robot/jointStates')
            return response.json()
        print('robot type not allow this command! The current function is only applicable to humans')

    def enable_debug_state(self, frequence: int = 1):
        if self.type == RobotType.HUMAN:
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

    async def stand(self) -> Dict[str, Any]:
        if self.type == RobotType.HUMAN:
            response = requests.post(f'{self.baseurl}/robot/stand')
            return response.json()
        print('robot type not allow this command! The current function is only applicable to human')

    async def move(self, angle: float, speed: float):
        angle = self._cover_param(angle, 'angle', -45, 45)
        speed = self._cover_param(speed, 'speed', -0.8, 0.8)
        self._send_websocket_msg({
            'command': 'move',
            'data': {
                'angle': angle,
                'speed': speed
            }
        })

    async def head(self, roll: float, pitch: float, yaw: float):
        if self.type == RobotType.HUMAN:
            await self._send_websocket_msg({
                'command': 'head',
                'data': {
                    'roll': roll,
                    'pitch': pitch,
                    'yaw': yaw
                }
            })
        print('robot type not allow this command! The current function is only applicable to human')

    @staticmethod
    def _cover_param(param: float, value: str, min_threshold: float, max_threshold: float) -> float:
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

    def _send_websocket_msg(self, message: json):
        self.ws.send(json.dumps(message))

    def close_websocket(self):
        self.ws.close()
