import math
import threading
import time
import unittest

from rocs_client import Human

"""
python -m unittest test_human_motor.TestHumanMotor.test_action_hello

"""

human = Human(host="192.168.137.210")


def open_set_pd_flag():
    for motor in human.motor_limits:
        human.check_motor_for_flag(motor['no'], motor['orientation'])


def set_pds():
    for motor in human.motor_limits:
        human.check_motor_for_set_pd(motor['no'], motor['orientation'], 0.36, 0.042)


def enable_all():
    for motor in human.motor_limits:
        human.enable_motor(motor['no'], motor['orientation'])
    time.sleep(1)


def _disable_left():
    for i in range((len(human.motor_limits) - 1), -1, -1):
        motor = human.motor_limits[i]
        if motor['orientation'] == 'left':
            smooth_move_motor_example(motor['no'], motor['orientation'], 0, offset=0.5, wait_time=0.04)
            human.disable_motor(motor['no'], motor['orientation'])


def _disable_right():
    for i in range((len(human.motor_limits) - 1), -1, -1):
        motor = human.motor_limits[i]
        if motor['orientation'] != 'left':
            smooth_move_motor_example(motor['no'], motor['orientation'], 0, offset=0.5, wait_time=0.04)
            human.disable_motor(motor['no'], motor['orientation'])


def disable_all():
    time.sleep(2)
    threading.Thread(target=_disable_left).start()
    threading.Thread(target=_disable_right).start()


def wait_target_done(no, orientation, target_angle, rel_tol=1):
    while True:
        p, _, _ = human.get_motor_pvc(str(no), orientation)['data']
        if math.isclose(p, target_angle, rel_tol=rel_tol):
            break


def smooth_move_motor_example(no, orientation: str, target_angle: float, offset=0.05, wait_time=0.003):
    current_position = 0
    while True:
        try:
            current_position, _, _ = (human.get_motor_pvc(no, orientation))['data']
            if current_position is not None and current_position != 0:
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
        human.move_motor(no, orientation, current_position)
        time.sleep(wait_time)
    wait_target_done(no, orientation, current_position)


class TestHumanMotor(unittest.TestCase):

    def test_open_set_pd_flag(self):
        open_set_pd_flag()

    def test_set_pd(self):
        set_pds()

    def test_enabled_all(self):
        enable_all()

    def test_disable_all(self):
        disable_all()

    def test_get_pvc(self):
        print(f"left  4====={human.get_motor_pvc('4', 'left')}")
        print(f"right 4====={human.get_motor_pvc('4', 'right')}")

    def test_action_hug(self):
        enable_all()

        def left():
            smooth_move_motor_example('1', 'left', 30)
            smooth_move_motor_example('2', 'left', -60)
            smooth_move_motor_example('4', 'left', 60)
            smooth_move_motor_example('1', 'left', 45)

        def right():
            smooth_move_motor_example('1', 'right', -30)
            smooth_move_motor_example('2', 'right', 60)
            smooth_move_motor_example('4', 'right', -60)
            smooth_move_motor_example('1', 'right', -45)

        left = threading.Thread(target=left)
        right = threading.Thread(target=right)
        left.start(), right.start()
        left.join(), right.join()

        disable_all()

    def test_action_hello(self):
        enable_all()
        joint_1 = threading.Thread(target=smooth_move_motor_example, args=('1', 'right', -65, 0.17, 0.004))
        joint_2 = threading.Thread(target=smooth_move_motor_example, args=('2', 'right', 0, 0.15, 0.004))
        joint_4 = threading.Thread(target=smooth_move_motor_example, args=('4', 'right', -90, 0.175, 0.003))
        joint_5 = threading.Thread(target=smooth_move_motor_example, args=('5', 'right', 90, 0.18, 0.003))
        joint_1.start(), joint_2.start(), joint_4.start(), joint_5.start()
        joint_1.join(), joint_2.join(), joint_4.join(), joint_5.join()
        time.sleep(1.5)

        for i in range(0, 3):
            smooth_move_motor_example('3', 'right', -35, offset=0.15, wait_time=0.003)
            smooth_move_motor_example('3', 'right', 8, offset=0.15, wait_time=0.003)
        disable_all()

    def test_action_hold(self):

        def test_action_hold_left():
            for i in range(0, 3):
                smooth_move_motor_example('2', 'left', -35, offset=0.05, wait_time=0.004)
                smooth_move_motor_example('2', 'left', -80, offset=0.05, wait_time=0.004)
                time.sleep(0.5)

        def test_action_hold_right():
            for i in range(0, 3):
                smooth_move_motor_example('2', 'right', 35, offset=0.05, wait_time=0.004)
                smooth_move_motor_example('2', 'right', 80, offset=0.05, wait_time=0.004)
                time.sleep(0.5)

        enable_all()

        left_joint_2 = threading.Thread(target=smooth_move_motor_example, args=('2', 'left', -60, 0.14, 0.003))
        left_joint_3 = threading.Thread(target=smooth_move_motor_example, args=('3', 'left', 90, 0.2, 0.003))
        left_joint_4 = threading.Thread(target=smooth_move_motor_example, args=('4', 'left', 40, 0.16, 0.004))
        left_joint_5 = threading.Thread(target=smooth_move_motor_example, args=('5', 'left', -90, 0.16, 0.004))
        left_joint_6 = threading.Thread(target=smooth_move_motor_example, args=('6', 'left', 15, 0.16, 0.004))

        right_joint_2 = threading.Thread(target=smooth_move_motor_example, args=('2', 'right', 60, 0.14, 0.003))
        right_joint_3 = threading.Thread(target=smooth_move_motor_example, args=('3', 'right', -90, 0.2, 0.003))
        right_joint_4 = threading.Thread(target=smooth_move_motor_example, args=('4', 'right', -40, 0.16, 0.004))
        right_joint_5 = threading.Thread(target=smooth_move_motor_example, args=('5', 'right', 90, 0.16, 0.004))
        right_joint_6 = threading.Thread(target=smooth_move_motor_example, args=('6', 'right', -15, 0.16, 0.004))

        left_joint_2.start(), left_joint_3.start(), left_joint_4.start(), left_joint_5.start(), left_joint_6.start()
        right_joint_2.start(), right_joint_3.start(), right_joint_4.start(), right_joint_5.start(), right_joint_6.start()

        left_joint_2.join(), left_joint_3.join(), left_joint_4.join()
        right_joint_2.join(), right_joint_3.join(), right_joint_4.join()

        time.sleep(1)

        hold_left = threading.Thread(target=test_action_hold_left)
        hold_right = threading.Thread(target=test_action_hold_right)
        hold_left.start(), hold_right.start()
        hold_left.join(), hold_right.join()

        disable_all()
