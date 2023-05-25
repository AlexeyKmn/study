import csv
import requests
from bs4 import BeautifulSoup

init_url = 'https://parsinger.ru/html/index1_page_1.html'
domen_url = 'https://parsinger.ru/html/'


def parse_pages_urls(url: str, domen: str):
    """getting all the pages urls for every type of goods"""
    try:
        res = []
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        goods_urls = [f'{domen}{link["href"]}' for link in soup.find('div', class_='nav_menu').find_all('a')]
        for link in goods_urls:
            response = requests.get(link)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'lxml')
            pagen_urls = [f'{domen}{link["href"]}' for link in soup.find('div', class_='pagen').find_all('a')]
            res.extend(pagen_urls)
        return res
    except:
        raise NameError('Некорректная начальная страница')


def parse_data(urls: list) -> list[list]:
    """parsing text from textplate, urls - list of pages for parsing"""
    data = []
    try:
        for url in urls:
            response = requests.get(url)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'lxml')
            res = [[s.strip() for s in i.text.split('\n') if s][:-1] for i in  # recieving data
                   soup.find('div', 'item_card').find_all(class_='item')]
            data.extend(res)
        for lst in data:  # removing headers from result
            for i in range(1, 5):
                lst[i] = lst[i].split(':', maxsplit=1)[1]
        return data
    except:
        raise Exception('Некорректно заданы данные для поиска')


def export_to_csv(data: list[list], filename: str):
    """saving data to CSV"""
    try:
        with open(f'{filename}.csv', 'w', encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(data)
        print('Файл создан в папке с проектом')
    except:
        raise PermissionError('Ошибка доступа к файлу или его создания')


if __name__ == '__main__':
    links = parse_pages_urls(init_url, domen_url)
    export_to_csv(parse_data(links), 'result')
