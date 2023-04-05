import functools
import logging
import typing as tp


__all__ = ['log_msg']


class Class:
    logger: logging.Logger


Param = tp.ParamSpec("Param")
RetType = tp.TypeVar("RetType")

Function = tp.Callable[Param, RetType]
Method = tp.Callable[tp.Concatenate[tp.Type[Class], Param], RetType]

Callable = Function | Method
Decorator = tp.Callable[[Callable], Callable]


def wrap_function(msg: str,
                  log_level: int,
                  func: Function) -> Function:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> RetType:
        logging.log(level=log_level,
                    msg=msg)
        return func(*args, **kwargs)
    return wrapper


def wrap_method(msg: str,
                log_level: int,
                func: Method) -> Method:
    @functools.wraps(func)
    def wrapper(self: Class,
                *args, **kwargs) -> RetType:
        self.logger.log(level=log_level,
                        msg=msg)
        return func(self, *args, **kwargs)
    return wrapper


def log_msg(msg: str | None = None,
            level: int | None = logging.DEBUG,
            ) -> Decorator:
    def decorator(func: Callable) -> Callable:
        nonlocal msg
        msg = f'{func.__name__}()' if msg is None else msg
        if '.' in func.__qualname__:
            return wrap_method(msg, level, func)
        return wrap_function(msg, level, func)
    return decorator
