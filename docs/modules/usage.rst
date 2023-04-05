Usage
=====


Add logging functionality to function
-------------------------------------

.. code-block:: python

    from log_decor import log_info


    # logs at DEBUG level
    @log_info()
    def f():
        pass
        

Add logger to class
-------------------

.. code-block:: python

    from log_decor import add_logger


    # logger with name 'Exaxmple'
    @add_logger()
    class Example:
        pass

    # logger with name 'LoggerName'
    @add_logger('LoggerName')
    class Example:
        pass


Add logging functionality to method
-----------------------------------

.. code-block:: python

    from log_decor import add_logger, log_info


    # logger with name 'Example'
    @add_logger()
    class Example:

        # logs at DEBUG level
        @log_info()
        def f(self):
            pass


Define logging configuration
----------------------------

.. code-block:: python

   import logging


   logging.basicConfig(filename='example.log',
                       level=logging.WARNING)
