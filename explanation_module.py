import os

from gemini_client import generate_text


USE_LOCAL_EXPLAINER = (
    os.getenv("USE_LOCAL_EXPLAINER", "false").lower()
    in {"true", "1", "yes"}
)

LOCAL_MODEL = os.getenv(
    "LOCAL_MODEL",
    "MBZUAI/LaMini-Flan-T5-783M",
)


_local_pipeline = None


def _load_local_model():
    """
    Load the LaMini-Flan-T5 model only when local mode is enabled.
    """

    global _local_pipeline

    if _local_pipeline is not None:
        return _local_pipeline

    try:
        from transformers import pipeline

        _local_pipeline = pipeline(
            "text2text-generation",
            model=LOCAL_MODEL,
            device=-1,
        )

        return _local_pipeline

    except ImportError as exc:
        raise RuntimeError(
            "Local explanation mode requires transformers and torch. "
            "Install requirements-local.txt."
        ) from exc

    except Exception as exc:
        raise RuntimeError(
            f"Unable to load local model '{LOCAL_MODEL}': {exc}"
        ) from exc


def explain_with_local_model(topic: str) -> str:
    model = _load_local_model()

    prompt = f"""
Explain the following educational topic simply.

Topic:
{topic}

The explanation should:
1. Start with a simple definition.
2. Explain the main idea.
3. Give a simple example.
4. End with a short summary.

Use easy language.
"""

    result = model(
        prompt,
        max_new_tokens=350,
        do_sample=True,
        temperature=0.7,
    )

    if not result:
        raise RuntimeError("Local model returned an empty response.")

    return result[0]["generated_text"].strip()


def explain_topic(topic: str) -> str:
    """
    Explain a concept.

    If USE_LOCAL_EXPLAINER=true, LaMini-Flan-T5 is attempted.
    Otherwise Gemini is used.
    """

    if USE_LOCAL_EXPLAINER:
        try:
            return explain_with_local_model(topic)
        except Exception:
            # Fall back to Gemini instead of breaking the application.
            pass

    prompt = f"""
Explain the educational topic below to a beginner.

Topic:
{topic}

Use this structure:

## Simple Definition
Explain what it means.

## How It Works
Explain the main idea step by step.

## Example
Give one simple example.

## Remember
Give 2 or 3 important points to remember.

Keep the language simple and clear.
"""

    return generate_text(
        prompt,
        system_instruction=(
            "You are a patient teacher who simplifies difficult "
            "academic concepts for students."
        ),
        temperature=0.4,
        max_output_tokens=1200,
    )
