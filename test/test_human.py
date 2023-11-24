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

    def test_disable_motor(self):
        self.human.disable_motor("4", "left")
        self.human.disable_motor("4", "right")


    def smooth_move_motor_example(self, no, orientation: str, angle: float, offset=0.05):
        current_offset = 0
        offset_angle = offset if angle >= 0 else offset * -1
        cycle = int(angle / offset)
        for i in range(0, abs(cycle)):
            current_offset += offset_angle
            self.move_motor(no, orientation, current_offset)
            time.sleep(0.002)


    def test_move_joints(self):
        self.human.enable_motor('4', orientation='left')
        threading.Thread(target=self.test_move_joint, args=('4', 'left', 45)).start()

        self.human.enable_motor('4', orientation='right')
        threading.Thread(target=self.test_move_joint, args=('4', 'right', -45)).start()
        #
        self.human.enable_motor('2', orientation='left')
        threading.Thread(target=self.test_move_joint, args=('2', 'left', -45)).start()

        self.human.enable_motor('2', orientation='right')
        threading.Thread(target=self.test_move_joint, args=('2', 'right', 45)).start()
