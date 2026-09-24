import json

from gemini_client import generate_text


def get_learning_recommendations(
    topic: str,
    level: str = "Beginner",
) -> str:

    prompt = f"""
Create a personalized learning path for:

Topic: {topic}
Current level: {level}

Organize the learning path from beginner to advanced.

Include:

1. Prerequisites
2. Beginner stage
3. Intermediate stage
4. Advanced stage
5. Suggested practice activities
6. Project ideas
7. Revision strategy
8. Useful resource types such as:
   - Videos
   - Articles
   - Documentation
   - Books
   - Practice websites

For each stage, explain what the learner should understand before moving forward.

Give approximate timelines, but make it clear that they are flexible.

Do not invent specific URLs.
"""

    return generate_text(
        prompt,
        system_instruction=(
            "You are a personalized educational planning assistant. "
            "Create realistic and structured learning paths."
        ),
        temperature=0.5,
        max_output_tokens=2200,
    )
