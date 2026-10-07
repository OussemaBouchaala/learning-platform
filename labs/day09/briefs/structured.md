# JSON you can trust
**Topic:** schema in the prompt, validation on the way out, one retry with the error.

## Your mission
Turn listing text into a validated `Listing`, with one automatic retry.

## Steps
1. Fill `listings.json` with 10 real listings and your labels.
2. `Listing`: four optional fields.
3. `parse_listing`: `model_validate_json`, catch `ValidationError`.
4. `build_prompt`: the schema, the listing, and the previous error if any.
5. `extract`: try, retry once with the error, return `(listing, attempts)`.

## Done when
**Check** runs `extract` against fake models: valid, fixed on retry, and failing.
