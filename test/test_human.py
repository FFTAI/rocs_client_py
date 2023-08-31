import unittest

import websocket

from src.gros_client import robot


async def on_open(ws: websocket):
    print("WebSocket opened...")


async def on_message(ws: websocket, message: str):
    print("Received message:", message)


async def on_close(ws: websocket.WebSocketConnectionClosedException):
    print("WebSocket closed")


async def on_error(ws: websocket.WebSocketException, error: Exception):
    print("WebSocket error:", error)


human = robot.Human(on_connected=on_open,host="192.168.9.17", on_message=on_message, on_close=on_close, on_error=on_error)


class TestHuman(unittest.TestCase):

    def test_enable_debug_state(self):
        res = human.enable_debug_state(1)
        assert res.get('code') == 0

    def test_disable_debug_state(self):
        res = human.disable_debug_state()
        assert res.get('code') == 0

    def test_get_video_status(self):
        res: bool = human.camera.video_stream_status
        print(f'test_get_video_status: {res}')
        assert res is True

    def test_get_video_stream_url(self):
        res: str = human.camera.video_stream_url
        print(f'video stream url:  {res}')

    def test_get_joint_limit(self):
        res = human.get_joint_limit()
        print(f'human.test_get_joint_limit: {res}')
        assert res.get('code') == 0

    def test_get_joint_states(self):
        res = human.get_joint_states()
        print(f'human.test_get_joint_states: {res}')
        assert res.get('code') == 0

    def test_start(self):
        res = human.start()
        print(f'human.test_start: {res}')
        assert res.get('code') == 0

    def test_stop(self):
        res = human.stop()
        print(f'human.test_stop: {res}')
        assert res.get('code') == 0

    def test_stand(self):
        res = human.stand()
        print(f'human.test_stand: {res}')
        assert res.get('code') == 0

    def test_move(self):
        human.walk(1, 0.8)

    def test_head(self):
        human.head(1, 1, 0.8)
