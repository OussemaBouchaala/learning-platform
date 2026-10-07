"""Full curriculum for Bench. Week 1 lives in curriculum_week1.py.

To add next week's daily plan: append day dicts to that week's "days" list
(same shape as Week 1), or replace the file Claude sends you on Sunday.
"""
from curriculum_week1 import WEEK1
from lab_files import lab

PROJECT = "Document extraction service: messy real estate listings (Arabic, French, English) to clean JSON."

DAY8 = {
    "id": "w2d1", "folder": "day08", "date": "2026-10-12", "weekday": "Mon",
    "title": "First LLM API calls", "minutes": 75,
    "why": "Everything in Phase 1 sits on this: prompts, tokens, and cost.",
    "lesson": """
## The shape of a call

Every chat API takes a list of messages (plus an optional system prompt) and returns generated text and token counts. Temperature controls randomness: 0 for repeatable extraction, higher for varied writing.

## Tokens are the unit of cost

Providers bill input and output tokens separately, usually per million tokens. Arabic text often splits into more tokens than English for the same meaning, so it costs more and fills context faster.

```python
def call_cost(tokens_in, tokens_out, price_in_per_m, price_out_per_m):
    return (tokens_in * price_in_per_m + tokens_out * price_out_per_m) / 1_000_000

# 1,000 calls of 500 input + 200 output tokens at $3 / $15 per million
print(f"${1000 * call_cost(500, 200, 3, 15):.2f}")
```

## Keys stay out of code

Read API keys from environment variables, never paste them into files you commit.

```bash
# PowerShell:   $env:LLM_API_KEY="..."
# Mac/Linux:    export LLM_API_KEY="..."
```

Start Bench from the same terminal after setting it, so your scripts can read it.
""",
    "files": [
        lab("day08", "llm_basics.py"),
    ],
    "tasks": [
        "Create an API account with a small prepaid credit ([Anthropic Console](https://console.anthropic.com) or [OpenAI Platform](https://platform.openai.com)); read its quickstart ([Anthropic](https://docs.anthropic.com/en/docs/get-started), [OpenAI](https://platform.openai.com/docs/quickstart))",
        "llm_basics.py: one call with a system prompt, tokens printed",
        "Compare temperature 0 vs 1.0",
        "Log tokens and cost per call",
        "Notes: what tokens are, and why Arabic often costs more",
    ],
    "done_when": "Every call logs tokens and cost.",
    "resources": [],
    "quiz": [
        {"q": "1,000 calls of 500 input + 200 output tokens at $3/M input and $15/M output. Total?", "options": ["$0.45", "$4.50", "$18.00", "$45.00"], "answer": 1,
         "explain": "Per call: 500 x 3 + 200 x 15 = 4,500 per million = $0.0045. Times 1,000 = $4.50."},
        {"q": "For extracting fields from documents, temperature should usually be...", "options": ["0 or close to it", "1.0", "2.0", "It doesn't matter"], "answer": 0,
         "explain": "Low temperature gives consistent, repeatable output."},
    ],
}

DAY9 = {
    "id": "w2d2", "folder": "day09", "date": "2026-10-13", "weekday": "Tue",
    "title": "Structured output", "minutes": 75,
    "why": "Real systems need JSON they can trust, not free text.",
    "lesson": """
## Schema first

Define the output with Pydantic, put the schema in the prompt, ask for JSON only, and validate every response.

```python
from pydantic import BaseModel, ValidationError

class Listing(BaseModel):
    price_tnd: float | None
    surface_m2: float | None
    rooms: int | None
    city: str | None

raw = '{"price_tnd": 250000, "surface_m2": 120, "rooms": "three", "city": "Sousse"}'
try:
    print(Listing.model_validate_json(raw))
except ValidationError as e:
    print(e)
```

## Validate, then retry once

When validation fails, send the error back to the model and ask for a corrected JSON. One retry fixes most failures; log the rest.

## Never eval model output

Parse with `json` or Pydantic. `eval()` on generated text would execute whatever it contains.
""",
    "files": [
        lab("day09", "listings.json"),
        lab("day09", "structured.py"),
    ],
    "tasks": [
        "Collect 10 real listings (e.g. [Tayara](https://www.tayara.tn), [Mubawab](https://www.mubawab.tn)) and hand-label price, surface, rooms, city",
        "Define the Pydantic schema ([Pydantic models](https://docs.pydantic.dev/latest/concepts/models/))",
        "Prompt for JSON, validate, retry once on failure",
        "Notes: which fields fail most and why",
    ],
    "done_when": "10 listings in, 10 validated JSON objects out.",
    "resources": [{"label": "Pydantic docs", "url": "https://docs.pydantic.dev"}],
    "quiz": [
        {"q": "The model returns JSON with rooms as \"three\". Best handling?", "options": ["eval() it", "Accept it as is", "Validate with Pydantic and retry with the error message", "Drop the listing silently"], "answer": 2,
         "explain": "Validation catches it; feeding the error back usually gets a corrected answer."},
        {"q": "Why never eval() model output?", "options": ["It's slow", "It can execute arbitrary code", "It loses Unicode", "It only works on dicts"], "answer": 1,
         "explain": "Generated text is untrusted input."},
    ],
}

