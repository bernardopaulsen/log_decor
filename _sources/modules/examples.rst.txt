Examples
========

log_msg
-------

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


>>> logging.basicConfig(level=logging.DEBUG)
>>> example = Example()
>>> example.f1()
DEBUG:Example:message
>>> example.f2()
INFO:Example:f2()


log_info
--------

.. code-block:: python

    import logging

    from log_decor import log_info


    @log_info(level=logging.WARNING)
    def f1(a: int, b: int, c: int):
        return a + b + c


>>> logging.basicConfig(level=logging.DEBUG)
>>> f1(1, 2, c=3)
WARNING:root:f1(1, 2, c=3) [0.0001s] -> 6


log_func
--------

.. code-block:: python

    import logging

    from log_decor import log_func


    def arg_func(*args, **kwargs):
        return 'args and kwargs'

    
    def res_func(result):
        return 'result'


    @log_func(arg_func=arg_func, res_func=res_func)
    def f1(a: int, b: int, c: int):
        return a + b + c


    @log_func('message', logging.WARNING, arg_func=arg_func, res_func=res_func)
    def f2(a: int, b: int, c: int):
        return a + b + c


>>> logging.basicConfig(level=logging.DEBUG)
>>> f1(1, 2, c=3)
DEBUG:root:f1(args and kwargs) -> result
>>> f2(1, 2, c=3)
WARNING:root:message(args and kwargs) -> result