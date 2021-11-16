import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

SPEED_TEST_URL = "https://www.speedtest.net"


class SpeedTestInterface:

    def test_speeds(self, driver):
        driver.get(SPEED_TEST_URL)

        test_button = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, "div.start-button a")))
        test_button.click()

        try:
            # TRY SPEED TEST FOR MAC POPUP
            x_button = WebDriverWait(driver, 50).until(
                ec.visibility_of_element_located((By.XPATH,
                                                  "//*[@id='container']/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[8]/div/a")))
        except:
            # if this errors, then we may be on windows, or it just didn't popup.
            pass
        else:
            x_button.click()

        result_download_speed = WebDriverWait(driver, 5).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR,
                                              "div.result-data span.download-speed"))).text
        result_upload_speed = WebDriverWait(driver, 5).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR,
                                              "div.result-data span.upload-speed"))).text

        return result_download_speed, result_upload_speed
