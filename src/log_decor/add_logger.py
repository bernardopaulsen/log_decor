import functools
import logging
from typing import Optional, Type, TypeVar


Class = TypeVar('Class')


class AddLogger:
    """Class decorator that adds a logger attribute to the decorated class.

    :param name: Name of Logger. If None, the qualified name of the class
        passed to :meth:`add_logger.AddLogger.__call__` will be the name of
        the logger.
    """
    def __init__(self,
                 name: Optional[str] = None
                 ) -> None:
        self._name = name

    def __call__(self,
                 cls: Class
                 ) -> Type[Class]:
        """Add logger attribute to class.

        The name of the attribute will be '_logger'.

        :param cls: Class to which add logger. If no name was passed to
            :meth:`add_logger.AddLogger.__init__`, the qualified name of the
            class passed to this parameter will be the name of the logger.
        :return: Class with logger attribute.
        """
        @functools.wraps(cls,
                         updated=())
        class LoggedClass(cls):
            def __init__(self_,
                         *args,
                         **kwargs
                         ) -> None:
                self_.logger = logging.getLogger(
                    name=self._name if self._name is not None else cls.__name__
                )
                super().__init__(*args,
                                 **kwargs)
        return LoggedClass
