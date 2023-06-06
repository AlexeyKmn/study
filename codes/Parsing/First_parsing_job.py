from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
import time

link = 'https://regdocs.bd.com/regdocs/qcinfo'
ref = 442023
lot_num = 3102718


def lot_found(ref: str | int, lot: str | int, browser):
    """
    returnes true if documentation with # lot found
    :param ref: ref number
    :param lot: lot number (parsed)
    :param browser: instance of selenium drived browser
    """
    try:
        browser.find_element(By.NAME, "qualityCert[0].materialNumber").send_keys(ref)
        print('ref')
        browser.find_element(By.NAME, "qualityCert[0].batchNumber").send_keys(lot)
        print('lot')
        browser.find_element(By.XPATH, '//button[@type="submit"]').click()
        print('click')
        if browser.find_elements(By.XPATH, '//button[@class="button full-width"]'):
            print(f'lot # {lot} found')
        else:
            print(f'lot # {lot} not found')
    except:
        pass


with webdriver.Chrome() as browser:
    wait = WebDriverWait(browser, 5)
    for i in range(3102717, 3102727):
        browser.get(link)
        lot_found(ref, i, browser)
    time.sleep(20)
