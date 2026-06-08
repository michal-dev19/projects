from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from auth import get_db, router as auth_router
import sqlite3


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)


# initialise the database
def init():
    conn, cursor = get_db()
    # create tables users and jobs if they don't already exist
    try:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS jobs
            (id INTEGER PRIMARY KEY,
            user_id INT
            job_name TEXT,
            company TEXT,
            date_posted TEXT,
            description TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id))"""
        )
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users 
            (id INTEGER PRIMARY KEY, 
            full_name TEXT,
            email TEXT UNIQUE,
            password TEXT, 
            date_of_birth TEXT, 
            current_occupation TEXT)"""
        )
        conn.commit()
        conn.close()
    except RuntimeError:
        conn.rollback()
        conn.close()
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.on_event("startup")
def startup():
    init()


def seed():
    pass
