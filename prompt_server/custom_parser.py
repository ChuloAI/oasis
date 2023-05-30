import ast

from typing import Tuple

USED_BODY_CHARS_TO_SPLIT = 3

def _extract_function_header(fun_code: ast.FunctionDef) -> str:
    full = ast.unparse(fun_code)
    body = ast.unparse(fun_code.body)
    print(f"Parsed body:", body)
    return full.split(body[0:USED_BODY_CHARS_TO_SPLIT])[0].strip()

def _extract_function_body(function_header: str, input_code_str: str) -> str:
    print(f"input code : '{input_code_str}'")
    print(f"function header: '{function_header}'")
    return input_code_str.split(function_header.strip())[1]

def _get_leading_indentation(input_code_str: str) -> str:
    try:
        return input_code_str.split("def")[0]
    except (ValueError, IndexError):
        return ""

def _get_indentation_type(input_code_str: str) -> str:

    try:
        try:
            second_string = input_code_str.split("def")[1]
        except (KeyError, IndexError):
            second_string = input_code_str

        try:
            second_line = second_string.splitlines()[1]
        except (IndexError):
            second_line = second_string

        whitespaces = ""
        for ch in second_line:
            if ch == "\t" or ch == " ":
                whitespaces += ch
            else:
                break
        return whitespaces
    except (ValueError, IndexError) as excp:
        raise excp

def _remove_extra_indentation(input_code_str: str, leading_indentation: str) -> str:
    if not leading_indentation:
        return input_code_str

    lines = input_code_str.splitlines()
    trimmed_lines = [line.replace(leading_indentation, "", 1) for line in lines]
    return "\n".join(trimmed_lines)

class FailedToParseFunctionException(Exception):
    pass

def function_parser(input_code_str: str) -> Tuple[str, str, str]:
    leading_indentation = _get_leading_indentation(input_code_str)
    simple_indented_code = _remove_extra_indentation(input_code_str, leading_indentation)
    indentation_type = _get_indentation_type(input_code_str)

    parsed = ast.parse(simple_indented_code, filename="<string>")
    parsed
    try:
        first_node = parsed.body[0]
    except IndexError:
        raise FailedToParseFunctionException from IndexError
    
    if not isinstance(first_node, ast.FunctionDef):
        raise FailedToParseFunctionException(f"Parsed type is not a function: '{type(first_node)}'")
    
    function_header = _extract_function_header(first_node)
    function_body = _extract_function_body(function_header, input_code_str)

    return function_header, function_body, leading_indentation, indentation_type