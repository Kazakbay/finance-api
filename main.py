from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import Transaction, User
from schemas import UserCreate, UserResponse, TransactionCreate, TransactionResponse
from dotenv import load_dotenv
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    get_db
)
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()




@app.get("/")
def home():
    return {"message": "Finance API working"}


# --- Authentication ---
@app.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with same email already exist"
        )

    new_user = User(
        email=user_data.email,
        hashed_password = hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login")
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid email or password'
        )

    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


# --- Transactions (secured endpoints) ---

@app.post("/add", response_model=TransactionResponse)
def add_transaction(
        transaction_data: TransactionCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
        ):

    transaction = Transaction(
        amount = transaction_data.amount,
        category = transaction_data.category,
        user_id = current_user.id
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


@app.get("/list", response_model=list[TransactionResponse])
def get_transactions(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == current_user.id)
        .all()
    )
    return transactions


@app.delete("/delete/{transaction_id}")
def delete_transaction(
        transaction_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):

    transaction = (db.query(Transaction)
                   .filter(Transaction.id == transaction_id,
                           Transaction.user_id == current_user.id)
                   .first())
    if not transaction:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Transaction not found"
        )
    db.delete(transaction)
    db.commit()
    return {"message": f"Transaction {transaction_id} deleted"}

@app.put("/update/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
        transaction_id: int,
        transaction_data: TransactionCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
    transaction = (
        db.query(Transaction)
        .filter(
            Transaction.id == transaction_id,
            Transaction.user_id == current_user.id
        )
        .first()
    )
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Transaction not found'
        )
    transaction.amount = transaction_data.amount
    transaction.category = transaction_data.category
    db.commit()
    db.refresh(transaction)
    return transaction
