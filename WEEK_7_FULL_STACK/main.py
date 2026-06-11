from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from auth import get_db, get_current_user, router as auth_router
import sqlite3


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)


class createJob(BaseModel):
    job_name: str
    company: str
    date_posted: str
    description: str


# initialise the database
def init():
    conn, cursor = get_db()
    # create tables users and jobs if they don't already exist
    try:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users 
            (id INTEGER PRIMARY KEY, 
            full_name TEXT,
            email TEXT UNIQUE,
            password TEXT, 
            date_of_birth TEXT, 
            current_occupation TEXT)"""
        )
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS jobs
            (id INTEGER PRIMARY KEY,
            user_id INT,
            job_name TEXT,
            company TEXT,
            date_posted TEXT,
            description TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id))"""
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        conn.rollback()
        conn.close()
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.on_event("startup")
def startup():
    init()


# /jobs endpoint to view all jobs listed on the server
@app.get("/jobs")
def get_jobs():
    conn, cursor = get_db()
    try:
        cursor.execute("SELECT job_name, company, date_posted, description FROM jobs")
        list_of_jobs = cursor.fetchall()
        conn.close()
        return list_of_jobs
    except sqlite3.Error:
        conn.rollback()
        conn.close()
        raise HTTPException(status_code=500, detail="Internal Server Error")


# /create_job enables posting jobs by users to the server
@app.post("/create_job")
def create_job(job_info: createJob, user=Depends(get_current_user)):
    conn, cursor = get_db()
    try:
        cursor.execute(
            """INSERT INTO jobs 
            (user_id, job_name, company, date_posted, description)
            VALUES
            (?, ?, ?, ?, ?)""",
            (
                user["sub"],
                job_info.job_name,
                job_info.company,
                job_info.date_posted,
                job_info.description,
            ),
        )
        conn.commit()
        conn.close()
        return {"Status": "success"}
    except Exception as e:
        print(e)
        conn.rollback()
        conn.close()
        raise HTTPException(status_code=500, detail="Internal Server Error")
