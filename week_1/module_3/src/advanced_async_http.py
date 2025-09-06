import asyncio
import json
from typing import AsyncGenerator, Dict, Optional
import aiofiles
import aiohttp
from aiohttp import ClientError
from aiohttp.client_exceptions import ClientConnectionError, ServerTimeoutError

from week_1 import constants


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
    except ClientError as e:
        print("Client error for URL: %s. Error %s" % (url, e))
        return None


async def read_urls(file_path: str) -> AsyncGenerator[str, None]:
    async with aiofiles.open(file_path, "r") as file:
        async for line in file:
            url = line.strip()
            if url:
                yield url


async def worker(session: aiohttp.ClientSession, queue: asyncio.Queue, output_file: aiofiles):
    while True:
        url = await queue.get()
        if url is None:
            queue.task_done()
            break
        result = await fetch_url(session, url)
        if result is not None:
            await output_file.write(json.dumps(result) + "\n")
        queue.task_done()


async def fetch_urls(input_file: str, output_file: str):
    queue = asyncio.Queue()

    async with aiohttp.ClientSession() as session:
        async with aiofiles.open(output_file, "w") as out_file:
            num_workers = constants.MAX_CONCURRENT_REQUESTS
            workers = [asyncio.create_task(worker(session, queue, out_file)) for _ in range(num_workers)]

            try:
                async for url in read_urls(input_file):
                    await queue.put(url)
            finally:
                for _ in workers:
                    await queue.put(None)

            await queue.join()
            await asyncio.gather(*workers, return_exceptions=True)


if __name__ == "__main__":
    try:
        asyncio.run(fetch_urls("urls.txt", "./results.jsonl"))
    except KeyboardInterrupt:
        print("Script stopped by user")
    except UnicodeError as e:
        print("Error as %s" % e)
    except FileNotFoundError as e:
        print("File not found: %s" % e)