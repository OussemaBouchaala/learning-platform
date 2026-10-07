# The results table
**Topic:** report p50 and p95 latency; the mean hides the slow tail.

## Your mission
Produce one table comparing both models on accuracy, latency and cost.

## Steps
1. `p50_p95`: `statistics.quantiles(..., n=100, method="inclusive")`, items 49 and 94.
2. `field_accuracy` and `cost_per_1k`.
3. `results_table`: one Markdown line per model under the header.
4. With the service running, **Run**: `results.md` is written.

## Done when
**Check** confirms the helpers and the table format.
