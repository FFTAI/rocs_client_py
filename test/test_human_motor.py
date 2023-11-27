import math
import threading
import time
import unittest

from rocs_client import Human

"""
python -m unittest test_human_motor.TestHumanMotor.test_action_hello

"""


class TestHumanMotor(unittest.TestCase):
    human = Human(host="127.0.0.1")

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

    def test_move_joints(self):
        self.enable_all()

        # threading.Thread(target=self.smooth_move_motor_example, args=('1', 'left', 20)).start()
        # threading.Thread(target=self.smooth_move_motor_example, args=('1', 'right', -20)).start()
        #
        # threading.Thread(target=self.smooth_move_motor_example, args=('2', 'left', -20)).start()
        # threading.Thread(target=self.smooth_move_motor_example, args=('2', 'right', 20)).start()

        # threading.Thread(target=self.smooth_move_motor_example, args=('3', 'left', -20)).start()
        # threading.Thread(target=self.smooth_move_motor_example, args=('3', 'right', 20)).start()

        # threading.Thread(target=self.smooth_move_motor_example, args=('4', 'left', 0)).start()
        # threading.Thread(target=self.smooth_move_motor_example, args=('4', 'right', -0)).start()

        # threading.Thread(target=self.smooth_move_motor_example, args=('5', 'left', 20)).start()
        # threading.Thread(target=self.smooth_move_motor_example, args=('5', 'right', -20)).start()

        # threading.Thread(target=self.smooth_move_motor_example, args=('6', 'left', -21)).start()
        # threading.Thread(target=self.smooth_move_motor_example, args=('6', 'right', 21)).start()
        #
        # threading.Thread(target=self.smooth_move_motor_example, args=('7', 'left', 21)).start()
        # threading.Thread(target=self.smooth_move_motor_example, args=('7', 'right', -21)).start()

        threading.Thread(target=self.smooth_move_motor_example, args=('8', 'left', 0)).start()
        threading.Thread(target=self.smooth_move_motor_example, args=('8', 'right', 0)).start()

    def test_right(self):
        self.enable_all()

        def left_1():
            self.smooth_move_motor_example('1', 'right', -20)
            self.smooth_move_motor_example('1', 'right', 0)
            self.smooth_move_motor_example('1', 'right', -20)
            self.smooth_move_motor_example('1', 'right', 0)
            self.smooth_move_motor_example('1', 'right', -20)

        def left_2():
            self.smooth_move_motor_example('2', 'right', 20)
            self.smooth_move_motor_example('2', 'right', 40)
            self.smooth_move_motor_example('2', 'right', 20)
            self.smooth_move_motor_example('2', 'right', 40)
            self.smooth_move_motor_example('2', 'right', 20)

        def left_4():
            self.smooth_move_motor_example('4', 'right', -40)
            self.smooth_move_motor_example('4', 'right', -60)
            self.smooth_move_motor_example('4', 'right', -40)
            self.smooth_move_motor_example('4', 'right', -60)
            self.smooth_move_motor_example('4', 'right', -40)

        # threading.Thread(target=left_1).start()
        threading.Thread(target=left_2).start()
        threading.Thread(target=left_4).start()

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
        time.sleep(3)
        self.disable_all()

    def test_action_hello(self):
        self.enable_all()

        joint_1 = threading.Thread(target=self.smooth_move_motor_example, args=('1', 'right', -75))
        joint_2 = threading.Thread(target=self.smooth_move_motor_example, args=('2', 'right', 0))
        joint_4 = threading.Thread(target=self.smooth_move_motor_example, args=('4', 'right', -90))
        joint_5 = threading.Thread(target=self.smooth_move_motor_example, args=('5', 'right', 90))
        joint_1.start(), joint_2.start(), joint_4.start(), joint_5.start()
        joint_1.join(), joint_2.join(), joint_4.join(), joint_5.join()
        time.sleep(4)

        for i in range(0, 5):
            self.smooth_move_motor_example('3', 'right', -15, offset=0.08)
            self.smooth_move_motor_example('3', 'right', -45, offset=0.08)

        time.sleep(2)
        self.disable_all()
