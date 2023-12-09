import math
import threading
import time
import unittest

from rocs_client import Human

human = Human(host="192.168.137.210")

motors = human.motor_limits[0:15]


def set_pds_flag():
    for motor in motors:
        human.set_motor_pd_flag(motor['no'], motor['orientation'])
    human.exit()


def set_pds():
    for motor in motors:
        human.set_motor_pd(motor['no'], motor['orientation'], 0.36, 0.042)
    human.exit()


def enable_all():
    for motor in motors:
        human.enable_motor(motor['no'], motor['orientation'])
    time.sleep(1)


def _disable_left():
    for i in range((len(motors) - 1), -1, -1):
        motor = motors[i]
        if motor['orientation'] == 'left':
            smooth_move_motor_example(motor['no'], motor['orientation'], 0, offset=1, wait_time=0.04)

    for i in range((len(motors) - 1), -1, -1):
        motor = motors[i]
        if motor['orientation'] == 'left':
            human.disable_motor(motor['no'], motor['orientation'])


def _disable_right():
    for i in range((len(motors) - 1), -1, -1):
        motor = motors[i]
        if motor['orientation'] != 'left':
            smooth_move_motor_example(motor['no'], motor['orientation'], 0, offset=1, wait_time=0.04)

    for i in range((len(motors) - 1), -1, -1):
        motor = motors[i]
        if motor['orientation'] != 'left':
            human.disable_motor(motor['no'], motor['orientation'])


def disable_all():
    time.sleep(2)
    t_left = threading.Thread(target=_disable_left)
    t_right = threading.Thread(target=_disable_right)
    t_left.start(), t_right.start()
    t_left.join(), t_right.join()
    human.exit()


def wait_target_done(no, orientation, target_angle, rel_tol=1):
    while True:
        p = human.get_motor_pvc(str(no), orientation)['data']['position']
        if math.isclose(p, target_angle, rel_tol=rel_tol):
            break


def smooth_move_motor_example(no, orientation: str, target_angle: float, offset=0.05, wait_time=0.004):
    if int(no) > 8:
        print('than 8 not support')
        return
    current_position = 0
    while True:
        try:
            current_position = (human.get_motor_pvc(no, orientation))['data']['position']
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


def enable_hand():
    human.enable_hand()


def disable_hand():
    human.disable_hand()


class TestHumanMotor(unittest.TestCase):

    def test_set_pd_flag(self):
        set_pds_flag()

    def test_set_pd(self):
        set_pds()

    def test_action_simple(self):
        """
        This is the action of simple
        When you first single-control a motor, I strongly recommend that you must run this function for testing

        If the motor's motion is linear and smooth, then you can try something slightly more complicated
        But if it freezes, you need to debug your P and D parameters.
        """
        enable_all()
        smooth_move_motor_example('2', 'left', -20)
        disable_all()

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

        def move_3():
            for i in range(0, 5):
                smooth_move_motor_example('3', 'right', -40, offset=0.2, wait_time=0.003)
                smooth_move_motor_example('3', 'right', 5, offset=0.2, wait_time=0.003)

        def shake_head():
            for i in range(0, 4):
                smooth_move_motor_example('0', 'yaw', 12, offset=0.2)
                smooth_move_motor_example('0', 'yaw', -12, offset=0.2)

        joint_1 = threading.Thread(target=smooth_move_motor_example, args=('1', 'right', -65, 0.17, 0.004))
        joint_2 = threading.Thread(target=smooth_move_motor_example, args=('2', 'right', 0, 0.15, 0.004))
        joint_4 = threading.Thread(target=smooth_move_motor_example, args=('4', 'right', -90, 0.175, 0.003))
        joint_5 = threading.Thread(target=smooth_move_motor_example, args=('5', 'right', 90, 0.18, 0.003))
        joint_1.start(), joint_2.start(), joint_4.start(), joint_5.start()
        joint_1.join(), joint_2.join(), joint_4.join(), joint_5.join()
        time.sleep(1)

        t_shake_head = threading.Thread(target=shake_head)
        t_shake_head.start()

        t_move_3 = threading.Thread(target=move_3)
        t_move_3.start()
        t_move_3.join()
        t_shake_head.join()

        disable_all()

    def test_get_pvc(self):
        print(human.get_motor_pvc('0', 'yaw'))
        human.exit()

    def test_get_hand_position(self):
        human.move_motor('10', 'left', 0)
        human.move_motor('10', 'left', 0)
        human.move_motor('10', 'left', 0)
        print(human.get_hand_position())
        human.exit()
