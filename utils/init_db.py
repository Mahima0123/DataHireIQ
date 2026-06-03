from utils.db import get_connection


conn = get_connection()
cur = conn.cursor()

with open("sql/schema.sql", "r") as f:
    cur.execute(f.read())

conn.commit()

cur.close()
conn.close()

print("Database initialized successfully.")