from gemini_client import generate_text


def summarize_text(text: str) -> str:
    prompt = f"""
Summarize the following educational text.

TEXT:
{text}

Requirements:
- Keep the important information.
- Remove unnecessary repetition.
- Use simple language.
- Organize the result with headings or bullet points when useful.
- Do not introduce information that is not in the original text.
- Make the summary useful for quick revision.
"""

    return generate_text(
        prompt,
        system_instruction=(
            "You are an educational summarization assistant. "
            "Preserve important facts and meaning."
        ),
        temperature=0.3,
        max_output_tokens=1500,
    )
