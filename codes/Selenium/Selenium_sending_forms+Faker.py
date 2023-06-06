from selenium import webdriver
from selenium.webdriver.common.by import By
from faker import Faker
import random
import time

browser = webdriver.Chrome()
browser.get('https://parsinger.ru/selenium/1/1.html')
f = Faker('ru_RU')
form_list = [f.first_name_male(), f.last_name_male(), f.middle_name_male(), random.randint(30, 40), f.city_name(),
             f.email()
             ]
inp_forms = browser.find_elements(By.CLASS_NAME, "form")
for text, form in zip(form_list, inp_forms):
    form.send_keys(text)

btn = browser.find_element(By.ID, "btn").click()

time.sleep(20)
