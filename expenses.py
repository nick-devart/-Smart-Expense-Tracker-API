from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from src.models import Expense, ExpenseCreate, TotalSummary, CategorySummary
from src import store

router = APIRouter()


@router.post("/", response_model=Expense, status_code=201)
def add_expense(payload: ExpenseCreate):
    """Add a new expense."""
    expense = Expense(**payload.model_dump())
    return store.add(expense)


@router.get("/", response_model=list[Expense])
def list_expenses(category: Optional[str] = Query(None, description="Filter by category")):
    """View all expenses, optionally filtered by category."""
    expenses = store.get_all()
    if category:
        expenses = [e for e in expenses if e.category.lower() == category.lower()]
    return expenses


@router.get("/summary", response_model=TotalSummary)
def get_summary(category: Optional[str] = Query(None, description="Summarize by specific category")):
    """Calculate total expenses overall and by category."""
    expenses = store.get_all()
    if category:
        expenses = [e for e in expenses if e.category.lower() == category.lower()]

    total = sum(e.amount for e in expenses)
    count = len(expenses)

    # Group by category
    category_map: dict[str, list[float]] = {}
    for e in expenses:
        category_map.setdefault(e.category, []).append(e.amount)

    by_category = [
        CategorySummary(category=cat, total=sum(amounts), count=len(amounts))
        for cat, amounts in category_map.items()
    ]

    return TotalSummary(total=total, count=count, by_category=by_category)


@router.delete("/{expense_id}", status_code=204)
def delete_expense(expense_id: str):
    """Delete an expense by ID."""
    if not store.delete(expense_id):
        raise HTTPException(status_code=404, detail="Expense not found")
