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
    return {"message": "Added", "category": category, "amount": amount}

@app.get("/list")
def get_transactions(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()
    return {"transactions": [{"id": t.id, "amount": t.amount, "category": t.category} for t in transactions]}

@app.delete("/delete/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        return {"error": "Transaction is not found "}
    db.delete(transaction)
    db.commit()
    return {"message": f"Transaction {transaction_id} deleted"}

@app.put("/update/{transaction_id}")
def update_transaction(transaction_id: int, amount: float = None, category: str = None, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        return {"error": "Transaction is not found"}
    if amount:
        transaction.amount = amount
    if category:
        transaction.category = category
    db.commit()
    return {"message": "Updated", "id": transaction_id, "amount": transaction.amount, "category": transaction.category}