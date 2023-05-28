import pytest
from prompt_server.custom_parser import function_parser, _get_indentation_type, _extract_function_header
import ast

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
    (header, body, leading, indentation_type) = function_parser(input_function)
    assert header == 'def hello():'
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



normal_string = """def different_indentations(input_function, expected_leading):
    header, body, leading, indentation_type = function_parser(input_function)
    assert header == "def hello():"
    assert body == expected_leading + indentation_type + "print('hello')"
    assert leading == expected_leading
"""
def test_extract_header():
    parsed_body = ast.parse(normal_string).body[0]
    unparsed_body = ast.unparse(parsed_body)
    print("Unparsed body: ", unparsed_body)
    assert _extract_function_header(parsed_body) == "def different_indentations(input_function, expected_leading):"

test_string = """def test_different_indentations(input_function, expected_leading):
    header, body, leading, indentation_type = function_parser(input_function)
    assert header == "def hello():"
    assert body == expected_leading + indentation_type + "print('hello')"
    assert leading == expected_leading
"""

def test_extract_header():
    parsed_body = ast.parse(test_string).body[0]
    unparsed_body = ast.unparse(parsed_body)
    print("Unparsed body: ", unparsed_body)
    assert _extract_function_header(parsed_body) == "def test_different_indentations(input_function, expected_leading):"