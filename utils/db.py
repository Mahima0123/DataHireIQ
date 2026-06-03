import psycopg2


def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5434,
        database="datahireiq",
        user="datahireiq_user",
        password="datahireiq_pass"
    )