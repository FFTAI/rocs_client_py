import unittest

from rocs_client import Car, Mod


class TestCar(unittest.TestCase):
    car = Car()

    def test_start(self):
        res = self.car.start()
        print(f'car.test_start: {res}')
        self.car.exit()

    def test_stop(self):
        res = self.car.stop()
        print(f'cat.test_stop: {res}')
        self.car.exit()

    def test_move(self):
        self.car.move(1, 0.8)
        self.car.exit()

    def test_set_mode(self):
        self.car.set_mode(Mod.MOD_4_WHEEL)
        self.car.exit()
