import pytest
import ast

from prompt_server.parser import function_parser



def test_no_indent_tab():
    s = "def hello():\n\tprint('hello')"
    header, body, leading = function_parser(s)
    assert header == "def hello():"
    assert body == "\tprint('hello')"
    assert leading == ""

# def test_no_indent_spaces():
#     s = "def hello():\n    print('hello')"
#     h = function_parser(s)

# def test_indent_tabs():
#     try:
#         s = "\tdef hello():\n\t\tprint('hello')"
#         h2 = function_parser(s)
#     except IndentationError as excp:
#         raise excp

# def test_indent_spaces():
#     try:
#         s = "    def hello():\n        print('hello')"
#         h2 = function_parser(s)
#     except IndentationError as excp:
#         raise excp

