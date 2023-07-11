"""Provide standard type annotations."""
import logging
import typing as tp


UserClass = tp.TypeVar('UserClass')

ClassDecorator = tp.Callable[[UserClass], tp.Type[UserClass]]


class ClassWithLogger(UserClass):
    """Type annotation of a class with logger attribute."""
    logger: logging.Logger


Param = tp.ParamSpec("Param")
RetType = tp.TypeVar("RetType")

Function = tp.Callable[Param, RetType]
Method = tp.Callable[tp.Concatenate[tp.Type[ClassWithLogger], Param], RetType]

Callable = Function | Method
Decorator = tp.Callable[[Callable], Callable]

FormatFunc = tp.Callable[..., str]
