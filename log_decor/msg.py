"""Logging decorator that logs a fixed message."""
import functools
import logging

from .type_annotation import (
    Callable,
    ClassWithLogger,
    Decorator,
    Function,
    Method,
    RetType,
)


__all__ = ["log_msg"]


def _wrap_function(msg: str, log_level: int, func: Function) -> Function:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> RetType:
        logging.log(level=log_level, msg=msg)
        return func(*args, **kwargs)

    return wrapper


def _wrap_method(msg: str, log_level: int, func: Method) -> Method:
    @functools.wraps(func)
    def wrapper(self: ClassWithLogger, *args, **kwargs) -> RetType:
        self.logger.log(level=log_level, msg=msg)
        return func(self, *args, **kwargs)

    return wrapper


def log_msg(
    msg: str | None = None,
    level: int | None = logging.DEBUG,
) -> Decorator:
    """Add logging functionality to function|method.

    Logs given message. The format of the log message is:

    .. code-block::

        given_message

    :param msg: Message to log. Default is 'function_name()'.
    :param level: Log level. Default is DEBUG.
    """

    def decorator(func: Callable) -> Callable:
        nonlocal msg
        msg = f"{func.__name__}()" if msg is None else msg
        if "." in func.__qualname__:
            return _wrap_method(msg, level, func)
        return _wrap_function(msg, level, func)

    return decorator
