from selenium import webdriver

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.edge.webdriver import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import time


# default linkedin url takes you to the jobs page under specified criteria in the URL
# - Python Developer
# - Experience Level : Internship, Entry Level
LINKEDIN_URL = "https://www.linkedin.com/jobs/search/?f_E=1%2C2&keywords=python%20developer"
DRIVER_PATH = "C:\\edgedriver_win64\\msedgedriver.exe"

EMAIL = ""
PASSWORD = ""
PHONE_NUMBER = ""


class LinkedInInterface:

    def __init__(self):
        service = Service(executable_path=DRIVER_PATH)
        self.driver = webdriver.Edge(service=service)
        self.driver.get(LINKEDIN_URL)

    def terminate_driver(self):
        self.driver.quit()

    def _login(self, email_css: str, password_css: str, sign_in_button_css: str):
        print("Logging in")
        email_input = self.driver.find_element(By.CSS_SELECTOR, email_css)
        email_input.send_keys(EMAIL)
        password_input = self.driver.find_element(By.CSS_SELECTOR, password_css)
        password_input.send_keys(PASSWORD)
        time.sleep(2)
        submit_button = self.driver.find_element(By.CSS_SELECTOR, sign_in_button_css)
        submit_button.click()

# If greeted with the login page, enter creds and click submit
    def check_for_login_page(self):
        if "Log In" in self.driver.title:
            self._login("input#session_key", "input#session_password", "button.sign-in-form__submit-button")
        else:
            # If we're not signed in, sign in
            try:
                sign_in_button = self.driver.find_element(By.CSS_SELECTOR, "a.nav__button-secondary")
                sign_in_button.click()
            except:
                # only time this would trigger is if the button can't be found, then we must be signed in
                pass
            else:
                self._login("input#username", "input#password", "button.btn__primary--large")

    def evaluate_job_listings(self):
        job_search_left_rail = self.driver.find_element(By.CSS_SELECTOR, "section.jobs-search__right-rail")
        job_list = self.driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search-results__list li")

        for job in job_list:
            job.click()

            has_been_evaluated = False
            while not has_been_evaluated:
                # check for easy apply, if no easy apply, just save the job listing. If easy apply, apply.
                try:
                    apply_button = self.driver.find_element(By.CSS_SELECTOR, "div.jobs-apply-button--top-card")
                except NoSuchElementException:
                    # this will trigger if the webpage hasn't loaded the job information yet.
                    # sleep for a sec and then reiterate to check again
                    time.sleep(1)
                    pass
                else:
                    if apply_button.find_element(By.CSS_SELECTOR, "span.artdeco-button__text").text == "Easy Apply":
                        apply_button.click()

                        phone_number_input = self.driver.find_element(By.CSS_SELECTOR, "input[name*='phoneNumber']")
                        phone_number_input.send_keys(PHONE_NUMBER)

                        # uncomment for submit functionality
                        # submit_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']")
                        # submit_button.click()
                        # ----------------------------------


                        # comment to turn off auto closing the submit window
                        x_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Dismiss']")
                        x_button.click()

                        confirm_discard_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-control-name='discard_application_confirm_btn']")
                        confirm_discard_button.click()
                        # --------------------------------------------------
                    else:
                        save_button = self.driver.find_element(By.CSS_SELECTOR, "button.jobs-save-button")
                        if "Saved" not in save_button.text:
                            # if this evals to true, this means that the job listing is not saved
                            save_button.click()

                            try:
                                # see if there is a notification popup, dismiss if there
                                popup_dismiss_button = WebDriverWait(self.driver, 5).until(
                                    ec.visibility_of_element_located((By.CSS_SELECTOR, "button.artdeco-toast-item__dismiss")))
                            except:
                                # if any possible errors popup, just ignore all
                                pass
                            else:
                                popup_dismiss_button.click()
                    # break loop
                    has_been_evaluated = True
