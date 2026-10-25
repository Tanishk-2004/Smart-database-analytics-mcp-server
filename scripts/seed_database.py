
import os

import psycopg
from dotenv import load_dotenv
from faker import Faker

load_dotenv()

fake = Faker("en_IN")

try:
    with psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    ) as conn:

        with conn.cursor() as cur:
            for _ in range(20):
                full_name = fake.name()
                email = f"{fake.uuid4()}@example.com"
                city = fake.city()

                cur.execute(
                    """
                    INSERT INTO customers (full_name, email, city)
                    VALUES (%s, %s, %s)
                    """,
                    (full_name, email, city),
                )

        print("Database connection successful!")
        print("20 customers inserted successfully!")

except psycopg.Error as e:
    print("Database operation failed!")
    print(e)

