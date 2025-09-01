import asyncio
import json
from typing import AsyncGenerator, Dict, Optional

import aiofiles
import aiohttp
from aiohttp import ClientError
from aiohttp.client_exceptions import ClientConnectionError, ServerTimeoutError

from week_1 import constants

# TODO \
#  Напишите асинхронную функцию fetch_urls, которая принимает файл со списком урлов \
#  (каждый URL адрес возвращает JSON) и сохраняет результаты выполнения в другой файл (result.jsonl), где ключами \
#  являются URL, а значениями — распарсенный json, при условии что статус код — 200. \
#  Используйте библиотеку aiohttp для выполнения HTTP-запросов.\
#  Требования:\
#  Ограничьте количество одновременных запросов до 5\
#  Обработайте возможные исключения (например, таймауты, недоступные ресурсы) ошибок соединения\
#  Контекст:\
#  Урлов в файле может быть десятки тысяч\
#  Некоторые урлы могут весить до 300-500 мегабайт\
#  При внезапной остановке и/или перезапуске скрипта - допустимо скачивание урлов по новой.


async def fetch_url(session: aiohttp.ClientSession, url: str) -> Optional[Dict]:
    try:
        async with session.get(url, timeout=constants.TIMEOUT) as response:
            if response.status == 200:
                data = await response.json()
                return {"url": url, "content": data}
            else:
                print("Status error %s for URL: %s" % (response.status, url))
                return None
    except ClientConnectionError:
        print("Connection error for URL: %s" % url)
        return None
    except (ServerTimeoutError, asyncio.TimeoutError) as e:
        print("Timeout error for URL: %s. Error %s" % (url, e))
        return None
    except json.JSONDecodeError:
        print("Decode error for URL: %s" % url)
        return None
    except ClientError:
        print("Client error for URL: %s" % url)
        return None


async def read_urls(file_path: str) -> AsyncGenerator[str, None]:
    async with aiofiles.open(file_path, "r") as file:
        async for line in file:
            yield line.strip()


async def fetch_urls(input_file: str, output_file: str):
    semaphore = asyncio.Semaphore(constants.MAX_CONCURRENT_REQUESTS)

    async def bounded_fetch(url: str) -> dict:
        async with semaphore:
            return await fetch_url(session, url)

    async with aiohttp.ClientSession() as session:
        async with aiofiles.open(output_file, "w") as out_file:
            async for url in read_urls(input_file):
                result = await bounded_fetch(url)
                if result:
                    await out_file.write(json.dumps(result) + "\n")


if __name__ == "__main__":
    try:
        asyncio.run(fetch_urls("<URLS_FILE_NAME_THIS>", "./results.jsonl"))
    except KeyboardInterrupt:
        print("Script stopped by user")
    except UnicodeError as e:
        print("Error as %s" % e)
    except FileNotFoundError as e:
        print("File not found: %s" % e)
