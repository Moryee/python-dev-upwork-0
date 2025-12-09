Create very simple flask application with /transform endpoint, that satisfies the following document. Make it step by step just like contract described, include only code without your explanation.

# File structure

main.py — the FastAPI/Flask service
requirements.txt - with all dependencies, use venv to handle them
test_transform.py
README.md - 3 lines: how to run the API, use latest 3.13

# The document:
```
# Contract 1
## What goes in
- Required fields: `"text"`
- Optional fields: none
- Expected types: only valid JSON mandatory field `"text"` containing a string.
- Unknown fields: are accepted, but won't be used in the endpoint.

## Guarantees & Invariants
- `count` == length of the `tokens` array
- Every token in `tokens` can be any case, they are split by whitespaces.
- `has_numbers` is true if and only if the original input text contained at least one digit.
- Tokens are returned in the exact order they appeared in the input.

## Error behavior
- Missing `text` -> 400 with `{"error": "missing required field 'text'"}`
- `text` not a string -> 400
- Non-JSON body -> 400

## Example that fully respects the contract
```json
POST /transform
{ "text": "Hello world" }
->
{
  "tokens": ["hello", "world"],
  "count": 2,
  "has_numbers": false
}
```

# Contract 2, new feature

I'm changing my contract. Because the client requires new feature and we need to support multiple languages.

## What this change breaks (backwards compatibility impact)
- When clients sending only text parameter or any other additional parameter, it works exactly as before, no breaking change
- When new clients want other languages and send language parameter, they will get exactly what they ask for.

## What Goes In (Request)
- Requiried fields: `"text"` (string)
- Optional fields: `"language"` (string) - default value = `"english"`
- Allowed values for `language`: `"english"`, `"spanish"`
- Expected types: JSON object
- Unknown fields: are accepted, but won't be used in the endpoint.

## Guarantees & Invariants, updated
- `count` == length of the `tokens` array -> still true
- `has_numbers` is true if and only if the original input text contained at least one digit -> still true.
- Every token in `tokens` can be any case, they are split by whitespaces -> still true.
- Tokens are returned in the exact order they appeared in the input - still true.
- Tokens are using language-specific rules:
  - `"english"`: classic ASCII
  - `"spanish"`: correctly handles ñ → ñ, á → á (preserves accents when appropriate) and uses Spanish-aware

## Error behavior, unchanged except for new field
- Missing `text` -> 400 with `{"error": "missing required field 'text'"}`
- `text` not a string -> 400
- Non-JSON body -> 400
- Invalid `language` value -> 400 with `{"error": unsupported language}`

## Examples under the new contract

1. Old request (still works 100% identically)
```json
{ "text": "Hello world" }
->
{ "tokens": ["hello", "world"], "count": 2, "has_numbers": false }
```

2. New Spanish request
```json
{ "text": "¡Hola mundo cruel!", "language": "spanish" }
->
{ "tokens": ["¡hola", "mundo", "cruel!"], "count": 3, "has_numbers": false }
```

```