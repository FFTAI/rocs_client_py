# 安装依赖
# pip install gros_client

# 引入依赖
from gros_client import Human

# 实例化human对象
human = Human(host='192.168.9.17')
# 调用启动方法
human.start()