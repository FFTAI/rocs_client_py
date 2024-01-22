from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Callable

from rocs_client.robot.robot_base import RobotBase


@dataclass
class ArmAction(Enum):
    """
    ArmAction Enum

    Enumerates different arm actions that can be performed with a robot's arms.

    Actions:
        - RESET (str): Reset the arm to its default position.
        - LEFT_ARM_WAVE (str): Wave the left arm.
        - ARMS_SWING (str): Swing both arms.
        - HELLO (str): Wave hello with the arm.

    Example:
        # Using the ArmAction enumeration

        arm_reset = ArmAction.RESET

        arm_wave_left = ArmAction.LEFT_ARM_WAVE
    """

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
    """
    HandAction Enum

    Enumerates different hand actions that can be performed with a robot's hand.

    Actions:
        - HALF_HANDSHAKE (str): Perform a half handshake.
        - THUMB_UP (str): Show a thumbs-up gesture.
        - OPEN (str): Open the hands.
        - SLIGHTLY_BENT (str): Slightly bend the hands.
        - GRASP (str): Perform a grasping motion.
        - TREMBLE (str): Tremble the hands.
        - HANDSHAKE (str): Perform a handshake.

    Example:
        # Using the HandAction enumeration

        half_handshake = HandAction.HALF_HANDSHAKE

        thumbs_up = HandAction.THUMB_UP

    """

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
    Human Class

    The `Human` class implements the behavior of the GR-1 robot. It establishes a connection
    to the robot and offers control functions along with status monitoring.

    Args:
        ssl (bool): Indicates whether SSL authentication is enabled. Default is False.
        host (str): Specifies the network IP address of the robot. Default is '127.0.0.1'.
        port (int): Specifies the PORT of the robot. Default is 8001.
        on_connected (Callable): Listener triggered when the connection to the robot is successful.
        on_message (Callable): Listener triggered when the robot sends messages.
        on_close (Callable): Listener triggered when the connection to the robot is closed.
        on_error (Callable): Listener triggered when an error occurs in the robot.

    Example:
        # Creating an instance of the Human class

        human_robot = Human()

    Note:
        The `Human` class inherits from `RobotBase` and extends its functionality to control the GR-1 robot.
        Ensure that you have the necessary dependencies installed and a valid connection to your robot before using the SDK.

    """

    def __init__(self, ssl: bool = False, host: str = '127.0.0.1', port: int = 8001, on_connected: Callable = None,
                 on_message: Callable = None, on_close: Callable = None, on_error: Callable = None):
        super().__init__(ssl, host, port, on_connected, on_message, on_close, on_error)

    def _control_svr_start(self):
        """Start the SDK control server and print the streaming log.

        This method sends a request to start the SDK control server and continuously prints the streaming log received.

        Returns:
            None
        """
        return self._send_request_stream(url='/robot/sdk_ctrl/start', method="GET")

    def _control_svr_log_view(self):
        """View the SDK control server log and print the streaming log.

        This method sends a request to view the SDK control server log and continuously prints the streaming log received.

        Returns:
            None
        """
        return self._send_request_stream(url='/robot/sdk_ctrl/log', method="GET")

    def _control_svr_close(self) -> Dict[str, Any]:
        """Close the SDK control server.

        This method sends a request to close the SDK control server.

        Returns:
            Dict:
                - code (int): Return code. 0 indicates success, -1 indicates failure.
                - msg (str): Return message. "ok" indicates normal, failure returns an error message.
                - data (dict): Data object containing specific details.
        """

        return self._send_request(url='/robot/sdk_ctrl/close', method="GET")

    def _control_svr_status(self) -> Dict[str, Any]:
        """Retrieve the status of the SDK control server.

        Returns:
            Dict[str, Any]: Status information with the following fields:

                - code (int): Return code. 0 indicates success, -1 indicates failure.
                - msg (str): Return message. "ok" indicates normal, failure returns an error message.
                - data (dict): Data object containing specific details.
        """

        return self._send_request(url='/robot/sdk_ctrl/status', method="GET")

    def stand(self) -> Dict[str, Any]:
        """
        Stand Method

        Make the robot stand up from a resting position or other positions.

        Once you've called start() and waited for stabilization, go ahead and use stand() to get the robot into a
        standing position. Only after making the stand() call can you then give further control commands or motion
        instructions. If the robot is walking or in the middle of other movements, you can also use this function
        to bring it to a stop.

        Returns:
            Dict:
                - `code` (int): Status code. 0 for Normal and -1 for Anomaly.

                - `msg` (str): Result message.

        """

        return self._send_request(url='/robot/stand', method='POST')

    def reset(self):
        """
        Reset Method

        Initiates the process to reset, zero, or calibrate the robot, bringing it to its initial state.

        Returns:
            Dict:
                - `code` (int): Status code. 0 for Normal and -1 for Anomaly.
                - `msg` (str): Result message.

        """

        return self._send_request(url='/robot/reset', method="POST")

    def get_joint_limit(self) -> Dict[str, Any]:
        """
        Get Joint Limit Information

        Obtain the robot's joint limit information.

        Returns:
            Dict:
                - `code` (int): Status code. 0 for Normal, -1 for Anomaly.
                - `msg` (str): Result message.

                - `data` (dict): Results.

                    - `function` (str): Function name.

                    - `data` (dict):

                        - `jointlimit` (list): List of dictionaries, each representing the limits of a joint.
                          Each dictionary contains the following information for a joint:
                            - `name` (str): The name of the joint.
                            - `qaMax` (float): Maximum joint angle, unit: radians.
                            - `qaMin` (float): Minimum joint angle, unit: radians.
                            - `qdotaMax` (float): Maximum joint speed, unit: rad/s.
                            - `tauaMax` (float): Maximum joint torque, unit: N.M.

        Example:
            .. code-block:: json

                {
                    "code": 0,
                    "msg": "ok",
                    "data": {
                        "function": "SonnieGetStatesLimit",
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
                        }
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

                - `function` (str): name of the Function that invoked this interface.

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
                        - qdota (float): Actual (measured) joint velocity, unit: rad/s.
                        - taua (float): Actual joint torque, unit: N.m.
                        - qc (float): Commanded (desired) joint angle, unit: rad.
                        - qdotc (float): Commanded (desired) joint velocity, unit: rad/s。
                        - tauc (float): Commanded (desired) joint torques, unit: N.m.
                    - stanceindex (dict): Pose index (not used).
                    - contactforce (dict): Contact force data (not used).

                        - fxL (float): Force along the X-axis for the left foot.
                        - fyL (float): Force along the Y-axis for the left foot.
                        - fzL (float): Force along the Z-axis for the left foot.
                        - mxL (float): Moment (torque) around the X-axis for left foot.
                        - myL (float): Moment (torque) around the Y-axis for left foot.
                        - mzL (float): Moment (torque) around the Z-axis for left foot.
                        - fxR (float): Force along the X-axis for the right foot.
                        - fyR (float): Force along the Y-axis for the right foot.
                        - fzR (float): Force along the Z-axis for the right foot.
                        - mxR (float): Moment (torque) around the X-axis for right foot.
                        - myR (float): Moment (torque) around the Y-axis for right foot.
                        - mzR (float): Moment (torque) around the Z-axis for right foot.
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
                            // ... additional parameters omitted ...
                            "z": 0
                        },
                        "contactforce": {
                            "fxL": 0,
                            "fxR": 6,
                            // ... additional parameters omitted ...
                            "mzR": 11
                        },
                        "fsmstatename": {
                            "currentstatus": "Start"
                        },
                        "jointStates": [
                            {
                                "name": "left_hip_roll",
                                "qa": -0.000002967348844382189,
                                // ... additional parameters omitted ...
                                "tauc": 0.00000421397498061693
                            },
                            // ... additional parameters omitted ...
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
        """Disable debug state mode.

        Returns:
            dict:
                - code (int): Return code. 0 indicates success, -1 indicates failure.
                - msg (str): Return message. "ok" indicates normal, failure returns an error message.
        """

        return self._send_request(url='/robot/disable_states_listen', method="GET")

    def walk(self, angle: float, speed: float):
        """
        Control the walking behavior of the robot via a long-lived connection.

        Args:
            angle (float): Angle to control the direction, ranging from -45 to 45 degrees.
                           Positive values turn left, negative values turn right. Precision of 8 decimal places.
            speed (float): Speed to control forward/backward, ranging from -0.8 to 0.8 meters per second.
                           Positive values move forward, negative values move backward. Precision of 8 decimal places.

        Returns:
            None

        Raises:
            Any exceptions raised during the execution.

        Notes:
            - The request is sent via a long-lived connection.
            - The provided angle and speed values are automatically adjusted to fit within the specified valid ranges if they go beyond the given thresholds.

        Example:
            To make the robot turn left at a speed of 0.5 m/s:

            >>> Human.walk(angle=30.0, speed=0.5)
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
        Control the movement of the robot's head via a long-lived connection.

        Args:
            roll (float): Rotation around the x-axis. Negative values turn the head to the left,
                         and positive values turn it to the right. Range: -17.1887 to 17.1887.
            pitch (float): Rotation around the y-axis. Positive values tilt the head forward,
                          and negative values tilt it backward. Range: -17.1887 to 17.1887.
            yaw (float): Rotation around the z-axis. Negative values twist the head to the left,
                        and positive values twist it to the right. Range: -17.1887 to 17.1887.

        Returns:
            None

        Raises:
            Any exceptions raised during the execution.

        Notes:
            - The request is sent via a long-lived connection.
            - The roll, pitch, and yaw values are automatically adjusted to fit within the specified valid ranges if they go beyond the given thresholds.

        Example:
            To turn the robot's head to the right (roll), tilt it backward (pitch), and twist it to the left (yaw):

            >>> Human.head(roll=10.0, pitch=-5.0, yaw=-7.0)
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
            arm (ArmAction): Arm action. Options: RESET, LEFT_ARM_WAVE, TWO_ARMS_WAVE, ARMS_SWING, HELLO.
            hand (HandAction): Hand action. Options: HALF_HANDSHAKE, THUMBS_UP, OPEN, SLIGHTLY_BENT, GRASP, TREMBLE, HANDSHAKE.

        Returns:
            Dict:
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
