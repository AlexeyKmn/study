from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from math import sqrt

with webdriver.Chrome() as browser:
    sites = ['http://parsinger.ru/blank/1/1.html', 'http://parsinger.ru/blank/1/2.html',
             'http://parsinger.ru/blank/1/3.html', 'http://parsinger.ru/blank/1/4.html',
             'http://parsinger.ru/blank/1/5.html', 'http://parsinger.ru/blank/1/6.html'
             ]
    for i, site in enumerate(sites, 1):
        browser.execute_script(f'window.open("{site}", "random_tab_{i}");')  # у вкладок должны быть РАЗНЫЕ ИМЕНА
        # иначе откроется ТОЛЬКО ОДНА из них. Шабло JS скрипта: 'window.open("<url>", "<tab_name>");'
    sleep(1)  # ждём открытия всех вкладок

    res = [0, []]
    for tab in reversed(browser.window_handles):  # пробегаемся по вкладкам
        browser.switch_to.window(tab)  # переключаемся на вкладку
        #  убираем начальную вкладку из парсинга (ЕЁ TITLE ПУСТАЯ СТРОКА - '')
        if browser.execute_script("return document.title;"):
            browser.find_element(By.CLASS_NAME, "checkbox_class").click()
            res[0] += sqrt(int(browser.find_element(By.ID, 'result').text))  # по заданию сумма корней
            res[1].append(browser.execute_script("return document.title;"))
    print(*res)
