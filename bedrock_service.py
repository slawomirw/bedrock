import json
import os
from typing import Any, Dict

import boto3

REGION = os.getenv("AWS_REGION", "us-east-1")
MAIN_MODEL_ID = os.getenv("BEDROCK_MAIN_MODEL_ID", "us.anthropic.claude-haiku-4-5-20251001-v1:0")
LIMITED_MODEL_ID = os.getenv("BEDROCK_LIMITED_MODEL_ID", "amazon.nova-micro-v1:0")

bedrock_client = boto3.client("bedrock-runtime", region_name=REGION)


def _invoke_model(model_id: str, content: str) -> Dict[str, Any]:
    response = bedrock_client.invoke_model(
        modelId=model_id,
        body=json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": content}],
            }
        ),
    )
    return json.loads(response["body"].read())


def call_main_agent(content: str) -> Dict[str, Any]:
    return _invoke_model(MAIN_MODEL_ID, content)


def call_limited_agent(content: str) -> Dict[str, Any]:
    return _invoke_model(LIMITED_MODEL_ID, content)
