import json
import os
from functools import wraps
from typing import Any, Dict

import boto3
from botocore.exceptions import ClientError
from flask import jsonify, request

REGION = os.getenv("AWS_REGION", "us-east-1")
API_KEYS_SECRET_NAME = os.getenv("API_KEYS_SECRET_NAME", "bedrock/api-keys")

secrets_client = boto3.client("secretsmanager", region_name=REGION)


def _load_api_keys_config() -> Dict[str, Any]:
    """
    Expected AWS Secrets Manager JSON format:
    {
      "keys": {
        "my-api-key": {"role": "admin", "permissions": ["bedrock:invoke"]},
        "readonly-key": {"role": "reader", "permissions": []}
      }
    }
    """
    secret_response = secrets_client.get_secret_value(SecretId=API_KEYS_SECRET_NAME)
    secret_string = secret_response.get("SecretString", "{}")
    return json.loads(secret_string)

def _load_api_keys_config_dummy() -> Dict[str, Any]:
    """
    Expected AWS Secrets Manager JSON format:
    {
      "keys": {
        "my-api-key": {"role": "admin", "permissions": ["bedrock:invoke"]},
        "readonly-key": {"role": "reader", "permissions": []}
      }
    }
    """
    # response = secrets_client.create_secret(
    #     Name='my-dummy-secret',
    #     Description='A test secret',
    #     SecretString=json.dumps({'username':'admin','password':'password123',\
    #     'keys':{'my-api-key': {'role': 'admin', 'permissions': ['bedrock:invoke']}}})
    # )
    return {'keys': {'my-api-key': {'role': "admin", 'permissions': ["bedrock:invoke"]}}}


def _authenticate_and_authorize(api_key: str, required_permission: str) -> Dict[str, Any]:
    config = _load_api_keys_config_dummy() if os.getenv("DEBUG_MODE") == "True" else _load_api_keys_config()
    keys = config.get("keys", {})
    principal = keys.get(api_key)
    if not principal:
        raise PermissionError("Invalid API key")

    permissions = principal.get("permissions", [])
    if required_permission not in permissions:
        raise PermissionError("Insufficient permissions")
    return principal


def require_api_key(required_permission: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                return jsonify({"error": "Missing bearer token"}), 401

            api_key = auth_header.replace("Bearer ", "", 1).strip()
            try:
                principal = _authenticate_and_authorize(api_key, required_permission)
            except PermissionError as exc:
                return jsonify({"error": str(exc)}), 403
            except ClientError as exc:
                return (
                    jsonify(
                        {
                            "error": "Unable to validate API key with AWS service",
                            "details": str(exc),
                        }
                    ),
                    500,
                )

            request.principal = principal  # type: ignore[attr-defined]
            return func(*args, **kwargs)

        return wrapper

    return decorator
