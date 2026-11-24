
import sqlite3
from pathlib import Path

# =====================================
# PriceHunter AI - Backend Core
# =====================================

APP_NAME = "PriceHunter AI"
VERSION = "0.2.0"

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_FILE = DATABASE_DIR / "pricehunter.db"


def connect_db():
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_FILE)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    with connect_db() as connection:
        schema_file = DATABASE_DIR / "schema.sql"
        schema = schema_file.read_text(encoding="utf-8")
        connection.executescript(schema)


def add_product(name, brand=None, category_id=None):
    with connect_db() as connection:
        cursor = connection.execute(
            """
            INSERT INTO products (name, brand, category_id)
            VALUES (?, ?, ?)
            """,
            (name, brand, category_id)
        )
        return cursor.lastrowid


def add_seller(name, shop_name=None):
    with connect_db() as connection:
        cursor = connection.execute(
            """
            INSERT INTO sellers (name, shop_name)
            VALUES (?, ?)
            """,
            (name, shop_name)
        )
        return cursor.lastrowid


def add_offer(product_id, seller_id, price, currency="IRR"):
    if price < 0:
        raise ValueError("Price cannot be negative.")

    with connect_db() as connection:
        cursor = connection.execute(
            """
            INSERT INTO offers
            (product_id, seller_id, price, currency)
            VALUES (?, ?, ?, ?)
            """,
            (product_id, seller_id, price, currency)
        )
        return cursor.lastrowid


def get_products():
    with connect_db() as connection:
        return connection.execute(
            """
            SELECT id, name, brand, model
            FROM products
            ORDER BY id DESC
            """
        ).fetchall()


def compare_prices(product_id):
    with connect_db() as connection:
        return connection.execute(
            """
            SELECT
                sellers.shop_name,
                sellers.name,
                offers.price,
                offers.currency
            FROM offers
            JOIN sellers ON offers.seller_id = sellers.id
            WHERE offers.product_id = ?
            ORDER BY offers.price ASC
            """,
            (product_id,)
        ).fetchall()


def main():
    initialize_database()

    print("=" * 40)
    print(APP_NAME)
    print("Version:", VERSION)
    print("Database initialized successfully.")
    print("=" * 40)


if __name__ == "__main__":
    main()
