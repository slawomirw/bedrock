# Demonstration of Bedrock api call

# Application start

## debug mode (no secret necessary)

> export DEBUG_MODE=True

use:  'Bearer my-api-key'

## regular mode

> python3 start.py

## example call

> curl -X POST http://localhost:8080/v1/content/process   -H "Content-Type: application/json"   -H "Authorization: Bearer my-api-key"   -d '{"content":"Tell me a short story about a robot."}'