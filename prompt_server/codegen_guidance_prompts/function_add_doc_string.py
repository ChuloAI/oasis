from andromeda_chain import AndromedaPrompt

function_doc_string_guidance_prompt = AndromedaPrompt(
    name="function_add_doc_string",
    prompt_template="""
def print_hello_world():
    print("hello_world")

def print_hello_world():
# Docstring below
    \"\"\"Prints the string 'hello_world' to the standard output.\"\"\"

def sum_2(x, y):
    return x + y

def sum_2(x, y):
# Docstring below
    \"\"\"Computes the sum of two numbers.
    
    Parameters:
        int: x - first number to sum
        int: y - second number to sum

    Returns:
        int: sum of the two given integers
    \"\"\"
    return x + y

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

def call_guidance(prompt_template, output_vars, input_vars=None, guidance_kwargs=None):
# Docstring below
    \"\"\"
    Calls a guidance API with the given parameters and returns the response.
    
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

{{leading_indentation}}{{function_header}}
{{function_body}}

{{function_header}}
# Docstring below
\"\"\"{{gen 'description' temperature=0.1 max_tokens=128 stop='.'}}

Parameters: {{gen 'parameters' temperature=0.1 max_tokens=128 stop='Returns:'}}
Returns: {{gen 'returns' temperature=0.1 max_tokens=128 stop='\"\"\"'}}
""",
    guidance_kwargs={},
    input_vars=["function_header", "function_body", "leading_indentation"],
    output_vars=["description", "parameters", "returns"],
)