DAY10 = {
    "id": "w2d3", "folder": "day10", "date": "2026-10-14", "weekday": "Wed",
    "title": "Run an open model yourself", "minutes": 75,
    "why": "Self-hosting is the cost and privacy alternative you'll compare against the API.",
    "lesson": """
## Ollama in two commands

```bash
ollama pull qwen2.5:3b
ollama run qwen2.5:3b "Say hello in Arabic"
```

Ollama also serves an HTTP API on `http://localhost:11434`. Pick the model size your machine can handle: 3B runs on most laptops, 7B wants a GPU or patience.

## Call it from Python

```python
import httpx

resp = httpx.post("http://localhost:11434/api/chat", json={
    "model": "qwen2.5:3b",
    "messages": [{"role": "user", "content": "Return {\\"ok\\": true} as JSON."}],
    "format": "json",
    "stream": False,
}, timeout=120)
print(resp.json()["message"]["content"])
```

## Quantization

Local models are usually quantized (for example 4-bit), cutting memory several times at a small quality cost. You used this at Octomiro with Qwen2.5-VL.

## Cold start

The first call loads the model into memory, so it's much slower than the next ones. Measure after a warm-up call.
""",
    "files": [
        lab("day10", "local_model.py"),
    ],
    "tasks": [
        "[Install Ollama](https://ollama.com/download) and pull a small [Qwen2.5 model](https://ollama.com/library/qwen2.5)",
        "Run the 10 extractions locally with latency per call",
        "Compare field accuracy with the API model",
        "PFE: finish the host list ([LinkedIn Jobs](https://www.linkedin.com/jobs/search/?keywords=PFE%20machine%20learning&location=Tunisia))",
    ],
    "done_when": "Accuracy and latency for both models on the same 10 inputs.",
    "resources": [{"label": "Ollama", "url": "https://ollama.com"}],
    "quiz": [
        {"q": "Why is the first local call much slower?", "options": ["Network latency", "The model loads into memory (cold start)", "Ollama compiles the prompt", "Quantization runs first"], "answer": 1,
         "explain": "Always warm up before measuring."},
        {"q": "What does 4-bit quantization trade?", "options": ["Speed for accuracy", "Memory savings for a small quality loss", "Context length for speed", "Nothing"], "answer": 1,
         "explain": "Smaller weights, slightly less precise outputs."},
    ],
}

DAY11 = {
    "id": "w2d4", "folder": "day11", "date": "2026-10-15", "weekday": "Thu",
    "title": "Wrap it in FastAPI", "minutes": 75,
    "why": "A model isn't a product until it's a service. Apply Day 2's async lesson for real.",
    "lesson": """
## The endpoint

`POST /extract` takes listing text and a model choice and returns validated JSON.

## Async done right

Inside `async def`, call models with `httpx.AsyncClient` and `await`. Using `requests` there would block every other request, exactly what you measured on Day 2.

## Honest status codes

- **422**: the client's request is invalid (FastAPI does this automatically for bad bodies).
- **502 Bad Gateway**: your upstream (the model) returned something unusable.
- **504 Gateway Timeout**: the model took too long.

Run the service in your terminal:

```bash
cd ml-fundamentals-lab/day11
uvicorn service:app --port 8002 --reload
```
""",
    "files": [
        lab("day11", "service.py"),
        lab("day11", "concurrency_check.py"),
    ],
    "tasks": [
        "POST /extract with async model calls",
        "Validation, one retry, 502 and 504 errors",
        "Prove concurrency with your Day 2 load test",
    ],
    "done_when": "Concurrent requests don't block each other.",
    "resources": [{"label": "HTTPX async client", "url": "https://www.python-httpx.org/async/"}],
    "quiz": [
        {"q": "Inside async def, which client should call Ollama?", "options": ["requests", "httpx.AsyncClient with await", "urllib", "subprocess curl"], "answer": 1,
         "explain": "It's awaitable, so the loop keeps serving other requests."},
        {"q": "The model returns unparseable output after a retry. Status code?", "options": ["200", "400", "422", "502"], "answer": 3,
         "explain": "The client's request was fine; the upstream failed."},
    ],
}

