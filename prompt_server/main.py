from fastapi import FastAPI, HTTPException
import logging
import codegen_guidance_prompts
import wizard_lm_guidance_prompts

from pydantic import BaseModel
from guidance_client import call_guidance
from commands.commands import build_command_mapping


logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)

class Request(BaseModel):
    data: str


app = FastAPI()


prompts_module = codegen_guidance_prompts
commands_mapping = build_command_mapping(prompts_module)


MAGIC_STOP_STRING = "###Done"
MAGIC_SPLIT_STRING = "###FixedCode"
MAGIC_PYTHON_MD_START = "```python"
MAGIC_PYTHON_MD_END = "```"


@app.post("/{command}/")
def read_root(command, request: Request):
    logger.info("Received command: '%s'", command)
    logger.debug("Received data: '%s'", request)
    received_code = request.data
    try:
        command_to_apply = commands_mapping[command]
        logger.info("Loaded command: '%s'", command_to_apply)

    except KeyError:
        raise HTTPException(status_code=404, detail=f"Command not supported: {command}")

    prompt_key, prompt_to_apply, extracted_input = command_to_apply.prompt_picker(received_code)
    logger.info("Extracted input: %s", extracted_input)

    keys_difference = set(prompt_to_apply.input_vars) - set(extracted_input.keys())

    if keys_difference:
        error_msg = f"Missing input keys for the prompt: {keys_difference}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)


    logger.info("Loaded command: '%s'", command_to_apply)

    logger.info("Calling LLM...")
    result = call_guidance(
        prompt_template=prompt_to_apply.prompt_template,
        input_vars=extracted_input,
        output_vars=prompt_to_apply.output_vars,
        guidance_kwargs={}
    )
    logger.info("LLM output: '%s'", result)
    
    result = command_to_apply.output_extractor(prompt_key, extracted_input, result)

    if MAGIC_STOP_STRING in result:
        result = result.split(MAGIC_STOP_STRING)[0]

    if MAGIC_SPLIT_STRING in result:
        result = result.split(MAGIC_SPLIT_STRING)[1]

    if MAGIC_PYTHON_MD_START in result:
        result = result.split(MAGIC_PYTHON_MD_START)[1]

    if MAGIC_PYTHON_MD_END in result:
        result = result.split(MAGIC_PYTHON_MD_END)[0]

    logger.info("parsed output: '%s'", result)

    return {"text": result}
