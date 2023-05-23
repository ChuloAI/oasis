import requests
import json

guidance_url = "http://0.0.0.0:9090"
def call_guidance(prompt_template, output_vars, input_vars=None, guidance_kwargs=None):
    if input_vars is None:
        input_vars = {}
    if guidance_kwargs is None:
        guidance_kwargs = {}

    data = {
            "prompt_template": prompt_template,
            "output_vars": output_vars,
            "guidance_kwargs": guidance_kwargs,
            "input_vars": input_vars,
        }
    print("Sending data: ", data)
    response = requests.post(
        guidance_url, 
        json=data
    )
    response.raise_for_status()
    return response.json()