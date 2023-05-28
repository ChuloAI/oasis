from dataclasses import dataclass

from prompts_interface import PromptModuleInterface
from guidance_prompt import GuidancePrompt
from typing import Dict, Callable

@dataclass
class Command:
    prompt: GuidancePrompt
    input_extractor: Callable[[str], Dict[str, str]]


def extract_docstring_command_input(input_: str) -> Dict[str, str]:
    return {"input": input_}



def build_command_mapping(prompt_module: PromptModuleInterface):
    """
    This function builds a mapping of commands to their corresponding prompt.
    
    Parameters:
    prompt_module (PromptModuleInterface): The prompt module to use for the guidance.
    
    Returns:
    dict: The mapping of commands to their corresponding prompts.
    """
    add_docstring_command = Command(
        prompt=prompt_module.doc_string_guidance_prompt,
        input_extractor=extract_docstring_command_input,
    )


    commands_mapping = {
        "add_docstring": add_docstring_command,
        # "add_type_hints": ADD_TYPE_HINTS,
        # "fix_syntax_error": FIX_SYNTAX_ERROR,
        # "custom_prompt": CUSTOM_PROMPT
    }

    return commands_mapping
