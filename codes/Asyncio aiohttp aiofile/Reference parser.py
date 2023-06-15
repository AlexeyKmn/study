# Для запуска этого когда потребуются рабочие прокси.
import aiohttp  # асинхронный аналог requests
import asyncio  # библиотека асинронного выполнения
import requests  # библиотека
from bs4 import BeautifulSoup  # библиотека поиска в html
from aiohttp_socks import ChainProxyConnector  # класс управления разными типами прокси
from aiohttp_retry import RetryClient, ExponentialRetry  # асинхронные переподключения при ошибке апроса к серверу
from fake_useragent import UserAgent  # подделывает строку запроса от клиента на сервер

category_lst = []
pagen_lst = []
domain = 'https://parsinger.ru/html/'


def get_soup(url):  # синхронная функция, возвращает объект BS4 c html разметкой
    resp = requests.get(url=url)
    return BeautifulSoup(resp.text, 'lxml')


def get_urls_categories(soup):  # ищет категории на странице, создаёт список ссылок на них category_lst
    all_link = soup.find('div', class_='nav_menu').find_all('a')

    for cat in all_link:
        category_lst.append(domain + cat['href'])


def get_urls_pages(category_lst):  # ищет страницы каждой категории, создаёт список ссылок на них pagen_lst
    for cat in category_lst:
        resp = requests.get(url=cat)
        soup = BeautifulSoup(resp.text, 'lxml')
        for pagen in soup.find('div', class_='pagen').find_all('a'):
            pagen_lst.append(domain + pagen['href'])


async def get_data(session, link):  # асинхронная функция, ищет на страницах карточки и парсит каждую из них
    retry_options = ExponentialRetry(attempts=5)  # экспоненциальное увеличение времени ретрая подкючения
    # raise_for_status=False - не использовать полученное время ответа как параметр для следующего подключения
    # retry_options - см. выше, client_session - передача сессии, start_timeout - начальное время таймаута до Исключения
    retry_client = RetryClient(raise_for_status=False, retry_options=retry_options, client_session=session,
                               start_timeout=0.5)
    async with retry_client.get(link) as response:  # обращение к серверу методом get
        if response.ok:
            resp = await response.text()  # асинхронно получаем текст, парсим ссылки
            soup = BeautifulSoup(resp, 'lxml')
            item_card = [x['href'] for x in soup.find_all('a', class_='name_item')]
            for x in item_card:  # получаем и выводим интересующую нас информацию
                url2 = domain + x
                async with session.get(url=url2) as response2:
                    resp2 = await response2.text()
                    soup2 = BeautifulSoup(resp2, 'lxml')
                    article = soup2.find('p', class_='article').text
                    name = soup2.find('p', id='p_header').text
                    price = soup2.find('span', id='price').text
                    print(url2, price, article, name)


async def main():
    ua = UserAgent()  # создаём поддельную строку headers клиента при запросе
    fake_ua = {'user-agent': ua.random}
    # передаём классу ChainProxyConnector список str вида: тип прокси, пароль:логин от прокси, адреса прокси
    connector = ChainProxyConnector.from_urls(
        [
            'socks5://D2Frs6:75JjrW@194.28.210.39:9867',
            'socks5://D2Frs6:75JjrW@194.28.209.68:9925',
        ]
    )
    async with aiohttp.ClientSession(connector=connector, headers=fake_ua) as session:
        tasks = []
        for link in pagen_lst:  # передаём список ссылок на все страницы с товарами
            task = asyncio.create_task(get_data(session, link))  # вызываем для них асинхроннку, передавая каждый link
            tasks.append(task)  # собираем для каждого линка таск
        await asyncio.gather(*tasks)  # методом gather запускаем асинхронное получение данных из get_data


url = 'https://parsinger.ru/html/index1_page_1.html'
soup = get_soup(url)  # получили BS4
get_urls_categories(soup)  # получили линки категорий
get_urls_pages(category_lst)  # получили линки всех страниц с товарами

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # строка настройки политики лупа в винде
asyncio.run(main())  # собственно сам метод ран

"""
# Код ниже, как пример, уровней вложенности при асинхронном парсинге. Имеет вложенные циклы (они же функции выше)
import aiohttp
import asyncio
from bs4 import BeautifulSoup


async def main(url):
    async with aiohttp.ClientSession() as session:
        # первый уровень вложенности (например, типы товаров)
        async with session.get(url=url) as response:
            resp = await response.text()
            soup = BeautifulSoup(resp, 'lxml')
            item_card = [x['href'] for x in soup.find_all('a', class_='link')]
            for url2 in item_card:
                # второй уровень вложенности (например, страницы с товарами)
                async with session.get(url=url2) as response2:
                    resp2 = await response2.text()
                    soup2 = BeautifulSoup(resp2, 'lxml')
                    item_card2 = [x['href'] for x in soup2.find_all('a', class_='link2')]
                    for url3 in item_card2:
                    # третий уровень вложенности и т.д.
"""
