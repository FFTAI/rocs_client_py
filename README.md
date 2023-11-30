<p align="center">
    <a href="https://fftai.github.io" target="_blank" rel="noopener noreferrer">
        <img width="200" src="https://raw.githubusercontent.com/FFTAI/rocs_server/main/assets/ico.jpg" alt="logo">
    </a>
</p>

# RoCS-Client SDK (python)

## Overview
This example (RoCS Client SDK) is suitable for you already have a robot device provided by Fourier!
This example can be used to control the robot.
It provides a set of simple APIs that allow you to easily interact with the robot.

## Installation
```shell
pip install rocs_client 
```

## Function introduction
**You can use the following methods to control the robot**

- _control_svr_start(): Turn on the robot control program
- _control_svr_status(): View the running status of the robot
- _control_svr_log_view(): View robot run logs
- _control_svr_close(): Turn off the robot control program
- start(): Zero/Start control
- stop(): Emergency stop (will stop with power off)
- exit(): Exit robot control
- stand(): Stand in place
- walk(angle, speed): Control the robot to move, walk
    - angle(float): Angle controls direction, range is plus or minus 45 degrees. Left is positive, right is negative! (
      Floating point number with 8 digits)
    - speed(float): Speed controls forward and backward, range is plus or minus 0.8. Forward is positive, backward is
      negative! (Floating point number with 8 digits)
- head(roll, pitch, yaw): Control GR-01 humanoid head movement
    - roll(float): roll (roll angle): describes the angle of rotation around the x-axis, left turn head is negative,
      right turn is positive, range (-17.1887-17.1887)
    - pitch(float): pitch (pitch angle): describes the angle of rotation around the y-axis. Nodding forward is positive,
      nodding backward is negative, range (-17.1887-17.1887)
    - yaw(float): yaw (yaw angle): describes the angle of rotation around the z-axis. Turning left head is negative,
      turning right head is positive, range (-17.1887-17.1887)
- upper_body(arm_action, hand_action): Upper limb preset command
    - arm_action(ArmAction): Arm preset command enumeration
    - hand_action(HandAction): Hand preset command enumeration

## Usage

### Import sdk
First, you need to import this SDK in your Python code
```python
import rocs_client  # Import root
```

### Create a robot object
Then, you need to create a robot object in order to use this SDK
```python
from rocs_client import Human  # Import Human as needed, similarly there are Car, Dog, etc.

human = Human(host='192.168.12.1')# Please replace host with the ip of your device
```

## Sample Code
Below is a complete sample code that demonstrates how to use this SDK to control a robot:


### Whole machine control (rocs_client>=1.0)
```python 
import time
from rocs_client import Human
from rocs_client.robot.human import ArmAction, HandAction

human = Human(host='192.168.9.17')  # Please replace host with the ip of your device
        
human.start()  # Start remote control
time.sleep(10)  # Control system built-in state machine. To ensure normal calibration and startup of the robot, it is recommended to execute subsequent instructions after start() instruction for 10s
human.stand()  # Stand up

human.upper_body(arm=ArmAction.LEFT_ARM_WAVE)  # Wave left hand
human.upper_body(hand=HandAction.TREMBLE)  # Tremble fingers

human.stand()  # Stand up
human.walk(0, 0.1)  # Move forward at a speed of 0.1
```

### Single motor control (rocs_client>=1.2.8)
```python
import math
import threading
import time

from rocs_client import Human

human = Human(host="192.168.9.17")  # Please replace host with the ip of your device

def set_pds_flag():
    for motor in human.motor_limits:
        human.set_motor_pd_flag(motor['no'], motor['orientation'])
    human.exit()


def set_pds():
    for motor in human.motor_limits:
        human.set_motor_pd(motor['no'], motor['orientation'], 0.36, 0.042)
    human.exit()


def enable_all():
    for motor in human.motor_limits:
        human.enable_motor(motor['no'], motor['orientation'])
    time.sleep(1)


def _disable_left():
    for i in range((len(human.motor_limits) - 1), -1, -1):
        motor = human.motor_limits[i]
        if motor['orientation'] == 'left':
            smooth_move_motor_example(motor['no'], motor['orientation'], 0, offset=1, wait_time=0.04)

    for i in range((len(human.motor_limits) - 1), -1, -1):
        motor = human.motor_limits[i]
        if motor['orientation'] == 'left':
            human.disable_motor(motor['no'], motor['orientation'])


def _disable_right():
    for i in range((len(human.motor_limits) - 1), -1, -1):
        motor = human.motor_limits[i]
        if motor['orientation'] != 'left':
            smooth_move_motor_example(motor['no'], motor['orientation'], 0, offset=1, wait_time=0.04)

    for i in range((len(human.motor_limits) - 1), -1, -1):
        motor = human.motor_limits[i]
        if motor['orientation'] != 'left':
            human.disable_motor(motor['no'], motor['orientation'])


def disable_all():
    time.sleep(2)
    t_left = threading.Thread(target=_disable_left)
    t_right = threading.Thread(target=_disable_right)
    t_left.start(), t_right.start()
    t_left.join(), t_right.join()
    human.exit()


def wait_target_done(no, orientation, target_angle, rel_tol=1):
    while True:
        p, _, _ = human.get_motor_pvc(str(no), orientation)['data']
        if math.isclose(p, target_angle, rel_tol=rel_tol):
            break


def smooth_move_motor_example(no, orientation: str, target_angle: float, offset=0.05, wait_time=0.004):
    current_position = 0
    while True:
        try:
            current_position, _, _ = (human.get_motor_pvc(no, orientation))['data']
            if current_position is not None and current_position != 0:
                break
        except Exception as e:
            pass
    target_position = target_angle
    cycle = abs(int((target_position - current_position) / offset))

    for i in range(0, cycle):
        if target_position > current_position:
            current_position += offset
        else:
            current_position -= offset
        human.move_motor(no, orientation, current_position)
        time.sleep(wait_time)
    wait_target_done(no, orientation, current_position)


"""
This is the action of simple
When you first single-control a motor, I strongly recommend that you must run this function for testing

If the motor's motion is linear and smooth, then you can try something slightly more complicated
But if it freezes, you need to debug your P and D parameters.
"""
human.enable_motor('2', 'left')
time.sleep(2)
smooth_move_motor_example('2', 'left', -10)
smooth_move_motor_example('2', 'left', -20)
smooth_move_motor_example('2', 'left', -10)
time.sleep(2)
human.disable_motor('2', 'left')
```

[More test cases are in the Test folder](./test/)

## Journey

| Version | Author                      | Date    | Description                                                        | Quick Preview                                                |
|---------|-----------------------------|---------|--------------------------------------------------------------------|--------------------------------------------------------------|
| 0.1     | Fourier Software Department | 2023.8  | 1. Project initiation<br/>2. Confirm basic architecture            | [0.1 Description](https://fftai.github.io/release/v0.1.html) |
| 0.2     | Fourier Software Department | 2023.9  | 1. Control module, system module<br/>2. Specific coding            | [0.2 Description](https://fftai.github.io/release/v0.2.html) |
| 1.1     | Fourier Software Department | 2023.10 | 1. Hand, head preset actions<br/>2. Single joint control of upper body | [1.1 Description](https://fftai.github.io/release/v1.1.html) |
| 1.2     | Fourier Software Department | 2023.11 | smooth movement example for single motor control                   |                                                              |

