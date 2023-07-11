"""Logging decorator that creates a message containing arguments, result and execution
time.
"""
import functools
import logging
import time

from .type_annotation import (
    Callable,
    ClassWithLogger,
    Decorator,
    Function,
    Method,
    RetType,
)


__all__ = ["log_info"]


def _duration(func: Callable, *args, **kwargs) -> tuple[float, RetType]:
    """Execute callable with given arguments and return a tuple containing:

    0. duration of execution,
    1. callable's return.
    """
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    return end_time - start_time, result


def _parse(*args, **kwargs) -> str:
    """Parse arguments into a easy-to-read string."""

    def dict_item_to_str(item: tuple) -> str:
        key, value = item
        return f"{str(key)}={str(value)}"

    args_ = map(str, args)
    kwargs_ = map(dict_item_to_str, kwargs.items())
    return ", ".join(list(args_) + list(kwargs_))


def _wrap_function(log_level: int, func: Function) -> Function:
    """Add (information) logging functionality to function."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> RetType:
        exec_time, result = _duration(func, *args, **kwargs)
        logging.log(
            level=log_level,
            msg=f"{func.__name__}({_parse(*args, **kwargs)}) [{exec_time}s] -> {result}",
        )
        return result

    return wrapper


def _wrap_method(log_level: int, func: Method) -> Method:
    """Add (information) logging functionality to method."""

    @functools.wraps(func)
    def wrapper(self: ClassWithLogger, *args, **kwargs) -> RetType:
        exec_time, result = _duration(func, self, *args, **kwargs)
        self.logger.log(
            level=log_level,
            msg=f"{func.__name__}({_parse(*args, **kwargs)}) [{exec_time}s] -> {result}",
        )
        return result

    return wrapper


def log_info(level: int | None = logging.DEBUG) -> Decorator:
    """Add logging functionality to function|method.

    Logs the args|kwargs, time duration of execution, and result. The format of
    the message is:

    .. code-block::

        function_name(args|kwargs) [0-9*.0-9*s] -> result

    :param level: Log level. Default is DEBUG.
    """

    def decorator(func: Callable) -> Callable:
        if "." in func.__qualname__:
            return _wrap_method(level, func)
        return _wrap_function(level, func)

    return decorator
