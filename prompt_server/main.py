from fastapi import FastAPI, HTTPException
import logging
import codegen350_guidance_prompts
import wizard_lm_guidance_prompts

from pydantic import BaseModel
from guidance_client import call_guidance

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)

class Request(BaseModel):
    data: str


app = FastAPI()


prompts_module = codegen350_guidance_prompts

commands_mapping = {
    "add_docstring": prompts_module.doc_string_guidance_prompt
    # "add_type_hints": ADD_TYPE_HINTS,
    # "fix_syntax_error": FIX_SYNTAX_ERROR,
    # "custom_prompt": CUSTOM_PROMPT
}
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
        prompt_to_apply = commands_mapping[command]
        logger.info("Loaded prompt: '%s'", prompt_to_apply)

    except KeyError:
        raise HTTPException(status_code=404, detail=f"Command not supported: {command}")

    logger.info("Calling LLM...")
    result = call_guidance(
        prompt_template=prompt_to_apply.prompt_template,
        input_vars={"input": received_code},
        output_vars=["output"],
        guidance_kwargs={}
    )
    result = result["output"]
    logger.info("LLM output: '%s'", result)
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
