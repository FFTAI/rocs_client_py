import math
import threading
import time

from rocs_client import Human

human = Human(host="192.168.137.210")


def enable_all():
    for motor in human.motor_limits:
        human.enable_motor(motor['no'], motor['orientation'])
    time.sleep(1)


def disable_left():
    for i in range((len(human.motor_limits) - 1), -1, -1):
        motor = human.motor_limits[i]
        if motor['orientation'] == 'left':
            smooth_move_motor_example(motor['no'], motor['orientation'], 0, offset=0.3, wait_time=0.03)
            human.disable_motor(motor['no'], motor['orientation'])


def disable_right():
    for i in range((len(human.motor_limits) - 1), -1, -1):
        motor = human.motor_limits[i]
        if motor['orientation'] != 'left':
            smooth_move_motor_example(motor['no'], motor['orientation'], 0, offset=0.3, wait_time=0.03)
            human.disable_motor(motor['no'], motor['orientation'])


def disable_all():
    time.sleep(1)
    threading.Thread(target=disable_left).start()
    threading.Thread(target=disable_right).start()


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


"""
==============================================================================================

"""


def test_move_joints():
    enable_all()
    smooth_move_motor_example('2', 'left', -40)
    smooth_move_motor_example('4', 'left', 80)
    smooth_move_motor_example('2', 'left', -10)
    smooth_move_motor_example('1', 'left', 30)
    smooth_move_motor_example('1', 'left', -30)
    smooth_move_motor_example('1', 'left', 30)
    smooth_move_motor_example('1', 'left', -30)
    disable_all()


def test_move_joints_async():
    enable_all()
    threading.Thread(target=smooth_move_motor_example, args=('2', 'left', -45)).start()
    threading.Thread(target=smooth_move_motor_example, args=('2', 'right', 45)).start()
    threading.Thread(target=smooth_move_motor_example, args=('4', 'left', 45)).start()
    threading.Thread(target=smooth_move_motor_example, args=('4', 'right', -45)).start()
    disable_all()


def test_action_hello():
    enable_all()

    joint_1 = threading.Thread(target=smooth_move_motor_example, args=('1', 'right', -65, 0.16, 0.003))
    joint_2 = threading.Thread(target=smooth_move_motor_example, args=('2', 'right', 0, 0.15, 0.004))
    joint_4 = threading.Thread(target=smooth_move_motor_example, args=('4', 'right', -90, 0.18, 0.003))
    joint_5 = threading.Thread(target=smooth_move_motor_example, args=('5', 'right', 90, 0.18, 0.003))
    joint_1.start(), joint_2.start(), joint_4.start(), joint_5.start()
    joint_1.join(), joint_2.join(), joint_4.join(), joint_5.join()

    time.sleep(1)

    for i in range(0, 5):
        smooth_move_motor_example('3', 'right', -40, offset=0.2, wait_time=0.003)
        smooth_move_motor_example('3', 'right', 5, offset=0.2, wait_time=0.003)

    disable_all()


def test_action_hug():
    enable_all()

    def left():
        smooth_move_motor_example('2', 'left', -15)
        smooth_move_motor_example('1', 'left', 30)
        smooth_move_motor_example('2', 'left', -60)
        smooth_move_motor_example('4', 'left', 60)
        smooth_move_motor_example('1', 'left', 45)

    def right():
        smooth_move_motor_example('2', 'right', 15)
        smooth_move_motor_example('1', 'right', -30)
        smooth_move_motor_example('2', 'right', 60)
        smooth_move_motor_example('4', 'right', -60)
        smooth_move_motor_example('1', 'right', -45)

    left = threading.Thread(target=left)
    right = threading.Thread(target=right)
    left.start(), right.start()
    left.join(), right.join()

    time.sleep(2)
    disable_all()


if __name__ == '__main__':
    test_move_joints()
    # test_move_joints_async()
    # test_action_hello()
    # test_action_hug()
    pass
