"""RobotBase Class

The `RobotBase` class is the base class for interacting with robots in the RoCS (Robot Control System) Client SDK.

Attribute:
    - _baseurl (str): The base URL for HTTP requests.
    - _ws_url (str): The WebSocket URL for connecting to the robot.
    - _ws (WebSocket): WebSocket connection object.
    - _on_connected (Callable): Callback function for the connection event.
    - _on_message (Callable): Callback function for incoming messages.
    - _on_close (Callable): Callback function for the connection close event.
    - _on_error (Callable): Callback function for connection errors.
    - camera (Camera): Instance of the Camera class for camera-related functionalities.
    - system (System): Instance of the System class for system-related functionalities.

Method:
    - __init__(ssl: bool = False, host: str = '127.0.0.1', port: int = 8001,
    Constructor method for the RobotBase class.
            - on_connected: Callable = None, on_message: Callable = None,

            - on_close: Callable = None, on_error: Callable = None):



    - _event():

        Private method handling events from the WebSocket connection.

    - _send_websocket_msg(message: json):

        Private method for sending WebSocket messages.
    - _send_request(url: str, method: str = 'GET', params=None, json=None):

        Private method for sending HTTP requests.
    - _send_request_stream(url: str, method: str = 'GET', params=None, json=None):

        Private method for sending HTTP requests with streaming support.
    - _cover_param(value: float, name: str, min_threshold: float, max_threshold: float) -> float:

        Class method for handling numerical parameters within defined thresholds.
    - start() -> dict:

        Method for initiating the process to reset, zero, or calibrate the robot.
    - stop() -> dict:

        Method for initiating the process to safely power down the robot.
    - exit():

        Method for disconnecting from the robot.

Usage:
    from rocs_client.robot.robot_base import RobotBase

Example:
    # Creating an instance of the RobotBase class

    robot = RobotBase()

    # Initiating the process to reset, zero, or calibrate the robot

    result = robot.start()
    print(result)

    # Safely powering down the robot

    result = robot.stop()
    print(result)

    # Disconnecting from the robot

    robot.exit()

Note:
    Ensure that you have the necessary dependencies installed and a valid connection to your robot before using the SDK.
"""
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
    """ Base class for Robot

    When instantiated, it connects to the corresponding robot's port via WebSocket.
    """

    def __init__(self, ssl: bool = False, host: str = '127.0.0.1', port: int = 8001,
                 on_connected: Callable = None, on_message: Callable = None,
                 on_close: Callable = None, on_error: Callable = None):
        if ssl:
            self._baseurl: str = f'https://{host}:{port}'
            self._ws_url = f'wss://{host}:{port}/ws'
        else:
            self._baseurl: str = f'http://{host}:{port}'
            self._ws_url: str = f'ws://{host}:{port}/ws'

        try:
            self._ws: WebSocket = create_connection(self._ws_url)
        except ConnectionRefusedError as e:
            print(f'Error connecting to the robot. Please check the server status. {e}')
            return
        except Exception as e:
            print(
                f'Error connecting to the robot. Please check the network settings, server availability, and ensure '
                f'the correct IP address and port are used. {e}')
            return

        self._on_connected = on_connected
        self._on_message = on_message
        self._on_close = on_close
        self._on_error = on_error

        self.camera = Camera(self._baseurl)
        self.system = System()

        self._receive_thread = threading.Thread(target=self._event)
        self._receive_thread.start()

    def _event(self):
        if self._on_connected:
            asyncio.run(self._on_connected())
        try:
            while True:
                message = self._ws.recv()
                if self._on_message:
                    asyncio.run(self._on_message(message))
        except websocket.WebSocketConnectionClosedException:
            if self._on_close:
                asyncio.run(self._on_close())
        except websocket.WebSocketException as e:
            if self._on_error:
                asyncio.run(self._on_error(e))

    def _send_websocket_msg(self, message: json):
        self._ws.send(json.dumps(message))

    def _send_request(self, url: str, method: str = 'GET', params=None, json=None):
        try:
            response = requests.request(method, f'{self._baseurl}{url}', params=params, json=json)
            return response.json()
        except Exception as e:
            print(f'Failed to send command. Please check the server status and ensure the command is valid. {e}')
            return {"code": -1,
                    "msg": f"Failed to send command. Please check the server status and ensure the command is valid.",
                    "data": None}

    def _send_request_stream(self, url: str, method: str = 'GET', params=None, json=None):
        response = requests.request(method, f'{self._baseurl}{url}', params=params, json=json, stream=True)
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                yield chunk

    @classmethod
    def _cover_param(cls, value: float, name: str, min_threshold: float, max_threshold: float) -> float:
        """
        Used to handle a numerical parameter along with its value, minimum, and maximum thresholds. It guarantees that the parameter stays within the defined range, and if it falls outside those bounds, it adjusts it to the nearest threshold.

        """
        if value is None:
            print(f"Invalid parameter: {name} is {value}. The value 0 will be used")
            value = 0
        if value > max_threshold:
            print(
                f"Invalid parameter: {name} ({value}) exceeds maximum allowed value ({max_threshold}). The maximum value {max_threshold} will be used."
            )
            value = max_threshold
        if value < min_threshold:
            print(
                f"Invalid parameter: {name} ({value}) is less than the minimum allowed value ({min_threshold}). The minimum value ({min_threshold}) will be used."
            )
            value = min_threshold
        return value

    def start(self):
        """
        Used to initiate the process to reset, zero, or calibrate the robot, bringing it to its initial state.
        This command is crucial when you intend to take control of the robot, ensuring it starts from a known and calibrated position.
        Ensure that the robot has sufficient clearance and is ready for the calibration process before issuing this command.
        """
        return self._send_request(url='/robot/start', method='POST')

    def stop(self):
        """
        Used to initiate the process to safely power down the robot. This command takes precedence over other commands, ensuring an orderly shutdown. It is recommended to trigger this command in emergency situations or when an immediate stop is necessary.

        Use this command with caution, as it results in a powered-down state of the robot. Ensure that there are no critical tasks or movements in progress before invoking this command to prevent unexpected behavior.

        """
        return self._send_request(url="/robot/stop", method="POST")

    def exit(self):
        """ Used to disconnect from the robot."""
        self._ws.close()
