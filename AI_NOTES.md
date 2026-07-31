# AI Usage Notes

## Which parts were AI-generated vs. written by me

This project was built with significant AI assistance .Here's the breakdown:

AI-generated:
- Initial project scaffold and file structure
- `src/models.py` — Pydantic models for `Expense`, `ExpenseCreate`, `TotalSummary`, `CategorySummary`
- `src/store.py` — in-memory store with `get_all`, `add`, `delete`, `clear` functions
- `src/routers/expenses.py` — all five route handlers
- `src/main.py` — FastAPI app setup and router inclusion
- `tests/test_expenses.py` — the full test suite (20 tests covering happy paths and edge cases)
- `README.md` — structure, commands, and example curl calls
- `requirements.txt` and `requirements-dev.txt`

Written / shaped by me:
- The decision to use FastAPI over Flask (faster development, built-in validation and docs)
- Choosing in-memory storage with a module-level dict rather than a JSON file (simpler, no I/O concerns)
- The `clear()` function in `store.py` — added specifically to make tests fully isolated (AI initially proposed a global fixture that patched the dict, which was messier)
- Structuring the summary endpoint to accept an optional `category` query param rather than having two separate endpoints
- The decision to keep `category` filtering case-insensitive (`.lower()` comparison) — the AI's first draft was case-sensitive

## What I validated, tested, or changed

- Ran the full test suite and confirmed all 20 tests pass
- Verified the Swagger UI (`/docs`) renders correctly with all routes
- Tested the `summary` endpoint manually with curl to confirm the by-category breakdown is correct
- Confirmed the `autouse` fixture in tests resets state properly between tests — without this, test ordering affected results
- Checked that `amount: 0` returns 422 — the AI used `ge=0` (greater-than-or-equal) initially, which I changed to `gt=0` (strictly positive) since a zero-amount expense makes no sense
- Fixed a Pydantic 2.13 compatibility issue — the AI generated `Field(..., description="...")` on annotated fields, which newer Pydantic rejects. Simplified field definitions to remove the redundant positional `...` and description args that conflicted with the type annotation

## AI suggestions I decided not to use

- JSON file persistence — AI offered to add optional JSON file storage. I decided against it because the spec says in-memory is fine, and adding file I/O would complicate testing and introduce platform-specific path handling with no benefit here.
- A separate `GET /expenses/{id}` endpoint — AI included this by default. I removed it because the spec doesn't require it and keeping the surface minimal is better for a take-home scope.
- `patch_object` approach in tests — AI first suggested mocking the store dict with `unittest.mock.patch`. I replaced it with an explicit `store.clear()` fixture, which is simpler and tests the actual store logic rather than bypassing it.
- Docker support — AI offered to generate a `Dockerfile`. I skipped this as the bonus options say "pick at most one" and I judged the Swagger UI (already included via FastAPI) as the more useful built-in bonus.
