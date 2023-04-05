import logging
import unittest

from log_decor import add_logger


class AddLoggerTests(unittest.TestCase):

    def setUp(self) -> None:

        class A:
            pass

        self._class_a = A

    def test_logger(self):

        a = add_logger()(self._class_a)()
        self.assertIsInstance(a.logger, logging.Logger)

    def test_name(self):

        a = add_logger('some-name')(self._class_a)()
        self.assertEqual(a.logger.name, 'some-name')

    def test_name_null(self):

        a = add_logger()(self._class_a)()
        self.assertEqual(a.logger.name, 'A')
