# Two services, one command
**Topic:** inside Compose, containers reach each other by service name, not `localhost`.

## Your mission
Run the API and Ollama together with `docker compose up --build`.

## Steps
1. In `api`: `OLLAMA_URL: http://ollama:11434`.
2. In `ollama`: `image: ollama/ollama` and a volume `ollama:/root/.ollama`.
3. Declare the volume at the bottom under `volumes:`.

## Done when
**Check** finds the service name URL, the image and the named volume.
