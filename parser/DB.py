import psycopg2 as ps
import time
from .config import DB_CONNECTION


class DB:
    def __init__(self):
        try:
            self.connection: ps.connect = ps.connect(**DB_CONNECTION)
            self.cursor = self.connection.cursor()
            self.create()
        except Exception as e:
            print(f"Failed to connect to the database: {e}")
            raise Exception("Failed to connect to the database")

    def create(self):
        existing_categories = self.get_category()  # Получаем существующие категории
        res = ["Телефон", "Компьютер", "Планшет", "Ноутбук"]

        for category in res:
            if (
                category not in existing_categories
            ):  # Проверяем, отсутствует ли категория
                query = f"""
                INSERT INTO "category" (name)
                VALUES ('{category}') 
                RETURNING id
                """
                self.cursor.execute(query)
                category_id = self.cursor.fetchone()[0]
                print(f"Создана новая категория: {category}, ID: {category_id}")
        self.connection.commit()

    def get_id_categories(self):
        query = "SELECT id, name FROM category"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return {d[1]: d[0] for d in data}

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
        return [row[0] for row in data]

    def get_url(self):
        query = "SELECT id, url from product WHERE image_url is null LIMIT 100"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    def update(self, res):
        query = """Update product
        SET description=%s,
        image_url=%s
        Where id=%s
        """
        try:
            self.cursor.executemany(query, res)
            print("Обновлены описания и изображения товаров")
        except Exception as e:
            print(e)
            print(
                "Ошибка при выполнении запроса на изменение описания и изображения товара"
            )
        finally:
            self.connection.commit()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
