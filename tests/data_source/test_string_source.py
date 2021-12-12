import io
import unittest

from src.data_sources.string_source import StringSource
from src.utils.position import Position


class TestStringSource(unittest.TestCase):


    def test_advance_position(self):

        line_of_code = "a = 10"

        string_source = StringSource(
            io.StringIO(line_of_code)
        )

        self.assertEqual(string_source.character, "a")
        self.assertEqual(string_source.position, Position(1, 1))

        string_source.read_char()
        string_source.read_char()

        self.assertEqual(string_source.character, "=")
        self.assertEqual(string_source.position, Position(1, 3))