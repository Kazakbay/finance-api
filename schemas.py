from pydantic import BaseModel, EmailStr

# --- User ---

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str

    model_config = {"from_attributes": True}


# --- Transaction ---

class TransactionCreate(BaseModel):
    amount: float
    category: str

    model_config = {"from_attributes": True}

class TransactionResponse(BaseModel):
    id: int
    amount: float
    category: str

    model_config = {"from_attributes": True}