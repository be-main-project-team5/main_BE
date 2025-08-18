import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

try:
    print("Attempting to connect to the database...")
    print(f"DB_NAME: {os.getenv('POSTGRES_DB')}")
    print(f"DB_USER: {os.getenv('POSTGRES_USER')}")
    print(f"DB_PASSWORD: {os.getenv('POSTGRES_PASSWORD')}")
    print(f"DB_HOST: {os.getenv('DB_HOST')}")
    print(f"DB_PORT: {os.getenv('DB_PORT')}")

    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    print("\nDatabase connection successful!")
    conn.close()
except Exception as e:
    print(f"\nDatabase connection failed: {e}")
