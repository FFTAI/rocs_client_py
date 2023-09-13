import time
import unittest
# 安装依赖
# pip install gros_client_car
# 引入依赖
from gros_client_car.car import Mod, Car
# 实例化Car对象
car = Car(host='127.0.0.1')
# 调用启动方法
time.sleep(5)


class TestCar(unittest.TestCase):

    def test_start(self):
        res = car.start()
        print(f'car.test_start: {res}')

    def test_stop(self):
        res = car.stop()
        print(f'cat.test_stop: {res}')
        assert res.get('code') == 0

    def test_set_mode(self):
        car.set_mode(Mod.MOD_4_WHEEL)

    def test_move(self):
        car.move(1, 0.8)
