from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, Transaction

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Finance API working"}


@app.post("/add")
def add_transaction(amount: float, category: str, db: Session = Depends(get_db)):
    transaction = Transaction(amount=amount, category=category)
    db.add(transaction)
    db.commit()
    return {"message": "Added", "transaction": transaction, "category": category}

@app.get("/list")
def get_transactions(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()
    return {"transactions": [{"id": t.id, "amount": t.amount, "category": t.category} for t in transactions]}