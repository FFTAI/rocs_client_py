import unittest

import websocket

from src.gros_client.mod import Mod
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

    def test_disable_debug_state(self):
        robot.disable_debug_state()

    def test_get_video_status(self):
        res = robot.get_video_status()
        print(f'video_status {res["data"]}')
        assert res.get('data')

    def test_get_video_stream_url(self):
        res = robot.get_video_stream_url()
        print(f'video stream url = {res}')

    def test_set_mode(self):
        res = robot.set_mode(Mod.MOD_4_WHEEL)
        print(f'test_set_mode {res["data"]}')
        assert res.get('code') == 0

    def test_get_joint_limit(self):
        res = robot.get_joint_limit()
        print(f'robot.test_get_joint_limit: {res}')
        assert res.get('code') == 0

    def test_get_joint_states(self):
        res = robot.get_joint_states()
        print(f'robot.test_get_joint_states: {res}')
        assert res.get('code') == 0

    def test_stand(self):
        res = robot.stand()
        print(f'robot.test_stand: {res}')
        assert res.get('code') == 0

    def test_move(self):
        res = robot.move(1, 0.8)
        print(f'robot.test_move: {res}')
        assert res.get('code') == 0

    def test_head(self):
        res = robot.head(1,1, 0.8)
        print(f'robot.test_head: {res}')
        assert res.get('code') == 0
