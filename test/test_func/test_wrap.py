from abc import abstractmethod
from unittest import TestCase
from unittest.mock import Mock, patch

from log_decor.func import wrap_function, wrap_method

from .wrap_cases import WrapCases


class LoggerMock:
    kwargs: dict
    def log(self, level: int, msg: str):
        self.kwargs = dict(level=level, msg=msg)


class A:
    logger = LoggerMock()
    def func(self, *args, **kwargs):
        return args, kwargs


def func(*args, **kwargs):
    return args, kwargs


class WrapFunctionTests(TestCase, WrapCases):

    def setUp(self) -> None:
        self._func = func
        self._logging_mock = Mock()

    def execute_test(self,
                     msg: str,
                     level: int,
                     args: tuple,
                     kwargs: dict,
                     arg_func,
                     res_func,
                     logged_msg: str):
        with patch('logging.log', self._logging_mock):
            func = wrap_function(msg, level, arg_func, res_func, self._func)
            result = func(*args, **kwargs)
        self.assertEqual(result, (args, kwargs))
        self._logging_mock.assert_called_once_with(
            level=level,
            msg=logged_msg
        )


class WrapMethodTests(TestCase, WrapCases):

    def setUp(self) -> None:
        self._func = A.func
        self._self = A()

    def execute_test(self,
                     msg: str,
                     level: int,
                     arg_func,
                     res_func,
                     args: tuple,
                     kwargs: dict,
                     logged_msg: str):
        func = wrap_method(msg, level, arg_func, res_func, self._func)
        result = func(self._self, *args, **kwargs)
        self.assertEqual(result, (args, kwargs))
        self.assertEqual(
            self._self.logger.kwargs,
            dict(level=level, msg=logged_msg)
        )