# Smart Expense Tracker API

A REST API to manage personal expenses, built with Python and FastAPI.

## Stack

- Python 3.11+
- FastAPI
- Pydantic v2
- In-memory storage (no database required)
- pytest + httpx for testing

## Install

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Run the server

```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`.

Interactive docs (Swagger UI): `http://localhost:8000/docs`

## Run the tests

```bash
pytest tests/
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/expenses/` | Add a new expense |
| GET | `/expenses/` | List all expenses |
| GET | `/expenses/?category=Food` | Filter expenses by category |
| GET | `/expenses/summary` | Total expenses (overall and by category) |
| GET | `/expenses/summary?category=Food` | Summary for a specific category |
| DELETE | `/expenses/{id}` | Delete an expense by ID |

## Expense Schema

```json
{
  "title": "Lunch",
  "amount": 12.50,
  "category": "Food",
  "date": "2026-07-01"
}
```

- `title` — string, required
- `amount` — float, must be > 0
- `category` — string, required
- `date` — date string in `YYYY-MM-DD` format

## Example Usage

**Add an expense**
```bash
curl -X POST http://localhost:8000/expenses/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Lunch", "amount": 12.50, "category": "Food", "date": "2026-07-01"}'
```

**List all expenses**
```bash
curl http://localhost:8000/expenses/
```

**Filter by category**
```bash
curl http://localhost:8000/expenses/?category=Food
```

**Get summary**
```bash
curl http://localhost:8000/expenses/summary
```

**Delete an expense**
```bash
curl -X DELETE http://localhost:8000/expenses/<id>
```
