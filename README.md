### 文档


### 使用示例

```python

# 安装依赖
# pip install gros_client_car

# 引入依赖
from gros_client_car import Car

# 实例化human对象
car = Car(host='192.168.9.17')

# 调用启动方法
car.start()

# 切换四轮模式
car.set_mod(Mod.MOD_4_WHEEL)

# 以速度10向正前方移动 
car.move(10, 0)

# 以速度20向正后方移动
car.move(-20, 0)

# 以速度20向右(30度)后方移动
car.move(-20, 30)

