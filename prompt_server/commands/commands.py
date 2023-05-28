import logging
import abc
from dataclasses import dataclass

from prompts_interface import PromptModuleInterface
from guidance_prompt import GuidancePrompt
from typing import Dict, Tuple


logger = logging.getLogger("uvicorn")


@dataclass
class Command:
    prompt: Dict[str, GuidancePrompt]


    @abc.abstractclassmethod
    def prompt_picker(self, input_: str) -> Tuple[str, GuidancePrompt, Dict[str, str]]:
        raise NotImplementedError()

    @abc.abstractclassmethod
    def output_extractor(self, prompt_key: str, extracted_input: Dict[str, str], result: Dict[str, str]) -> str:
        raise NotImplementedError()

class DocStringCommand(Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)


    def prompt_picker(self, input_: str) -> Tuple[str, GuidancePrompt, Dict[str, str]]:
        is_function = "):\n" in input_
        if is_function:
            logger.info("Detected function")
            parts = input_.split(":\n")
            logger.info("Broke into parts: %s", parts)
            if len(parts) == 2:
                function_header = parts[0] + ":\n"
                function_body = parts[1]
                logger.info("Found function header and body")

                prompt_key = "function_prompt"
                return_value = prompt_key, self.prompt[prompt_key], {"function_header": function_header, "function_body": function_body}
        
        else:
            logger.warn("Failed to identify specific type of code block, falling back to generic prompt")

            prompt_key = "generic_prompt"
            return_value = prompt_key, self.prompt[prompt_key], {"input": input_}


        logger.info("Chosen prompt: %s", prompt_key)
        return return_value

    def output_extractor(self, prompt_key, extracted_input, result: Dict[str, str]) -> str:
        if prompt_key == "generic_prompt":
            return result["output"]
        elif prompt_key == "function_prompt":
            return (
                extracted_input["function_header"]
                + '    """'
                + result["description"] 
                + result["parameters"]
                + result["returns"] 
                + '"""\n'
                + extracted_input["function_body"]
            )


def build_command_mapping(prompt_module: PromptModuleInterface):
    """
    This function builds a mapping of commands to their corresponding functions
    Parameters:
    prompt_module (PromptModuleInterface): The prompt module to use for the guidance.
    
    Returns:
    dict: The mapping of commands to their corresponding functions.
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

