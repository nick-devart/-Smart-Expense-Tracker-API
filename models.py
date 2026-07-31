from pydantic import BaseModel, Field
from datetime import date
import uuid
class ExpenseCreate(BaseModel):
    title: str
    amount: float = Field(gt=0)
    category: str
    date: date
class Expense(ExpenseCreate):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
class CategorySummary(BaseModel):
    category: str
    total: float
    count: int
class TotalSummary(BaseModel):
    total: float
    count: int
    by_category: list[CategorySummary]
