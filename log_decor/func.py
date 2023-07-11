"""Logging decorator that creates a log message by parsing the arguments and the result
with an user-defined function.
"""
import functools
import logging
import typing as tp

from .type_annotation import (
    Callable,
    ClassWithLogger,
    Decorator,
    Function,
    Method,
    RetType,
)


__all__ = ["log_func"]


FormatFunc = tp.Callable[..., str]


def _wrap_function(
    msg: str, log_level: int, arg_func: FormatFunc, res_func: FormatFunc, func: Function
) -> Function:
    """Add logging functionality to method."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> RetType:
        result = func(*args, **kwargs)
        logging.log(
            level=log_level,
            msg=f"{msg}({arg_func(*args, **kwargs)}) -> {res_func(result)}",
        )
        return result

    return wrapper


def _wrap_method(
    msg: str, log_level: int, arg_func: FormatFunc, res_func: FormatFunc, func: Method
) -> Method:
    """Add logging functionality to method."""

    @functools.wraps(func)
    def wrapper(self: ClassWithLogger, *args, **kwargs) -> RetType:
        result = func(self, *args, **kwargs)
        self.logger.log(
            level=log_level,
            msg=f"{msg}({arg_func(*args, **kwargs)}) -> {res_func(result)}",
        )
        return result

    return wrapper


def log_func(
    msg: str | None = None,
    level: int | None = logging.DEBUG,
    arg_func: FormatFunc | None = None,
    res_func: FormatFunc | None = None,
) -> Decorator:
    """Add logging functionality to function|method.

    Applies a function (arg_func) to the args|kwargs and other function
    (res_func) to the result before logging. The format of the message is:

    .. code-block::

        message(arg_func_result) -> res_func_result

    :param msg: Start of log message. If not given, the name of the
        function|method is used.
    :param level: Log level. Default is DEBUG.
    :param arg_func: Function to apply to args|kwargs. If not given, a function
        that returns an empty string is used.
    :param res_func: Function to apply to result. If not given, a function that
        returns an empty string is used.
    """
    arg_func = str if arg_func is None else arg_func
    res_func = str if res_func is None else res_func

    def decorator(func: Callable) -> Callable:
        nonlocal msg
        msg = func.__name__ if msg is None else msg
        if "." in func.__qualname__:
            return _wrap_method(msg, level, arg_func, res_func, func)
        return _wrap_function(msg, level, arg_func, res_func, func)

    return decorator
