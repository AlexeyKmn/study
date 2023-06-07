import csv
import requests
from bs4 import BeautifulSoup

init_url = 'https://parsinger.ru/html/index4_page_1.html'
domen_url = 'https://parsinger.ru/html/'
headers = ['Наименование', 'Бренд', 'Форм-фактор', 'Ёмкость', 'Объём буф.памяти', 'Цена']


def parse_pages_urls(url: str, domen: str):
    """getting all the pages urls for the selected category"""
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        pagen_urls = [f'{domen}{link["href"]}' for link in soup.find('div', class_='pagen').find_all('a')]
        return pagen_urls
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
            for lst in res:  # removing headers from result
                for i in range(1, 4):
                    lst[i] = lst[i].split(maxsplit=1)[1]
                lst[4] = lst[4].split(':')[-1].strip()
            data.extend(res)
        return data
    except:
        raise Exception('Некорректно заданы данные для поиска')


def export_to_csv(headers: list, data: list[list], filename: str):
    """headers - list of csv headers"""
    try:
        with open(f'{filename}.csv', 'w', encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(headers)
            writer.writerows(data)
        print('Файл создан в папке с проектом')
    except:
        raise PermissionError('Ошибка доступа к файлу или его создания')


if __name__ == '__main__':
    res = parse_data(parse_pages_urls(init_url, domen_url))
    export_to_csv(headers, res, filename='res')
