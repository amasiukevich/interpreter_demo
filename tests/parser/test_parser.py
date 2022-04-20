import io
import unittest

from src.data_sources import StringSource
from src.parser import Parser
from src.scanner import Scanner
from src.utils.program3.block import Block
from src.utils.program3.classes._class import Class
from src.utils.program3.expressions.math.add_expression import AddExpression
from src.utils.program3.expressions.math.and_expression import AndExpression
from src.utils.program3.expressions.math.equality_expression import EqualityExpression
from src.utils.program3.expressions.math.multiply_expression import MultiplyExpression
from src.utils.program3.expressions.math.or_expression import OrExpression
from src.utils.program3.expressions.math.relation_expression import RelationExpression
from src.utils.program3.expressions.math.unary_expression import UnaryExpression
from src.utils.program3.functions.function import Function
from src.utils.program3.program import Program

from src.utils.program3.statements._return import Return
from src.utils.program3.statements.assign import Assign
from src.utils.program3.statements.comment import Comment
from src.utils.program3.statements.foreach_loop import ForeachLoop
from src.utils.program3.statements.func_call import FunctionCall
from src.utils.program3.statements.while_loop import WhileLoop
from src.utils.program3.values.complex_getter import ComplexGetter
from src.utils.program3.statements.conditional import Conditional
from src.utils.program3.values.iterative_getter import CallGetter
from src.utils.program3.values.literals.bool_literal import BoolLiteral
from src.utils.program3.values.literals.float_literal import FloatLiteral
from src.utils.program3.values.literals.int_literal import IntLiteral
from src.utils.program3.values.literals.string_literal import StringLiteral
from src.utils.program3.values.literals.null_literal import NullLiteral


