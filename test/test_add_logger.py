import logging
import unittest

from log_decor import add_logger


class AddLoggerTests(unittest.TestCase):

    def test_logger(self):

        @add_logger()
        class A:
            def __init__(self):
                pass

        a = A()

        self.assertIsInstance(a.logger, logging.Logger)

    def test_name(self):

        @add_logger('some-name')
        class A:
            def __init__(self):
                pass

        a = A()

        self.assertEqual(a.logger.name, 'some-name')

    def test_name_null(self):

        @add_logger()
        class A:
            def __init__(self):
                pass

        a = A()

        self.assertEqual(a.logger.name, 'A')
