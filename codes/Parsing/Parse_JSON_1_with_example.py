import requests
from bs4 import BeautifulSoup
import json

start_url = 'https://parsinger.ru/html/index3_page_1.html'
domen = 'http://parsinger.ru/html/'


def get_pages_urls(url: str, domen: str) -> list:
    """gets all the pages urls for the selected category"""
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        res = [f'{domen}{link["href"]}' for link in soup.find('div', class_='pagen').find_all('a')]
        return res
    except:
        raise NameError('Некорректная страница для парсинга')


def parse_data(urls: list) -> list:
    """parses required data and returns dict"""
    try:
        data = []
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
                    'name': name,
                    'brand': [x.split(':')[1] for x in list_item][0],
                    'type': [x.split(':')[1] for x in list_item][1],
                    'connect': [x.split(':')[1] for x in list_item][2],
                    'gaming': [x.split(':')[1] for x in list_item][3],
                    'price': price_item

                })
        return data
    except:
        raise Exception("Неверно указаны алгориты извлечения данных")


def dump_to_json(data: list[dict], filename: str):
    """creates and writes a JSON file"""
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    links = get_pages_urls(start_url, domen)
    dump_to_json(parse_data(links), 'result')
    print('Success')
