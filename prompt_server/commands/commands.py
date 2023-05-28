import logging
import ast
import abc
from dataclasses import dataclass

from prompts_interface import PromptModuleInterface
from guidance_prompt import GuidancePrompt
from typing import Dict, Callable, Tuple


logger = logging.getLogger("uvicorn")


@dataclass
class Command:
    prompt: Dict[str, GuidancePrompt]


    @abc.abstractclassmethod
    def prompt_picker(input_: str) -> Tuple[GuidancePrompt, Dict[str, str]]:
        raise NotImplementedError()


class DocStringCommand(Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)


    def prompt_picker(self, input_: str) -> Tuple[GuidancePrompt, Dict[str, str]]:
        parsed = None
        is_function = False
        try:
            parsed = ast.parse(input_)
            function_def = parsed.body[0]
            if isinstance(function_def, ast.FunctionDef):
                is_function = True
        except Exception:
            pass

        if parsed:
            logger.info("Parsed code: %s", parsed.body)

            if is_function:
                logger.info("Detected function")
                parts = input_.split(":\n")
                logger.info("Broke into parts: %s", parts)
                if len(parts) == 2:
                    function_header = parts[0] + ":\n"
                    function_body = parts[1]
                    logger.info("Found function header and body")
                    return self.prompt["function_prompt"], {"header": function_header, "body": function_body}
        
        logger.warn("Failed to parse code, falling back to generic prompt")

        return self.prompt["generic_prompt"], {"input": input_}



def build_command_mapping(prompt_module: PromptModuleInterface):
    """
    This function builds a mapping of commands to their corresponding prompt.
    
    Parameters:
    prompt_module (PromptModuleInterface): The prompt module to use for the guidance.
    
    Returns:
    dict: The mapping of commands to their corresponding prompts.
    """
    add_docstring_command = DocStringCommand(
        prompt={
            "generic_prompt": prompt_module.doc_string_guidance_prompt,
            "function_prompt": prompt_module.function_doc_string_guidance_prompt
        }
    )


    commands_mapping = {
        "add_docstring": add_docstring_command,
        # "add_type_hints": ADD_TYPE_HINTS,
        # "fix_syntax_error": FIX_SYNTAX_ERROR,
        # "custom_prompt": CUSTOM_PROMPT
    }

    return commands_mapping

