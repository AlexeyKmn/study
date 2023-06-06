from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

with webdriver.Chrome() as browser:
    browser.get('https://parsinger.ru/scroll/3/')
    boxes = browser.find_elements(By.CLASS_NAME, 'checkbox_class')
    for box in boxes:
        box.click()
    total = 0
    for i in range(1, 501):
        if browser.find_element(By.ID, 'result' + str(i)).text:
            total += int(browser.find_element(By.ID, str(i)).get_attribute('id'))
    print(total)
    sleep(10)
