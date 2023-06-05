from selenium import webdriver
from selenium.webdriver.common.by import By

opts = webdriver.ChromeOptions()
opts.add_experimental_option("detach", True)  # не закрыает браузер по завершении кода
browser = webdriver.Chrome(options=opts)  # выполнять без менеджера контекста with

browser.get('https://parsinger.ru/selenium/3/3.html')
res = sum(map(int, [i.text for i in browser.find_elements(By.XPATH, "//div/p[2]")]))
print(res)
