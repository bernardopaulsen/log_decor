log-decor
=========

Introduction
############

This package has class and method decorators that provide logging functionality.

Example
#######

.. code-block:: python

   import logging

   from log_decor import AddLogger, LogMsg

   @AddLogger()
   class Example:

       @LogMsg('message',
               level=logging.DEBUG)
       def f1(self):
           pass

       @LogMethod(level=logging.INFO)
       def f2(self):
           pass

       @LogInfo(level=logging.WARNING)
       def f3(self,
              *args,
              **kwargs):
           pass


>>> logging.basicConfig(level=logging.DEBUG)
>>> example = Example()
>>> example.f1()
ERROR:Example:message
>>> example.f2()
INFO:Example:f2()
>>> example.f3('a', x=1)
WARNING:Example:f3(a, x=1) [1.1e-06s] -> None
