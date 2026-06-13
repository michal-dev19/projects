import os
import psycopg2
from dotenv import load_dotenv

# load .env, get DATABASE_URL
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


# establish the connection to the db via a helper function
def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    return conn, cursor
