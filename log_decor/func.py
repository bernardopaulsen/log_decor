import functools
import logging
import typing as tp


__all__ = ['log_func']


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
                  arg_func: tp.Callable,
                  res_func: tp.Callable,
                  func: Function) -> Function:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> RetType:
        result = func(*args, **kwargs)
        logging.log(
            level=log_level,
            msg=f'{msg}({arg_func(*args, **kwargs)}) -> {res_func(result)}'
        )
        return result
    return wrapper


def wrap_method(msg: str,
                log_level: int,
                arg_func: tp.Callable,
                res_func: tp.Callable,
                func: Method) -> Method:
    @functools.wraps(func)
    def wrapper(self: Class,
                *args, **kwargs) -> RetType:
        result = func(self, *args, **kwargs)
        self.logger.log(
            level=log_level,
            msg=f'{msg}({arg_func(*args, **kwargs)}) -> {res_func(result)}'
        )
        return result
    return wrapper


def none_func(*args, **kwargs):
    return str()


def log_func(msg: str | None = None,
             level: int | None = logging.DEBUG,
             arg_func: tp.Callable | None = None,
             res_func: tp.Callable | None = None,
             ) -> Decorator:
    arg_func = none_func if arg_func is None else arg_func
    res_func = none_func if res_func is None else res_func
    def decorator(func: Callable) -> Callable:
        nonlocal msg
        msg = func.__name__ if msg is None else msg
        if '.' in func.__qualname__:
            return wrap_method(msg, level, arg_func, res_func, func)
        return wrap_function(msg, level, arg_func, res_func, func)
    return decorator
