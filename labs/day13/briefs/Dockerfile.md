# Containerize the API
**Topic:** copy requirements first so Docker caches the install layer.

## Your mission
Write a small image for `service.py`.

## Steps
1. `COPY requirements.txt .` then `RUN pip install --no-cache-dir -r requirements.txt`.
2. `COPY service.py .`
3. `CMD` uvicorn on `0.0.0.0` port `8002`.

## Done when
**Check** reads the file and finds each step in the right order.
