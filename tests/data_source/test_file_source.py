from src.data_sources.file_source import FileSource
from src.utils.position import Position

import os
import io

import unittest

from time import sleep

class TestFileSource(unittest.TestCase):

    def test_advance_position(self):

        with io.open(os.path.abspath("../../grammar_stuff/test_codes/test1.txt")) as file_stream:

            file_source = FileSource(file_stream)

            while file_source.character != -1:
                file_source.read_char()

            pos1 = file_source.position
            pos2 = Position(3, 5)


        self.assertEqual(pos1, pos2)


    def test_text(self):

        with io.open(os.path.abspath("../../grammar_stuff/test_codes/test_arithmetic.txt")) as file_stream:

            file_source = FileSource(file_stream)

            chars = []
            while file_source.character != -1:
                chars.append(file_source.character)
                file_source.read_char()

        real_chars = [c for c in "define main() {\n    discount_perc = 10;\n    init_price = 100;\n    price_after_discount = init_price * (100 - discount_perc) / 100;\n}"]
        self.assertListEqual(chars, real_chars)