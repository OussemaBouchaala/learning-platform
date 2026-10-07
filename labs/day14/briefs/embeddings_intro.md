# Search by meaning
**Topic:** cosine similarity compares direction, not length.

## Your mission
Implement cosine similarity yourself and rank documents against a query.

## Steps
1. `cosine`: `np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))`.
2. `rank`: `sorted(docs, key=..., reverse=True)`.
3. **Run** and check the ranking makes sense.
4. Fill `CORPUS_NAME` and `CORPUS_PATH` for Weeks 3-6.

## Done when
**Check** confirms the maths, the ranking, and your corpus choice.
