import json
import os
from typing import Any, Dict

import boto3

REGION = os.getenv("AWS_REGION", "us-east-1")
MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "us.anthropic.claude-haiku-4-5-20251001-v1:0")

bedrock_client = boto3.client("bedrock-runtime", region_name=REGION)


def invoke_bedrock(clean_content: str) -> Dict[str, Any]:
    response = bedrock_client.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": clean_content}],
            }
        ),
    )
    return json.loads(response["body"].read())
