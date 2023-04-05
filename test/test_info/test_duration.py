from unittest import TestCase
from unittest.mock import Mock, patch

from log_decor.info import duration


class DurationTests(TestCase):

    def setUp(self) -> None:
        def f(*args, **kwargs):
            return (args, kwargs)
        self._f = f
        self._perf_counter_mock = Mock(side_effect=[0.0, 1.0])

    def test_null_args(self):
        with patch('time.perf_counter', self._perf_counter_mock):
            exec_time, result = duration(self._f)
        self.assertEqual(exec_time, 1.0)
        self.assertEqual(result, (tuple(), dict()))

    def test_with_args(self):
        with patch('time.perf_counter', self._perf_counter_mock):
            exec_time, result = duration(self._f, 1, 2, 3, a=4, b=5, c=6)
        self.assertEqual(exec_time, 1.0)
        self.assertEqual(result, ((1, 2, 3), dict(a=4, b=5, c=6)))
