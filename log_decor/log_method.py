import functools
import logging
import sys
import typing as tp

if sys.version_info < (3, 10):
    from typing_extensions import Concatenate, ParamSpec
else:
    from typing import Concatenate, ParamSpec


class Class:
    logger: logging.Logger


Param = ParamSpec("Param")
RetType = tp.TypeVar("RetType")
Method = tp.Callable[Concatenate[tp.Type[Class], Param], RetType]


class LogMethod:
    """Method decorator that logs the name of the method.

    :param level: Logging level of message.
    """
    def __init__(self,
                 level: int = logging.DEBUG,
                 ) -> None:
        self._level = level

    def __call__(self,
                 func: Method
                 ) -> Method:
        """Decorate method.

        :param func: Method.
        """
        @functools.wraps(func)
        def wrapper(self_: tp.Type[Class],
                    *args,
                    **kwargs):
            try:
                self_.logger.log(level=self._level,
                             msg=func.__name__ + '()')
            except AttributeError as err:
                raise RuntimeError(
                    'Remember to decorate the class with log_decor.AddLogger'
                ) from err
            return func(self_, *args, **kwargs)
        return wrapper
