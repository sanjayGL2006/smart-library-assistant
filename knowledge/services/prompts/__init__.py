from .teacher import TEACHER_PROMPT
from .human import HUMAN_PROMPT
from .ai import AI_PROMPT
from .code import CODE_PROMPT
from .debug import DEBUG_PROMPT
from .example import EXAMPLE_PROMPT
from .quiz import QUIZ_PROMPT
from .review import REVIEW_PROMPT
from .research import RESEARCH_PROMPT
from .summarize import SUMMARIZE_PROMPT
from .notes import NOTES_PROMPT
from .default import DEFAULT_PROMPT

MODE_PROMPTS = {
    "teacher": TEACHER_PROMPT,
    "human": HUMAN_PROMPT,
    "ai": AI_PROMPT,
    "code": CODE_PROMPT,
    "debug": DEBUG_PROMPT,
    "example": EXAMPLE_PROMPT,
    "quiz": QUIZ_PROMPT,
    "review": REVIEW_PROMPT,
    "research": RESEARCH_PROMPT,
    "summarize": SUMMARIZE_PROMPT,
    "notes": NOTES_PROMPT,
    "default": DEFAULT_PROMPT
}
