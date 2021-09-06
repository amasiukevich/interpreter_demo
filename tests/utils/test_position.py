from src.utils.position import Position
from src.exceptions.position_exception import PositionException

import unittest

class TestPosition(unittest.TestCase):

    def test_position_creation(self):

        pos = Position(line=12, column=32)
        pos_default = Position()

        self.assertEqual(pos.line, 12)
        self.assertEqual(pos.column, 32)

        self.assertEqual(pos_default.line, 1)
        self.assertEqual(pos_default.column, 0)

    def test_invalid_line(self):

        with self.assertRaises(PositionException) as context:
            Position(line=0, column=0)

        exception = context.exception

        self.assertEqual(
            exception.message,
            "Line cannot be less than 1"
        )


    def test_invalid_column(self):

        with self.assertRaises(PositionException) as context:
            Position(line=1, column=-2)

        exception = context.exception

        self.assertEqual(
            exception.message,
            "Column cannot be less than 0"
        )


    def test_advance_column(self):

        pos = Position()
        pos.advance_column()

        self.assertEqual(pos.column, 1)
        self.assertEqual(pos.line, 1)

    def test_advance_line(self):

        pos = Position(13, 142)
        pos.advance_line()

        self.assertEqual(pos.line, 14)
        self.assertEqual(pos.column, 0)

    def test_equality(self):

        pos1 = Position()
        pos2 = Position(line=2, column=17)

        pos1.advance_line()
        for i in range(17):
            pos1.advance_column()

        self.assertEqual(pos1, pos2)

        pos2.advance_column()
        self.assertNotEqual(pos1, pos2)


    def test_invalid_comparison(self):

        obj1 = Position()
        obj2 = (1, 0)

        with self.assertRaises(PositionException) as context:
            result = (obj1 == obj2)

        exception = context.exception

        self.assertEqual(
            exception.message,
            "Cannot compare Position and tuple"
        )