from enum import Enum
from typing import Callable, Dict

from .robot_base import RobotBase


class Mod(Enum):
    """
    Enumerates arguments applicable to the `set_mode` function.
    """
    MOD_4_WHEEL = "WHEEL_4"
    MOD_3_WHEEL = "WHEEL_3"
    MOD_2_WHEEL = "WHEEL_2"

    _MOD_HOME = 'HOME'
    _MOD_FIX = 'FIX'
    _MOD_ACTION = 'ACTION'


class Car(RobotBase):
    """
    This class represents a Car object, providing functionality for connecting to the control system and controlling the car's movements and monitoring its status.

    Args:

        ssl(bool): Indicates whether SSL authentication is enabled. Default is False.
        host(str): Specifies the network IP address of the car robot. Default is '127.0.0.1'.
        port(int): Specifies the PORT of the car robot. Default is 8001.
        on_connected(callable): Listener triggered when the connection to the car robot is successful.
        on_message(callable): Listener triggered when the car robot sends messages.
        on_close(callable): Listener triggered when the connection to the car robot is closed.
        on_error(callable): Listener triggered when error occurs in the car robot.
    """

    def __init__(self, ssl: bool = False, host: str = '127.0.0.1', port: int = 8001, on_connected: Callable = None,
                 on_message: Callable = None, on_close: Callable = None, on_error: Callable = None):
        super().__init__(ssl, host, port, on_connected, on_message, on_close, on_error)
        self._mod = None

    def set_mode(self, mod: Mod):
        """
        Set the motion mode of the car robot. This function sends a POST request to the "/robot/mode" endpoint with the
        specified mode value.

        Once completed, the car robot will move in the corresponding mode, including 4-wheel, 3-wheel, and 2-wheel modes.

        Args:

            mod(Mod): Mode object definition

        Returns:

            Dict:
                `code` (int): Status code. 0 for normal, -1 for anomaly.
                `msg` (str): Result message.
        """
        self._mod: Mod = mod
        return self._send_request(url='/robot/mode', method="POST", json={'mod_val': mod})

    def move(self, angle: float, speed: float):
        """
        Control the car robot's movements.

        The request is sent via a long-lived connection

        Args:

             angle(float): Angle control for direction. Range: -45 to 45 degrees. Positive for left, negative for right. Precision with 8 decimal places.
             speed(float): Speed control for forward and backward. Range: -500 to 500. Positive for forward, negative for backward. Precision with 8 decimal places.
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
