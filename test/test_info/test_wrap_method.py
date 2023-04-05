from unittest import TestCase
from unittest.mock import Mock, patch

from .log_info_cases import LogInfoCases

from log_decor.info import wrap_method


class LoggerMock:
    kwargs: dict
    def log(self, level: int, msg: str):
        self.kwargs = dict(level=level, msg=msg)


class A:
    logger = LoggerMock()
    def func(self, *args, **kwargs):
        return args, kwargs
    

def duration(func, *args, **kwargs):
    return 0.0, func(*args, **kwargs)


class WrapMethodTests(TestCase, LogInfoCases):

    def setUp(self) -> None:
        self._func = A.func
        self._self = A()
        self._duration_mock = Mock(side_effect=duration)

    def execute_test(self,
                     level: int,
                     args: tuple,
                     kwargs: dict,
                     msg: str):
        with patch('log_decor.info.duration', self._duration_mock):
            func = wrap_method(level, self._func)
            result = func(self._self, *args, **kwargs)
        self.assertEqual(result, (args, kwargs))
        self.assertEqual(
            self._self.logger.kwargs,
            dict(level=level, msg=msg)
        )
