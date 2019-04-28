from test.unitMin import unitMin, driver_control
import unittest


class TestUnitTear(unitMin):

    @driver_control
    def test_add_min(self):
        self.assertEqual(1, 2)

if __name__ == '__main__':
    unittest.main()