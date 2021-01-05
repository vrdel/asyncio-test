#!/usr/bin/python3

import aiohttp
import asyncio
import time


url_beer = 'https://random-data-api.com/api/beer/random_beer'
url_crypto = 'https://random-data-api.com/api//crypto_coin/random_crypto_coin'


def write_file(suffix, content):
    with open(f'file-{suffix}', 'a') as fn:
        fn.write(content)
        fn.write("\n")


async def aiohttp_get(url):
    epoch_seconds = time.time()

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(resp.status, f'{time.ctime()}')
            content = await resp.text()
            return content


async def wrap_one(url, suffix):
    print('wrap_one - started -', f'{time.ctime()}')
    await asyncio.sleep(1)
    data = await aiohttp_get(url)
    write_file(suffix, data)


async def wrap_two(url, suffix):
    print('wrap_two - started -', f'{time.ctime()}')
    await asyncio.sleep(5)
    data = await aiohttp_get(url)
    write_file(suffix, data)


async def wrap(suffix, urlo, urlt):
    await wrap_one(urlo, suffix)
    await wrap_two(urlt, suffix)


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        # sequential
        loop.run_until_complete(wrap(time.time(), url_beer, url_crypto))

        # concurrent
        suffix = time.time()
        loop.run_until_complete(asyncio.gather(
            wrap_one(url_beer, suffix),
            wrap_two(url_crypto, suffix)
        ))
    finally:
        loop.close()
