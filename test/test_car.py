# 安装依赖
# pip install gros_client_car

# 引入依赖
from gros_client_car import Car

# 实例化human对象
car = Car(host='192.168.9.17')
# 调用启动方法
car.start()

import unittest


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
