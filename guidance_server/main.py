from fastapi import FastAPI
import logging
import guidance
from guidance import Program
from pydantic import BaseModel
from typing import Dict, List
import torch

from transformers import BitsAndBytesConfig


# New 4 bit quantized
nf4_config = BitsAndBytesConfig(
   load_in_4bit=True,
   bnb_4bit_quant_type="nf4",
   bnb_4bit_use_double_quant=True,
   bnb_4bit_compute_dtype=torch.bfloat16
)


logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)


class Request(BaseModel):
    input_vars: Dict[str, str]
    output_vars: List[str]
    guidance_kwargs: Dict[str, str]
    prompt_template: str


app = FastAPI()

print("Loading model, this may take a while...")
# model = "TheBloke/wizardLM-7B-HF"
# model = "Salesforce/codegen-16B-mono"
model = "Salesforce/codegen-350m-mono"
# model = "Salesforce/codegen2-7B"

llama = guidance.llms.Transformers(model, quantization_config=nf4_config, trust_remote_code=True, revision="main")
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
