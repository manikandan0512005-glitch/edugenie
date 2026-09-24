import json

from gemini_client import generate_structured
from schemas import QuizResponse


def generate_quiz(text: str) -> dict:
    prompt = f"""
Create a short educational quiz from the following text.

TEXT:
{text}

Requirements:

1. Generate exactly 3 multiple-choice questions.
2. Each question must have exactly 4 options.
3. Exactly one option must be correct.
4. The questions must be based only on the supplied text.
5. Make the questions useful for checking understanding.
6. Include a short explanation for the correct answer.
7. Return only data matching the requested JSON schema.
"""

    raw_json = generate_structured(
        prompt,
        QuizResponse,
        system_instruction=(
            "You are an educational quiz generator. "
            "Create clear, accurate multiple-choice questions."
        ),
    )

    try:
        parsed = json.loads(raw_json)
        result = QuizResponse.model_validate(parsed)
        return result.model_dump()

    except Exception as exc:
        raise RuntimeError(
            f"Unable to parse quiz response: {exc}"
        ) from exc
