from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

with webdriver.Chrome() as browser:
    browser.get('https://parsinger.ru/draganddrop/2/index.html')
    action = ActionChains(browser)
    boxes = browser.find_elements(By.CLASS_NAME, 'box')
    sourse = browser.find_element(By.ID, 'draggable')
    for box in boxes:
        action.drag_and_drop(sourse, box).perform()
    sleep(1)
    print(browser.find_element(By.ID, 'message').text)
