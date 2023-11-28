from rocs_client import Human

"""
set p and d
"""

human = Human(host="192.168.137.210")


def set_pds():
    for motor in human.motor_limits:
        human.check_motor_for_set_pd(motor['no'], motor['orientation'], 0.36, 0.042)


if __name__ == '__main__':
    set_pds()
