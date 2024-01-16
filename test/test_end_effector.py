import time
import unittest

from rocs_client import EndEffector, EndEffectorScheme


async def on_connected():
    print("WebSocket opened...")


async def on_message(message: str):
    print("Received message:", message)


async def on_close():
    print("WebSocket closed")


async def on_error(error: Exception):
    print("WebSocket error:", error)


end_effector = EndEffector(host="127.0.0.1",
                           on_connected=on_connected, on_message=on_message, on_close=on_close, on_error=on_error)


class TestEndEffector(unittest.TestCase):

    def test_enable(self):
        """ Enable the end control service.

        After executing this command, you will be able to utilize the 'control_* function for end control.
        """
        result = end_effector.enable()
        print(f'test_enable:  {result}')
        end_effector.exit()

    def test_disable(self):
        """ Disable the end control service.

        After executing this command, The end control will terminate
        """
        result = end_effector.disable()
        print(f'test_disable:  {result}')
        end_effector.exit()

    def test_enable_state(self):
        """
        The activation of this function enables status monitoring, Allowing access to information such as the current
        live location of the recipient through the `on_message` function
        """
        result = end_effector.enable_state(2)
        print(f'test_enable_state:  {result}')
        time.sleep(5)
        end_effector.exit()

    def test_disable_state(self):
        """ Disable status monitoring """
        result = end_effector.disable_state()
        print(f'test_disable_state:  {result}')
        end_effector.exit()

    def test_control_left(self):
        """ Controlling left hand """
        end_effector.control_left(EndEffectorScheme(x=1, y=1, z=1, qx=1, qy=1, qz=1, qw=1))
        time.sleep(5)
        end_effector.exit()

    def test_control_right(self):
        """ Controlling right hand """
        end_effector.control_right(EndEffectorScheme(x=1, y=1, z=1, qx=1, qy=1, qz=1, qw=1))
        time.sleep(5)
        end_effector.exit()
