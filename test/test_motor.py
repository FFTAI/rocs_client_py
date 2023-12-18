import math
import threading
import time
import unittest

from rocs_client import Motor

motor = Motor(host="192.168.12.1")

arm_motor = motor.limits[0:17]
clamping_jaw = motor.limits[17:19]
dexterous_hand = motor.limits[19:31]

print(f'arm_motor: {arm_motor}')
print(f'clamping_jaw: {clamping_jaw}')
print(f'dexterous_hand: {dexterous_hand}')

motors = arm_motor + clamping_jaw


def set_pds_flag():
    """ Enable the switch/flag for setting pd parameters """
    for item in motors:
        motor.set_motor_pd_flag(item['no'], item['orientation'])
    motor.exit()


def set_pds():
    """ Set pd parameters """
    for item in motors:
        motor.set_motor_pd(item['no'], item['orientation'], 0.36, 0.042)
    motor.exit()


def smooth_move_motor_with_differential(no, orientation, target_angle, offset=0.05, interval=0.004):
    """
    Use the difference to move the motor smoothly
    Args:
        no: Number of the motor to be operated
        orientation: Orientation of the motor to be operated
        target_angle: Angle of motion
        offset: The Angle of each move
        interval: Interval of difference
    """
    if int(no) > 8:
        print('than 8 not support')
        return

    def wait_target_done(rel_tol=2):
        while True:
            try:
                p = motor.get_motor_pvc(no, orientation)['data']['position']
                if math.isclose(p, target_angle, rel_tol=rel_tol):
                    break
            except Exception as e:
                print(f'wait_target_done err: {e}')

    while True:
        try:
            result = motor.get_motor_pvc(no, orientation)
            current_position = result['data']['position']
            if current_position is not None and current_position != 0:
                break
        except Exception as e:
            print(f'current_position err: {e}')

    target_position = target_angle
    cycle = abs(int((target_position - current_position) / offset))

    for i in range(0, cycle):
        if target_position > current_position:
            current_position += offset
        else:
            current_position -= offset
        motor.move_motor(no, orientation, current_position)
        time.sleep(interval)
    wait_target_done()


def enable_all():
    """ Enable All Motors """
    for item in motors:
        motor.enable_motor(item['no'], item['orientation'])
    time.sleep(1)


def disable_all():
    """Disable All Motors """

    def _disable_left():
        for i in range((len(motors) - 1), -1, -1):
            item = motors[i]
            if item['orientation'] == 'left':
                smooth_move_motor_with_differential(item['no'], item['orientation'], 0, offset=1.5, interval=0.02)

        for i in range((len(motors) - 1), -1, -1):
            item = motors[i]
            if item['orientation'] == 'left':
                motor.disable_motor(item['no'], item['orientation'])

    def _disable_right():
        for i in range((len(motors) - 1), -1, -1):
            item = motors[i]
            if item['orientation'] != 'left':
                smooth_move_motor_with_differential(item['no'], item['orientation'], 0, offset=1.5, interval=0.02)

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


class TestHumanMotor(unittest.TestCase):

    def test_set_pd_flag(self):
        """ Enable the switch/flag for setting pd parameters """
        set_pds_flag()

    def test_set_pd(self):
        """ Set pd parameters """
        set_pds()

    def test_enable_motors(self):
        """ Enable All Motors """
        enable_all()

    def test_disable_motors(self):
        """ Disable All Motors """
        disable_all()

    def test_get_pvc(self):
        """ Obtain the specified motor information """
        print(f"test_get_pvc {motor.get_motor_pvc('0', 'yaw')}")
        motor.exit()

    def test_action_simple(self):
        """
        This is the action of simple
        When you first single-control a motor, I strongly recommend that you must run this function for testing

        If the motor's motion is linear and smooth, then you can try something slightly more complicated
        But if it freezes, you need to debug your P and D parameters.
        """
        enable_all()
        smooth_move_motor_with_differential('2', 'left', -20)
        disable_all()

    def test_enable_hand(self):
        """Enabling hand"""
        motor.enable_hand()
        motor.exit()

    def test_disable_hand(self):
        """ Disabled hand """
        motor.disable_hand()
        motor.exit()

    def test_get_hand_position(self):
        """ Obtain Hand Position"""
        print(f'test_get_hand_position:  {motor.get_hand_position()}')

    def test_action_simple_hand(self):
        angle = 500

        motor.move_motor('11', 'left', angle)
        motor.move_motor('12', 'left', angle)
        motor.move_motor('13', 'left', angle)
        motor.move_motor('14', 'left', angle)

        motor.move_motor('11', 'right', angle)
        motor.move_motor('12', 'right', angle)
        motor.move_motor('13', 'right', angle)
        motor.move_motor('14', 'right', angle)
        motor.exit()

    def test_action_hug(self):
        enable_all()

        def left():
            smooth_move_motor_with_differential('1', 'left', 30, 0.3, 0.005)
            smooth_move_motor_with_differential('2', 'left', -60, 0.3, 0.005)
            smooth_move_motor_with_differential('4', 'left', 60, 0.3, 0.005)
            smooth_move_motor_with_differential('1', 'left', 45, 0.3, 0.005)

        def right():
            smooth_move_motor_with_differential('1', 'right', -30, 0.3, 0.005)
            smooth_move_motor_with_differential('2', 'right', 60, 0.3, 0.005)
            smooth_move_motor_with_differential('4', 'right', -60, 0.3, 0.005)
            smooth_move_motor_with_differential('1', 'right', -45, 0.3, 0.005)

        left = threading.Thread(target=left)
        right = threading.Thread(target=right)
        left.start(), right.start()
        left.join(), right.join()

        disable_all()

    def test_action_hello(self):
        enable_all()

        def move_3():
            for i in range(0, 5):
                smooth_move_motor_with_differential('3', 'right', -40, offset=0.3, interval=0.003)
                smooth_move_motor_with_differential('3', 'right', 5, offset=0.3, interval=0.003)

        joint_1 = threading.Thread(target=smooth_move_motor_with_differential, args=('1', 'right', -65, 0.4, 0.005))
        joint_2 = threading.Thread(target=smooth_move_motor_with_differential, args=('2', 'right', 0, 0.4, 0.005))
        joint_4 = threading.Thread(target=smooth_move_motor_with_differential, args=('4', 'right', -90, 0.4, 0.005))
        joint_5 = threading.Thread(target=smooth_move_motor_with_differential, args=('5', 'right', 90, 0.4, 0.005))
        joint_1.start(), joint_2.start(), joint_4.start(), joint_5.start()
        joint_1.join(), joint_2.join(), joint_4.join(), joint_5.join()
        time.sleep(1)

        t_move_3 = threading.Thread(target=move_3)
        t_move_3.start()
        t_move_3.join()
        disable_all()
