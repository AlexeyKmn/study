import requests
import time
import aiofiles
import asyncio
import aiohttp

url = 'https://parsinger.ru/asyncio/aiofile/1/video/nu_pogodi.mp4'


def sync_write():
    with open('video/sync_video_async.mp4', 'wb') as video:
        response = requests.get(url, stream=True)
        for piece in response.iter_content(chunk_size=5120):
            video.write(piece)


async def async_write():
    async with aiohttp.ClientSession() as session:
        async with aiofiles.open('video/async_video_async.mp4', mode='wb') as video:
            async with session.get(url) as response:
                async for piece in response.content.iter_chunked(5120):
                    await video.write(piece)


start = time.perf_counter()
sync_write()
print(f'Cохранено синхронным способом за {round(time.perf_counter() - start, 3)} сек')

start = time.perf_counter()
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(async_write())
print(f'Cохранено асинхронным способом за {round(time.perf_counter() - start, 3)} сек')

# Результат
# Cохранено синхронным способом за 217.121 сек
# Cохранено асинхронным способом за 240.855 сек