class TestParser(unittest.TestCase):


    def test_function(self):

        programs = [
            "main() {}",
            "calc_discount(total, percent) { return total * percent / 100;}",
            "print_values(val1, val2) { print(val1); print(val2);}",
            "get_name(this) { return this.name; }"
        ]

        parsed = []

        for program in programs:
            data_source = StringSource(io.StringIO(program))
            scanner = Scanner(data_source)
            parser = Parser(scanner)
            parsed_program = parser.parse_function()
            parsed.append(parsed_program)

        self.assertListEqual(
            [(type(func), len(func.params), len(func.block.statements)) for func in parsed],
            [
                (Function, 0, 0),
                (Function, 2, 1),
                (Function, 2, 2),
                (Function, 1, 1)
            ]
        )

    def test_class(self):

        programs = [
            "class Person {}",
            """
            class Person {
                Person(this, name, age) {
                    this.name = name;
                    this.age = age;
                }
            }""",
        ]

        parsed = []

        for program in programs:
            data_source = StringSource(io.StringIO(program))
            scanner = Scanner(data_source)
            parser = Parser(scanner)
            parsed_program = parser.parse_class()
            parsed.append(parsed_program)

        self.assertListEqual(
            [(type(_class), len(_class.class_block)) for _class in parsed],
            [
                (Class, 0),
                (Class, 1)
            ]
        )


    def test_block(self):

        programs = [
            "{}",
            "{this.name = name; this.age = age;}",
            "{ if i < 10 { i = i + 1;}}"
        ]

        parsed = []
        for program in programs:
            data_source = StringSource(io.StringIO(program))
            scanner = Scanner(data_source)
            parser = Parser(scanner)
            parsed_program = parser.parse_block()
            parsed.append(parsed_program)

        self.assertListEqual(
            [(type(block), len(block.statements)) for block in parsed],
            [
                (Block, 0),
                (Block, 2),
                (Block, 1)
            ]
        )

    # TODO: More restricted acceptance criteria for all tests

    def test_return(self):

        programs = [
            "return 2;",
            "return 3 + 3;",
            "return value;",
            'return this.get_value();'
            "return this.get_value(alpha);"
        ]

        parsed = []
        for program in programs:

            data_source = StringSource(io.StringIO(program))
            scanner = Scanner(data_source)
            parser = Parser(scanner)
            parsed_program = parser.parse_return()
            parsed.append(parsed_program)

        self.assertEqual(
            True,
            all([isinstance(parsed_program, Return) for parsed_pogram in parsed])
        )

    def test_assign(self):

        programs = [
            "a = 10;"
            "value = get_gradient(weights, bias)"
            "this.get_children()[0] = 1;"
        ]

        parsed = []

        for program in programs:
            data_source = StringSource(io.StringIO(program))
            scanner = Scanner(data_source)
            parser = Parser(scanner)
            parsed_program = parser.parse_assign_or_function_call()
            parsed.append(parsed_program)

        self.assertEqual(
            True,
            all([isinstance(parsed_program, Assign) for parsed_program in parsed])
        )

    def test_comment(self):

        programs = [
            "# comment",
            "# 1234. asylum afwoefascojscasd",
            "# cawieoiafaoinfsadf\n#ajdoasijdoiajsdoajs",
            "# cawejaosjdfo iadsf jsadf\r\n",
        ]

        parsed = []

        for program in programs:
            data_source = StringSource(io.StringIO(program))
            scanner = Scanner(data_source)
            parser = Parser(scanner)
            parsed_program = parser.parse_comment()
            parsed.append(parsed_program)

        self.assertEqual(
            True,
            all([isinstance(parsed_program, Comment) for parsed_program in parsed])
        )

    def test_foreach(self):

        programs = [
            "foreach i in array {}",
            "foreach attr in david.attributes {\nprint(attr);\n}",
            "foreach attr in david.rec_attributes() {\nprint(attr);\n}"
        ]

        parsed = []

        for program in programs:
            data_source = StringSource(io.StringIO(program))
            scanner = Scanner(data_source)
            parser = Parser(scanner)
            parsed_program = parser.parse_foreach_loop()
            parsed.append(parsed_program)

        self.assertEqual(
            True,
            all([isinstance(parsed_program, ForeachLoop) for parsed_program in parsed])
        )

    def test_conditional(self):

        programs = [
            'if a < 10 {print(a);}',
            'if a < 10 {print(a);} else { print(b);}',
            'if a < 10 {print(a);} else if a < 20 {print(b);} else if a < 30 {print(c);} else {print(d);}'
        ]

        parsed = []

        for program in programs:
            data_source = StringSource(io.StringIO(program))
            scanner = Scanner(data_source)
            parser = Parser(scanner)
            parsed_program = parser.parse_conditional()
            parsed.append(parsed_program)

        self.assertEqual(
            True,
            all([isinstance(parsed_program, Conditional) for parsed_program in parsed])
        )

    def test_function_call(self):

        programs = [
            "print(a);",
            "this.get_children().get_name();"
            "parent.get_attributes();"
        ]

        parsed = []
        for program in programs:
            data_source = StringSource(io.StringIO(program))
            scanner = Scanner(data_source)
            parser = Parser(scanner)
            parsed_program = parser.parse_assign_or_function_call()
            parsed.append(parsed_program)

        self.assertEqual(
            True,
            all([isinstance(parsed_program, FunctionCall) for parsed_program in parsed])
        )

        self.assertEqual(
            True,
            all([isinstance(program.complex_getter.get_last_getter(), CallGetter) for program in parsed])
        )

    def test_while_loop(self):

        programs = [
            "while True {print(a);}",
            "while a < b {print(c);}",
            "while a == b || True {print(d);}"
        ]

        parsed = []
        for program in programs:
            data_source = StringSource(io.StringIO(program))
            scanner = Scanner(data_source)
            parser = Parser(scanner)
            parsed_program = parser.parse_while_loop()
            parsed.append(parsed_program)

        self.assertEqual(
            True,
            all([isinstance(parsed_program, WhileLoop) for parsed_program in parsed])
        )

    def test_or_expression(self):

        programs = [
            "b == a || a == c || c == d",
            "i % 2 == 0 || a * c % 11 == 0 && c + 2 == 11"
        ]

        parsed = []
        for program in programs:
            data_source = StringSource(io.StringIO(program))
            scanner = Scanner(data_source)
            parser = Parser(scanner)
            parsed_program = parser.parse_or_expression()
            parsed.append(parsed_program)

        self.assertListEqual(
            [type(program) for program in parsed],
            [OrExpression] * len(programs)
        )

    def test_and_expression(self):

        programs = [
            "true && false",
            "true && value",
            "a + b == 0 && b < 100 && c % 2 == 1",
            "c + d != 0 && c > 100"
        ]

        parsed = []
        for program in programs:
            data_source = StringSource(io.StringIO(program))
            scanner = Scanner(data_source)
            parser = Parser(scanner)
            parsed_program = parser.parse_and_expression()
            parsed.append(parsed_program)

        self.assertListEqual(
            [type(program) for program in parsed],
            [AndExpression] * len(programs)
        )

    def test_eq_expression(self):

        programs = [
            "value * 25 + 7 == 132",
            "i % 2 != 1",
            'this.get_expression() != "Expression"'
        ]

        parsed = []
        for program in programs:
            data_source = StringSource(io.StringIO(program))
            scanner = Scanner(data_source)
            parser = Parser(scanner)
            parsed_program = parser.parse_eq_expression()
            parsed.append(parsed_program)

        self.assertListEqual(
            [type(program) for program in parsed],
            [EqualityExpression] * len(programs)
        )

    def test_rel_expression(self):

        programs = [
            "a > b",
            "c * b <= a + b",
            "a + this.keyword >= c + z",
            "g + b < a - 7"
        ]

        parsed = []
        for program in programs:
            data_source = StringSource(io.StringIO(program))
            scanner = Scanner(data_source)
            parser = Parser(scanner)
            parsed_program = parser.parse_rel_expression()
            parsed.append(parsed_program)

        self.assertListEqual(
            [type(program) for program in parsed],
            [RelationExpression] * len(programs)
        )

    def test_add_expression(self):

        programs = [
            # "2 + 2 * 2",
            # "3*5 - (2 * 7)",
            # "3 * 5 - (127 % 20)",
            "value * 1000 + percent",
            "this.get_children().get_age() - this.get_children().get_age()"
        ]

        parsed = []
        for program in programs:
            data_source = StringSource(io.StringIO(program))
            scanner = Scanner(data_source)
            parser = Parser(scanner)
            parsed_program = parser.parse_add_expression()
            parsed.append(parsed_program)

        self.assertListEqual(
            [type(program) for program in parsed],
            [AddExpression] * len(programs)
        )


    def test_mul_expression(self):

        programs = [
            "2 * 3",
            "2 * (-3)",
            "125 % 12",
            "22 / 9"
        ]

        parsed = []
        for program in programs:
            data_source = StringSource(io.StringIO(program))
            scanner = Scanner(data_source)
            parser = Parser(scanner)
            parsed_program = parser.parse_mult_expression()
            parsed.append(parsed_program)

        self.assertListEqual(
            [type(program) for program in parsed],
            [MultiplyExpression] * len(programs)
        )

    def test_unary_expression(self):

        programs = [
            "!(i == 0 || a < 10)",
            "!valid",
            "-(a * 10 + 10)"
        ]

        parsed = []
        for program in programs:
            data_source = StringSource(io.StringIO(program))
            scanner = Scanner(data_source)
            parser = Parser(scanner)
            parsed_program = parser.parse_unary_expression()
            parsed.append(parsed_program)

        self.assertListEqual(
            [type(program) for program in parsed],
            [UnaryExpression] * len(programs)
        )

    def test_general_value(self):

        programs = [
            "1",
            "2.5",
            "true",
            "false",
            '\"Something in the way she moves\"',
            "null"
        ]

        parsed = []
        for program in programs:
            data_source = StringSource(io.StringIO(program))
            scanner = Scanner(data_source)
            parser = Parser(scanner)
            parsed_program = parser.parse_value()
            parsed.append(parsed_program)

        self.assertListEqual(
            [(type(parsed_program), parsed_program.value) for parsed_program in parsed],
            [
                (IntLiteral, 1),
                (FloatLiteral, 2.5),
                (BoolLiteral, True),
                (BoolLiteral, False),
                (StringLiteral, "Something in the way she moves"),
                (NullLiteral, None)
            ]
        )
