import pytest
from prompt_server.custom_parser import function_parser, _get_indentation_type


@pytest.mark.parametrize(
    "input_function, expected_leading",
    [
        ("def hello():\n\tprint('hello')", ""),
        ("def hello():\n    print('hello')", ""),
        ("\tdef hello():\n\t\tprint('hello')", "\t"),
        ("    def hello():\n        print('hello')", "    "),
    ]
)
def test_different_indentations(input_function, expected_leading):
    header, body, leading, indentation_type = function_parser(input_function)
    assert header == "def hello():"
    assert body == expected_leading + indentation_type + "print('hello')"
    assert leading == expected_leading



@pytest.mark.parametrize(
    "input_function, expected_type",
    [
        ("def hello():\n\tprint('hello')", "\t"),
        ("def hello():\n    print('hello')", "    "),
        ("\tdef hello():\n\t\tprint('hello')", "\t\t"),
        ("    def hello():\n        print('hello')", "        "),
    ]
)
def test_get_indentation_type(input_function, expected_type):
    assert _get_indentation_type(input_function) == expected_type
