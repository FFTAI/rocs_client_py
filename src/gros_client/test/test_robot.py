import unittest

import websocket

from src.gros_client.robot import Robot
from src.gros_client.robot_type import RobotType


async def on_open(ws: websocket):
    print("WebSocket opened...")


async def on_message(ws: websocket, message: str):
    print("Received message:", message)


async def on_close(ws: websocket.WebSocketConnectionClosedException):
    print("WebSocket closed")


async def on_error(ws: websocket.WebSocketException, error: Exception):
    print("WebSocket error:", error)


robot = Robot(host='127.0.0.1',
              on_open=on_open,
              on_message=on_message,
              on_close=on_close,
              on_error=on_error)


class TestRobot(unittest.TestCase):

    def test_get_type(self):
        res = robot.get_type()
        print(res)
        assert res.get('data') == RobotType.HUMAN.value

    def test_enable_debug_state(self):
        robot.enable_debug_state(1)

    def test_get_video_status(self):
        ...

    def test_get_video_stream_url(self):
        ...
        # Test the get_video_stream_url method
        # ...

    def test_set_mode(self):
        ...
        # Test the set_mode method
        # ...

    def test_get_joint_limit(self):
        ...
        # Test the get_joint_limit method
        # ...

    def test_get_joint_states(self):
        ...
        # Test the get_joint_states method
        # ...

    def test_stand(self):
        ...
        # Test the stand method
        # ...

    def test_move(self):
        ...
        # Test the move method
        # ...

    def test_head(self):
        ...
        # Test the head method
        # ...

    def test_close_websocket(self):
        ...
