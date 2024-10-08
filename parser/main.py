import asyncio
from run import main
from search import main as page_pars


async def tasks():
    await page_pars()
    await main()


def run_parser_site():
    asyncio.run(tasks())
