import functools
import logging
import time
import typing as tp


class Class:
    logger: logging.Logger


Param = tp.ParamSpec("Param")
RetType = tp.TypeVar("RetType")
Method = tp.Callable[tp.Concatenate[tp.Type[Class], Param], RetType]


def get_duration(func: Method,
                 self_: tp.Type[Class],
                 *args,
                 **kwargs
                 ) -> tuple[float, RetType]:
    """Execute a method and return a tuple with the time duration of execution
    and return value.

    :param func: Method.
    :param self_: 'self' argument of method.
    :return: Readable string.
    """
    start_time = time.perf_counter()
    result = func(self_, *args, **kwargs)
    end_time = time.perf_counter()
    return end_time - start_time, result


def parse_args(args: tuple
               ) -> str:
    """Create a readable representation of a tuple by creating a string where
    elements are separated by a comma.

    :param args: Tuple.
    :return: Readable string.
    """
    return ', '.join(str(a) for a in args)


def parse_kwargs(kwargs: dict
                  ) -> str:
    """Create a readable representation of a dictionary where elements are
    represented as 'parameter=value' and separated by a comma.

     :param kwargs: Dictionary.
     :return: Readable string.
    """
    return ', '.join(f'{str(k)}={str(v)}' for k, v in kwargs.items())


class LogInfo:
    """Method decorator that logs the name, arguments, time duration of
    execution and result of a method.

    :param level: Logging level of message.
    """
    def __init__(self,
                 level: int = logging.DEBUG
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
            duration, result = get_duration(func, self_, *args, **kwargs)
            msg = (func.__name__ +
                   f'({parse_args(args)}, {parse_kwargs(kwargs)})' +
                   f' [{duration}s] -> {result}')
            try:
                self_.logger.log(level=self._level,
                                 msg=msg)
            except AttributeError as err:
                raise RuntimeError(
                    'Remember to decorate the class with log_decor.AddLogger'
                ) from err
            return result
        return wrapper
