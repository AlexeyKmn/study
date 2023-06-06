from selenium import webdriver
from itertools import product
from selenium.webdriver.common.by import By

options_chrome = webdriver.ChromeOptions()
options_chrome.add_argument('--headless=chrome')

with webdriver.Chrome(options=options_chrome) as browser:
    browser.get('https://parsinger.ru/window_size/2/index.html')
    window_size_x = [616, 648, 680, 701, 730, 750, 805, 820, 855, 890, 955, 1000]
    window_size_y = [300, 330, 340, 388, 400, 421, 474, 505, 557, 600, 653, 1000]
    for w, h in product(window_size_x, window_size_y):
        browser.set_window_size(w, h)
        res = browser.find_element(By.ID, "result").text
        if res:
            sizes = browser.get_window_size()
            print(f'{res}, {w}, {h}', sizes)
            break
