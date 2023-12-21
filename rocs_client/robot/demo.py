import time

from rocs_client import Human

from rocs_client.robot.human import ArmAction, HandAction, Motor

# Connect to your robot using its IP address
human = Human(host='192.168.204.129') # Replace '192.168.12.1' with your robot's actual IP

# Activate remote control for the robot
#human.start()

# Wait for 10 seconds to ensure the robot's control system stabilizes after initiating the remote control command start().
#time.sleep(10)

# Instruct the robot to stand up
#human.stand()

# Move the robot forward at a speed of 0.1
human.walk(0, 0.1)

# Gesture: Wave the left hand
#human.upper_body(arm=ArmAction.LEFT_ARM_WAVE)

# Gesture: Wave both hands
#human.upper_body(arm=ArmAction.TWO_ARMS_WAVE)

# Gesture: Tremble the fingers
#human.upper_body(hand=HandAction.TREMBLE)

# Move motor no.1 left and right by 10 degrees each
#human.move_joint(Motor(no='1', angle=10, orientation='left'),

                 #Motor(no='1', angle=10, orientation='right'))