DAY12 = {
    "id": "w2d5", "folder": "day12", "date": "2026-10-16", "weekday": "Fri",
    "title": "Measure", "minutes": 75,
    "why": "Anis asked for accuracy, cost, and latency. Today you produce that table.",
    "lesson": """
## What to measure

- **Accuracy:** per-field exact match against your labels, then the average.
- **Latency:** p50 (typical) and p95 (the slow tail users notice). The mean hides the tail.
- **Cost:** per 1,000 requests. For the local model, write down the hardware instead.

```python
import statistics
latencies = [0.8, 0.9, 1.1, 0.7, 4.2, 0.9, 1.0, 0.8, 0.9, 5.1]
q = statistics.quantiles(latencies, n=100, method="inclusive")
print("mean", round(statistics.mean(latencies), 2), "p50", round(q[49], 2), "p95", round(q[94], 2))
```

Run each input 3 times to see variance.
""",
    "files": [
        lab("day12", "measure.py"),
    ],
    "tasks": [
        "measure.py: both models, 10 listings, 3 runs",
        "Field accuracy, p50/p95 latency, cost per 1,000 requests",
        "Results table saved as results.md",
    ],
    "done_when": "One table comparing both models on accuracy, latency, and cost.",
    "resources": [],
    "quiz": [
        {"q": "Why report p95 latency, not just the mean?", "options": ["It's always lower", "It shows the slow tail users actually feel", "It's easier to compute", "Providers require it"], "answer": 1,
         "explain": "A few very slow calls hide inside a mean."},
    ],
}

DAY13 = {
    "id": "w2d6", "folder": "day13", "date": "2026-10-17", "weekday": "Sat",
    "title": "Ship it", "minutes": 180,
    "why": "A repo someone can run with one command is portfolio proof.",
    "lesson": """
## Two containers

The service and Ollama run as two services in Docker Compose. Inside the Compose network, containers reach each other by **service name**, not `localhost`: your API calls `http://ollama:11434`.

```yaml
services:
  api:
    build: .
    ports: ["8002:8002"]
    environment:
      OLLAMA_URL: http://ollama:11434
    depends_on: [ollama]
  ollama:
    image: ollama/ollama
    volumes: [ollama:/root/.ollama]
volumes:
  ollama:
```

## The README that gets read

Problem, architecture sketch, results table, one-command run instructions, and what you'd improve.
""",
    "files": [
        lab("day13", "Dockerfile"),
        lab("day13", "docker-compose.yml"),
        lab("day13", "README.md"),
    ],
    "tasks": [
        "Dockerfile and docker-compose.yml (API + Ollama), see the [Compose docs](https://docs.docker.com/compose/)",
        "README with the results table",
        "Push as a public repo ([create llm-extraction-service](https://github.com/new)) and [pin it](https://github.com/OussemaBouchaala)",
        "PFE: send your first 2 applications ([LinkedIn Jobs](https://www.linkedin.com/jobs/search/?keywords=PFE%20machine%20learning&location=Tunisia))",
    ],
    "done_when": "Someone can clone the repo and run it with one command.",
    "resources": [{"label": "Docker Compose docs", "url": "https://docs.docker.com/compose/"}],
    "quiz": [
        {"q": "Inside Compose, how does the api container reach Ollama?", "options": ["http://localhost:11434", "http://ollama:11434", "http://127.0.0.1:11434", "It can't"], "answer": 1,
         "explain": "Each container has its own localhost; service names resolve on the Compose network."},
    ],
}

DAY14 = {
    "id": "w2d7", "folder": "day14", "date": "2026-10-18", "weekday": "Sun",
    "title": "Retro and RAG prep", "minutes": 150,
    "why": "Week 3 is RAG. Embeddings and vector search are its foundation.",
    "lesson": """
## Embeddings

An embedding model turns text into a vector so that similar meanings land close together. Search becomes "find the nearest vectors to the question's vector".

## Cosine similarity

```python
import numpy as np

def cosine(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

q = np.array([0.9, 0.1, 0.0])
docs = {"rent law": np.array([0.8, 0.2, 0.1]), "football": np.array([0.0, 0.1, 0.9])}
for name, v in docs.items():
    print(name, round(cosine(q, v), 3))
```

## pgvector

A PostgreSQL extension that stores vectors in a column and searches them by distance, so your documents, metadata, and vectors live in one database you already know.
""",
    "files": [
        lab("day14", "embeddings_intro.py"),
    ],
    "tasks": [
        "Read about [embeddings](https://huggingface.co/blog/getting-started-with-embeddings) and cosine similarity; read the [pgvector README](https://github.com/pgvector/pgvector#readme)",
        "embeddings_intro.py: cosine similarity and ranking",
        "Choose and download the Arabic corpus for Weeks 3-6 ([Arabic datasets on Hugging Face](https://huggingface.co/datasets?language=language:ar))",
        "Weekly retro: tick the tracker and [send Claude](https://claude.ai) your progress",
    ],
    "done_when": "The corpus is on disk and you know how pgvector stores and searches vectors.",
    "resources": [{"label": "pgvector", "url": "https://github.com/pgvector/pgvector"}],
    "quiz": [
        {"q": "Cosine similarity of two vectors pointing the same direction (any lengths)?", "options": ["0", "1", "-1", "Depends on length"], "answer": 1,
         "explain": "Cosine measures angle, not magnitude."},
    ],
}

