import functools
import logging
import sys
import typing as tp

if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec


class Class:
    logger: logging.Logger


Param = ParamSpec("Param")
RetType = tp.TypeVar("RetType")
Method = tp.Callable[tp.Concatenate[tp.Type[Class], Param], RetType]


class LogMsg:
    """Method decorator that logs a custom message.

    :param msg: Message that will be logged.
    :param level: Logging level of message.
    """
    def __init__(self,
                 msg: str,
                 level: int = logging.DEBUG,
                 ) -> None:
        self._msg = msg
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
                                 msg=self._msg)
            except AttributeError as err:
                raise RuntimeError(
                    'Remember to decorate the class with log_decor.AddLogger'
                ) from err
            return func(self_, *args, **kwargs)
        return wrapper
