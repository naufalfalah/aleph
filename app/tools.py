import datetime
from zoneinfo import ZoneInfo

from google.adk.tools.tool_context import ToolContext


# Tools
def get_weather(query: str) -> str:
    """Simulates a web search. Use it get information on weather.

    Args:
        query: A string containing the location to get weather information for.

    Returns:
        A string with the simulated weather information for the queried location.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."


def get_current_time(query: str) -> str:
    """Simulates getting the current time for a city.

    Args:
        city: The name of the city to get the current time for.

    Returns:
        A string with the current time information.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        tz_identifier = "America/Los_Angeles"
    else:
        return f"Sorry, I don't have timezone information for query: {query}."

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    return f"The current time for query {query} is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"


def set_username(username: str, tool_context: ToolContext) -> str:
    """Save or update username into  state agent.

    Call this function soon after user mention their username.
    """
    tool_context.state["user:username"] = username
    return f"Success! Username saved as '{username}'."


def save_user_preference(
    preference_key: str, preference_value: str, tool_context: ToolContext
) -> str:
    """Save user preference and fact into memory agent.

    Example: preference_key='hobby', preference_value='Cleaning'
    """
    state_key = f"user:{preference_key}"
    tool_context.state[state_key] = preference_value
    return f"Memory saved: {preference_key} = {preference_value}"


def get_user_memories(tool_context: ToolContext) -> str:
    """Retrieve all fact/preference about user."""
    memories = {k: v for k, v in tool_context.state.to_dict().items() if k.startswith("user:")}
    if not memories:
        return "There is no memory yet about the user."

    formatted = "\n".join(
        [f"- {k.replace('user:', '')}: {v}" for k, v in memories.items()]
    )
    return f"List of memory about user:\n{formatted}"
