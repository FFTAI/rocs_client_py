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
        end_effector.enable()
        end_effector.exit()

    def test_disable(self):
        end_effector.disable()
        end_effector.exit()

    def test_enable_state(self):
        end_effector.enable_state(2)
        time.sleep(5)
        end_effector.exit()

    def test_disable_state(self):
        end_effector.disable_state()
        end_effector.exit()

    def test_control_left(self):
        end_effector.control_left(EndEffectorScheme(x=1, y=1, z=1, qx=1, qy=1, qz=1, qw=1))
        time.sleep(5)
        end_effector.exit()

    def test_control_right(self):
        end_effector.control_right(EndEffectorScheme(x=1, y=1, z=1, qx=1, qy=1, qz=1, qw=1))
        time.sleep(5)
        end_effector.exit()
