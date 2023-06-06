from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Keys  # driver.find_element(By.TAG_NAME, 'input').send_keys(Keys.DOWN) в цикле
from selenium.webdriver.common.by import By

with webdriver.Chrome() as driver:
    driver.get('https://parsinger.ru/infiniti_scroll_1/')
    div = driver.find_element(By.XPATH, '//*[@id="scroll-container"]/div')
    for _ in range(100):
        ActionChains(driver).move_to_element(div).scroll_by_amount(1, 500).perform()
        sleep(0.1)
        try:
            driver.find_element(By.CLASS_NAME, 'last-of-list')
            break
        except:
            continue
    res = sum([int(i.text) for i in driver.find_element(By.ID, "scroll-container").find_elements(By.TAG_NAME, "span")])
    print(res)
    sleep(20)
