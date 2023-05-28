ADD_TYPE_HINTS = """You're an AI programmer with the task of helping improving the code quality.
You receive code snippets each day with a problem. For instance, commonly they lack type hints.
You communicate your answer back over a specific protocol of adding a ###Done after each input question.

Example 1
Below is a Python function without type hints or with incomplete type hints:
###CodeToFix:
def sum_2(x, y):
    return x + y

###Task: Add type hints to the function above.
###FixedCode:
def sum_2(x: float, y: float) -> float:
    return x + y

###Done

Now let's begin!

Below is a Python function without type hints or with incomplete type hints:
###CodeToFix:
{input}

###Task: Add type hints to the function above.
###FixedCode:
"""