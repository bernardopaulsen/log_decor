import functools
import inspect
import logging
import typing as tp


__all__ = ['log_method']


class Class:
    logger: logging.Logger


Param = tp.ParamSpec("Param")
RetType = tp.TypeVar("RetType")

Function = tp.Callable[Param, RetType]
Method = tp.Callable[tp.Concatenate[tp.Type[Class], Param], RetType]

Callable = Function | Method
Decorator = tp.Callable[[Callable], Callable]


def wrap_function(log_level: int,
                  func: Function) -> Function:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> RetType:
        logging.log(level=log_level,
                    msg=f'{func.__name__}(...) -> ...')
        return func(*args, **kwargs)
    return wrapper


def wrap_method(log_level: int,
                func: Method) -> Method:
    @functools.wraps(func)
    def wrapper(self: Class,
                *args, **kwargs) -> RetType:
        self.logger.log(level=log_level,
                        msg=f'{func.__name__}(...) -> ...')
        return func(self, *args, **kwargs)
    return wrapper


def log_method(level: int | None = logging.DEBUG
               ) -> Decorator:
    def decorator(func: Callable) -> Callable:
        if inspect.isfunction(func):
            return wrap_function(level, func)
        return wrap_method(level, func)
    return decorator
