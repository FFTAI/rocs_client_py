from enum import Enum
from typing import Callable, Dict

from .robot_base import RobotBase


class Mod(Enum):
    """
    Arguments that apply to the `set_mode` Function
    """
    MOD_4_WHEEL = "WHEEL_4"
    MOD_3_WHEEL = "WHEEL_3"
    MOD_2_WHEEL = "WHEEL_2"

    _MOD_HOME = 'HOME'
    _MOD_FIX = 'FIX'
    _MOD_ACTION = 'ACTION'


class Car(RobotBase):
    """
    When you need to connect a Car, you can create a Car() object!
    This will connect to the control system in the background,
    and provide the corresponding control function and status monitoring!

    Args:

        ssl(bool): Indicates whether ssl authentication is enabled. Default False
        host(str): indicates the network IP address of the car
        port(int): specifies the PORT of the car control service
        on_connected(callable): This listener is triggered when the car connection is successful
        on_message(callable): This listener will be triggered when the car sends system status
        on_close(callable): This listener will be triggered when the car connection is closed
        on_error(callable): This listener will be triggered when a car error occurs
    """

    def __init__(self, ssl: bool = False, host: str = '127.0.0.1', port: int = 8001, on_connected: Callable = None,
                 on_message: Callable = None, on_close: Callable = None, on_error: Callable = None):
        super().__init__(ssl, host, port, on_connected, on_message, on_close, on_error)
        self._mod = None

    def set_mode(self, mod: Mod):
        """
        set the car mode

        the car will move in the corresponding mode, including 4 rounds, 3 rounds and 2 rounds

        Args:

            mod(Mod): Mode object definition

        Returns:

            Dict:
                `code` (int): statu code，0: Normal -1: Anomaly
                `msg` (str): result msg
        """
        self._mod: Mod = mod
        return self._send_request(url='/robot/mode', method="POST", json={'mod_val': mod})

    def move(self, angle: float, speed: float):
        """
        Control Car walk

        ``The request is sent by maintaining a long link``

        Args:

             angle(float): Angle Control direction. The value ranges from plus to minus 45 degrees. Left is positive, right is negative! (floating point 8 bits)
             speed(float): Before and after the speed control, the value can be plus or minus 500. Forward is positive, backward is negative! (floating point 8 bits)
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
