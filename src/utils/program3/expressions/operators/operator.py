from src.utils.program3.node import Node


class Operator(Node):

    def __init__(self):
        self.oper = ""

    def __str__(self):
        return self.oper

    def __repr__(self):
        return f"Operator(\"{self.oper}\")"