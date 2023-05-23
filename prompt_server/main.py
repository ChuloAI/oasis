from fastapi import FastAPI, HTTPException
import logging
from prompts.add_doc_string import ADD_DOC_STRING
from prompts.add_type_hints import ADD_TYPE_HINTS
from prompts.fix_syntax_error import FIX_SYNTAX_ERROR
from prompts.custom_prompt import CUSTOM_PROMPT

from pydantic import BaseModel
from text_generation_web_ui import build_text_generation_web_ui_client_llm

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)


class Request(BaseModel):
    data: str


app = FastAPI()

commands_mapping = {
    "add_docstring": ADD_DOC_STRING,
    "add_type_hints": ADD_TYPE_HINTS,
    "fix_syntax_error": FIX_SYNTAX_ERROR,
    "custom_prompt": CUSTOM_PROMPT
}
MAGIC_STOP_STRING = "###Done"
MAGIC_SPLIT_STRING = "###FixedCode"
MAGIC_PYTHON_MD_START = "```python"
MAGIC_PYTHON_MD_END = "```"

llm_client = build_text_generation_web_ui_client_llm()

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
    result = llm_client._call(prompt=prompt_to_apply.format(input=received_code), stop=[MAGIC_STOP_STRING])
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
