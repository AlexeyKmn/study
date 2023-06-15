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
        self._domain = None
        self._total_size = 0
        self._links = []

    def _get_all_links(self, url):
        """returns all links from the start page"""
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        raw_links = map(lambda attr: attr['href'], soup.find_all('a'))
        self._links.extend([f'{self._domain}{link}' for link in raw_links])

    async def _download_img(self, session, url, img_name):
        """async saving of the image"""
        async with aiofiles.open(f'images/{img_name}.jpg', 'wb') as file:
            async with session.get(url) as response:
                async for chunck in response.content.iter_chunked(3072):
                    await file.write(chunck)

    async def _find_images(self, session, url, pbar):
        """async download func for images"""
        retry_options = ExponentialRetry(attempts=5)
        retry_client = RetryClient(raise_for_status=False, retry_options=retry_options, client_session=session,
                                   start_timeout=0.5)

        async with retry_client.get(url) as page_response:
            if page_response.ok:
                p_response = await page_response.text()
                p_soup = BeautifulSoup(p_response, 'lxml')
                images_links = map(lambda x: x['src'], p_soup.find_all('img'))
                for img_url in images_links:
                    img_name = re.search(r'(?<=img\/)(?:.+)(?=\.jpg)', img_url).group()
                    # (?<=re) - text after re, (?:re) - zero-width (na cathc) group (greedy), (?=re) - text before re
                    await self._download_img(retry_client, img_url, img_name)
                    pbar.update(1)  # tqdm progress bar increase

    async def _main(self):
        """entry point with gather method and tqdm status bar"""
        async with aiohttp.ClientSession() as session:
            # tqdm status bar object
            pbar = tqdm(total=500, desc='Обработано изображений: ')
            tasks = [asyncio.create_task(self._find_images(session, link, pbar)) for link in self._links]
            await asyncio.gather(*tasks)
            pbar.close()

    def _get_folder_size(self, filepath):
        """Returns total size of downloaded images"""
        for root, dirs, files in os.walk(filepath):
            for f in files:
                self._total_size += os.path.getsize(os.path.join(root, f))

    def __call__(self, default_args):
        self._domain = default_args.get('domain')  # constant part of url
        self._get_all_links(default_args.get('url'))  # get all links from start page

        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(self._main())
        self._get_folder_size(default_args.get('folder_path'))
        print(f'Общий размер скачанных изображений: {self._total_size}')


parser_args = {
    'domain': 'https://parsinger.ru/asyncio/aiofile/2/',
    'url': 'https://parsinger.ru/asyncio/aiofile/2/index.html',
    'folder_path': 'images'
}

image_dowloader = AsyncImagesDownloader()
image_dowloader(default_args=parser_args)
