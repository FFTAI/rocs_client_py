import math
import threading
import time
import unittest

from rocs_client import Human

"""
python -m unittest test_human_motor.TestHumanMotor.test_action_hello

"""


class TestHumanMotor(unittest.TestCase):
    human = Human(host="192.168.137.210")

    def enable_all(self):
        for motor in self.human.motor_limits:
            self.human.enable_motor(motor['no'], motor['orientation'])

    def disable_all(self):
        for i in range((len(self.human.motor_limits) - 1), -1, -1):
            motor = self.human.motor_limits[i]
            self.smooth_move_motor_example(motor['no'], motor['orientation'], 0, offset=0.1, wait_time=0.03)
            self.human.disable_motor(motor['no'], motor['orientation'])

    def wait_target_done(self, no, orientation, target_angle, rel_tol=1):
        while True:
            p, _, _ = self.human.get_motor_pvc(str(no), orientation)['data']
            if math.isclose(p, target_angle, rel_tol=rel_tol):
                break

    def test_check_motor_for_flag(self):
        for motor in self.human.motor_limits:
            self.human.check_motor_for_flag(motor['no'], motor['orientation'])

    def test_check_motor_for_set_pd(self):
        for motor in self.human.motor_limits:
            self.human.check_motor_for_set_pd(motor['no'], motor['orientation'], 0.36, 0.042)

    def test_enabled_all(self):
        self.enable_all()
        time.sleep(1)

    def test_disable_all(self):
        self.disable_all()

    def smooth_move_motor_example(self, no, orientation: str, target_angle: float, offset=0.05, wait_time=0.003):
        current_position = 0
        while True:
            try:
                current_position, _, _ = (self.human.get_motor_pvc(no, orientation))['data']
                if current_position is not None and current_position is not 0:
                    break
            except Exception as e:
                pass
        target_position = target_angle
        cycle = abs(int((target_position - current_position) / offset))

        for i in range(0, cycle):
            if target_position > current_position:
                current_position += offset
            else:
                current_position -= offset
            self.human.move_motor(no, orientation, current_position)
            time.sleep(wait_time)
        self.wait_target_done(no, orientation, current_position)

    def test_get_pvc(self):
        print(f"left  4====={self.human.get_motor_pvc('4', 'left')}")
        print(f"right 4====={self.human.get_motor_pvc('4', 'right')}")

    def test_action_hug(self):
        self.enable_all()

        def left():
            self.smooth_move_motor_example('1', 'left', 30)
            self.smooth_move_motor_example('2', 'left', -60)
            self.smooth_move_motor_example('4', 'left', 60)
            self.smooth_move_motor_example('1', 'left', 45)

        def right():
            self.smooth_move_motor_example('1', 'right', -30)
            self.smooth_move_motor_example('2', 'right', 60)
            self.smooth_move_motor_example('4', 'right', -60)
            self.smooth_move_motor_example('1', 'right', -45)

        left = threading.Thread(target=left)
        right = threading.Thread(target=right)
        left.start(), right.start()
        left.join(), right.join()

        time.sleep(2)

        threading.Thread(target=self.smooth_move_motor_example, args=('1', 'left', 0, 0.15, 0.002)).start()
        threading.Thread(target=self.smooth_move_motor_example, args=('2', 'left', 0, 0.2, 0.002)).start()
        threading.Thread(target=self.smooth_move_motor_example, args=('4', 'left', 0, 0.15, 0.002)).start()

        threading.Thread(target=self.smooth_move_motor_example, args=('1', 'right', 0, 0.15, 0.002)).start()
        threading.Thread(target=self.smooth_move_motor_example, args=('2', 'right', 0, 0.2, 0.002)).start()
        threading.Thread(target=self.smooth_move_motor_example, args=('4', 'right', 0, 0.15, 0.002)).start()

    def test_action_hello(self):
        self.enable_all()

        joint_1 = threading.Thread(target=self.smooth_move_motor_example, args=('1', 'right', -65, 0.17, 0.004))
        joint_2 = threading.Thread(target=self.smooth_move_motor_example, args=('2', 'right', 0, 0.15, 0.004))
        joint_4 = threading.Thread(target=self.smooth_move_motor_example, args=('4', 'right', -90, 0.175, 0.003))
        joint_5 = threading.Thread(target=self.smooth_move_motor_example, args=('5', 'right', 90, 0.18, 0.003))
        joint_1.start(), joint_2.start(), joint_4.start(), joint_5.start()
        joint_1.join(), joint_2.join(), joint_4.join(), joint_5.join()

        time.sleep(0.5)

        for i in range(0, 3):
            self.smooth_move_motor_example('3', 'right', -35, offset=0.15, wait_time=0.003)
            self.smooth_move_motor_example('3', 'right', 8, offset=0.15, wait_time=0.003)

        threading.Thread(target=self.smooth_move_motor_example, args=('1', 'right', 0, 0.15, 0.002)).start()
        threading.Thread(target=self.smooth_move_motor_example, args=('4', 'right', 0, 0.2, 0.002)).start()
        threading.Thread(target=self.smooth_move_motor_example, args=('2', 'right', 0, 0.15, 0.002)).start()
        threading.Thread(target=self.smooth_move_motor_example, args=('3', 'right', 0, 0.2, 0.002)).start()
        threading.Thread(target=self.smooth_move_motor_example, args=('5', 'right', 0, 0.2, 0.002)).start()

    def test_action_hold_left(self):
        for i in range(0, 3):
            self.smooth_move_motor_example('2', 'left', -35, offset=0.1, wait_time=0.004)
            self.smooth_move_motor_example('2', 'left', -80, offset=0.1, wait_time=0.004)
            time.sleep(0.5)

    def test_action_hold_right(self):
        for i in range(0, 3):
            self.smooth_move_motor_example('2', 'right', 35, offset=0.1, wait_time=0.004)
            self.smooth_move_motor_example('2', 'right', 80, offset=0.1, wait_time=0.004)
            time.sleep(0.5)

    def test_action_hold(self):
        self.enable_all()

        left_joint_2 = threading.Thread(target=self.smooth_move_motor_example, args=('2', 'left', -60, 0.14, 0.003))
        left_joint_3 = threading.Thread(target=self.smooth_move_motor_example, args=('3', 'left', 90, 0.2, 0.003))
        left_joint_4 = threading.Thread(target=self.smooth_move_motor_example, args=('4', 'left', 40, 0.16, 0.004))
        left_joint_5 = threading.Thread(target=self.smooth_move_motor_example, args=('5', 'left', -90, 0.16, 0.004))
        left_joint_6 = threading.Thread(target=self.smooth_move_motor_example, args=('6', 'left', 15, 0.16, 0.004))

        right_joint_2 = threading.Thread(target=self.smooth_move_motor_example, args=('2', 'right', 60, 0.14, 0.003))
        right_joint_3 = threading.Thread(target=self.smooth_move_motor_example, args=('3', 'right', -90, 0.2, 0.003))
        right_joint_4 = threading.Thread(target=self.smooth_move_motor_example, args=('4', 'right', -40, 0.16, 0.004))
        right_joint_5 = threading.Thread(target=self.smooth_move_motor_example, args=('5', 'right', 90, 0.16, 0.004))
        right_joint_6 = threading.Thread(target=self.smooth_move_motor_example, args=('6', 'right', -15, 0.16, 0.004))

        left_joint_2.start(), left_joint_3.start(), left_joint_4.start(), left_joint_5.start(), left_joint_6.start()
        right_joint_2.start(), right_joint_3.start(), right_joint_4.start(), right_joint_5.start(), right_joint_6.start()
        #
        left_joint_2.join(), left_joint_3.join(), left_joint_4.join()
        right_joint_2.join(), right_joint_3.join(), right_joint_4.join()

        time.sleep(3.5)

        hold_left = threading.Thread(target=self.test_action_hold_left)
        hold_left.start()

        hold_right = threading.Thread(target=self.test_action_hold_right())
        hold_right.start()

        hold_left.join()
        hold_right.join()

        threading.Thread(target=self.smooth_move_motor_example, args=('2', 'left', 0, 0.15, 0.002)).start()
        threading.Thread(target=self.smooth_move_motor_example, args=('3', 'left', 0, 0.2, 0.002)).start()
        threading.Thread(target=self.smooth_move_motor_example, args=('4', 'left', 0, 0.2, 0.002)).start()
        threading.Thread(target=self.smooth_move_motor_example, args=('5', 'left', 0, 0.2, 0.002)).start()
        threading.Thread(target=self.smooth_move_motor_example, args=('6', 'left', 0, 0.2, 0.002)).start()

        threading.Thread(target=self.smooth_move_motor_example, args=('2', 'right', 0, 0.15, 0.002)).start()
        threading.Thread(target=self.smooth_move_motor_example, args=('3', 'right', 0, 0.2, 0.002)).start()
        threading.Thread(target=self.smooth_move_motor_example, args=('4', 'right', 0, 0.2, 0.002)).start()
        threading.Thread(target=self.smooth_move_motor_example, args=('5', 'right', 0, 0.2, 0.002)).start()
        threading.Thread(target=self.smooth_move_motor_example, args=('6', 'right˚¬', 0, 0.2, 0.002)).start()
