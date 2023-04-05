from unittest import TestCase
from unittest.mock import Mock, patch

from .log_info_cases import LogInfoCases

from log_decor.info import wrap_function


def func(*args, **kwargs):
    return args, kwargs


def duration(func, *args, **kwargs):
    return 0.0, func(*args, **kwargs)


class WrapFunctionTests(TestCase, LogInfoCases):

    def setUp(self) -> None:
        self._func = func
        self._duration_moch = Mock(side_effect=duration)
        self._logging_mock = Mock()

    def execute_test(self,
                     level: int,
                     args: tuple,
                     kwargs: dict,
                     msg: str):
        with patch('log_decor.info.duration', self._duration_moch):
            with patch('logging.log', self._logging_mock):
                func = wrap_function(level, self._func)
                result = func(*args, **kwargs)
        self.assertEqual(result, (args, kwargs))
        self._logging_mock.assert_called_once_with(
            level=level,
            msg=msg)
