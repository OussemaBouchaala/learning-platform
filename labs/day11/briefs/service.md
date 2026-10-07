# Wrap it in FastAPI
**Topic:** honest status codes: 422 bad request, 502 bad upstream, 504 slow upstream.

## Your mission
Build `POST /extract` with async model calls, one retry, and the right errors.

## Steps
1. `call_model`: `await client.post(...)` to Ollama, return the reply text.
2. `extract`: call, validate, retry once with the error.
3. Still invalid: `HTTPException(502)`. `httpx.TimeoutException`: `HTTPException(504)`.
4. Start it in a terminal: `uvicorn service:app --port 8002 --reload`.

## Done when
**Check** drives the endpoint with fake model answers and gets 200, 502, 504 and 422.
