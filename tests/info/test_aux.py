from unittest import TestCase
from unittest.mock import Mock, patch

from log_decor.info import duration, parse


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


class ParseTests(TestCase):

    def test_null(self):
        result = parse()
        self.assertEqual(result, '')

    def test_args(self):
        result = parse(1, 2, 3)
        self.assertEqual(result, '1, 2, 3')

    def test_kwargs(self):
        result = parse(a=4, b=5, c=6)
        self.assertEqual(result, 'a=4, b=5, c=6')

    def test_args_kwargs(self):
        result = parse(1, 2, 3, a=4, b=5, c=6)
        self.assertEqual(result, '1, 2, 3, a=4, b=5, c=6')
