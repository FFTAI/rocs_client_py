# 傅利叶Car-客户端SDK（python）

## 概述
    本例(GROS_Client_Car SDK)适用于您已经拥有傅利叶（Fourier）所提供的Car设备，通过本例可实现对机器人的控制。它提供了一组简单的API，让你可以轻松地进行交互。

## 快速上手

### 安装
    
```shell
pip install gros_client_car
```

### 导入sdk
首先你需要在你的Python代码中导入这个SDK
```python
from gros_client_car import Car
```

### 创建Car对象
然后，你需要创建一个Car对象，以便使用这个SDK
```python
from gros_client_car import Car  # 按需导入Human、同理还有Car、Dog等

car = Car(host='192.168.9.17')
```

### 示例代码
下面是一个完整的示例代码，演示如何使用这个SDK来控制机器人：

```python
from gros_client_car import Car

# 引入依赖
from gros_client_car import Car, Mod

# 实例化human对象
car = Car(host='192.168.9.17')

# 调用启动方法
car.start()

# 切换四轮模式
car.set_mode(Mod.MOD_4_WHEEL)

# 以速度10向正前方移动 
car.move(-10, 0)

# 以速度20向正后方移动
car.move(20, 0)

# 以速度20向右(30度)后方移动
car.move(20, 30)
```