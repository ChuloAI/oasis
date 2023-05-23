from fastapi import FastAPI
import logging
import guidance
from guidance import Program
from pydantic import BaseModel
from typing import Dict, List

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)


class Request(BaseModel):
    input_vars: Dict[str, str]
    output_vars: List[str]
    guidance_kwargs: Dict[str, str]
    prompt_template: str


app = FastAPI()

print("Loading model, this may take a while...")
llama = guidance.llms.Transformers("TheBloke/wizardLM-7B-HF", device=0, load_in_8bit=True)
print("Server loaded!")


@app.post("/")
def call_llama(request: Request):
    input_vars = request.input_vars
    kwargs = request.guidance_kwargs
    output_vars = request.output_vars

    guidance_program: Program = guidance(request.prompt_template)
    program_result = guidance_program(
        **kwargs,
        stream=False,
        async_mode=False,
        caching=False,
        **input_vars,
        llm=llama,
    )
    output = {}
    for output_var in output_vars:
        output[output_var] = program_result[output_var]
    return output
