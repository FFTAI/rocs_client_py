from typing import Callable

from ..robot_base import RobotBase
from ..robot_type import RobotType


class Dog(RobotBase):
    def __init__(self, ssl: bool = False, host: str = '127.0.0.1', port: int = 8001, on_open: Callable = None,
                 on_message: Callable = None, on_close: Callable = None, on_error: Callable = None):
        super().__init__(ssl, host, port, on_open, on_message, on_close, on_error)
        self.type: RobotType = RobotType.DOG
