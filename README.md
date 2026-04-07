# Demonstration of Bedrock api call

# Application start

## bedrock app secret

define before application start

export AWS_BEARER_TOKEN_BEDROCK=....

## debug mode (no user credentials necessary)

> export DEBUG_MODE=True

in http header use:  Authorization: 'Bearer my-api-key'

## regular mode

> python3 start.py

## example call

> curl -X POST http://localhost:8080/v1/content/process   -H "Content-Type: application/json"   -H "Authorization: Bearer my-api-key"   -d '{"content":"Tell me a short story about a robot."}'