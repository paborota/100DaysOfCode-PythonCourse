from selenium import webdriver

from speed_test_interface import SpeedTestInterface
from twitter_interface import TwitterInterface

PROMISED_DOWN = 150
PROMISED_UP = 10


driver = webdriver.Safari()

speed_test_interface = SpeedTestInterface()
download, upload = speed_test_interface.test_speeds(driver)

if float(download) < PROMISED_DOWN or float(upload) < PROMISED_UP:
    msg = f"Hello, internet provider. Why am i receiving {download} down and {upload} up, when i am promised {PROMISED_DOWN} down and {PROMISED_UP} up?"
    twitter_interface = TwitterInterface()
    twitter_interface.go_to_site(driver)
    twitter_interface.login(driver)
    twitter_interface.tweet(driver, msg)
