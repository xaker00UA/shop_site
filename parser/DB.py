import psycopg2 as ps
import time
from .config import DB_CONNECTION


class DB:
    def __init__(self):
        try:
            self.connection = ps.connect(**DB_CONNECTION)
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(f"Failed to connect to the database: {e}")
            raise Exception("Failed to connect to the database")

    def add_product(self, products: list):

        query = f"""
            INSERT INTO "product" (name, price, url, category_id, image_url, seller_id)
            VALUES (%s, %s, %s, %s, %s, %s) 
        """
        items = [
            (
                product["name"],
                product["price"],
                product["url"],
                product["category_id"],
                product["image"],
                product["seller_id"],
            )
            for product in products
        ]

        self.cursor.executemany(query, items)
        self.connection.commit()

    def get_category(self):
        query = "Select name from category"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    def get_url(self):
        query = "SELECT id, url from product WHERE image_url is null "
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    def update(self, res):
        query = """Update product
        SET image_url=%s
        Where id=%s

        """

        self.cursor.executemany(query, res)
        self.connection.commit()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
