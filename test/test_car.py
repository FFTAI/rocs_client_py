import unittest

from gros_client import robot

car = robot.Car()


class TestCar(unittest.TestCase):

    def test_start(self):
        res = car.start()
        print(f'car.test_start: {res}')
        assert res.get('code') == 0

    def test_stop(self):
        res = car.stop()
        print(f'cat.test_stop: {res}')
        assert res.get('code') == 0

    def test_move(self):
        car.move(1, 0.8)
