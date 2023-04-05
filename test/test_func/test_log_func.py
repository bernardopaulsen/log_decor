from abc import abstractmethod
from unittest import TestCase
from unittest.mock import Mock, patch

from log_decor.func import log_func

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


def none_func(*args, **kwargs):
    return str()


def arg_func(*args, **kwargs):
    return str(args[0]) + ' ' + str(list(kwargs.values()))


def res_func(result):
    args, kwargs = result
    return str(args[0]) + ' ' + str(list(kwargs.values()))


class LogMsgCases(WrapCases):

    def test_null(self):
        self.execute_test(msg=None,
                          level=10,
                          args=(1, 2),
                          kwargs=dict(b=3, c=4),
                          arg_func=None,
                          res_func=None,
                          logged_msg='func() -> '
                          )

class LogMsgFunctionTests(TestCase, LogMsgCases):

    def setUp(self) -> None:
        self._func = func
        self._logging_mock = Mock()

    def execute_test(self,
                     msg: str,
                     level: int,
                     arg_func,
                     res_func,
                     args: tuple,
                     kwargs: dict,
                     logged_msg: str):
        with patch('logging.log', self._logging_mock):
            func = log_func(
                msg=msg, level=level,
                arg_func=arg_func, res_func=res_func
            )(self._func)
            result = func(*args, **kwargs)
        self.assertEqual(result, (args, kwargs))
        self._logging_mock.assert_called_once_with(
            level=level,
            msg=logged_msg)
        

class LogMsgMethodTests(TestCase, LogMsgCases):

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
        func = log_func(
            msg=msg, level=level,
            arg_func=arg_func, res_func=res_func
        )(self._func)
        result = func(self._self, *args, **kwargs)
        self.assertEqual(result, (args, kwargs))
        self.assertEqual(
            self._self.logger.kwargs,
            dict(level=level, msg=logged_msg)
        )
