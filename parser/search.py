import aiohttp
import asyncio
from bs4 import BeautifulSoup
from .DB import DB
import time
from decimal import Decimal


async def fetch(session, url, page):
    async with session.get(url + f"page={page}") as response:
        return await response.text()


async def task(category="computers"):
    tasks = []
    async with aiohttp.ClientSession() as session:
        url = f"https://hard.rozetka.com.ua/ua/" + category
        one_page = await fetch(session, url, 1)
        count_pages = check_page(one_page)
        for page in range(1, count_pages + 1):  # 68 pages
            tasks.append(fetch(session, url, page))
        htmls: list[str] = await asyncio.gather(*tasks)
    return htmls


def check_count_products():
    pass


def check_page(html):
    soup = BeautifulSoup(html, "html.parser")
    pages = soup.find_all(class_="pagination__item ng-star-inserted")[-1].text
    return int(pages)


def parse(string, category_id, seller_id):
    def parse_html(string, category_id, seller_id):
        soup = BeautifulSoup(string, "html.parser")
        products = soup.find_all(
            "li",
            class_="catalog-grid__cell catalog-grid__cell_type_slim ng-star-inserted",
        )
        res = []
        for product in products:
            name = product.find("span", class_="goods-tile__title").text
            url = product.find(
                class_="product-link goods-tile__picture",
            ).get("href")
            price = product.find("span", class_="goods-tile__price-value").text
            images = product.find_all(class_="product-link goods-tile__picture")

            for image in images:
                if image.img and image.img.get("src").endswith(".jpg"):
                    jpg_image_url = image.img.get("src")
                    break
                else:
                    jpg_image_url = None
            price = Decimal(price.replace("\xa0", "").replace("₴", ""))
            res.append(
                {
                    "name": name,
                    "price": price,
                    "url": url,
                    "image": jpg_image_url,
                    "seller_id": seller_id,
                    "category_id": category_id,
                }
            )
        return res

    results = []
    for h in string:
        results.extend(parse_html(h, category_id, seller_id))
    return results


async def main():
    products = []
    htmls = []
    List_url = [("notebooks/c80004/", 4, 1), ("tablets/c130309/", 3, 1)]
    for url in List_url:
        htmls.append(await task(url[0]))
    for html, url in zip(htmls, List_url):
        products.extend(parse(html, category_id=url[1], seller_id=url[2]))
    db = DB()
    db.add_product(products)
    db.close()
    return True


if __name__ == "__main__":
    start_time = time.time()
    data = asyncio.run(main())
    end_time = time.time()
    print(f"Time: {end_time - start_time} seconds")
