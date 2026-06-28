import os

from flask import Flask, jsonify, request

from bedrock_service import call_main_agent
from inputVerifier import process
from security import require_api_key

REQUIRED_PERMISSION = "bedrock:invoke"

app = Flask(__name__)


@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response


@app.post("/v1/content/process")
@require_api_key(REQUIRED_PERMISSION)
def process_content():
    payload = request.get_json(silent=True) or {}
    raw_content = payload.get("content")

    if raw_content is None:
        return jsonify({"error": "`content` field is required"}), 400

    try:
        processed = process(raw_content)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    bedrock_result = call_main_agent(processed["cleaned_content"])

    return jsonify(
        {
            "analysis": processed["analysis"],
            "cleaned_content": processed["cleaned_content"],
            "bedrock_response": bedrock_result,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")), debug=True)
