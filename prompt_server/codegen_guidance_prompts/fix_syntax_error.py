FIX_SYNTAX_ERROR = """You're an AI programmer with the task of helping improving the code quality.
You receive code snippets each day with a problem. For instance, commonly they have syntax errors.
You communicate your answer back over a specific protocol of adding a ###Done after each input question.

Example 1
Below is a Python function with syntax errors:
###CodeToFix:
def print_hello_world():
    print("hello_world"


###Task: Fix Syntax Errors
###Thought: I should close the parenthesis on the second line
###FixedCode:
def print_hello_world():
    print("hello_world")

###Done

Now let's begin!

Below is a Python function with syntax errors:
###CodeToFix:
{input}

###Task: Fix Syntax Errors
###Thought:
"""