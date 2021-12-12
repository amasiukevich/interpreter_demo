import unittest

from src.utils.program3.functions.parameters import Parameters


class TestStrAndRepr(unittest.TestCase):

    def test_param_str(self):

        param_names = ["a", "b", "c"]
        param_obj = Parameters(has_this=True, param_names=param_names)

        self.assertEqual(
            str(param_obj), "this, a, b, c"
        )

    def test_param_repr(self):

        param_obj = Parameters(has_this=True)

        self.assertEqual(
            param_obj.__repr__(), "Parameters(is_method=True, n_params=0)"
        )

    # TODO: test it after adding values
    def test_arguments_str(self):
        pass

    def test_arguments_repr(self):
        pass

    def test_argument_str(self):
        pass

    def test_argument_repr(self):
        pass

    def test_function_str(self):
        pass

    def test_function_repr(self):
        pass
