from gemini_client import generate_text


SYSTEM_PROMPT = """
You are EduGenie, an educational AI assistant.

Your job is to answer students' academic questions accurately and clearly.

Rules:
- Give a direct answer first.
- Explain difficult ideas in simple language.
- Use examples when useful.
- Avoid unnecessary complexity.
- If a question requires calculations, show the important steps.
- If you are uncertain, clearly say so.
- Keep the response educational and student-friendly.
"""


def answer_question(question: str) -> str:
    prompt = f"""
Answer the following student's question.

Student question:
{question}

Give a clear and concise educational answer.
"""

    return generate_text(
        prompt,
        system_instruction=SYSTEM_PROMPT,
        temperature=0.3,
        max_output_tokens=1200,
    )
