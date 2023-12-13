import math
import threading
import time
import unittest

from rocs_client import Motor

motor = Motor(host="192.168.137.210")

motors = motor.limits[0:19]


def set_pds_flag():
    for item in motors:
        motor.set_motor_pd_flag(item['no'], item['orientation'])
    motor.exit()


def set_pds():
    for item in motors:
        motor.set_motor_pd(item['no'], item['orientation'], 0.36, 0.042)
    motor.exit()


def smooth_move_motor_for_differential(no, orientation, target_angle, offset=0.05, wait_time=0.004):
    if int(no) > 8:
        print('than 8 not support')
        return

    def wait_target_done(rel_tol=1):
        while True:
            p = motor.get_motor_pvc(no, orientation)['data']['position']
            if math.isclose(p, target_angle, rel_tol=rel_tol):
                break

    while True:
        try:
            current_position = (motor.get_motor_pvc(no, orientation))['data']['position']
            if current_position is not None and current_position != 0:
                break
        except Exception as e:
            print(f'err: {e}')
            pass
    target_position = target_angle
    cycle = abs(int((target_position - current_position) / offset))

    for i in range(0, cycle):
        if target_position > current_position:
            current_position += offset
        else:
            current_position -= offset
        motor.move_motor(no, orientation, current_position)
        time.sleep(wait_time)
    wait_target_done()


def enable_all():
    for item in motors:
        motor.enable_motor(item['no'], item['orientation'])
    time.sleep(1)


def disable_all():
    def _disable_left():
        for i in range((len(motors) - 1), -1, -1):
            item = motors[i]
            if item['orientation'] == 'left':
                smooth_move_motor_for_differential(item['no'], item['orientation'], 0, offset=2.5, wait_time=0.035)

        for i in range((len(motors) - 1), -1, -1):
            item = motors[i]
            if item['orientation'] == 'left':
                motor.disable_motor(item['no'], item['orientation'])

    def _disable_right():
        for i in range((len(motors) - 1), -1, -1):
            item = motors[i]
            if item['orientation'] != 'left':
                smooth_move_motor_for_differential(item['no'], item['orientation'], 0, offset=2.5, wait_time=0.035)

        for i in range((len(motors) - 1), -1, -1):
            item = motors[i]
            if item['orientation'] != 'left':
                motor.disable_motor(item['no'], item['orientation'])

    time.sleep(2)

    t_left = threading.Thread(target=_disable_left)
    t_right = threading.Thread(target=_disable_right)
    t_left.start(), t_right.start()
    t_left.join(), t_right.join()
    motor.exit()


def enable_hand():
    motor.enable_hand()


def disable_hand():
    motor.disable_hand()


class TestHumanMotor(unittest.TestCase):

    def test_set_pd_flag(self):
        set_pds_flag()

    def test_set_pd(self):
        set_pds()

    def test_get_pvc(self):
        print(motor.get_motor_pvc('0', 'yaw'))
        motor.exit()

    def test_action_simple(self):
        """
        This is the action of simple
        When you first single-control a motor, I strongly recommend that you must run this function for testing

        If the motor's motion is linear and smooth, then you can try something slightly more complicated
        But if it freezes, you need to debug your P and D parameters.
        """
        enable_all()
        smooth_move_motor_for_differential('2', 'left', -20)
        disable_all()

    def test_action_simple_hand(self):
        motor.move_motor('9', 'left', 100)
        motor.move_motor('10', 'left', 150)
        motor.move_motor('11', 'left', 200)
        print(motor.get_hand_position())
        motor.exit()

    def test_action_hug(self):
        enable_all()

        def left():
            smooth_move_motor_for_differential('1', 'left', 30, 0.3, 0.005)
            smooth_move_motor_for_differential('2', 'left', -60, 0.3, 0.005)
            smooth_move_motor_for_differential('4', 'left', 60, 0.3, 0.005)
            smooth_move_motor_for_differential('1', 'left', 45, 0.3, 0.005)

        def right():
            smooth_move_motor_for_differential('1', 'right', -30, 0.3, 0.005)
            smooth_move_motor_for_differential('2', 'right', 60, 0.3, 0.005)
            smooth_move_motor_for_differential('4', 'right', -60, 0.3, 0.005)
            smooth_move_motor_for_differential('1', 'right', -45, 0.3, 0.005)

        left = threading.Thread(target=left)
        right = threading.Thread(target=right)
        left.start(), right.start()
        left.join(), right.join()

        disable_all()

    def test_action_hello(self):
        enable_all()

        def move_3():
            for i in range(0, 5):
                smooth_move_motor_for_differential('3', 'right', -40, offset=0.3, wait_time=0.003)
                smooth_move_motor_for_differential('3', 'right', 5, offset=0.3, wait_time=0.003)

        def shake_head():
            for i in range(0, 4):
                smooth_move_motor_for_differential('0', 'yaw', 12, offset=0.2)
                smooth_move_motor_for_differential('0', 'yaw', -12, offset=0.2)

        joint_1 = threading.Thread(target=smooth_move_motor_for_differential, args=('1', 'right', -65, 0.4, 0.005))
        joint_2 = threading.Thread(target=smooth_move_motor_for_differential, args=('2', 'right', 0, 0.4, 0.005))
        joint_4 = threading.Thread(target=smooth_move_motor_for_differential, args=('4', 'right', -90, 0.4, 0.005))
        joint_5 = threading.Thread(target=smooth_move_motor_for_differential, args=('5', 'right', 90, 0.4, 0.005))
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

    def test_action_shake_hands(self):

        enable_all()

        def hand():
            for i in range(0, 10):
                smooth_move_motor_for_differential('8', "right", 30, 1, 0.03)
                smooth_move_motor_for_differential('8', "right", 10, 1, 0.03)

        t1 = threading.Thread(target=smooth_move_motor_for_differential, args=('1', 'right', -65, 0.4, 0.006))
        t2 = threading.Thread(target=smooth_move_motor_for_differential, args=('2', 'right', 0, 0.4, 0.006))
        t3 = threading.Thread(target=smooth_move_motor_for_differential, args=('3', 'right', 90, 0.45, 0.005))
        t4 = threading.Thread(target=smooth_move_motor_for_differential, args=('4', 'right', -20, 0.4, 0.006))
        t5 = threading.Thread(target=smooth_move_motor_for_differential, args=('5', 'right', -60, 0.4, 0.006))
        t6 = threading.Thread(target=smooth_move_motor_for_differential, args=('6', 'right', 15, 0.4, 0.006))

        t1.start(), t2.start(), t3.start(), t4.start(), t5.start(), t6.start()
        t1.join(), t2.join(), t3.join(), t4.join(), t5.join(), t6.join()

        hand()
        disable_all()

    def test_action_grab(self):
        enable_all()