WEEK2 = {
    "n": 2, "phase": "Phase 1", "title": "LLM basics and serving", "dates": "Oct 12-18",
    "goal": PROJECT,
    "gate": "Repo with a results table for API vs local model",
    "days": [DAY8, DAY9, DAY10, DAY11, DAY12, DAY13, DAY14],
}


def roadmap_week(n, phase, title, dates, goal, tasks, gate):
    return {"n": n, "phase": phase, "title": title, "dates": dates, "goal": goal,
            "gate": gate, "days": [], "tasks": tasks}


CURRICULUM = [
    WEEK1,
    WEEK2,
    roadmap_week(3, "Phase 1", "RAG from scratch", "Oct 19-25",
                 "Working RAG over a small document set.",
                 ["Chunking strategies (fixed, by heading, overlap)", "Multilingual embeddings ([bge-m3](https://huggingface.co/BAAI/bge-m3) or [multilingual-e5](https://huggingface.co/intfloat/multilingual-e5-large))",
                  "Vector search with [pgvector](https://github.com/pgvector/pgvector)", "Add a reranker"], "Working RAG"),
    roadmap_week(4, "Phase 1", "Evaluation", "Oct 26-Nov 1",
                 "An eval script and a results table.",
                 ["Test set of 50-100 questions with expected answers", "Retrieval recall@k",
                  "Answer faithfulness (LLM-as-judge or [RAGAS](https://docs.ragas.io))", "Latency and cost per query"], "Eval table"),
    roadmap_week(5, "Phase 1", "Tool calling and agents", "Nov 2-8",
                 "An agent that performs one real action.",
                 ["Function calling with tool schemas ([Anthropic tool use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use), [OpenAI function calling](https://platform.openai.com/docs/guides/function-calling))", "Agent calling your own FastAPI endpoints", "[MCP](https://modelcontextprotocol.io) basics"],
                 "Working agent"),
    roadmap_week(6, "Phase 1", "Real Arabic data", "Nov 9-15",
                 "Arabic RAG prototype with eval numbers.",
                 ["Pick and load a public Arabic corpus ([Hugging Face](https://huggingface.co/datasets?language=language:ar))", "Normalization: alef/hamza, taa marbuta, diacritics",
                  "Mixed Arabic/English/French text", "Re-run the Week 4 eval on Arabic questions"],
                 "Arabic RAG prototype with eval numbers"),
    roadmap_week(7, "Phase 2", "Scope the project", "Nov 16-22",
                 "One-page problem statement with a real user and data.",
                 ["Choose the project option", "Confirm the real user and data access",
                  "Success metrics: accuracy, latency, cost targets"], "Signed-off scope"),
    roadmap_week(8, "Phase 2", "Build I", "Nov 23-29",
                 "Ingestion and retrieval working end to end.",
                 ["Ingestion pipeline (OCR/parsing, chunking, indexing)", "Retrieval + generation with citations"],
                 "End-to-end path works"),
    roadmap_week(9, "Phase 2", "Build II", "Nov 30-Dec 6",
                 "Tool calling and a usable UI.",
                 ["Tool calling for at least one real action", "Simple web UI"], "Usable demo"),
    roadmap_week(10, "Phase 2", "Evaluate", "Dec 7-13",
                 "Two configurations compared on accuracy, latency, cost.",
                 ["Compare self-hosted vs API, with vs without reranker", "Results table", "Failure cases written up"],
                 "Results table"),
    roadmap_week(11, "Phase 2", "Ship", "Dec 14-20",
                 "Deployable, documented, tested.",
                 ["[Docker Compose](https://docs.docker.com/compose/) deployment", "README and architecture diagram", "Tests for core functions"],
                 "One-command run"),
    roadmap_week(12, "Phase 2", "Present", "Dec 21-27",
                 "Demo video and the message to Anis.",
                 ["3-5 minute demo video", "Update CV and [LinkedIn](https://www.linkedin.com/)", "Send the follow-up message to Anis"],
                 "Message sent"),
]
