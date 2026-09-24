import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")


_client = None


def get_client():
    """
    Create the Gemini client only when it is needed.
    """
    global _client

    if _client is not None:
        return _client

    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Please add your Gemini API key to the .env file."
        )

    _client = genai.Client(api_key=GEMINI_API_KEY)

    return _client


def generate_text(
    prompt: str,
    system_instruction: str | None = None,
    temperature: float = 0.4,
    max_output_tokens: int = 1000,
) -> str:
    """
    Generate normal text using Gemini.
    """

    client = get_client()

    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
    )

    if system_instruction:
        config.system_instruction = system_instruction

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=config,
    )

    text = getattr(response, "text", None)

    if not text:
        raise RuntimeError("Gemini returned an empty response.")

    return text.strip()


def generate_structured(
    prompt: str,
    response_schema,
    system_instruction: str | None = None,
):
    """
    Generate structured JSON using a Pydantic schema.
    """

    client = get_client()

    config = types.GenerateContentConfig(
        temperature=0.3,
        max_output_tokens=2500,
        response_mime_type="application/json",
        response_schema=response_schema,
    )

    if system_instruction:
        config.system_instruction = system_instruction

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=config,
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty structured response.")

    return response.text.strip()
