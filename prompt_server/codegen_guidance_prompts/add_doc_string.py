from guidance_prompt import GuidancePrompt

doc_string_guidance_prompt = GuidancePrompt(
    prompt_template="""You're an AI programmer with the task of helping improving the code quality.
You receive code snippets each day with a problem. For instance, commonly they lack docstrings.
You communicate your answer back over a specific protocol of adding a ###Done after each input question.

Example 1
Below is a Python block of code without docstrings or with incomplete docstrings:
###CodeToFix:
def print_hello_world():
    print("hello_world")

###Task: Add docstrings to the code block above.
###FixedCode:
def print_hello_world():
    \"\"\"This functions print the string 'hello_world' to the standard output.\"\"\"

###Done


Example 2
Below is a Python block of code without docstrings or with incomplete docstrings:
###CodeToFix:
def sum_2(x, y):
    return x + y

###FixedCode:
def sum_2(x, y):
    \"\"\"This functions receives two parameters and returns the sum.
    
    Parameters:
        int: x - first number to sum
        int: y - second number to sum

    Returns:
        int: sum of the two given integers
    \"\"\"
    return x + y

###Done


Example 3
###CodeToFix:
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
    
    response = requests.post(
        guidance_url, 
        json=data
    )
    
    response.raise_for_status()
    
    return response.json()


###FixedCode:
def call_guidance(prompt_template, output_vars, input_vars=None, guidance_kwargs=None):
    \"\"\"
    This function calls a guidance API with the given parameters and returns the response.
    
    Parameters:
    prompt_template (str): The prompt template to use for the guidance.
    output_vars (dict): The output variables to use for the guidance.
    input_vars (dict): The input variables to use for the guidance.
    guidance_kwargs (dict): The guidance keywords to use for the guidance.
    
    Returns:
    dict: The response from the guidance API.
    \"\"\"

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
    
    response = requests.post(
        guidance_url, 
        json=data
    )
    
    response.raise_for_status()
    

    return response.json()

###Done

Example 4
Below is a Python block of code without docstrings or with incomplete docstrings:
###CodeToFix:
{{input}}

###Task: Add docstrings to the code block above.
###FixedCode:
{{gen 'output' temperature=0.1 max_tokens=500 stop='###Done'}}
""",
    guidance_kwargs={},
    input_vars=["input"],
    output_vars=["output"],
)

