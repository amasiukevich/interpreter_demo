from src.utils.program3.node import Node


class ThisValueGetter(Node):

    def __init__(self):
        pass

    def __str__(self):
        return "this."

    def __repr__(self):
        return "ThisValueGetter()"
