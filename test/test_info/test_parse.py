from unittest import TestCase

from log_decor.info import parse


class ParseTests(TestCase):

    def test_null(self):
        result = parse()
        self.assertEqual(result, '')

    def test_args(self):
        result = parse(1, 2, 3)
        self.assertEqual(result, '1, 2, 3')

    def test_kwargs(self):
        result = parse(a=4, b=5, c=6)
        self.assertEqual(result, 'a=4, b=5, c=6')

    def test_args_kwargs(self):
        result = parse(1, 2, 3, a=4, b=5, c=6)
        self.assertEqual(result, '1, 2, 3, a=4, b=5, c=6')
