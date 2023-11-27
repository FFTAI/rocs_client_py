import math
import threading
import time
import unittest

from rocs_client import Human, Motor


class TestHumanMotor(unittest.TestCase):
    #
    human = Human(host="127.0.0.1")

    def enable_all(self):
        for motor in self.human.motor_limits:
            self.human.enable_motor(motor['no'], motor['orientation'])

    def disable_all(self):
        for motor in self.human.motor_limits:
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

    def smooth_move_motor_example(self, no, orientation: str, target_angle: float, offset=0.05, wait_time=0.002):
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

        threading.Thread(target=self.smooth_move_motor_example, args=('8', 'left', 30)).start()
        threading.Thread(target=self.smooth_move_motor_example, args=('8', 'right', 30)).start()

    def test_action_left(self):

        self.enable_all()

        self.smooth_move_motor_example('2', 'left', -10)
        self.smooth_move_motor_example('4', 'left', 10)
        self.smooth_move_motor_example('2', 'left', -30)
        self.smooth_move_motor_example('4', 'left', 30)
        self.smooth_move_motor_example('2', 'left', -60)
        self.smooth_move_motor_example('4', 'left', 60)
        self.smooth_move_motor_example('2', 'left', -10)
        self.smooth_move_motor_example('4', 'left', 10)
        self.smooth_move_motor_example('2', 'left', -0)
        self.smooth_move_motor_example('4', 'left', 0)

    def test_action_right(self):
        self.enable_all()

        self.smooth_move_motor_example('2', 'right', 10)
        self.smooth_move_motor_example('4', 'right', -10)
        self.smooth_move_motor_example('2', 'right', 30)
        self.smooth_move_motor_example('4', 'right', -30)
        self.smooth_move_motor_example('2', 'right', 60)
        self.smooth_move_motor_example('4', 'right', -60)
        self.smooth_move_motor_example('2', 'right', 10)
        self.smooth_move_motor_example('4', 'right', -10)
        self.smooth_move_motor_example('2', 'right', 0)
        self.smooth_move_motor_example('4', 'right', -0)

    def test_async(self):
        self.enable_all()
        # threading.Thread(target=self.test_action_left).start()
        # threading.Thread(target=self.test_action_right).start()
