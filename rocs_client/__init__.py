"""
RoCS Client SDK Package

The RoCS (Robot Control System) Client SDK provides a comprehensive set of tools and classes for interacting with robots. This package facilitates communication and control of both human and car robots, offering features for motor control, arm and hand actions, as well as different modes for car robots.

Usage:
    from rocs_client import Human, Car, Mod, Motor, ArmAction, HandAction

Modules:
    - `common`: Contains common functionalities shared across different robot types.

        - `camera`: Module for camera-related functionalities.
        - `system`: Module for system-related functionalities.

    - `robot`: Module encompassing robot-related classes.

        - `car`: Module containing classes specific to car robots.

            - `Car`: Class representing car robots with specific functionalities.

        - `human`: Module containing classes specific to humanoid robots.

            - `Human`: Class representing humanoid robots with general functionalities.

        - `robot_base`: Module containing the base class for all robots.
    - `__init__`: Initialization module for the robot package.

Example:
    # Importing modules

    from rocs_client import Human, Car, Mod, Motor, ArmAction, HandAction

    # Creating instances of robot classes

    human_robot = Human()

    car_robot = Car()

    car_modes = Mod()

    motor_controller = Motor()

    arm_action_performer = ArmAction()

    hand_action_performer = HandAction()

Note:
    Ensure that you have the necessary dependencies installed and a valid connection to your robot before using the SDK.

For more details, refer to the documentation for each specific class within the package.
"""


from . import common
from .robot import Human, Car
from .robot.car import Mod
from .motor.motor import Motor
