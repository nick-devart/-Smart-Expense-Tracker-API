from fastapi import FastAPI
from src.routers import expenses
app = FastAPI(
    title="Smart Expense Tracker API",
    description="A REST API to manage personal expenses",
    version="1.0.0",
)
app.include_router(expenses.router, prefix="/expenses", tags=["expenses"])
@app.get("/")
def root():
    return {"message": "Smart Expense Tracker API is running"}
