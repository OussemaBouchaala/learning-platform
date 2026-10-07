# Prove it doesn't block
**Topic:** day 2's lesson, on your real service.

## Your mission
Send 5 requests at once and show they overlap.

## Steps
1. `burst`: `await asyncio.gather(*[one(client) for _ in range(n)])`; return total time and the list.
2. With the service running, **Run**: 5 concurrent should take about as long as 1.

## Done when
**Check** shows `burst` overlaps its requests.
