import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup


class Parser:
    def __init__(self, host):
        self._host = host
        self._cat_url_lst, self._pagen_url_lst = [], []
        self._res = 0

    @staticmethod
    def get_soup(url):
        return BeautifulSoup(requests.get(url).text, 'lxml')

    def get_url(self, ref):
        return f'{self._host}{ref["href"]}'

    def get_urls_categories(self, soup):
        links = soup.find('div', class_='nav_menu').find_all('a')
        self._cat_url_lst = [self.get_url(i) for i in links]

    def get_urls_pages(self):
        for cat in self._cat_url_lst:
            soup = self.get_soup(cat)
            self._pagen_url_lst.extend([self.get_url(i) for i in soup.find('div', class_='pagen').find_all('a')])

    async def get_data(self, session, link):
        async with session.get(url=link) as response:
            # await через доп переменную для наглядности. Асинхронно ждём именно ответа такста от сервера
            resp = await response.text()
            soup = BeautifulSoup(resp, 'lxml')
            for card_link in [self.get_url(i) for i in soup.find_all('a', class_='name_item')]:
                async with session.get(url=card_link) as response_2:
                    # аналог строки выше без доп переменной, ждём всё так же ответа от сервера
                    soup_2 = BeautifulSoup(await response_2.text(), 'lxml')
                    # ниже код из условия задачи
                    old_price = int(soup_2.find(id='old_price').text.split()[0])
                    price = int(soup_2.find(id='price').text.split()[0])
                    in_stock = int(soup_2.find(id='in_stock').text.split()[-1])
                    self._res += in_stock * (old_price - price)

    async def main(self):
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.create_task(self.get_data(session, link)) for link in self._pagen_url_lst]
            await asyncio.gather(*tasks)

    def __call__(self, url, *args, **kwargs):
        soup = self.get_soup(url)
        self.get_urls_categories(soup)
        self.get_urls_pages()
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(self.main())
        return self._res


if __name__ == '__main__':
    parse = Parser(host='https://parsinger.ru/html/')
    print(parse(url='https://parsinger.ru/html/index1_page_1.html'))
