from selenium import webdriver
from selenium.webdriver.common.by import By
import time

opts = webdriver.ChromeOptions()
opts.add_experimental_option("detach", True)  # не закрыает браузер по завершении кода
browser = webdriver.Chrome(options=opts)  # выполнять без менеджера контекста with

browser.get('https://parsinger.ru/selenium/2/2.html')
browser.find_element(By.PARTIAL_LINK_TEXT, '16243162441624').click()
res = browser.find_element(By.ID, 'result').text
print(res)
