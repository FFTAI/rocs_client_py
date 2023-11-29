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
            smooth_move_motor_example(motor['no'], motor['orientation'], 0, offset=1.3, wait_time=0.04)

    for i in range((len(human.motor_limits) - 1), -1, -1):
        motor = human.motor_limits[i]
        if motor['orientation'] == 'left':
            human.disable_motor(motor['no'], motor['orientation'])


def disable_right():
    for i in range((len(human.motor_limits) - 1), -1, -1):
        motor = human.motor_limits[i]
        if motor['orientation'] != 'left':
            smooth_move_motor_example(motor['no'], motor['orientation'], 0, offset=1.3, wait_time=0.04)

    for i in range((len(human.motor_limits) - 1), -1, -1):
        motor = human.motor_limits[i]
        if motor['orientation'] != 'left':
            human.disable_motor(motor['no'], motor['orientation'])


def disable_all():
    time.sleep(2)
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
    smooth_move_motor_example('1', 'left', 30)

    smooth_move_motor_example('5', 'left', -90)

    smooth_move_motor_example('8', 'left', 50)
    smooth_move_motor_example('8', 'left', 0)
    smooth_move_motor_example('8', 'left', 50)
    smooth_move_motor_example('8', 'left', 0)
    smooth_move_motor_example('8', 'left', 50)
    smooth_move_motor_example('8', 'left', 0)
    disable_all()


def test_move_joints_async():
    enable_all()
    left_2 = threading.Thread(target=smooth_move_motor_example, args=('2', 'left', -45))
    right_2 = threading.Thread(target=smooth_move_motor_example, args=('2', 'right', 45))
    left_4 = threading.Thread(target=smooth_move_motor_example, args=('4', 'left', 45))
    right_4 = threading.Thread(target=smooth_move_motor_example, args=('4', 'right', -45))
    left_2.start(), right_2.start(), left_4.start(), right_4.start()
    left_2.join(), right_2.join(), left_4.join(), right_4.join()
    disable_all()


def test_action_hello():
    def move_3():
        for i in range(0, 5):
            smooth_move_motor_example('3', 'right', -40, offset=0.2, wait_time=0.003)
            smooth_move_motor_example('3', 'right', 5, offset=0.2, wait_time=0.003)

    def move_5():
        for i in range(0, 3):
            smooth_move_motor_example('5', 'right', 90, offset=0.15, wait_time=0.005)
            smooth_move_motor_example('5', 'right', 55, offset=0.15, wait_time=0.005)

    enable_all()

    joint_1 = threading.Thread(target=smooth_move_motor_example, args=('1', 'right', -65, 0.16, 0.003))
    joint_2 = threading.Thread(target=smooth_move_motor_example, args=('2', 'right', 0, 0.15, 0.004))
    joint_4 = threading.Thread(target=smooth_move_motor_example, args=('4', 'right', -90, 0.18, 0.003))
    joint_5 = threading.Thread(target=smooth_move_motor_example, args=('5', 'right', 90, 0.18, 0.003))
    joint_1.start(), joint_2.start(), joint_4.start(), joint_5.start()
    joint_1.join(), joint_2.join(), joint_4.join(), joint_5.join()

    time.sleep(1)
    t_move_3 = threading.Thread(target=move_3)
    t_move_5 = threading.Thread(target=move_5)

    t_move_3.start()
    t_move_5.start()
    t_move_3.join()
    t_move_5.join()

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

    disable_all()


if __name__ == '__main__':
    test_move_joints()
    # test_move_joints_async()
    # test_action_hello()
    # test_action_hug()
    pass
