import re

# Supported slash commands and aliases
COMMAND_MAP = {
    "/teacher": "teacher",
    "/teach": "teacher",
    "/human": "human",
    "/simple": "human",
    "/ai": "ai",
    "/quick": "ai",
    "/code": "code",
    "/debug": "debug",
    "/example": "example",
    "/quiz": "quiz",
    "/review": "review",
    "/research": "research",
    "/summarize": "summarize",
    "/notes": "notes"
}

def parse_mode(question: str) -> dict:
    """
    Parses a user question for a slash command.
    Returns {"mode": mode_name, "question": cleaned_question}.
    Defaults to 'default' mode if no valid command is found.
    """
    question = question.strip()
    
    for command, mode_name in COMMAND_MAP.items():
        if question.startswith(command):
            cleaned_question = re.sub(f"^{command}\\s*", "", question, count=1).strip()
            return {
                "mode": mode_name,
                "question": cleaned_question
            }

    # Handle unknown slash commands safely (e.g. /unknown) by ignoring them
    # and just defaulting to the standard mode.
    # The actual text is kept as-is.
    return {
        "mode": "default",
        "question": question
    }
