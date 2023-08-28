import asyncio
import json
import threading
from typing import Callable, Dict, Any

import requests
import websocket
from websocket import *

from .common.camera import Camera
from .common.system import System


class RobotBase:
    """ robot base class

    when instantiated create A websocket client!
    so you need to implement the corresponding 'on_**' function to process to your business logic
    """

    def __init__(self, ssl: bool = False, host: str = '127.0.0.1', port: int = 8001,
                 on_open: Callable = None, on_message: Callable = None,
                 on_close: Callable = None, on_error: Callable = None):
        """

        Args:
            ssl(bool):  https ?
            host(str):  The host where your service or robot is located
            port(int):  The port where your service or robot is located
            on_open(Callable):  events when connected to robotic devices
            on_message(Callable): events when the robot replies
            on_close(Callable): events when closed to robotic devices
            on_error(Callable): events when error to robotic devices
        """
        if ssl:
            self._baseurl: str = f'https://{host}:{port}'
            self._ws_url = f'wss://{host}:{port}/ws'
        else:
            self._baseurl = f'http://{host}:{port}'
            self._ws_url = f'ws://{host}:{port}/ws'

        self._ws: WebSocket = create_connection(self._ws_url)
        self._on_open = on_open
        self._on_message = on_message
        self._on_close = on_close
        self._on_error = on_error

        self.camera = Camera(self._baseurl)
        self.system = System()

        if self._ws:
            asyncio.run(self._on_open(self._ws))
        self._receive_thread = threading.Thread(target=self._event_)
        self._receive_thread.start()

    def _event_(self):
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

    def start(self) -> Dict[str, Any]:
        """ robot start

        When you want to control the robot
        """
        response = requests.post(f'{self._baseurl}/robot/start')
        return response.json()

    def stop(self):
        """ robot stop

        This command takes precedence over other commands! Stop in case of emergency
        """
        response = requests.post(f'{self._baseurl}/robot/stop')
        return response.json()

    def exit(self):
        """
        Close the socket link when you finish to avoid memory leaks
        """
        self._ws.close()
