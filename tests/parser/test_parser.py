import io
import os
import unittest

from typing import List

from src.data_sources.string_source import StringSource
from src.data_sources.file_source import FileSource
from src.scanner.scanner import Scanner
from src.parser.parser import Parser
from src.utils.position import Position
from src.utils.program3.values.no_call_value_getter import NoCallValueGetter

from src.utils.token import Token
from src.utils.token_type import TokenType

from src.utils.program3.block import Block

from src.utils.program3.statements.conditional import Conditional
from src.utils.program3.statements.foreach_loop import ForeachLoop
from src.utils.program3.statements.while_loop import WhileLoop
from src.utils.program3.statements.assign import Assign
from src.utils.program3.statements.comment import Comment
from src.utils.program3.statements.reflect import Reflect
from src.utils.program3.statements._return import Return


from src.utils.program3.values.complex_value_getter import ComplexValueGetter
from src.utils.program3.expressions.expression import Expression


class TestParser(unittest.TestCase):

    # TODO: Test program, functions and classes


    # TODO: Make use of these integrational expression
    # def test_conditional(self):
    #
    #     program = self.parser_general_test(file_path="../../grammar_stuff/parser_testing_files/conditional_test.txt")
    #
    #     # getting info we want
    #     expected = Conditional(expressions=[Expression(), Expression()], blocks=[Block(), Block(), Block()])
    #     got = program.get_functions()['main'].block.statements[0]
    #
    #     self.assertEqual(type(expected), type(got))
    #
    # def test_foreach_loop(self):
    #
    #     program = self.parser_general_test(file_path="../../grammar_stuff/parser_testing_files/foreach_loop_test.txt")
    #
    #     expected = ForeachLoop(identifier=None, expression=None, block=None)
    #     got = program.get_functions()['main'].block.statements[0]
    #
    #     self.assertEqual(type(expected), type(got))
    #
    # def test_while_loop(self):
    #
    #     program = self.parser_general_test(file_path="../../grammar_stuff/parser_testing_files/while_test.txt")
    #     expected = WhileLoop(expression=None, block=None)
    #     got = program.get_functions()['main'].block.statements[0]
    #
    #     self.assertEqual(type(expected), type(got))
    #
    # def test_assign(self):
    #     program = self.parser_general_test(file_path="../../grammar_stuff/parser_testing_files/return_test.txt")
    #     expected = Assign(complex_var_getter=None, expression=None)
    #     got = program.get_functions()['main'].block.statements[0]
    #
    #     self.assertEqual(type(expected), type(got))
    #
    # def test_comment(self):
    #
    #     program = self.parser_general_test(file_path="../../grammar_stuff/parser_testing_files/comment_test.txt")
    #     expected_comments = [
    #         Comment(comment_body=" THIS is a comment"),
    #         Comment(comment_body=" # and this is a comment"),
    #         Comment(comment_body=" and this is also a comment")
    #     ]
    #     got = program.get_functions()['main'].block.statements
    #     self.assertListEqual(
    #         expected_comments, got
    #     )
    #
    # def test_reflect(self):
    #
    #     program = self.parser_general_test(file_path="../../grammar_stuff/parser_testing_files/parsing_reflect_file.txt")
    #
    #     expected = Reflect(is_recursive=True, expression=None)
    #     got = program.get_functions()['main'].block.statements[1]
    #
    #     self.assertEqual(expected, got)
    #
    # def test_return(self):
    #
    #     program = self.parser_general_test(file_path="../../grammar_stuff/parser_testing_files/return_test.txt")
    #
    #     expected = Return(expression=None)
    #     got = program.get_functions()['calc_total_price'].block.statements[0]
    #
    #     self.assertEqual(type(expected), type(got))
    #
    # # Complex value getter here
    # def test_function_call(self):
    #
    #     program = self.parser_general_test(file_path="../../grammar_stuff/parser_testing_files/return_test.txt")
    #
    #     expected = ComplexValueGetter(
    #         this_value_getter=False,
    #         rest_value_getter=None,
    #         last_getter=None
    #     )
    #
    #     got = program.get_functions()['main'].block.statements[0].expression
    #
    #     self.assertEqual(type(expected), type(got))
    #
    # def parser_general_test(self, file_path: str):
    #
    #     with io.open(os.path.abspath(file_path)) as file_stream:
    #         file_source = FileSource(file_stream)
    #         scanner = Scanner(file_source)
    #         parser = Parser(scanner)
    #
    #         program = parser.parse_program()
    #
    #     return program

    # TODO: Test program

    # TODO: Testing functions

    # TODO: Testing classes

    # TODO: test statements

    def test_return(self):
        pass

    def test_assign(self):
        pass

    def test_comment(self):
        pass

    def test_foreach(self):
        pass

    def test_conditional(self):
        pass

    def test_reflect(self):
        pass

    def test_rest_function_call(self):
        pass

    def test_while_loop(self):
        pass

    def init_parser(self, test_case: str):

        string_source = StringSource(
            io.StringIO(test_case)
        )

        scanner = Scanner(string_source)
        parser = Parser(scanner)
        return parser

    def test_statement(self, test_cases: List[str], testing_obj: str):

        results = []
        for case in test_cases:

            if testing_obj == "assign":
                pass
            elif testing_obj == "conditional":
                pass
            elif testing_obj == "comment":
                pass
            elif testing_obj == "foreach":
                pass
            elif testing_obj == "reflect":
                pass
            elif testing_obj == "return":
                pass
            elif testing_obj == "rest_funcion_call":
                pass
            elif testing_obj == "while":
                pass

        return results
    # TODO: Testing expressions

    # TODO: Testing values