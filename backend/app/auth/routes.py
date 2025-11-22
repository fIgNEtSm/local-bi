from fastapi import APIRouter, HTTPException
from app.auth.schemas import RegisterIn, LoginIn
from app.auth.hashing import Hash
from app.auth.jwt_handler import create_token

router = APIRouter(tags=["Auth"])

fake_users_db = {}

@router.post("/register")
def register(data: RegisterIn):
    if data.email in fake_users_db:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_pw = Hash.encrypt(data.password)
    fake_users_db[data.email] = {
        "name": data.name,
        "email": data.email,
        "password": hashed_pw
    }

    token = create_token(data.email)
    return {"access_token": token}


@router.post("/login")
def login(data: LoginIn):
    user = fake_users_db.get(data.email)
    if not user:
        raise HTTPException(404, "User not found")

    if not Hash.verify(user["password"], data.password):
        raise HTTPException(401, "Incorrect password")

    token = create_token(data.email)
    return {"access_token": token}
