import time
from selenium import webdriver
from selenium.webdriver.common.by import By

with webdriver.Chrome() as browser:
    browser.get('https://parsinger.ru/scroll/4/index.html')
    elems = browser.find_elements(By.CLASS_NAME, 'btn')
    print(len(elems))
    res = 0
    for elem in elems:
        browser.execute_script('arguments[0].click();', elem)
        res += int(browser.find_element(By.ID, 'result').text)
    print(res)
    time.sleep(10)
