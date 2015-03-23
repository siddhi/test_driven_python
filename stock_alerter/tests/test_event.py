import unittest

from ..event import Event


class EventTest(unittest.TestCase):
    def test_a_listener_is_notified_when_an_event_is_raised(self):
        called = False
        def listener():
            nonlocal called
            called = True

        event = Event()
        event.connect(listener)
        event.fire()
        self.assertTrue(called)

    def test_a_listener_is_passed_right_parameters(self):
        params = ()
        def listener(*args, **kwargs):
            nonlocal params
            params = (args, kwargs)

        event = Event()
        event.connect(listener)
        event.fire(5, shape="square")
        self.assertEqual(((5, ), {"shape":"square"}), params)
