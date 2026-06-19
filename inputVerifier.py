import re
from typing import Any, Dict, Annotated
from aws_lambda_powertools.event_handler.bedrock_agent import BedrockAgentResolver
from aws_lambda_powertools.event_handler.openapi.params import Query, Body

app = BedrockAgentResolver()

def analyze(content: str) -> Dict[str, Any]:
    words = [w for w in re.split(r"\s+", content.strip()) if w]
    return {
        "characters": len(content),
        "words": len(words),
        "contains_question": "?" in content,
        "is_ascii": content.isascii(),
    }

def clean(content: str) -> str:
    # Normalize whitespace while keeping intent unchanged.
    normalized = re.sub(r"\s+", " ", content).strip()
    return normalized

def validate(content: str) -> None:
    if not isinstance(content, str):
        raise ValueError("`content` must be a string")
    if not content.strip():
        raise ValueError("`content` cannot be empty")
    if len(content) > 8000:
        raise ValueError("`content` exceeds max length of 8000 characters")

@app.post("/process", description="Analizes and verifies given prompt producing some characteristics")
def process(promptText: str) -> Dict[str, Any]:
    validate(promptText)
    cleaned_content = clean(promptText)
    analysis = analyze(cleaned_content)
    return {"cleaned_content": cleaned_content, "analysis": analysis}

@app.get(
    "/weather", 
    description="Returns a weather in user's location"
)
def get_weather(
    location: Annotated[str, Query(description="User geographical location in a form: coutry/direction")]
) -> Annotated[str, Body(description="General, one-word description of a weather condition")]:
    return "sunny"

def lambda_handler(event, context):
    return app.resolve(event, context)

