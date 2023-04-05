from unittest import TestCase
from unittest.mock import Mock, patch

from .wrap_cases import WrapCases

from log_decor.msg import wrap_function


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
                     logged_msg: str):
        with patch('logging.log', self._logging_mock):
            func = wrap_function(msg, level, self._func)
            result = func(*args, **kwargs)
        self.assertEqual(result, (args, kwargs))
        self._logging_mock.assert_called_once_with(
            level=level,
            msg=logged_msg)
