from typing import Annotated

from aws_lambda_powertools.event_handler.bedrock_agent import BedrockAgentResolver
from aws_lambda_powertools.event_handler.openapi.params import Query, Body
from bedrock_service import call_limited_agent

app = BedrockAgentResolver()


@app.get(
    "/weather",
    description="Returns a weather in user's location",
)
def get_weather(
    location: Annotated[str, Query(description="User geographical location in a form: country/direction")]
) -> Annotated[str, Body(description="General, one-word description of a weather condition")]:
    prompt = f"What is the current weather like in {location}? Give a one-word answer."
    result = call_limited_agent(prompt)
    return result.get("content", [{}])[0].get("text", "unknown")


def lambda_handler(event, context):
    return app.resolve(event, context)
