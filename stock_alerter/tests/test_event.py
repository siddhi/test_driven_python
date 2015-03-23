import unittest
from unittest import mock

from ..event import Event


class EventTest(unittest.TestCase):
    def test_a_listener_is_notified_when_an_event_is_raised(self):
        listener = mock.Mock()
        event = Event()
        event.connect(listener)
        event.fire()
        self.assertTrue(listener.called)

    def test_a_listener_is_passed_right_parameters(self):
        listener = mock.Mock()
        event = Event()
        event.connect(listener)
        event.fire(5, shape="square")
        listener.assert_has_calls([mock.call(5, shape="square")])
