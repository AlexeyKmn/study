import time
import aiofiles
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import os


async def write_file(session, url, img_name):  # корутина сохранения файла
    async with aiofiles.open(f'images/{img_name}', mode='wb') as f:  # асинхронно открываем
        async with session.get(url) as response:
            # iter_chunked - Iterates over data chunks(куски) with maximum size limit
            async for x in response.content.iter_chunked(1024):
                await f.write(x)  # асинхронный метод write (по кускам)
        print(f'Изображение сохранено {img_name}')


async def main():  # корутина main - точка входа
    url = 'https://parsinger.ru/asyncio/aiofile/2/index.html'
    img_urls, tasks = [], []
    async with aiohttp.ClientSession() as session:  # открываем сессию
        async with session.get(url) as response:  # получаем содержимое
            soup = BeautifulSoup(await response.text(), 'lxml')  # асинхронно (ожидая ответа сервера) передаём lxml
            pagen = [f'https://parsinger.ru/asyncio/aiofile/2/{x["href"]}' for x in soup.find_all(class_="lnk_img")]
            for link in pagen:
                async with session.get(link) as response2:
                    soup2 = BeautifulSoup(await response2.text(), 'lxml')
                    img_urls.extend([x['src'] for x in soup2.find_all('img')])
                    # asyncio.create_task(write_file(session, url, img_name))
            tasks = [asyncio.create_task(write_file(session, link, link.split('/')[6])) for link in img_urls]
            await asyncio.gather(*tasks)  # скармливаем методу gather


if __name__ == '__main__':
    start = time.perf_counter()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
    print(f'Cохранено изображений {len(os.listdir("images/"))} за {round(time.perf_counter() - start, 3)} сек')


    def get_folder_size(filepath, size=0):
        for root, dirs, files in os.walk(filepath):
            for f in files:
                size += os.path.getsize(os.path.join(root, f))
        return size


    print(get_folder_size('images/'))
