from selenium import webdriver
from selenium.webdriver.common.by import By

with webdriver.Chrome() as browser:
    browser.get('https://parsinger.ru/methods/1/index.html')
    while True:
        res = browser.find_element(By.ID, 'result').text
        if res == 'refresh page':
            browser.refresh()
            continue
        else:
            print(res)
            break
