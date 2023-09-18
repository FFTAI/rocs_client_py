# 傅利叶通用机器人系统-客户端SDK（python）


## 概述
    本例(GROS Client SDK)适用于您已经拥有傅利叶（Fourier）所提供的机器人设备，通过本例可实现对机器人的控制。它提供了一组简单的API，让你可以轻松地与机器人进行交互。

## 历程
    
| 版本号 | 作者     | 日期     | 描述                           | 快速预览                                       |
|-----|--------|--------|------------------------------|--------------------------------------------|
| 0.1 | 傅利叶软件部 | 2023.8 | 1. 立项<br/>2. 确认基础架构          | [0.1说明](https://fftai.github.io/v0.1.html) |
| 0.2 | 傅利叶软件部    | 2023.9 | 1. 控制模块、系统模块<br/>2. 具体coding | [0.2说明](https://fftai.github.io/v0.2.html) |


## 快速上手

### 安装
    
```shell
pip install gros_client 

# 如遇网络延迟，可选择清华源安装 
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gros_client
```


### 使用方法
#### 导入sdk
首先你需要在你的Python代码中导入这个SDK

```python
import gros_client   # 导入root
```
#### 创建机器人对象
然后，你需要创建一个机器人对象，以便使用这个SDK

```python
from gros_client import Human  # 按需导入Human、同理还有Car、Dog等

human = Human(host='192.168.12.1')
```

#### 示例代码
下面是一个完整的示例代码，演示如何使用这个SDK来控制机器人：

```python
import time
from gros_client import Human

human = Human(host='192.168.9.17') # 请将host替换为您所拥有设备的ip
human.start() # 启动远程控制
time.sleep(10) # 控制系统内置状态机。为了保证机器人的校准和启动正常，在start()指令之后建议10s再执行后续指令

human.stand() # 站立
human.walk(0, 0.1) # 以0.1的速度向正前方移动
```