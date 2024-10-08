import json
import time
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from .DB import DB


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
    semaphore = asyncio.Semaphore(15)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(fetch(session, url[1], sem=semaphore))
        htmls = await asyncio.gather(*tasks)
    return htmls


async def main():
    db = DB()
    url = db.get_url()
    htmls = await task(url)
    res = []
    for i, j in zip(htmls, url):
        res.append(parser(i, j[0]))
    db.update(res)
    db.close()


def parser(html, id):
    if html is None:
        return None, id
    soup = BeautifulSoup(html, "html.parser")
    img = soup.find(class_="picture-container__picture").get("src")
    return img, id


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    print(f"Time taken main() {time.time()-start}")
