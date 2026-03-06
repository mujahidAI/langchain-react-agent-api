from langchain_core.tools import tool


@tool
def calculator(expression: str) -> str:
    """Evaluates a mathematical expression and returns the result.
    Use this for any arithmetic or mathematical calculations.
    Input should be a valid math expression like '2 + 2' or '15 * 4 / 3'."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"
