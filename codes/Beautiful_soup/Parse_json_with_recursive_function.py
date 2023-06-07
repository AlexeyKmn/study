"""Используется универсальная рекурсивная функция для поиска всех страниц с товарами.
Принимает на вход список параметров для парсинга по BS4 объекту"""
import requests
from bs4 import BeautifulSoup
import json
from re import search
from random import randint

start_url = 'https://parsinger.ru/html/index2_page_1.html'
main_url = 'https://parsinger.ru/html/'

# для парсинга ссылок вида  soup.find('span', class_='label').find_all('span', class_='argument', 'text' = 'имя')
# в функцию для find / findall / select передаются параметры вида:
# first_params={'name': 'span', 'class_': 'label', ...},
# second_params={'name': 'span', 'class_': 'argument', 'text': 'имя', ...)
# ниже лист этих самых параметров для парсеров
parsers_lst = [[{'name': 'div', 'class_': 'nav_menu'}, {'name': 'a'}],  # поиск ссылок на категории товаров
               [{'name': 'div', 'class_': 'pagen'}, {'name': 'a'}],  # поиск ссылок на страницы с товаром №№ 1, 2, 3, ..
               [{'name': 'div', 'class_': 'item_card'}, {'name': 'a', 'class_': 'name_item'}]  # поиск ссылок на товары
               ]


def flatten_list(lst: list):
    # recursive function to flatten nested lists
    res = []
    for item in lst:
        if isinstance(item, list):
            res += (flatten_list(item))
        else:
            res += [item]
    return res


def get_urls(url, main_page: str, parsers: list[list[dict]]) -> list:
    """
    gets all urls recursively, works with arbitrary nesting
    :param url: start page for parsing
    :param main_page: main website page (constant part of url)
    :param parsers: list of data for soup BS4 objects
    :return: list of found urls
    """
    try:
        if parsers:
            print('*', end='')
            first_params, sec_params = parsers[0]
            response = requests.get(url)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'lxml')
            res = [f'{main_page}{link["href"]}' for link in soup.find(**first_params).find_all(**sec_params)]
            return flatten_list([get_urls(link, main_page, parsers[1:]) for link in res])
        else:
            return url
    except Exception as e:
        print("Ошибка поиска страниц:", e)


def parse_data(url: str, data: list[dict]):
    """
    parses the necessary data from url
    :param url: url of page for parsing
    :param data: list for collecting the data
    :return: None
    """
    try:
        res = {'category': search(r'html/(\w*)?/\d', url).group(1)}  # parse category from url via regex

        #  find the data from soup
        response = requests.get(url=url)
        response.encoding = 'utf-8-sig'
        soup = BeautifulSoup(response.text, 'lxml').find('div', class_='description')
        res['name'] = soup.find('p', id='p_header').text.strip()
        res['article'] = soup.find('p', class_='article').text.strip()
        res['description'] = {info['id']: info.text.split(':', maxsplit=1)[1].strip()
                              for info in soup.find('ul', id='description').find_all('li')}
        res['is_stock'] = soup.find('span', id='in_stock').text.split(':', maxsplit=1)[1].strip()
        res['price'] = soup.find('span', id='price').text.strip()
        res['old_price'] = soup.find('span', id='old_price').text.strip()
        res['link'] = url
        if randint(1, 30) > 25:
            print('*', end='')

        data.append(res)
        return None
    except Exception as e:
        print("Неверно указаны алгоритмы извлечения данных", e)


def dump_to_json(data: list[dict], filename: str):
    """creates and writes a JSON file"""
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    try:
        urls = get_urls(start_url, main_url, parsers_lst)
        print('\n', 'urls parsed...')
        data = []
        for url in urls:
            parse_data(url, data)
        print('\n', 'data parsed...')
        print('**************************')
        dump_to_json(data, 'results.json')
        print(' json file created. Success')

    except Exception as e:
        print(e)
