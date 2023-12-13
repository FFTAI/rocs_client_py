from dataclasses import dataclass

from rocs_client.robot import RobotBase


@dataclass
class MotorScheme:
    """
    Motor Class

    Represents a motor with specific attributes.

    Attribute:
        - no (str): The identifier or label for the motor.
        - orientation (str): The orientation of the motor.
        - angle (float, optional): The angle associated with the motor. Defaults to 0.

    Example:

        # Creating an instance of the Motor class
        motor_instance = Motor(no="1", orientation="Vertical", angle=45.0)

    Note:
        The Motor class is decorated with the @dataclass decorator, which automatically generates
        special methods like __init__ based on the class attributes.
    """
    no: str
    orientation: str
    angle: float = 0


class Motor(RobotBase):
    limits: list

    def __init__(self, ssl: bool = False, host: str = '127.0.0.1', port: int = 8001):
        super().__init__(ssl, host)
        self.limits = self._get_motor_limit_list()['data']

    def _get_motor_limit_list(self):
        """Retrieve motor limits.

        Returns:
            Dict:
                - code (int): Return code. 0 indicates success, -1 indicates failure.

                - msg (str): Return message. "ok" indicates normal, failure returns an error message.

                - data (dict): Data object containing motor limit information.
                    - motor1_limit (float): Limit for motor 1.
                    - motor2_limit (float): Limit for motor 2.
                    - ...
        """
        response = self._send_request(url='/robot/motor/limit/list', method="GET")
        self.limits = response['data']
        print(f'human_motor_limit: {self.limits}')
        return response

    def set_motor_pd_flag(self, no: str, orientation: str):
        """ Set PD mode for a specific motor.

        Args:
            no (str): Motor number.
            orientation (str): Motor orientation.
        """
        data = {
            'no': no,
            'orientation': orientation
        }
        self._send_websocket_msg({'command': 'check_motor_for_flag', 'data': {"command": data}})
        print(f"PD mode set! Please restart the motor: {no}-{orientation}")

    def set_motor_pd(self, no: str, orientation: str, p: float = 0.36, d: float = 0.042):
        """
        Set the parameters for a Proportional-Derivative (PD) control mode for a specific motor.

        This function allows you to configure the proportional (P) and derivative (D) gains for the motor.
        Providing valid values for 'no' (motor number), 'orientation' (motor orientation), 'p' (proportional gain),
        and 'd' (derivative gain) is crucial for accurate and stable motor control.

        Args:
            no (str): Motor number.
            orientation (str): Motor orientation.
            p (float): Proportional gain value.
            d (float): Derivative gain value.
        """
        data = {
            'no': no,
            'orientation': orientation,
            'p': p,
            'd': d
        }
        self._send_websocket_msg({'command': 'check_motor_for_set_pd', 'data': {"command": data}})
        print(f"Parameters set successfully! Please restart the motor: {no}-{orientation}")

    def enable_motor(self, no: str, orientation: str):
        """
        Enable the specified motor.

        Args:
            no (str): Motor number.
            orientation (str): Motor orientation.
        """
        if int(no) > 8:
            print(f"Motor enabled fail:  This function can only control 0-8. But current value: {no}")
            return
        data = {'no': no, 'orientation': orientation}
        self._send_websocket_msg({'command': 'enable_motor', 'data': {"command": data}})
        print(f"Motor enabled successfully:  {no}-{orientation}")

    def disable_motor(self, no: str, orientation: str):
        """
        Disable the specified motor.

        Args:
            no (str): Motor number.
            orientation (str): Motor orientation.
        """
        if int(no) > 8:
            print(f"Motor Disable fail:  This function can only control 0-8. But current value: {no}")
            return
        data = {'no': no, 'orientation': orientation}
        self._send_websocket_msg({'command': 'disable_motor', 'data': {"command": data}})
        print(f"Motor disabled successfully: {no}-{orientation}")

    def enable_hand(self):
        """  Enable the Hand for individual control. """
        return self._send_request(url='/robot/motor/hand/enable', method="GET")

    def disable_hand(self):
        """  Disable the Hand for individual control. """
        return self._send_request(url='/robot/motor/hand/disable', method="GET")

    def _move_joint(self, *args: MotorScheme):
        """ Move joints to specified positions, considering motor limits.

        Facilitates the movement of multiple joints of the robot. Takes an array of motors with target angles
        and ensures that each joint's movement adheres to predefined motor limits.

        Args:
            *args (Motor): An array of Motor objects with 'no', 'orientation', and 'angle' properties.

        Returns:
            None.
        """

        motors = []
        target_list = []
        for motor in args:
            motors.append({"no": motor.no, "orientation": motor.orientation, "angle": motor.angle})
        for item1 in motors:
            for item2 in self.limits:
                if item1.get('no') == item2.get('no') and item1.get('orientation') == item2.get('orientation'):
                    merged_item = {**item1, **item2}
                    target_list.append(merged_item)
        if len(target_list):
            for motor in target_list:
                motor['angle'] = (
                    self._cover_param(motor.get('angle'), f'{motor.get("no")}-{motor.get("orientation")}-angle',
                                      motor.get('min_angle'), motor.get('max_angle')))
                motor.pop('min_angle', 0)
                motor.pop('max_angle', 0)
                motor.pop('ip', 0)
            self._send_websocket_msg({'command': 'move_joint', 'data': {"command": target_list}})

    def move_motor(self, no, orientation: str, angle: float):
        """Move a specific motor to the specified angle.

        Args:
            no (str): Motor number.
            orientation (str): Motor orientation.
            angle (float): Target angle for the motor.
        """
        self._move_joint(MotorScheme(no=no, orientation=orientation, angle=angle))

    def get_motor_pvc(self, no, orientation: str):
        """
        Get the Position, Velocity, and Current (PVC) information for a specific motor.

        Args:
            no (str): Motor number.
            orientation (str): Motor orientation.

        Returns:
            Dict: Return data with the following fields:
                - code (int): Return code. 0 indicates success, -1 indicates failure.
                - msg (str): Return message. "ok" indicates normal, failure returns an error message.
                - data (dict): PVC information including position, velocity, and current.

        Examples:

        .. code-block:: json

            {
                "code": 0,
                "msg": "ok",
                "data": {
                    "no": "4",
                    "orientation": "right",
                    "position": "85.00",
                    "velocity": "0.0123",
                    "current": "0.85674"
                }
            }

        """

        data = {
            'no': str(no),
            'orientation': orientation
        }
        return self._send_request(url='/robot/motor/pvc', method="POST", json=data)

    def get_hand_position(self):
        """
        Get the current position of the robot's hand.

        Returns:

            Dict: Return data with the following fields:
                - code (int): Return code. 0 indicates success, -1 indicates failure.
                - msg (str): Return message. "ok" indicates normal, failure returns an error message.
                - data (dict): Data object containing specific data.
        """
        return self._send_request(url='/robot/motor/hand/state', method="POST", json={})
