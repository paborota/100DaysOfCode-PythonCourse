import time

import selenium
from selenium import webdriver
# from selenium.webdriver.edge.service import Service

from selenium.webdriver.common.by import By


# DRIVER_PATH = "C:\edgedriver_win64\msedgedriver.exe"
URL = "http://orteil.dashnet.org/experiments/cookie/"


# service = Service(executable_path=DRIVER_PATH)
driver = webdriver.Safari()
driver.get(url=URL)


cookie = driver.find_element(By.CSS_SELECTOR, "div#cookie")

upgrade_time = time.time() + 5
end_time = time.time() + 60 * 5  # current time + 5 minutes
current_money = driver.find_element(By.CSS_SELECTOR, "div#money")
while True:
    cookie.click()

    if time.time() >= upgrade_time:

        upgrade_time += 5

        upgrades = driver.find_elements(By.CSS_SELECTOR, "div#store div[id*='buy']")
        for upgrade in upgrades[::-1]:
            if upgrade.get_attribute("class") != "grayed":
                upgrade.click()
                break

    if time.time() >= end_time:
        print(f"Ending Cookies Per Second: {float(driver.find_element(By.CSS_SELECTOR, 'div#cps').text.split(':')[-1].strip())}")
        break

driver.quit()
