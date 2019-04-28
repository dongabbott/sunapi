import unittest
from unittest.case import _Outcome


class unitMin(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(unitMin, self).__init__(*args, **kwargs)

    def setUp(self):
        name = getattr(self, '_testMethodName')
        print(name)
        super(unitMin, self).setUp()

    def tearDown(self):
        name = getattr(_Outcome(self), 'errors')
        # result = self.defaultTestResult()  # these 2 methods have no side effects
        print(name)
        super(unitMin, self).tearDown()


def driver_control(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            print(1111)
    return  wrapper