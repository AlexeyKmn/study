from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

with webdriver.Chrome() as browser:
    browser.get('https://parsinger.ru/blank/modal/4/index.html')
    check = browser.find_element(By.ID, "check")  # кнопка отправки
    for pin in [i.text for i in browser.find_elements(By.CLASS_NAME, "pin")]:
        # ищем в модальных окнах нужный пинкод, при вводе которогов высветится верный код
        check.click()
        window = browser.switch_to.alert
        window.send_keys(pin)
        window.accept()
        res = browser.find_element(By.ID, "result").text
        if res != 'Неверный пин-код':
            print(pin, res)
    sleep(.5)
