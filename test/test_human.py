import datetime
import threading
import time
import unittest

from rocs_client import Human
from rocs_client.robot.human import ArmAction, HandAction, Motor


async def on_connected():
    print("WebSocket opened...")


async def on_message(message: str):
    print("Received message:", message)


async def on_close():
    print("WebSocket closed")


async def on_error(error: Exception):
    print("WebSocket error:", error)


class TestHuman(unittest.TestCase):
    human = Human(on_connected=on_connected, host="127.0.0.1", on_message=on_message, on_close=on_close,
                  on_error=on_error)

    def test_enable_debug_state(self):
        res = self.human.enable_debug_state(10)
        print(f'test_enable_debug_state: {res}')
        assert res.get('code') == 0

    def test_disable_debug_state(self):
        res = self.human.disable_debug_state()
        print(f'test_disable_debug_state: {res}')
        assert res.get('code') == 0

    def test_get_video_status(self):
        res: bool = self.human.camera.video_stream_status
        print(f'test_get_video_status: {res}')
        assert res is True

    def test_get_video_stream_url(self):
        res: str = self.human.camera.video_stream_url
        print(f'test_get_video_stream_url:  {res}')

    def test_get_joint_limit(self):
        res = self.human.get_joint_limit()
        print(f'test_get_joint_limit: {res}')
        assert res.get('code') == 0

    def test_get_joint_states(self):
        res = self.human.get_joint_states()
        print(f'human.test_get_joint_states: {res}')
        assert res.get('code') == 0

    def test_start(self):
        res = self.human.start()
        print(f'human.test_start: {res}')
        assert res.get('code') == 0

    def test_stop(self):
        res = self.human.stop()
        print(f'human.test_stop: {res}')
        assert res.get('code') == 0

    def test_stand(self):
        res = self.human.stand()
        print(f'human.test_stand: {res}')
        assert res.get('code') == 0

    def test_move(self):
        self.human.walk(0, 0)

    def test_head(self):
        self.human.head(1, 1, 0.8)

    def test_get_motor_list(self):
        print(f'test_get_motor_list: {self.human.motor_limits}')

    def test_upper_body_arm(self):
        # 胳膊动作测试
        # 1、左挥手
        self.human.upper_body(arm=ArmAction.LEFT_ARM_WAVE)

    def test_upper_body_hand(self):
        # 手部动作测试
        # 1、抖动手指头
        self.human.upper_body(hand=HandAction.TREMBLE)

    def test_start_control_svr(self):
        self.human._control_svr_start()

    def test_close_control_svr(self):
        self.human._control_svr_start()

    def test_status_control_svr(self):
        self.human._control_svr_start()

    def test_log_view_control_svr(self):
        self.human._control_svr_start()


