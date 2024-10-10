import asyncio
from .run import main
from .search import main as page_pars
import logging

logging.basicConfig(
    level=logging.INFO,
    format="|%(asctime)s| - |%(name)s| - |%(levelname)s| - %(message)s",
)
logger = logging.getLogger(__name__)


async def tasks():
    # await page_pars()
    # print("Странички пропасены")
    logger.info("Запуск парсера сайта")
    await main()
    print("Парсинг завершен")
    logger.info("Парсер сайта завершен")


def run_parser_site():
    asyncio.run(tasks())


if __name__ == "__main__":
    run_parser_site()
