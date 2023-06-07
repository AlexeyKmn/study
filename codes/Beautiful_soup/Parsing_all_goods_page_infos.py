import csv
import requests
from bs4 import BeautifulSoup

init_url = 'https://parsinger.ru/html/index1_page_1.html'
domen_url = 'https://parsinger.ru/html/'
headers = ['Наименование', 'Артикул', 'Бренд', 'Модель', 'Наличие', 'Цена', 'Старая цена', 'Ссылка']


def parse_pages_urls(url: str, domen: str):
    """getting all the pages urls for every type of goods"""
    try:
        res = []
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        # parse nav menu
        goods_urls = [f'{domen}{link["href"]}' for link in soup.find('div', class_='nav_menu').find_all('a')]
        for goods_url in goods_urls:
            response = requests.get(goods_url)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'lxml')
            # parse pages for every type of goods
            pagen_urls = [f'{domen}{link["href"]}' for link in soup.find('div', class_='pagen').find_all('a')]
            for item_url in pagen_urls:
                response = requests.get(item_url)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, 'lxml')
                # parse boxes with urls for every single product
                link_texts = [i.find('a') for i in soup.find_all('div', class_='img_box')]
                item_urls = [f'{domen}{link["href"]}' for link in link_texts]  # parse urls
                res.extend(item_urls)
        return res
    except:
        raise NameError('Некорректная начальная страница')


def parse_data(urls: list) -> list[list]:
    """urls - list of product page's urls"""
    data = []
    try:
        for url in urls:
            response = requests.get(url)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'lxml')
            res = [t.strip() for t in soup.find('div', class_='description').text.split('\n') if
                   t != '' and t != 'Купить']
            res = res[:4] + res[-3:]  # remove unnecessary data
            for i in range(1, 5):  # remove unnecessary headers
                res[i] = res[i].split(':', maxsplit=1)[1].strip()
            res.append(url)
            data.append(res)
        return data
    except:
        raise Exception('Некорректно заданы данные для поиска')


def export_to_csv(data: list[list], filename: str):
    """saving data to CSV"""
    try:
        with open(f'{filename}.csv', 'w', encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(headers)
            writer.writerows(data)
        print('Файл создан в папке с проектом')
    except:
        raise PermissionError('Ошибка доступа к файлу или его создания')


if __name__ == '__main__':
    links = parse_pages_urls(init_url, domen_url)
    export_to_csv(parse_data(links), 'result')
