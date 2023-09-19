import time
import unittest
# 安装依赖
# pip install gros_client_car
# 引入依赖
from src.gros_client_car.car import Mod, Car
# 实例化Car对象
car = Car(host='192.168.12.1')

# 调用启动方法

print(f'video_status: {car.video_status()}')
print(f'video_stream_url: {car.video_stream_url}')


class TestCar(unittest.TestCase):

    def test_start(self):
        res = car.start()
        print(f'car.test_start: {res}')
        assert res.get('code') == 0

    def test_stop(self):
        res = car.stop()
        print(f'cat.test_stop: {res}')
        assert res.get('code') == 0

    def test_set_mode(self):
        res = car.set_mode(Mod.MOD_4_WHEEL)
        assert res.get('code') == 0

    def test_move(self):
        car.set_mode(Mod.MOD_4_WHEEL)
        time.sleep(3)
        car.move(-0, 10)
        car.move(-0, 20)
        car.move(-0, 30)
        car.move(-0, 40)
        car.move(-0, 45)

