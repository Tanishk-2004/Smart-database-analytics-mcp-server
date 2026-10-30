
import os
import random

import psycopg
from dotenv import load_dotenv
from faker import Faker
from datetime import datetime, timedelta, timezone

load_dotenv()

fake = Faker("en_IN")


def seed_customers(cur, number_of_customers=20):
    for _ in range(number_of_customers):
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

    print(f"{number_of_customers} customers inserted successfully!")


def seed_products(cur):
    products = [
        ("Wireless Mouse", "Electronics"),
        ("Mechanical Keyboard", "Electronics"),
        ("USB-C Cable", "Electronics"),
        ("Bluetooth Headphones", "Electronics"),
        ("Laptop Stand", "Electronics"),
        ("Smartphone Case", "Electronics"),
        ("Power Bank", "Electronics"),
        ("Webcam", "Electronics"),
        ("Portable Speaker", "Electronics"),
        ("Monitor", "Electronics"),
        ("Water Bottle", "Home & Kitchen"),
        ("Coffee Mug", "Home & Kitchen"),
        ("Lunch Box", "Home & Kitchen"),
        ("Electric Kettle", "Home & Kitchen"),
        ("Desk Lamp", "Home & Kitchen"),
        ("Bedsheet Set", "Home & Kitchen"),
        ("Storage Organizer", "Home & Kitchen"),
        ("Cooking Pan", "Home & Kitchen"),
        ("Pillow", "Home & Kitchen"),
        ("Table Clock", "Home & Kitchen"),
        ("Running Shoes", "Fashion"),
        ("Casual T-Shirt", "Fashion"),
        ("Jeans", "Fashion"),
        ("Backpack", "Fashion"),
        ("Wrist Watch", "Fashion"),
        ("Sunglasses", "Fashion"),
        ("Wallet", "Fashion"),
        ("Sports Jacket", "Fashion"),
        ("Belt", "Fashion"),
        ("Travel Bag", "Fashion"),
        ("Office Chair", "Furniture"),
        ("Study Table", "Furniture"),
        ("Bookshelf", "Furniture"),
        ("Folding Chair", "Furniture"),
        ("Side Table", "Furniture"),
        ("Notebook Set", "Stationery"),
        ("Ballpoint Pens", "Stationery"),
        ("Marker Set", "Stationery"),
        ("Sticky Notes", "Stationery"),
        ("File Organizer", "Stationery"),
        ("Yoga Mat", "Sports"),
        ("Dumbbell Set", "Sports"),
        ("Skipping Rope", "Sports"),
        ("Cricket Bat", "Sports"),
        ("Football", "Sports"),
        ("Badminton Racket", "Sports"),
        ("Resistance Bands", "Sports"),
        ("Cycling Helmet", "Sports"),
        ("Tennis Ball Set", "Sports"),
        ("Gym Gloves", "Sports"),
    ]

    for product_name, category in products:
        price = round(random.uniform(99, 9999), 2)
        stock_quantity = random.randint(0, 200)
        is_active = random.choice([True, True, True, False])

        cur.execute(
            """
            INSERT INTO products
                (product_name, category, price, stock_quantity, is_active)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (product_name, category, price, stock_quantity, is_active),
        )

    print(f"{len(products)} products inserted successfully!")



def seed_orders(cur, number_of_orders=300):
    
    cur.execute("SELECT customer_id FROM customers")
    customer_ids = [row[0] for row in cur.fetchall()]

    if not customer_ids:
        raise ValueError("No customers found. Seed customers first.")

    order_statuses = [
        "pending",
        "confirmed",
        "shipped",
        "delivered",
        "cancelled",
        "returned",
    ]

    now = datetime.now(timezone.utc)
    start_date = now - timedelta(days=365)

    for _ in range(number_of_orders):
        customer_id = random.choice(customer_ids)

        random_seconds = random.randint(
            0, int((now - start_date).total_seconds())
        )
        order_date = start_date + timedelta(seconds=random_seconds)

        status = random.choice(order_statuses)

        cur.execute(
            """
            INSERT INTO orders (customer_id, order_date, status)
            VALUES (%s, %s, %s)
            """,
            (customer_id, order_date, status),
        )

    print(f"{number_of_orders} orders inserted successfully!")


def seed_order_items(cur):

    # Step 1: Fetch existing order IDs
    cur.execute("SELECT order_id FROM orders ORDER BY order_id")
    order_ids = [row[0] for row in cur.fetchall()]

    if not order_ids:
        raise ValueError("No orders found. Seed orders first.")

    # Step 2: Fetch all products, including active and inactive
    cur.execute(
        """
        SELECT product_id, price
        FROM products
        ORDER BY product_id
        """
    )
    products = cur.fetchall()

    if not products:
        raise ValueError("No products found. Seed products first.")

    # Step 3: Generate and insert order items
    total_items = 0

    for order_id in order_ids:

        # Randomly select 1–5 unique products per order
        number_of_items = random.randint(
            1, min(5, len(products))
        )

        selected_products = random.sample(
            products, number_of_items
        )

        for product_id, price in selected_products:

            quantity = random.randint(1, 5)

            cur.execute(
                """
                INSERT INTO order_items
                    (order_id, product_id, quantity, unit_price)
                VALUES (%s, %s, %s, %s)
                """,
                (order_id, product_id, quantity, price),
            )

            total_items += 1

    print(
        f"{total_items} order items inserted "
        f"across {len(order_ids)} orders!"
    )




def main():
    try:
        with psycopg.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        ) as conn:

            with conn.cursor() as cur:
                seed_order_items(cur)

            print("Database connection successful!")

    except psycopg.Error as e:
        print("Database operation failed!")
        print(e)


if __name__ == "__main__":
    main()

