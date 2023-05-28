import ast

from typing import Tuple

def _extract_function_header(fun_code: ast.FunctionDef) -> str:
    return ast.unparse(fun_code).replace(ast.unparse(fun_code.body), "").strip()

def _extract_function_body(fun_code: ast.FunctionDef, leading_indentation: str) -> str:
    body_code = ast.unparse(fun_code.body)
    lines = body_code.splitlines()
    indented_lines = [leading_indentation + line for line in lines]
    return "\n".join(indented_lines)

def _get_leading_indentation(input_code_str: str) -> str:
    try:
        return input_code_str.split("def")[0]
    except (ValueError, IndexError):
        return ""

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
    parsed = ast.parse(simple_indented_code, filename="<string>")
    parsed
    try:
        first_node = parsed.body[0]
    except IndexError:
        raise FailedToParseFunctionException from IndexError
    
    if not isinstance(first_node, ast.FunctionDef):
        raise FailedToParseFunctionException(f"Parsed type is not a function: '{type(first_node)}'")
    
    function_body = _extract_function_body(first_node, leading_indentation)
    function_header = _extract_function_header(first_node)
    return function_header, function_body, leading_indentation