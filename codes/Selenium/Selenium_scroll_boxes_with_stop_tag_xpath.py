from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

with webdriver.Chrome() as driver:
    driver.get('https://parsinger.ru/infiniti_scroll_3/')
    # ищем все скроллбоксы (элементы c возможностью прокручивания)
    requests = [f'//div[@id="scroll-container_{i}"]' for i in range(1, 6)]
    scroll_boxes = [driver.find_element(By.XPATH, i) for i in requests]
    # листаем их все до конца в цикле для загрузки данных. выход из цикла - наличие в dive class='last-of-list'
    res = 0
    for scroll_box in scroll_boxes:
        while True:
            AC = ActionChains(driver)
            AC.move_to_element(scroll_box.find_element(By.TAG_NAME, 'div')).scroll_by_amount(1, 500).perform()
            sleep(0.1)
            try:
                scroll_box.find_element(By.CLASS_NAME, 'last-of-list')
                break
            except:
                continue
        # суммируем по скроллбоксу и добавляем к результату
        res += sum([int(i.text) for i in scroll_box.find_elements(By.TAG_NAME, "span")])
    print(res)
    sleep(20)
