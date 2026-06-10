import os
from dotenv import load_dotenv
import psycopg2


def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )