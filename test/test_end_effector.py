import asyncio
import unittest

from rocs_client import EndEffector, EndEffectorScheme

end_effector = EndEffector(host="127.0.0.1")


class TestEndEffector(unittest.TestCase):

    def test_enable(self):
        end_effector.enable()
        end_effector.exit()

    def test_disable(self):
        end_effector.disable()
        end_effector.exit()

    def test_enable_state(self):
        end_effector.enable_state()
        end_effector.exit()

    def test_disable_state(self):
        end_effector.disable_state()
        end_effector.exit()

    def test_control_left(self):
        end_effector.control_left(EndEffectorScheme())

    def test_control_right(self):
        end_effector.control_left(EndEffectorScheme())
