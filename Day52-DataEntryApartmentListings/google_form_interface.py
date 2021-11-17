import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec


DRIVER_PATH = ""  # @TODO

GOOGLE_FORM_URL = ""  # @TODO
GOOGLE_FORMS_URL = ""  # @TODO


class GoogleFormInterface:

    def __init__(self):
        service = Service(executable_path=DRIVER_PATH)
        self.driver = webdriver.Edge(service=service)
        self.driver.get(GOOGLE_FORM_URL)

    def input_send_keys(self, xpath, data):
        input_ = WebDriverWait(self.driver, 15).until(
                                ec.visibility_of_element_located(
                                    (By.XPATH, xpath)))

        time.sleep(1.5)
        ActionChains(self.driver).move_to_element(input_).click().send_keys(data).perform()

    def click_button(self, xpath):
        button = WebDriverWait(self.driver, 5).until(
                                ec.visibility_of_element_located(
                                    (By.XPATH, xpath)))

        time.sleep(1.5)
        ActionChains(self.driver).move_to_element(button).click().perform()

    def fill_out_form(self, listings: list):

        for listing in listings:
            # Send keys to Address input
            self.input_send_keys("//*[@id='mG61Hd']/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input",
                                 listing["Address"])
            # Send keys to Price input
            self.input_send_keys("//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input",
                                 listing["Price"])
            # Send keys to Link input
            self.input_send_keys("//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input",
                                 listing["Link"])

            # Click the submit button
            self.click_button("//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div[1]/div")

            # Click the "Submit another response" link
            self.click_button("/ html / body / div[1] / div[2] / div[1] / div / div[4] / a")
