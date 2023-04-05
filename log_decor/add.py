import functools
import logging
import typing as tp


__all__ = ['add_logger']


Class = tp.TypeVar('Class')

Decorator = tp.Callable[[Class], tp.Type[Class]]


def add_logger(name: str | None = None
               ) -> Decorator:
    """Add logger to class.
    
    The logger will be saved in an attribute named 'logger'.

    :param name: Name of logger. If not given, the name of the class is used.
    """
    def decorator(cls: Class) -> tp.Type[Class]:
        @functools.wraps(cls, updated=())
        class Wrapper(cls):
            def __init__(self: tp.Type[Class],
                         *args, **kwargs) -> None:
                self.logger = logging.getLogger(
                    name if name is not None else cls.__name__
                )
                super().__init__(*args, **kwargs)
        return Wrapper
    return decorator
