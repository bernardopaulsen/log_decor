"""Provide decorator that adds logger attribute to class."""
import functools
import logging

from .type_annotation import (
    ClassDecorator,
    ClassWithLogger,
    UserClass
)


__all__ = ['add_logger']


def add_logger(name: str | None = None
               ) -> ClassDecorator:
    """Add logger to class.
    
    The logger will be saved in an attribute named 'logger'.

    :param name: Name of logger. If not given, the name of the class is used.
    """
    def decorator(cls: UserClass) -> ClassWithLogger:
        @functools.wraps(cls, updated=())
        class Wrapper(cls):
            """Add logger attribute when initiating class instance."""
            def __init__(self: ClassWithLogger,
                         *args, **kwargs) -> None:
                self.logger = logging.getLogger(
                    name if name is not None else cls.__name__
                )
                super().__init__(*args, **kwargs)
        return Wrapper
    return decorator
