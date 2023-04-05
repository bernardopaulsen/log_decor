import functools
import logging
import time
import typing as tp


__all__ = ['log_info']


class Class:
    logger: logging.Logger


Param = tp.ParamSpec("Param")
RetType = tp.TypeVar("RetType")

Function = tp.Callable[Param, RetType]
Method = tp.Callable[tp.Concatenate[tp.Type[Class], Param], RetType]

Callable = Function | Method
Decorator = tp.Callable[[Callable], Callable]


def duration(func: Callable,
             *args, **kwargs
             ) -> tuple[float, RetType]:
    """Execute callable with given arguments and return a tuple containing:
    
    0. duration of execution, 
    1. callable's return.
    """
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    return end_time - start_time, result


def parse(*args, **kwargs) -> str:
    """Parse arguments into a easy-to-read string."""
    def dict_item_to_str(item: tuple) -> str:
        key, value = item
        return f'{str(key)}={str(value)}'
    a = map(str, args)
    ka = map(dict_item_to_str, kwargs.items())
    return ', '.join(list(a) + list(ka))


def wrap_function(log_level: int,
                  func: Function
                  ) -> Function:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> RetType:
        exec_time, result = duration(func, *args, **kwargs)
        logging.log(level=log_level,
                    msg=f'{func.__name__}({parse(*args, **kwargs)}) [{exec_time}s] -> {result}')
        return result
    return wrapper



def wrap_method(log_level: int,
                func: Method
                ) -> Method:
    @functools.wraps(func)
    def wrapper(self: Class,
                *args, **kwargs) -> RetType:
        exec_time, result = duration(func, self, *args, **kwargs)
        self.logger.log(level=log_level,
                        msg=f'{func.__name__}({parse(*args, **kwargs)}) [{exec_time}s] -> {result}')
        return result
    return wrapper


def log_info(level: int | None = logging.DEBUG
             ) -> Decorator:
    """Add logging functionality to function|method.
    
    Logs the args|kwargs, time duration of execution, and result. The format of
    the message is:

    .. code-block::
        
        function_name(args|kwargs) [0-9*.0-9*s] -> result

    :param level: Log level. Default is DEBUG.
    """
    def decorator(func: Callable) -> Callable:
        if '.' in func.__qualname__:
            return wrap_method(level, func)
        return wrap_function(level, func)
    return decorator
