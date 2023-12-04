from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Callable

from rocs_client.robot.robot_base import RobotBase


@dataclass
class Motor:
    no: str
    orientation: str
    angle: float = 0


@dataclass
class ArmAction(Enum):
    # Reset
    RESET = "RESET"
    # Wave left arm
    LEFT_ARM_WAVE = "LEFT_ARM_WAVE"
    # Swing arms
    ARMS_SWING = "ARMS_SWING"
    # Wave hello
    HELLO = "HELLO"


@dataclass
class HandAction(Enum):
    # Half handshake
    HALF_HANDSHAKE = "HALF_HANDSHAKE"
    # Thumb up
    THUMB_UP = "THUMB_UP"
    # Open hands
    OPEN = "OPEN"
    # Slightly bend hands
    SLIGHTLY_BENT = "SLIGHTLY_BENT"
    # Grasp
    GRASP = "GRASP"
    # Tremble
    TREMBLE = "TREMBLE"
    # Handshake
    HANDSHAKE = "HANDSHAKE"


class Human(RobotBase):
    """
    The Human class implements the behavior of the GR-1 robot. It establishes a connection
    to the robot and offers control functions along with status monitoring.

    Args:

        ssl(bool): Indicates whether SSL authentication is enabled. Default is False.
        host(str): Specifies the network IP address of the robot. Default is '127.0.0.1'.
        port(int): Specifies the PORT of  the robot. Default is 8001.
        on_connected(callable): Listener triggered when the connection to the robot is successful.
        on_message(callable): Listener triggered when the robot sends messages.
        on_close(callable): Listener triggered when the connection to the robot is closed.
        on_error(callable): Listener triggered when error occurs in the robot.
    """
   
    motor_limits: list
    """ This function is used to retrieve the motor limits. """

    def __init__(self, ssl: bool = False, host: str = '127.0.0.1', port: int = 8001, on_connected: Callable = None,
                 on_message: Callable = None, on_close: Callable = None, on_error: Callable = None):
        super().__init__(ssl, host, port, on_connected, on_message, on_close, on_error)
        self.motor_limits = self._get_motor_limit_list()['data']

    def stand(self) -> Dict[str, Any]:
        """
        This method is used to make the robot stand up from a resting position or other positions.

        Once you've called start() and waited for stabilization, go ahead and use stand() to get the robot into a
        standing position.
        Only after making the stand() call can you then give further control commands or motion instructions.
        If the robot is walking or in the middle of other movements, you can also use this function to bring it to a
        stop.

        Returns:

             Dict:
                `code` (int): status code，0 for Normal and -1 for Anomaly
                `msg` (str): result message
        """
        return self._send_request(url='/robot/stand', method='POST')

    def reset(self):
        """
        Initiates the process to reset, zero, or calibrate the robot, bringing it to its initial state.
        """
        return self._send_request(url='/robot/reset', method="POST")

    def get_joint_limit(self) -> Dict[str, Any]:
        """
        Obtain joint limit information.

        Returns:

            Dict:
                - `code` (int):
                    statu code，0: Normal    -1: Anomaly

                - `msg` (str):
                    result msg

                - `data` (dict):
                    results

                    - function (str):
                        函数名称

                    - data(dict):
                        - jointlimit (list): List of dictionaries, each representing the limits of a joint. Each
                                             dictionary contains the following information for a joint:
                            - name (str): The name of the joint.
                            - qdotaMax (float): Maximum joint speed, unit: rad/s.
                            - qaMax (float): Maximum joint angle, unit: radians.
                            - qaMin (float): Minimum joint angle, unit: radians.
                            - tauaMax (float): Maximum joint torque, unit: N.M.


        Example:

        .. code-block:: json

            {
                "code": 0,
                "msg": "ok",
                "data": {
                    "data": {
                        "jointlimit": [
                            {
                                "name": "left_hip_roll",
                                "qaMax": 0.523598775598299,
                                "qaMin": -0.087266462599716,
                                "qdotaMax": 12.56637061435917,
                                "tauaMax": 82.5
                            },
                            {
                                "name": "left_hip_yaw",
                                "qaMax": 0.392699081698724,
                                "qaMin": -0.392699081698724,
                                "qdotaMax": 12.56637061435917,
                                "tauaMax": 82.5
                            },
                            {
                                "name": "left_hip_pitch",
                                "qaMax": 0.698131700797732,
                                "qaMin": -1.221730476396031,
                                "qdotaMax": 22.441443522143093,
                                "tauaMax": 200
                            },
                            {
                                "name": "left_knee_pitch",
                                "qaMax": 2.094395102393195,
                                "qaMin": -0.087266462599716,
                                "qdotaMax": 22.441443522143093,
                                "tauaMax": 200
                            }

                        ]
                    },
                    "function": "SonnieGetStatesLimit"
                }
            }
        """
        return self._send_request(url='/robot/joint_limit', method="GET")

    def get_joint_states(self) -> Dict[str, Any]:
        """
         Retrieve the current joint states of the robot.This data is essential for monitoring and controlling the
         robot's articulation in real-time, enabling precise adjustments and ensuring the robot's overall
         operational status.

        Returns:

            Dict: Response data with the following fields:

            - `code` (int): Status code. 0 indicates normal, -1 indicates an anomaly.
            - `msg` (str): Status message. "ok" indicates normal.
            - `data` (dict): Response data with the following fields:

                - `data` (dict): Status data with the following fields:

                    - `bodyandlegstate` (dict): Body and leg status with the following fields:

                        - `currentstatus` (str): Current status. "StartComplete" indicates startup completion.
                        - `log` (dict): Log information with the following fields:

                            - `logBuffer` (list): Log buffer with the following fields:

                                - `log` (str): Log content. "gRPC system state response init complete" indicates
                                               gRPC system state response initialization completion.

                    - `leftarmstate` (dict): Left arm status with the following fields:

                        - `armstatus` (str): Arm status. "Swing" indicates swing arm mode.

                    - `rightarmstate` (dict): Right arm state with the following fields:

                        - `armstatus` (str):  Arm status. "Swing" indicates swing arm mode.

                - `function` (str):Function name that invoked this interface.

        Example:

        .. code-block:: json

            {
                "code": 0,
                "msg": "ok",
                "data": {
                    "data": {
                        "bodyandlegstate": {
                            "currentstatus": "StartComplete",
                            "log": {
                                "logBuffer": [
                                    {
                                        "log": "gRPC system state response initialization completed"
                                    }
                                ]
                            }
                        },
                        "leftarmstate": {
                            "armstatus": "Swing"
                        },
                        "rightarmstate": {
                            "armstatus": "Swing"
                        }
                    },
                    "function": "SonnieGetSystemStates"
                }
            }

        """
        return self._send_request(url='/robot/joint_states', method="GET")

    def enable_debug_state(self, frequence: int = 1):
        """
        Enable debug mode

        Triggering this function activates the robot to proactively send status values in the background.
         Listen to the `on_message` function to process the received data.

        Args:

            frequence(int): Frequency of status updates.

        Returns:

            Dict:

                - log (dict): Log information.

                    - logBuffer (list): Log buffers.

                        - log (str): Log content.

                - states (dict): Joint data content

                    - basestate (dict): Robot status data

                        - a (float): Hip roll.
                        - b (float): Hip Pitch.
                        - c (float): Hip Yaw.
                        - va (float): Not used.
                        - vb (float): Not used.
                        - vc (float): Not used.
                        - vx (float): Forward-backward direction velocity, unit: m/s.
                        - vy (float): Left-right direction velocity, unit: m/s.
                        - vz (float): Not used.
                        - x (float): Base X position when standing.
                        - y (float): Base y position when standing.
                        - z (float): Base z position when standing.

                    - fsmstatename (dict): Data related to the state machine status.

                        - currentstatus (str): Current status (Unknown, Start, Zero, Stand, Walk, Stop).
                    - jointStates (list): Joint state list.

                        - name (str): Joint name.
                        - qa (float): Actual joint angle, unit: rad.
                        - qdota (float): Actual joint speed, unit: rad/s.
                        - taua (float): Actual joint torque, unit: N.m.
                        - qc (float): Expected joint angle, unit: rad.
                        - qdotc (float): Expected joint speed, unit: rad/s.
                        - tauc (float): Expected joint torque, unit: N.m.
                    - stanceindex (dict): Pose index (not used).
                    - contactforce (dict): Contact force data (not used).

                        - fxL (float): Left foot contact force.
                        - fyL (float): Left foot contact force.
                        - fzL (float): Left foot contact force.
                        - mxL (float): Left foot contact force.
                        - myL (float): Left foot contact force.
                        - mzL (float): Left foot contact force.
                        - fxR (float): Right foot contact force.
                        - fyR (float): Right foot contact force.
                        - fzR (float): Right foot contact force.
                        - mxR (float): Right foot contact force.
                        - myR (float): Right foot contact force.
                        - mzR (float): Right foot contact force.
                - timestamp (dict): Timestamp.

                    - nanos (int):
                    - seconds (str):

            function (str): interface name / function name

        Example:

        .. code-block:: json

            {
                "data": {
                    "states": {
                        "basestate": {
                            "a": -0.00008816774229518624,
                            "b": -0.0031777816310660227,
                            "c": 0,
                            "va": -3.2955695877132929e-9,
                            "vb": -6.542262024864478e-7,
                            "vc": 2.0403557796187139e-8,
                            "vx": 0,
                            "vy": 0,
                            "vz": 0,
                            "x": 0,
                            "y": 0,
                            "z": 0
                        },
                        "contactforce": {
                            "fxL": 0,
                            "fxR": 6,
                            "fyL": 1,
                            "fyR": 7,
                            "fzL": 2,
                            "fzR": 8,
                            "mxL": 3,
                            "mxR": 9,
                            "myL": 4,
                            "myR": 10,
                            "mzL": 5,
                            "mzR": 11
                        },
                        "fsmstatename": {
                            "currentstatus": "Start"
                        },
                        "jointStates": [
                            {
                                "name": "left_hip_roll",
                                "qa": -0.000002967348844382189,
                                "qc": -4.195799309522971e-9,
                                "qdota": -1.2811068419807388e-8,
                                "qdotc": -2.5650460977039419e-9,
                                "taua": 0.00000421397498061693,
                                "tauc": 0.00000421397498061693
                            },
                            {
                                "name": "left_hip_yaw",
                                "qa": 1.1561011056000389e-7,
                                "qc": 5.763118985802831e-10,
                                "qdota": 5.413053331490085e-10,
                                "qdotc": -1.998095673038479e-9,
                                "taua": -5.607576848879348e-7,
                                "tauc": -5.607576848879348e-7
                            },
                            {
                                "name": "left_hip_pitch",
                                "qa": 0.00004391517501779261,
                                "qc": 1.515751869369811e-8,
                                "qdota": 1.9014878092501132e-7,
                                "qdotc": -4.227869290635517e-8,
                                "taua": -0.000007239519592483131,
                                "tauc": -0.000007239519592483131
                            },
                            {
                                "name": "left_knee_pitch",
                                "qa": 0.00004577103623661791,
                                "qc": 1.825644254205245e-8,
                                "qdota": 1.9871683938840232e-7,
                                "qdotc": -1.3400628221563269e-7,
                                "taua": -0.000004188456587918816,
                                "tauc": -0.000004188456587918816
                            },
                            {
                                "name": "left_ankle_pitch",
                                "qa": 0.0000515945298803933,
                                "qc": 2.2981673142499234e-8,
                                "qdota": 2.242746827673787e-7,
                                "qdotc": -2.258893072672217e-7,
                                "taua": -7.153918887352573e-8,
                                "tauc": -7.153918887352573e-8
                            },
                            {
                                "name": "left_ankle_roll",
                                "qa": 6.419495520105573e-7,
                                "qc": 3.706374175342285e-11,
                                "qdota": 2.794181899265958e-9,
                                "qdotc": -5.949285977052194e-9,
                                "taua": 1.093729550329863e-10,
                                "tauc": 1.093729550329863e-10
                            },
                            {
                                "name": "right_hip_roll",
                                "qa": 0.0000028389355052439439,
                                "qc": 4.865708590789946e-9,
                                "qdota": 1.2246925191446977e-8,
                                "qdotc": -3.962174546204988e-9,
                                "taua": -0.000004837825973754749,
                                "tauc": -0.000004837825973754749
                            },
                            {
                                "name": "right_hip_yaw",
                                "qa": -4.364693140246345e-7,
                                "qc": 6.000702384094449e-10,
                                "qdota": -1.8497568931031923e-9,
                                "qdotc": -1.7781221204499439e-9,
                                "taua": -5.867529228984824e-7,
                                "tauc": -5.867529228984824e-7
                            },
                            {
                                "name": "right_hip_pitch",
                                "qa": 0.000045113585488131829,
                                "qc": 2.367752787246051e-8,
                                "qdota": 1.950714297088208e-7,
                                "qdotc": -6.520824184784889e-8,
                                "taua": -0.000011320537478692172,
                                "tauc": -0.000011320537478692172
                            },
                            {
                                "name": "right_knee_pitch",
                                "qa": 0.0000479437468878189,
                                "qc": 2.324249646390596e-8,
                                "qdota": 2.0757655546078694e-7,
                                "qdotc": -1.4486023522267125e-7,
                                "taua": -0.00000557281564261239,
                                "tauc": -0.00000557281564261239
                            },
                            {
                                "name": "right_ankle_pitch",
                                "qa": 0.00005468652781599774,
                                "qc": 2.4630029782206445e-8,
                                "qdota": 2.3684484798495586e-7,
                                "qdotc": -2.2533190930925487e-7,
                                "taua": -7.817536142908409e-8,
                                "tauc": -7.817536142908409e-8
                            },
                            {
                                "name": "right_ankle_roll",
                                "qa": -1.4411157156501987e-7,
                                "qc": 8.786951464767337e-11,
                                "qdota": -6.347293532005193e-10,
                                "qdotc": -6.275949957243541e-9,
                                "taua": 5.977234519649815e-11,
                                "tauc": 5.977234519649815e-11
                            },
                            {
                                "name": "waist_yaw",
                                "qa": 2.7287197903010758e-10,
                                "qc": -1.9509172839224989e-10,
                                "qdota": 2.182983232727597e-7,
                                "qdotc": -1.5630533392766103e-7,
                                "taua": -0.000003249343357926737,
                                "tauc": -0.0000017639729379187398
                            },
                            {
                                "name": "waist_pitch",
                                "qa": -1.1411541437762108e-8,
                                "qc": -5.783273072262379e-9,
                                "qdota": -5.121972652033971e-13,
                                "qdotc": 3.810219915783962e-8,
                                "taua": 0.000011505459672511687,
                                "tauc": 0.000005496170595926694
                            },
                            {
                                "name": "waist_roll",
                                "qa": -1.302909426086466e-8,
                                "qc": -6.480917136286735e-9,
                                "qdota": -3.6044103175709825e-13,
                                "qdotc": -4.3982596326637839e-10,
                                "taua": 0.000013027709577777855,
                                "tauc": 0.000006483935166648911
                            },
                            {
                                "name": "head_yaw",
                                "qa": 0,
                                "qc": 0,
                                "qdota": 0,
                                "qdotc": 0,
                                "taua": 0,
                                "tauc": 0
                            },
                            {
                                "name": "head_pitch",
                                "qa": 0,
                                "qc": 0,
                                "qdota": 0,
                                "qdotc": 0,
                                "taua": 0,
                                "tauc": 0
                            },
                            {
                                "name": "head_roll",
                                "qa": 0,
                                "qc": 0,
                                "qdota": 0,
                                "qdotc": 0,
                                "taua": 0,
                                "tauc": 0
                            }
                        ],
                        "stanceindex": {}
                    },
                    "timestamp": {
                        "nanos": 2,
                        "seconds": "1"
                    }
                },
                "function": "SonnieGetStates"
            }
        """
        return self._send_request(url=f'/robot/enable_states_listen?frequence={frequence}', method="GET")

    def disable_debug_state(self) -> Dict[str, Any]:
        """ Disable debug state mode.

        Returns:

            Dict:

            - code (int): Return code. 0 indicates success, -1 indicates failure.
            - msg (str): Return message. "ok" indicates normal, failure returns an error message.
            - data (dict): Data object containing specific details.
        """
        return self._send_request(url='/robot/disable_states_listen', method="GET")

    def walk(self, angle: float, speed: float):
        """
        Control the walking behavior of the robot. This request is sent via a long-lived connection.



        Args:

             angle(float): Angle to control the direction, ranging from -45 to 45 degrees.
                           Positive values turn left, negative values turn right. Precision of 8 decimal places.
             speed(float): Speed to control forward/backward, ranging from -0.8 to 0.8 meters per second.
                           Positive values move forward, negative values move backward. Precision of 8 decimal places.
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
        Control the movement of the robot's head. This request is sent via a long-lived connection.


        Args:

             roll(float): specify the rotation around the x-axis. Negative values turn the head to the left, and
                          positive values turn it to the right. Range: -17.1887 to 17.1887.
             pitch(float): specify the rotation around the y-axis. Positive values tilt the head forward, and negative
                           values tilt it backward. Range: -17.1887 to 17.1887.
             yaw(float): specify the rotation around the z-axis. Negative values twist the head to the left,
                         and positive values twist it to the right. Range: -17.1887 to 17.1887.
        """
        self._send_websocket_msg({
            'command': 'head',
            'data': {
                'roll': self._cover_param(roll, "roll", -17.1887, 17.1887),
                'pitch': self._cover_param(pitch, "pitch", -17.1887, 17.1887),
                'yaw': self._cover_param(yaw, "yaw", -17.1887, 17.1887)
            }
        })

    def upper_body(self, arm: ArmAction = None, hand: HandAction = None):
        """
        Execute predefined upper body actions by setting arm and hand movements.
        Args:
            - arm_action: (str): Arm action. Options: RESET, LEFT_ARM_WAVE, TWO_ARMS_WAVE, ARMS_SWING, HELLO.
            - hand_action: (str): Hand action. Options: HALF_HANDSHAKE, THUMBS_UP, OPEN, SLIGHTLY_BENT, GRASP, TREMBLE,
                                  HANDSHAKE.


        Returns:
            - code (int): Return code. 0 indicates success, -1 indicates failure.
            - msg (str): Return message. "ok" indicates normal, failure returns an error message.
            - data (dict): Data object containing specific details.

        """
        upper_body_action = {}
        if arm:
            upper_body_action["arm_action"] = arm.value
        if hand:
            upper_body_action["hand_action"] = hand.value
        return self._send_request(url='/robot/upper_body', method="POST", json=upper_body_action)

    def _get_motor_limit_list(self):
        """ Retrieve motor limits.

        Returns:

            Dict: Return data with the following fields:

            - code (int): Return code. 0 indicates success, -1 indicates failure.
            - msg (str): Return message. "ok" indicates normal, failure returns an error message.
            - data (dict): Data object containing specific data.
        """
        response = self._send_request(url='/robot/motor/limit/list', method="GET")
        self.motor_limits = response['data']
        print(f'human_motor_limit: {self.motor_limits}')
        return response

    def _control_svr_start(self):
        for chunk in self._send_request_stream(url='/robot/sdk_ctrl/start', method="GET"):
            print(chunk.decode("utf-8"))

    def _control_svr_log_view(self):
        for chunk in self._send_request_stream(url='/robot/sdk_ctrl/log', method="GET"):
            print(chunk.decode("utf-8"))

    def _control_svr_close(self) -> Dict[str, Any]:
        return self._send_request(url='/robot/sdk_ctrl/close', method="GET")

    def _control_svr_status(self) -> Dict[str, Any]:
        return self._send_request(url='/robot/sdk_ctrl/status', method="GET")

    def _move_joint(self, *args: Motor):
        """ This function is used to move joints to specified positions, considering motor limits.
            It facilitates the movement of multiple joints of the robot. It takes an array of motors with target angles
            and ensures that each joint's movement adheres to predefined motor limits. If motor limits are not available
            initially, the function retries after a delay until the limits are obtained.
            Please be noted that it is crucial to provide valid motor objects with 'no', 'orientation', and 'angle'
            properties. Additionally, having accurate motor limits ensures safe and controlled joint movements.

        Args:

            *args: (Motor) : All fields must be provided. Motor limits and other information
                           can be obtained through the motor_limits property.

        Returns: None.

        """
        motors = []
        target_list = []
        for motor in args:
            motors.append({"no": motor.no, "orientation": motor.orientation, "angle": motor.angle})
        for item1 in motors:
            for item2 in self.motor_limits:
                if item1.get('no') == item2.get('no') and item1.get('orientation') == item2.get('orientation'):
                    merged_item = {**item1, **item2}
                    target_list.append(merged_item)
        if len(target_list):
            for motor in target_list:
                motor['angle'] = (
                    self._cover_param(motor.get('angle'), 'angle', motor.get('min_angle'), motor.get('max_angle')))
                motor.pop('min_angle', 0)
                motor.pop('max_angle', 0)
                motor.pop('ip', 0)
            self._send_websocket_msg({'command': 'move_joint', 'data': {"command": target_list}})

    def move_motor(self, no, orientation: str, angle: float):
        self._move_joint(Motor(no=str(no), orientation=orientation, angle=angle))

    def set_motor_pd_flag(self, no: str, orientation: str):
        data = {
            'no': no,
            'orientation': orientation
        }
        self._send_websocket_msg({'command': 'check_motor_for_flag', 'data': {"command": data}})
        print(f"Set PID mode on! please reboot motor:  {no}-{orientation}")

    def set_motor_pd(self, no: str, orientation: str, p: float, d: float):
        data = {
            'no': no,
            'orientation': orientation,
            'p': p,
            'd': d
        }
        self._send_websocket_msg({'command': 'check_motor_for_set_pd', 'data': {"command": data}})
        print(f"Parameter setting successful! please reboot motor:  {no}-{orientation}")

    def enable_motor(self, no: str, orientation: str):
        data = {
            'no': no,
            'orientation': orientation
        }
        self._send_websocket_msg({'command': 'enable_motor', 'data': {"command": data}})
        print(f"Motor enabled successful:  {no}-{orientation}")

    def disable_motor(self, no: str, orientation: str):
        data = {
            'no': no,
            'orientation': orientation
        }
        self._send_websocket_msg({'command': 'disable_motor', 'data': {"command": data}})
        print(f"Motor disabled successful:  {no}-{orientation}")

    def get_motor_pvc(self, no: str, orientation: str):
        data = {
            'no': str(no),
            'orientation': orientation
        }
        return self._send_request(url='/robot/motor/pvc', method="POST", json=data)
