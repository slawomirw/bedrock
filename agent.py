import re
from typing import Any, Dict


class ContentAgent:
    """Analyzes, cleans, and validates user-provided content."""

    def analyze(self, content: str) -> Dict[str, Any]:
        words = [w for w in re.split(r"\s+", content.strip()) if w]
        return {
            "characters": len(content),
            "words": len(words),
            "contains_question": "?" in content,
            "is_ascii": content.isascii(),
        }

    def clean(self, content: str) -> str:
        # Normalize whitespace while keeping intent unchanged.
        normalized = re.sub(r"\s+", " ", content).strip()
        return normalized

    def validate(self, content: str) -> None:
        if not isinstance(content, str):
            raise ValueError("`content` must be a string")
        if not content.strip():
            raise ValueError("`content` cannot be empty")
        if len(content) > 8000:
            raise ValueError("`content` exceeds max length of 8000 characters")

    def process(self, content: str) -> Dict[str, Any]:
        self.validate(content)
        cleaned_content = self.clean(content)
        analysis = self.analyze(cleaned_content)
        return {"cleaned_content": cleaned_content, "analysis": analysis}
