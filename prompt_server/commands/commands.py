import logging
import abc
from dataclasses import dataclass

from custom_parser import function_parser, FailedToParseFunctionException
from prompts_interface import PromptModuleInterface
from andromeda_chain import AndromedaPrompt
from typing import Dict, Tuple


logger = logging.getLogger("uvicorn")


@dataclass
class Command:
    prompt: Dict[str, AndromedaPrompt]


    @abc.abstractclassmethod
    def prompt_picker(self, input_: str) -> Tuple[str, AndromedaPrompt, Dict[str, str]]:
        raise NotImplementedError()

    @abc.abstractclassmethod
    def output_extractor(self, prompt_key: str, extracted_input: Dict[str, str], result: Dict[str, str]) -> str:
        raise NotImplementedError()



class DocStringCommand(Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)


    def prompt_picker(self, input_: str) -> Tuple[str, AndromedaPrompt, Dict[str, str]]:
        prompt_key = "None"
        try:
            function_header, function_body, leading_indentation, indentation_type = function_parser(input_)
            prompt_key = "function_prompt"
            return_value = prompt_key, self.prompt[prompt_key], {
                "function_header": function_header,
                "function_body": function_body,
                "leading_indentation": leading_indentation,
                "indentation_type": indentation_type
            }

        except (FailedToParseFunctionException):
            logger.warn("Failed to identify specific type of code block, falling back to generic prompt")
            prompt_key = "generic_prompt"
            return_value = prompt_key, self.prompt[prompt_key], {"input": input_}

        logger.info("Chosen prompt: %s", prompt_key)
        return return_value

    def output_extractor(self, prompt_key, extracted_input, result: Dict[str, str]) -> str:
        if prompt_key == "generic_prompt":
            return result["output"]
        elif prompt_key == "function_prompt":
            ind = extracted_input["leading_indentation"]

            header_indentation = ind
            offset = ""
            indentation_type = extracted_input["indentation_type"]
            offset = "    "
            if indentation_type:
                offset = indentation_type

            body_indentation = ind + offset

            try:
                parameters = result["parameters"].strip().split("\n")
            except (KeyError, ValueError):
                parameters = []


            try:
                returns = result["returns"].strip().split("\n")
            except (KeyError, ValueError):
                returns = []


            parameters_string = ""
            if parameters:
                parameters_string = body_indentation + "Parameters: \n"
                for param in parameters:
                    parameters_string += f"{body_indentation}{indentation_type}{param.lstrip().strip()}\n"

                parameters_string += "\n"

            logger.info("Docstring parameters: %s", parameters_string)

            returns_string = ""
            if returns:
                returns_string = body_indentation + "Returns: \n"
                for return_ in returns:
                    returns_string += f"{body_indentation}{indentation_type}{return_.lstrip().strip()}\n"
                returns_string += "\n"

            logger.info("Docstring returns: %s", returns_string)

            code_with_docstring = (header_indentation + extracted_input["function_header"] + "\n") 
            code_with_docstring += (body_indentation + '"""')
            code_with_docstring += (result["description"].lstrip().strip() + "\n\n")

            logger.info("Header with description: %s", code_with_docstring)
            if parameters_string:
                code_with_docstring += (parameters_string)
            if returns_string:
                code_with_docstring += (returns_string)


            code_with_docstring += (body_indentation + '"""')
                
            code_with_docstring += extracted_input["function_body"]
            logger.info("Generated code with docstring: %s", code_with_docstring)
            return code_with_docstring


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

