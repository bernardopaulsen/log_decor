Examples
========

.. code-block:: python

   import logging

   from log_decor import AddLogger, LogMsg


   logging.basicConfig(level=logging.WARNING)


   @AddLogger()
   class Example:

       @LogMsg(msg='message',
               level=logging.ERROR)


>>> example = Example()
>>> example.func()
ERROR:Example:message
