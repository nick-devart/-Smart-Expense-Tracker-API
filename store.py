from src.models import Expense
_expenses: dict[str, Expense] = {}
def get_all() -> list[Expense]:
    return list(_expenses.values())
def get_by_id(expense_id: str) -> Expense | None:
    return _expenses.get(expense_id)
def add(expense: Expense) -> Expense:
    _expenses[expense.id] = expense
    return expense
def delete(expense_id: str) -> bool:
    if expense_id in _expenses:
        del _expenses[expense_id]
        return True
    return False
def clear():
    """Used in tests to reset state."""
    _expenses.clear()
