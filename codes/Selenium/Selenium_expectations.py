from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

with webdriver.Chrome() as browser:
    browser.get('https://parsinger.ru/expectations/6/index.html')
    # timeout - время до генерации исключения, poll_frequency - период опроса страницы
    WebDriverWait(browser, timeout=5, poll_frequency=0.3).until(EC.element_to_be_clickable((By.ID, 'btn'))).click()
    # задание 2 - пока тайтл не станет известной сторкой, тайминги случайны
    # WebDriverWait(browser, timeout=100, poll_frequency=0.2).until(EC.title_is('345FDG3245SFD'))
    # задание 3 - пока в тайтле не появится известная часть, тайминги случайны
    # WebDriverWait(browser, timeout=100, poll_frequency=0.1).until(EC.title_contains(EC.title_is('345FDG3245SFD'))
    # задание 4 - пока не появится элемент с ивестным заранее именем класса
    WebDriverWait(browser, timeout=100, poll_frequency=0.1).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'Y1DM2GR')))
    print(browser.find_element(By.CLASS_NAME, 'Y1DM2GR').text)
