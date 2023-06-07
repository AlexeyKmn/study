import requests
from bs4 import BeautifulSoup
import json

start_url = 'https://parsinger.ru/html/index1_page_1.html'
domen = 'http://parsinger.ru/html/'
headers = {1: ['name', 'brand', 'type', 'material', 'screen', 'price'],
           2: ['name', 'brand', 'diagonal', 'material', 'resolution', 'price'],
           3: ['name', 'brand', 'type', 'connection', 'game', 'price'],
           4: ['name', 'brand', 'form-factor', 'capacity', 'buffer memory size', 'price'],
           5: ['name', 'brand', 'connection', 'color', 'type', 'price']
           }


def get_goods_urls(start_url: str, domen: str) -> dict[int: str]:
    """gets start urls for every product category"""
    try:
        response = requests.get(start_url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        res = [f'{domen}{link["href"]}' for link in soup.find('div', class_='nav_menu').find_all('a')]
        return {i: j for i, j in enumerate(res, 1)}
    except Exception:
        raise NameError('Начальная страница не содержит меню навигации')


def get_pages_urls(url: str, domen: str) -> list:
    """gets all the pages urls for the selected category"""
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        res = [f'{domen}{link["href"]}' for link in soup.find('div', class_='pagen').find_all('a')]
        return res
    except Exception:
        raise NameError('Некорректные начальные страницы товаров')


def parse_data(urls: list, headers: dict[int: list[str]], num_of_url: int, data: list[dict]):
    """
    parses required data and returns dict
    :param urls: list of urls
    :param headers: dict with headers for JSON
    :param num_of_url: number of key in headers
    :param data: list of dicts for collecting results
    """
    try:
        for url in urls:
            response = requests.get(url=url)
            response.encoding = 'utf-8-sig'
            soup = BeautifulSoup(response.text, 'lxml')

            #  find the data from soup
            name = [x.text.strip() for x in soup.find_all('a', class_='name_item')]
            description = [x.text.strip().split('\n') for x in soup.find_all('div', class_='description')]
            price = [x.text for x in soup.find_all('p', class_='price')]

            #  create dict for json serialization
            for list_item, price_item, name in zip(description, price, name):
                data.append({
                    headers[num_of_url][0]: name,
                    headers[num_of_url][1]: [x.split(':')[1].strip() for x in list_item][0],
                    headers[num_of_url][2]: [x.split(':')[1].strip() for x in list_item][1],
                    headers[num_of_url][3]: [x.split(':')[1].strip() for x in list_item][2],
                    headers[num_of_url][4]: [x.split(':')[1].strip() for x in list_item][3],
                    headers[num_of_url][5]: price_item
                })
        return None
    except:
        raise Exception("Неверно указаны алгоритмы извлечения данных")


def dump_to_json(data: list[dict], filename: str):
    """creates and writes a JSON file"""
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    try:
        # get products urls
        res = []
        product_pages = get_goods_urls(start_url, domen)
        for i in range(1, len(product_pages) + 1):
            # get page's urls for every product
            pages_links = get_pages_urls(product_pages[i], domen)
            # finally parse the data into res list
            parse_data(pages_links, headers, i, res)
        # writing to JSON file
        dump_to_json(res, 'products.json')
        print('File successfully created')

    except Exception:
        print('An error occurred')
