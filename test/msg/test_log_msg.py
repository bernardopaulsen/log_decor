from unittest import TestCase
from unittest.mock import Mock, patch

from .wrap_cases import WrapCases

from log_decor.msg import log_msg


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


class LogMsgCases(WrapCases):

    def test_10_null(self):
        self.execute_test(msg=None,
                          level=10,
                          args=tuple(),
                          kwargs=dict(),
                          logged_msg='func()')
        
    def test_20_null(self):
        self.execute_test(msg=None,
                          level=20,
                          args=tuple(),
                          kwargs=dict(),
                          logged_msg='func()')


class LogMsgFunctionTests(TestCase, LogMsgCases):

    def setUp(self) -> None:
        self._func = func
        self._logging_mock = Mock()

    def execute_test(self,
                     msg: str,
                     level: int,
                     args: tuple,
                     kwargs: dict,
                     logged_msg: str):
        with patch('logging.log', self._logging_mock):
            func = log_msg(msg, level)(self._func)
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
                     args: tuple,
                     kwargs: dict,
                     logged_msg: str):
        func = log_msg(msg, level)(self._func)
        result = func(self._self, *args, **kwargs)
        self.assertEqual(result, (args, kwargs))
        self.assertEqual(
            self._self.logger.kwargs,
            dict(level=level, msg=logged_msg)
        )
