from dataclasses import dataclass
from typing import Callable

from rocs_client.robot import RobotBase


@dataclass
class EndEffectorScheme:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    qx: float = 0.0
    qy: float = 0.0
    qz: float = 0.0
    qw: float = 0.0
    vx: float = 0.0
    vy: float = 0.0
    vz: float = 0.0


class EndEffector(RobotBase):

    def __init__(self, ssl: bool = False, host: str = '127.0.0.1', port: int = 8001, on_connected: Callable = None,
                 on_message: Callable = None, on_close: Callable = None, on_error: Callable = None):
        super().__init__(ssl, host, port, on_connected, on_message, on_close, on_error)

    def enable(self):
        return self._send_request(url='/robot/end_effector/enable', method="GET")

    def disable(self):
        return self._send_request(url='/robot/end_effector/disable', method="GET")

    def enable_state(self, frequency: int = 1):
        return self._send_request(url='/robot/enable_terminal_state', method="GET")

    def disable_state(self):
        return self._send_request(url='/robot/enable_terminal_state', method="GET")

    async def control_left(self, param: EndEffectorScheme):
        data = {
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
        }
        await self._send_websocket_msg({'command': 'left_hand_pr', 'data': data})

    async def control_right(self, param: EndEffectorScheme):
        data = {
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
        }
        await self._send_websocket_msg({'command': 'right_hand_pr', 'data': data})
