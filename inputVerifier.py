import re
from typing import Any, Dict


def analyze(content: str) -> Dict[str, Any]:
    words = [w for w in re.split(r"\s+", content.strip()) if w]
    return {
        "characters": len(content),
        "words": len(words),
        "contains_question": "?" in content,
        "is_ascii": content.isascii(),
    }


def clean(content: str) -> str:
    normalized = re.sub(r"\s+", " ", content).strip()
    return normalized


def validate(content: str) -> None:
    if not isinstance(content, str):
        raise ValueError("`content` must be a string")
    if not content.strip():
        raise ValueError("`content` cannot be empty")
    if len(content) > 8000:
        raise ValueError("`content` exceeds max length of 8000 characters")


def process(content: str) -> Dict[str, Any]:
    validate(content)
    cleaned_content = clean(content)
    analysis = analyze(cleaned_content)
    return {"cleaned_content": cleaned_content, "analysis": analysis}
