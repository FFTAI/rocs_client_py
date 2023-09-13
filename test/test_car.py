# 安装依赖
# pip install gros_client_car
import time
import unittest

# 引入依赖
from src.gros_client_car import Car

# 实例化human对象
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

    def test_move(self):
        car.move(1, 0.8)
