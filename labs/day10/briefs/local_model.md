# Run an open model yourself
**Topic:** Ollama serves local models over HTTP; the first call is a slow cold start.

## Your mission
Run your 10 extractions through a local model and measure accuracy and latency.

## Steps
1. `chat`: `httpx.post` to `/api/chat` with `format="json"`, `stream=False`; return text and seconds.
2. `field_accuracy`: share of the 4 fields that match your label.
3. Install Ollama, `ollama pull qwen2.5:3b`, then **Run**.
4. Note accuracy and median latency next to yesterday's API results.

## Done when
**Check** confirms the request body and the accuracy maths (no Ollama needed).
