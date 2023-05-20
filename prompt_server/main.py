from fastapi import FastAPI, HTTPException
import logging
from prompts.add_doc_string import ADD_DOC_STRING
from prompts.add_type_hints import ADD_TYPE_HINTS
from prompts.fix_syntax_error import FIX_SYNTAX_ERROR
from prompts.improve_code_quality import IMPROVE_CODE_QUALITY

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
    "improve_code_quality": IMPROVE_CODE_QUALITY
}

llm_client = build_text_generation_web_ui_client_llm()

@app.post("/{command}/")
def read_root(command, request: Request):
    logger.info("Received command: '%s'", command)
    logger.debug("Received data: '%s'", request)
    received_code = request.data
    try:
        prompt_to_apply = commands_mapping[command]
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Command not supported: {command}")
    result = llm_client._call(prompt=prompt_to_apply.format(input=received_code), stop="###DONE")
    logger.info("LLM output: '%s'", result)
    return {"Hello": "World"}
