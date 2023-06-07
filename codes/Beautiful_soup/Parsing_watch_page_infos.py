import csv
import requests
from bs4 import BeautifulSoup

init_url = 'https://parsinger.ru/html/index1_page_1.html'
domen_url = 'https://parsinger.ru/html/'
headers = ['Наименование', 'Артикул', 'Бренд', 'Модель', 'Тип', 'Технология экрана',
           'Материал корпуса', 'Материал браслета', 'Размеры', 'Сайт производителя',
           'Наличие', 'Цена', 'Старая цена', 'Ссылка на карточку с товаром'
           ]


def parse_pages_urls(url: str, domen: str) -> list:
    """getting all the pages urls for the selected category"""
    try:
        res = []
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        pagen_urls = [f'{domen}{link["href"]}' for link in soup.find('div', class_='pagen').find_all('a')]
        for link in pagen_urls:
            response = requests.get(link)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.content, 'lxml')
            link_texts = [i.find('a') for i in soup.find_all('div', class_='img_box')]  # parsing boxes with urls
            item_urls = [f'{domen}{link["href"]}' for link in link_texts]  # parsing urls
            res.extend(item_urls)
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
            res = [t.strip() for t in soup.find('div', class_='description').text.split('\n') if
                   t != '' and t != 'Купить']
            for i in range(1, len(res) - 2):  # removing headers
                res[i] = res[i].split(':', maxsplit=1)[1].strip()
            res.append(url)
            data.append(res)
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
