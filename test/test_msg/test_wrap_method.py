from unittest import TestCase

from .wrap_cases import WrapCases

from log_decor.msg import wrap_method


class LoggerMock:
    kwargs: dict
    def log(self, level: int, msg: str):
        self.kwargs = dict(level=level, msg=msg)


class A:
    logger = LoggerMock()
    def func(self, *args, **kwargs):
        return args, kwargs
    

class WrapMethodTests(TestCase, WrapCases):

    def setUp(self) -> None:
        self._func = A.func
        self._self = A()

    def execute_test(self,
                     msg: str,
                     level: int,
                     args: tuple,
                     kwargs: dict,
                     logged_msg: str):
        func = wrap_method(msg, level, self._func)
        result = func(self._self, *args, **kwargs)
        self.assertEqual(result, (args, kwargs))
        self.assertEqual(
            self._self.logger.kwargs,
            dict(level=level, msg=logged_msg)
        )
