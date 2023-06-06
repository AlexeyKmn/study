from selenium import webdriver
from selenium.webdriver.common.by import By

opts = webdriver.ChromeOptions()
opts.add_experimental_option("detach", True)  # не закрыает браузер по завершении кода
browser = webdriver.Chrome(options=opts)  # выполнять без менеджера контекста with

browser.get('https://parsinger.ru/selenium/7/7.html')
# значения дроплиста дёргаются по тегу option
res = sum(map(int, [i.text for i in browser.find_elements(By.TAG_NAME, 'option')]))
print(res)
browser.find_element(By.ID, 'input_result').send_keys(res)
browser.find_element(By.CLASS_NAME, 'btn').click()
print(browser.find_element(By.ID, 'result').text)
