log-decor
=========

Introduction
############

This package contains decorators that provide logging functionality for functions
and methods.

Example
#######

.. code-block:: python

    import logging

    from log_decor import add_logger, log_msg


    @add_logger()
    class Example:

        @log_msg('message', level=logging.DEBUG)
        def f1(self):
            pass

        @log_msg(level=logging.INFO)
        def f2(self):
            pass
