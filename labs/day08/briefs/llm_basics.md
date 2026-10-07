# First API calls
**Topic:** every call is billed in input and output tokens.

## Your mission
Call a model, log tokens and cost for every call, and compare temperatures.

## Steps
1. Set `MODEL` and both prices from your provider's pricing page.
2. `call_cost`: `(tokens_in * price_in + tokens_out * price_out) / 1_000_000`.
3. `ask`: one `client.messages.create(...)` call (shape in the docstring); return text and both token counts.
4. Set `LLM_API_KEY` in your terminal, restart Bench, then **Run**.

## Done when
**Check** confirms the cost maths and the logging (no API call needed).
