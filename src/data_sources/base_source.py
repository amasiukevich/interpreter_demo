import abc


class BaseSource(metaclass=abc.ABCMeta):

    def __init__(self):
        pass

    @abc.abstractmethod
    def read_char(self):
        pass

    @abc.abstractmethod
    def get_curr_char(self):
        pass

    @abc.abstractmethod
    @staticmethod
    def advance_position(self, char):
        pass