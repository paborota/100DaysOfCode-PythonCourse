import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

TWITTER_URL = "https://twitter.com"
EMAIL = ""
USERNAME = ""  # Used when the "suspicious activity" check pops up
PASSWORD = ""


class TwitterInterface:

    def __init__(self):
        pass

    def go_to_site(self, driver):
        driver.get(TWITTER_URL)

    def input_user_info(self, driver, input_name, input_data):
        user_input = WebDriverWait(driver, 10).until(
                    ec.visibility_of_element_located((By.CSS_SELECTOR,
                                                      f"input[name='{input_name}']")))
        user_input.send_keys(input_data)
        next_button = WebDriverWait(driver, 5).until(
                    ec.visibility_of_element_located((By.CSS_SELECTOR,
                                                      "div[style='color: rgb(15, 20, 25);']")))
        time.sleep(2)
        next_button.click()

    def login(self, driver):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        try:
            sign_in_button = WebDriverWait(driver, 10).until(
                    ec.visibility_of_element_located((By.CSS_SELECTOR,
                                                      "div[data-testid='logInSignUpFooter'] span span")))
        except:
            # no matter how this errors, just return
            return

        sign_in_button.click()

        sign_in_with_email_button = driver.find_element(By.CSS_SELECTOR, "a[href='/login']")
        sign_in_with_email_button.click()

        self.input_user_info(driver, "username", EMAIL)
        try:
            WebDriverWait(driver, 5).until(
                ec.visibility_of_element_located((By.XPATH,
                                                  "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div/span")))
        except:
            # no matter how this errors, just ignore
            # because that means that the "suspicious activity" screen didn't pop
            pass
        else:
            self.input_user_info(driver, "text", USERNAME)
        self.input_user_info(driver, "password", PASSWORD)

    def tweet(self, driver, msg):
        try:
            tweet_box = WebDriverWait(driver, 10).until(
                        ec.visibility_of_element_located((By.XPATH,
                                                         "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div")))
        except:
            # if there is literally any error, just return, something is broken.
            return
        else:
            tweet_box.send_keys(msg)

            tweet_button = driver.find_element(By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]")
            tweet_button.click()
