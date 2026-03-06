from datetime import datetime

from langchain_core.tools import tool


@tool
def get_current_datetime(query: str) -> str:
    """Returns the current date and time.
    Use this when the user asks about today's date or current time."""
    return datetime.now().strftime("%A, %B %d, %Y %H:%M:%S")
