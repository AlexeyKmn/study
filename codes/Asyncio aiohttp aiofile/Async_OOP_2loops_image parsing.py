import aiofiles
import asyncio
import aiohttp
from aiohttp_retry import RetryClient, ExponentialRetry
from bs4 import BeautifulSoup
import os
import re
import requests
from tqdm import tqdm


class AsyncImagesDownloader:
    def __init__(self):
        self._domain, self._path = None, None
        self._total_size = 0
        self._links, self._nested_links = [], []

    def _get_links(self, url):
        """get all links from the start page into self._links"""
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        raw_links = map(lambda attr: attr['href'], soup.find_all('a'))
        self._links = [f'{self._domain}{link}' for link in raw_links]

    async def _get_all_links(self, session, url):
        """async gets all links from the nested pages into self._nested_links"""
        async with session.get(url) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')
            raw_links = map(lambda attr: attr['href'], soup.find_all('a'))
            self._nested_links.extend([f'{self._domain}depth2/{link}' for link in raw_links])

    async def _download_img(self, session, url, img_name):
        """async saving of the image"""
        async with aiofiles.open(f'{self._path}/{img_name}.jpg', 'wb') as file:
            async with session.get(url) as response:
                async for chunck in response.content.iter_chunked(3072):  # size of chunk
                    await file.write(chunck)

    async def _find_images(self, session, url, pbar):
        """async func, finds hrefs and downloads the images"""
        retry_options = ExponentialRetry(attempts=5)
        retry_client = RetryClient(raise_for_status=False, retry_options=retry_options, client_session=session,
                                   start_timeout=0.5)

        async with retry_client.get(url) as page_response:
            if page_response.ok:
                p_response = await page_response.text()
                p_soup = BeautifulSoup(p_response, 'lxml')
                images_links = map(lambda x: x['src'], p_soup.find_all('img'))
                for img_url in images_links:
                    # (?<=re) - text after re, (?:re) - zero-width (na cathc) group (greedy), (?=re) - text before re
                    img_name = re.search(r'(?<=img\/)(?:.+)(?=\.jpg)', img_url).group()
                    if not os.path.exists(f'{self._path}/{img_name}.jpg'):  # check whether the file already exists
                        pbar.update(1)
                        await self._download_img(retry_client, img_url, img_name)

    async def _main(self):
        """entry point with gather methods and tqdm status bar"""
        os.mkdir(self._path)  # os.mkdir("c://somedir/hello") syntax for direct paths
        async with aiohttp.ClientSession() as session:
            tasks_1 = [asyncio.create_task(self._get_all_links(session, link)) for link in self._links]
            await asyncio.gather(*tasks_1)
            print(f'{len(self._nested_links)} links collected. Starting download')
            dload_bar = tqdm(total=2_615, desc='Обработано изображений: ')  # tqdm status bar object
            tasks_2 = [asyncio.create_task(self._find_images(session, link, dload_bar)) for link in self._nested_links]
            await asyncio.gather(*tasks_2)
            dload_bar.close()

    def _get_folder_size(self, filepath):
        """Returns total size of downloaded images"""
        for root, dirs, files in os.walk(filepath):
            for f in files:
                self._total_size += os.path.getsize(os.path.join(root, f))

    def __call__(self, default_args):
        self._domain = default_args.get('domain')  # constant part of url
        self._path = default_args.get('folder_path')  # directory for saving
        self._get_links(default_args.get('url'))  # get all links from start page

        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(self._main())
        self._get_folder_size(self._path)
        print(f'Общий размер скачанных изображений: {self._total_size}')


parser_args = {'domain': 'https://parsinger.ru/asyncio/aiofile/3/',
               'url': 'https://parsinger.ru/asyncio/aiofile/3/index.html',
               'folder_path': 'images'
               }

image_dowloader = AsyncImagesDownloader()
image_dowloader(default_args=parser_args)
