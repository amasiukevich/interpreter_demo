import abc


class BaseSource(metaclass=abc.ABCMeta):

    def __init__(self):
        pass

    @abc.abstractmethod
    def read_char(self):
        pass

    @abc.abstractmethod
    def get_char(self):
        pass

    @abc.abstractmethod
    def advance_position(self, char):
        pass

    @abc.abstractmethod
    def get_position(self):
        pass