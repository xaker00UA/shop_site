import json
import time
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from .DB import DB
import logging

logger = logging.getLogger(__name__)


async def fetch(session, url, sem):
    async with sem:
        try:
            async with session.get(
                url, timeout=aiohttp.ClientTimeout(total=4)
            ) as response:
                return await response.text()
        except aiohttp.ClientError as e:
            print(f"Client error: {e}")
        except asyncio.TimeoutError:
            print(f"Timeout error for URL: {url}")


async def task(urls):
    semaphore = asyncio.Semaphore(20)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(fetch(session, url[1], sem=semaphore))
        htmls = await asyncio.gather(*tasks)
    return htmls


async def main():
    db = DB()

    while True:
        url = db.get_url()
        if not url:
            break
        htmls = await task(url)
        res = []
        for i, j in zip(htmls, url):
            res.append(parser(i, j[0]))
        db.update(res)
    db.close()


def parser(html, id):
    if html is None:
        return None, None, id
    soup = BeautifulSoup(html, "html.parser")
    try:
        description = soup.find("div", class_="ng-tns-c376246349-6")
        description2 = description.find("div", class_="ng-tns-c376246349-6")
        if description2:
            description = str(description2) if description2 else None
        description = str(description) if description else None
    except:
        description = "default"
    try:
        img = soup.find(class_="simple-slider__item ng-star-inserted")
        img_tag = img.find("img", class_="image").get("src", "default")
    except:
        img_tag = "default"
        logger.warning(f"ID product={id}, is not a image")

    return description, img_tag, id


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    print(f"Time taken main() {time.time()-start}")
