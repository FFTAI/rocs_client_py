from rocs_client import Human

"""
open set pid mod
"""

human = Human(host="192.168.137.210")


def open_set_pd_flag():
    for motor in human.motor_limits:
        human.check_motor_for_flag(motor['no'], motor['orientation'])


if __name__ == '__main__':
    open_set_pd_flag()
