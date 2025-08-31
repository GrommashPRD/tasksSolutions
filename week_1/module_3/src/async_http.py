# TODO\
#  Напишите асинхронную функцию fetch_urls, которая принимает список URL-адресов и возвращает словарь, \
#  где ключами являются URL, а значениями — статус-коды ответов. \
#  Используйте библиотеку aiohttp для выполнения HTTP-запросов.\
#  Требования:\
#  Ограничьте количество одновременных запросов до 5 (используйте примитивы синхронизации из asyncio библиотеки)\
#  Обработайте возможные исключения (например, таймауты, недоступные ресурсы)\
#  и присвойте соответствующие статус-коды (например, 0 для ошибок соединения).\
#  Сохраните все результаты в файл

import asyncio
import json
from asyncio import Semaphore

import aiohttp
from aiohttp import ClientError, ClientTimeout

from week_1.module_3.src import constants


async def fetch_url(
    session: aiohttp.ClientSession, url: str, semaphore: Semaphore
) -> tuple[str, int]:
    try:
        async with semaphore:
            async with session.get(
                url,
                timeout=ClientTimeout(total=constants.TIMEOUT),
            ) as response:
                return url, response.status
    except (ClientError, asyncio.TimeoutError):
        return url, 0


async def fetch_urls(urls: list[str], file_path: str):
    results = {}
    semaphore = asyncio.Semaphore(constants.MAX_CONCURRENT_REQUESTS)

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url, semaphore) for url in urls]
        responses = await asyncio.gather(*tasks)

        for url, status in responses:
            results[url] = status

    with open(file_path, "w") as file:
        for url, status in results.items():
            file.write(json.dumps({"url": url, "status_code": status}) + "\n")


if __name__ == "__main__":
    urls = [
        "https://example.com",
        "https://httpbin.org/status/404",
        "https://nonexistent.url",
    ]
    asyncio.run(fetch_urls(urls, "./results.jsonl"))
