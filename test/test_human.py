import time
import unittest

import websocket

from rocs_client import robot
from rocs_client.robot.human import ArmAction, HandAction, Motor


async def on_open(ws: websocket):
    print("WebSocket opened...")


async def on_message(ws: websocket, message: str):
    print("Received message:", message)


async def on_close(ws: websocket.WebSocketConnectionClosedException):
    print("WebSocket closed")


async def on_error(ws: websocket.WebSocketException, error: Exception):
    print("WebSocket error:", error)


human = robot.Human(on_connected=on_open, host="127.0.0.1", on_message=on_message, on_close=on_close, on_error=on_error)


class TestHuman(unittest.TestCase):

    def test_enable_debug_state(self):
        res = human.enable_debug_state(1)
        print(f'test_enable_debug_state: {res}')
        assert res.get('code') == 0

    def test_disable_debug_state(self):
        res = human.disable_debug_state()
        print(f'test_disable_debug_state: {res}')
        assert res.get('code') == 0

    def test_get_video_status(self):
        res: bool = human.camera.video_stream_status
        print(f'test_get_video_status: {res}')
        assert res is True

    def test_get_video_stream_url(self):
        res: str = human.camera.video_stream_url
        print(f'test_get_video_stream_url:  {res}')

    def test_get_joint_limit(self):
        res = human.get_joint_limit()
        print(f'test_get_joint_limit: {res}')
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
        human.walk(0, 0)

    def test_head(self):
        human.head(1, 1, 0.8)

    def test_get_motor_list(self):
        print(f'test_get_motor_list: {human.motor_limits}')

    def test_move_joint(self):
        human.move_joint(Motor(no='1', angle=100, orientation='left'), Motor(no='1', angle=100, orientation='right'))
        time.sleep(0.5)
        human.move_joint(Motor(no='1', angle=100, orientation='left'), Motor(no='1', angle=100, orientation='right'))
        time.sleep(0.5)
        human.move_joint(Motor(no='1', angle=100, orientation='left'), Motor(no='1', angle=100, orientation='right'))
        time.sleep(3)
        human.move_joint(Motor(no='1', angle=0, orientation='left'), Motor(no='1', angle=0, orientation='right'))

    def test_upper_body_arm(self):
        # 胳膊动作测试
        # 1、左挥手
        human.upper_body(arm=ArmAction.LEFT_ARM_WAVE)
        # 等待动作执行结束
        time.sleep(10)
        # 2、挥手
        human.upper_body(arm=ArmAction.TWO_ARMS_WAVE)

    def test_upper_body_hand(self):
        # 手部动作测试
        # 1、抖动手指头
        human.upper_body(hand=HandAction.TREMBLE)

