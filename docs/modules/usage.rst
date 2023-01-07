Usage
=====

Add logger to class
-------------------

.. code-block:: python

   from log_decor import AddLogger


   @AddLogger()
   class Example:
       pass

Add logging functionality to method
-----------------------------------

.. code-block:: python

   from log_decor import AddLogger, LogInfo


   @AddLogger()
   class Example:

       @LogInfo()
       def f(self):
           pass

Define logging configuration
----------------------------

.. code-block:: python

   import logging


   logging.basicConfig(filename='example.log',
                       level=logging.WARNING)
