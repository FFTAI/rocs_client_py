import websockets
import json
import asyncio
import time

from src.gros_client.robot import Robot

# 使用示例
if __name__ == "__main__":



    print("************")
    # 创建WebSocketClient并指定WebSocket服务器的URL和回调函数
    robot = Robot(host='127.0.0.1')
    print("************")
    robot.enable_debug_state(2)
    print("~~~~~~~~~~~~~~")
    result = robot.get_joint_limit()
    asyncio.run(robot.move(10,10))
    while True:
        print("消费者")
        print("length:", robot.states_queue.qsize(), robot.get_states())
        time.sleep(1)
    print(result)
    # print(robot.get_type())
    # print(robot.enable_debug_state())
