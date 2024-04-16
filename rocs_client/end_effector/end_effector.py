from dataclasses import dataclass
from typing import Callable

from rocs_client.robot import RobotBase


@dataclass
class EndEffectorScheme:
    """
    EndEffectorScheme Class

    Attribute:
        - x (float): position for x
        - y (float): position for y
        - z (float): position for z
        - qx (float): Quaternion .x
        - qy (float): Quaternion .y
        - qz (float): Quaternion .z
        - qw (float): Quaternion .w
        - vx (float): Velocity for x
        - vy (float): Velocity for y
        - vz (float): Velocity for z

    Example:
        # Creating an instance of the EndEffectorScheme class

        instance = EndEffectorScheme(x=1, y=1, z=1, qx=1, qy=1, qz=1, qw=1)
    """
    # Position
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    # Quaternion
    qx: float = 0.0
    qy: float = 0.0
    qz: float = 0.0
    qw: float = 0.0
    # Angular Velocity（Reserved field）
    vx: float = 0.0
    vy: float = 0.0
    vz: float = 0.0


class EndEffector(RobotBase):

    def __init__(self, ssl: bool = False, host: str = '127.0.0.1', port: int = 8001, on_connected: Callable = None,
                 on_message: Callable = None, on_close: Callable = None, on_error: Callable = None):
        super().__init__(ssl, host, port, on_connected, on_message, on_close, on_error)

    def enable(self):
        """ Enable the end control service. """
        return self._send_request(url='/robot/end_effector/enable', method="GET")

    def disable(self):
        """ Disable the end control service """
        return self._send_request(url='/robot/end_effector/disable', method="GET")

    def enable_state(self, frequency: int = 1):
        """ Enable status monitoring to obtain information such as current position and Angle! """
        return self._send_request(url=f'/robot/enable_terminal_state?frequency={frequency}', method="GET")

    def disable_state(self):
        """ Disable status monitoring """
        return self._send_request(url='/robot/enable_terminal_state', method="GET")

    def control_left(self, param: EndEffectorScheme):
        """ Controlling left hand """
        data = {
            "param": {
                "x": param.x,
                "y": param.y,
                "z": param.z,
                "qx": param.qx,
                "qy": param.qy,
                "qz": param.qz,
                "qw": param.qw,
                "vx": param.vx,
                "vy": param.vy,
                "vz": param.vz
            },
            "system": 1
        }
        self._send_websocket_msg({'command': 'left_hand_pr', 'data': data})

    def control_right(self, param: EndEffectorScheme):
        """ Controlling right hand """
        data = {
            "param": {
                "x": param.x,
                "y": param.y,
                "z": param.z,
                "qx": param.qx,
                "qy": param.qy,
                "qz": param.qz,
                "qw": param.qw,
                "vx": param.vx,
                "vy": param.vy,
                "vz": param.vz
            },
            "system": 1
        }
        self._send_websocket_msg({'command': 'right_hand_pr', 'data': data})
