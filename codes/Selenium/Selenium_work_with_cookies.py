from time import sleep
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By

with webdriver.Chrome() as webdriver:
    res = {}
    url = 'https://parsinger.ru/methods/5/index.html'
    webdriver.get(url)
    # хватаем все ссылки на странице
    links = [x.get_attribute('href') for x in webdriver.find_elements(By.TAG_NAME, 'a')]
    # хватаем куки со всех страниц и берём из них только поле
    for num, link in enumerate(links, 1):
        webdriver.get(link)
        res[num] = webdriver.get_cookie('foo2')['expiry']
    # задание вывести число с сайта с самым большим expiry в cookie
    url = links[max(res.items(), key=lambda x: x[1])[0] - 1]
    webdriver.get(url)
    print(url, '-', webdriver.find_element(By.ID, 'result').text)
    sleep(20)
    pprint(res)
