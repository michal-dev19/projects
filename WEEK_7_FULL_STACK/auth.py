import bcrypt
import sqlite3
from jose import jwt, JWTError
from fastapi import Header, Depends, HTTPException, APIRouter
from pydantic import BaseModel

# use a router object to route current functions/decorators to 'app' in main
router = APIRouter()

SECRET_KEY = "JFO39084S0D9V23INJBT09U4S"
ALGORITHM = "HS256"


class CreateUser(BaseModel):
    email: str
    password: str


# establish the connection to the db via a helper function
def get_db():
    conn = sqlite3.connect("job_board.db")
    cursor = conn.cursor()
    return conn, cursor


# hashes input password
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


# creates a signed token for the user
def create_token(id: str) -> str:
    try:
        return jwt.encode({"sub": id}, SECRET_KEY, ALGORITHM)
    except JWTError:
        raise HTTPException(status_code=500, detail="Internal Server Error")


# authorises user
def get_current_user(authorisation: str = Header()):
    id = authorisation.split(" ")[1]
    try:
        return jwt.decode(id, SECRET_KEY, ALGORITHM)
    except JWTError:
        raise HTTPException(status_code=401, detail="Unauthorized")


# this operation registers the user's email and password in the job_board database
@router.post("/register")
def register_user(register_info: CreateUser):
    conn, cursor = get_db()
    try:
        cursor.execute(
            """INSERT INTO users 
            (email, password) VALUES (?, ?)""",
            (register_info.email, hash_password(register_info.password)),
        )
        conn.commit()
        conn.close()
        return {"Status": "success"}
    except sqlite3.IntegrityError:
        conn.rollback()
        conn.close()
        raise HTTPException(status_code=400, detail="Bad Request")


# this operation verifies the user's input before logging them in
@router.post("/login")
def login_user(login_info: CreateUser):
    conn, cursor = get_db()
    try:
        cursor.execute(
            "SELECT id, email, password FROM users WHERE email=?", (login_info.email)
        )
        user_credentials = cursor.fetchone()
        if user_credentials is None:
            raise HTTPException(status_code=400, detail="Bad Request")
        if bcrypt.checkpw(
            login_info.password.encode("utf-8"), user_credentials[1].encode("utf-8")
        ):
            conn.close()
            return create_token(str(user_credentials[0]))
        conn.close()
    except sqlite3.Error:
        conn.rollback()
        conn.close()
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/me")
def me(user=Depends(get_current_user)):
    return user
