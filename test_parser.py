import pytest
from prompt_server.parser import function_parser


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
    header, body, leading = function_parser(input_function)
    assert header == "def hello():"
    assert body == expected_leading + "print('hello')"
    assert leading == expected_leading
