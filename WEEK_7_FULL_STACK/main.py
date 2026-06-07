from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI()


# initialise the database
def init():
    conn = sqlite3.connect("job_board.db")
    cursor = conn.cursor()
    # create tables users and jobs if they don't already exist
    try:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS jobs
            (id INTEGER PRIMARY KEY,
            user_id INT
            job_name TEXT,
            company TEXT,
            date_posted TEXT,
            description TEXT),
            FOREIGN KEY (user_id) REFERENCES users(id)"""
        )
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users 
            (id INTEGER PRIMARY KEY, 
            full_name TEXT,
            email TEXT,
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
