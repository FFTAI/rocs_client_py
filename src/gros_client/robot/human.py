from typing import Any, Dict, Callable

import requests

from ..robot_base import RobotBase


class Human(RobotBase):
    """
    GR-1人形机器人对象

    在你需要连接GR-1人形机器人的时候，你可以创建一个Human()对象！ 这将会在后台连接到人形的控制系统，并提供对应的控制函数和状态监听！

    Args:
        ssl(bool):  是否开启ssl认证。默认 False
        host(str):  GR-01人形设备的网络IP
        port(int):  GR-01人形设备的控制服务的PORT
        on_connected(Callable):  该监听将会在GR-01人形设备连接成功时触发
        on_message(Callable): 该监听将会在GR-01人形设备发送系统状态时候触发，你可能需要监听该回掉处理你的逻辑
        on_close(Callable): 该监听将会在GR-01人形设备连接关闭时触发
        on_error(Callable): 该监听将会在GR-01人形设备发生错误时触发
    """

    def __init__(self, ssl: bool = False, host: str = '127.0.0.1', port: int = 8001, on_connected: Callable = None,
                 on_message: Callable = None, on_close: Callable = None, on_error: Callable = None):
        super().__init__(ssl, host, port, on_connected, on_message, on_close, on_error)

    def stand(self) -> Dict[str, Any]:
        """
        GR-01人形设备将会原地站立

        当进行了start之后如果你想对GR-01人形设备进行指令控制，你同样需要调用该函数让其位置stand的模式。如果是在行走过程中需要停止，你同样可以调用该函数进行stand

        Returns:
             result(Dict): return一个结果集 {code: 0, msg: 'ok'}  or  {code: -1, msg: $ERR_MSG}

        """
        response = requests.post(f'{self._baseurl}/robot/stand')
        return response.json()

    def get_joint_limit(self) -> Dict[str, Any]:
        """
        获取关节限位

        Returns:
            result(Dict):

        """
        response = requests.get(f'{self._baseurl}/robot/joint_limit')
        return response.json()

    def get_joint_states(self) -> Dict[str, Any]:
        """
        获取关节状态

        Returns:
            result(Dict):

        """
        response = requests.get(f'{self._baseurl}/robot/joint_states')
        return response.json()

    def enable_debug_state(self, frequence: int = 1):
        """
        开启state调试模式

        触发该函数将会在后台触发GR-01人形设备主动发送状态值的指令，因此对应的你需要监听on_message函数进行处理

        Args:
            frequence(int): 频率

        """
        response = requests.get(f'{self._baseurl}/robot/enable_states_listen')
        return response.json()

    def disable_debug_state(self):
        """ 关闭state调试模式 """
        response = requests.get(f'{self._baseurl}/robot/disable_states_listen')
        return response.json()

    def walk(self, angle: float, speed: float):
        """
        控制GR-01人形设备行走

        ``该请求维持了长链接的方式进行发送``

        Args:
            angle(float): 角度 控制方向，取值范围为正负45度。向左为正，向右为负！(浮点数8位)
            speed(float): 速度 控制前后，取值范围为正负0.8。向前为正，向后为负！(浮点数8位)
        """
        angle = self._cover_param(angle, 'angle', -45, 45)
        speed = self._cover_param(speed, 'speed', -0.8, 0.8)
        self._send_websocket_msg({
            'command': 'move',
            'data': {
                'angle': angle,
                'speed': speed
            }
        })

    def head(self, roll: float, pitch: float, yaw: float):
        """
        控制GR-01人形头部运动

        ``该请求维持了长链接的方式进行发送``

        Args:
            roll(float): roll（翻滚角）：描述围绕x轴旋转的角度，左转头为负，向右转为正，范围（-17.1887-17.1887）
            pitch(float): pitch（俯仰角）：描述围绕y轴旋转的角度。前点头为正，后点头为负，范围（-17.1887-17.1887）
            yaw(float): yaw（偏航角）：描述围绕z轴旋转的角度。左扭头为负，右扭头为正，范围（-17.1887-17.1887）
        """
        self._send_websocket_msg({
            'command': 'head',
            'data': {
                'roll': roll,
                'pitch': pitch,
                'yaw': yaw
            }
        })
