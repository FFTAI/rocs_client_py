import threading
import time
import unittest

from rocs_client import Human


class TestHumanMotor(unittest.TestCase):
    human = Human(host="127.0.0.1")

    def test_check_motor_for_flag(self):
        self.human.check_motor_for_flag('1', 'left')

    def test_check_motor_for_set_pd(self):
        self.human.check_motor_for_set_pd('1', 'left', 0.36, 0.042)

    def enable_all(self):
        for motor in self.human.motor_limits:
            self.human.enable_motor(motor['no'], motor['orientation'])

    def disable_all(self):
        for motor in self.human.motor_limits:
            self.human.disable_motor(motor['no'], motor['orientation'])

    def test_enabled_all(self):
        self.enable_all()

    def test_disable_all(self):
        self.disable_all()

    def smooth_move_motor_example(self, no, orientation: str, angle: float, offset=0.05, wait_time=0.002):
        current_offset = 0
        offset_angle = offset if angle >= 0 else offset * -1
        cycle = int(angle / offset)
        for i in range(0, abs(cycle)):
            current_offset += offset_angle
            self.human.move_motor(no, orientation, current_offset)
            time.sleep(wait_time)

    def test_move_joints(self):

        self.human.enable_motor('2', orientation='left')
        threading.Thread(target=self.smooth_move_motor_example, args=('2', 'left', -45)).start()

        self.human.enable_motor('2', orientation='right')
        threading.Thread(target=self.smooth_move_motor_example, args=('2', 'right', 45)).start()

        self.human.enable_motor('4', orientation='left')
        threading.Thread(target=self.smooth_move_motor_example, args=('4', 'left', 45)).start()

        self.human.enable_motor('4', orientation='right')
        threading.Thread(target=self.smooth_move_motor_example, args=('4', 'right', -45)).start()

    def test_move_joints1(self):

        # self.human.enable_motor('6', orientation='left')
        # threading.Thread(target=self.smooth_move_motor_example, args=('6', 'left', -21)).start()
        #
        # self.human.enable_motor('6', orientation='right')
        # threading.Thread(target=self.smooth_move_motor_example, args=('6', 'right', 21)).start()

        # self.human.enable_motor('7', orientation='left')
        # threading.Thread(target=self.smooth_move_motor_example, args=('7', 'left', 21)).start()
        #
        # self.human.enable_motor('7', orientation='right')
        # threading.Thread(target=self.smooth_move_motor_example, args=('7', 'right', -21)).start()

        self.human.enable_motor('8', orientation='left')
        threading.Thread(target=self.smooth_move_motor_example, args=('8', 'left', 90)).start()

        self.human.enable_motor('8', orientation='right')
        threading.Thread(target=self.smooth_move_motor_example, args=('8', 'right', 90)).start()
