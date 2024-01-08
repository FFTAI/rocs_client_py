from enum import Enum
from typing import Callable, Dict

from .robot_base import RobotBase


class Mod(Enum):
    """
    Enumeration of Modes for the `set_mode` Function.
    """
    MOD_4_WHEEL = "WHEEL_4"
    MOD_3_WHEEL = "WHEEL_3"
    MOD_2_WHEEL = "WHEEL_2"

    _MOD_HOME = 'HOME'
    _MOD_FIX = 'FIX'
    _MOD_ACTION = 'ACTION'


class Car(RobotBase):
    """
    The `Car` class implements the behavior of car robots and facilitates communication with its control system. It provides
    control functions and real-time status monitoring.


    Args:

        - ssl (bool, optional): Indicates whether SSL authentication is enabled. Defaults to False.
        - host (str, optional): Specifies the network IP address of the car. Defaults to '127.0.0.1'.
        - port (int, optional): Specifies the PORT of the car control service. Defaults to 8001.
        - on_connected (Callable, optional): A callback function triggered upon successful car connection.
          Defaults to None.
        - on_message (Callable, optional): A callback function triggered when the car sends system status.
          Defaults to None.
        - on_close (Callable, optional): A callback function triggered when the car connection is closed.
          Defaults to None.
        - on_error (Callable, optional): A callback function triggered when a car-related error occurs.
          Defaults to None.
    """

    def __init__(self, ssl: bool = False, host: str = '127.0.0.1', port: int = 8001, on_connected: Callable = None,
                 on_message: Callable = None, on_close: Callable = None, on_error: Callable = None):
        super().__init__(ssl, host, port, on_connected, on_message, on_close, on_error)
        self._mod = None

    def set_mode(self, mod: Mod):
        """
        Set the car mode.

        The car will move in the corresponding mode, which can be one of the following:
           - 4-wheel mode
           - 3-wheel mode
           - 2-wheel mode

        Args:
           mod (Mod): The mode object definition.

        Returns:
           Dict: A dictionary containing the following keys:
              - `code` (int): Status code, where 0 indicates normal and -1 indicates an anomaly.
              - `msg` (str): Result message.
        """

        self._mod: Mod = mod
        return self._send_request(url='/robot/mode', method="POST", json={'mod_val': mod})

    def move(self, angle: float, speed: float):
        """
        Control the car's movement.

        The request is sent by maintaining a long-lived connection.

        Args:

             angle(float): Angle control for direction. The value ranges from -45 to +45 degrees, where left is positive and right is negative. Precision of 8 decimal places.
             speed(float): Speed control for forward and backward movement. The value can be between -500 and +500, with positive values indicating forward and negative values indicating backward. Precision of 8 decimal places.
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
