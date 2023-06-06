from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

with webdriver.Chrome() as browser:
    browser.get('https://parsinger.ru/blank/modal/3/index.html')
    input = browser.find_element(By.ID, "input")  # input box для ввода цифр
    check = browser.find_element(By.ID, "check")  # кнопка отправки
    for btn in browser.find_elements(By.CLASS_NAME, "buttons"):
        # ищем в модальных окнах нужный пинкод, при вводе которогов высветится верный код
        btn.click()
        window = browser.switch_to.alert
        pin = window.text
        window.accept()
        input.send_keys(pin)
        check.click()
        res = browser.find_element(By.ID, "result").text
        if res != 'Неверный пин-код':
            print(res)
    sleep(.5)
