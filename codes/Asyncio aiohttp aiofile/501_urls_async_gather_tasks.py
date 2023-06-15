import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
from time import perf_counter


class Parser:
    def __init__(self, host, url):
        self._res = 0
        self._host = host
        self._url = url

    def get_links(self):
        soup = BeautifulSoup(requests.get(url=self._url).text, 'lxml')
        return [f'{self._host}{i["href"]}' for i in soup.find_all(class_='lnk_img')]

    async def main(self, url):
        async with aiohttp.ClientSession() as session:
            # ClientSession(connector=aiohttp.TCPConnector(limit=503) если упираемся в лимит по подключениям
            async with session.get(url=url) as response:
                if response.ok:
                    res = BeautifulSoup(await response.text(), 'lxml').find('p', class_='text')
                    if res:
                        print(res.text)
                        self._res += int(res.text)

    async def run_tasks(self):
        await asyncio.gather(*[self.main(link) for link in self.get_links()])

    def __call__(self, *args, **kwargs):
        start = perf_counter()
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(self.run_tasks())
        end = perf_counter()
        return f"res: {self._res}, execution time: {end - start} 'sec'"


if __name__ == '__main__':
    parse = Parser(host='https://parsinger.ru/asyncio/create_soup/1/',
                   url='https://parsinger.ru/asyncio/create_soup/1/index.html')
    print(parse())
