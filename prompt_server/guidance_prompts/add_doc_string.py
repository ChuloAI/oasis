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
    '''This functions print the string 'hello_world' to the standard output.'''

###Done

Now let's begin!

Below is a Python block of codewithout docstrings or with incomplete docstrings:
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

