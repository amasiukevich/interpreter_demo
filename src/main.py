from src.data_sources import BaseSource
from src.data_sources.file_source import FileSource
from src.scanner.scanner import Scanner
from src.parser.parser import Parser
from src.interpreter.interpreter2 import Interpreter

import sys
import argparse


def run(source: BaseSource, start_function: str):

    scanner = Scanner(source=source)
    parser = Parser(scanner=scanner)

    tree = parser.parse_program()

    interpreter = Interpreter(program=tree, start_function=start_function)
    interpreter.execute()


def run_file(filepath: str, start_function: str):

    with open(filepath) as f:
        source = FileSource(file_obj=f)
        run(source, start_function)


def main():

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-f", "--filepath")
    arg_parser.add_argument('-sf', '--start_function', nargs="?", default="main", help="a function to start program")

    args = arg_parser.parse_args()

    run_file(filepath=args.filepath, start_function=args.start_function)
    # print(args.filepath)
    # print(args.start_function)

if __name__ == '__main__':
    main()