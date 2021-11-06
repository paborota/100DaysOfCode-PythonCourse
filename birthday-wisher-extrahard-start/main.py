##################### Extra Hard Starting Project ######################
import datetime as dt
from random import choice
import os
import pandas
import smtplib

"""
    ---- DO BE AWARE THAT THE BIRTHDAYS.CSV FILE IS EMPTY AND THEREFORE THE PROGRAM WILL NOT WORK ----
"""

# --------------------- CONSTANTS --------------------- #
"""
    ---- THESE NEED TO BE UPDATED OR CODE WILL NOT WORK ----
"""
MY_EMAIL = "" # ENTER SENDER EMAIL HERE
PASSWORD = "" # ENTER SENDER PASSWORD HERE
EMAIL_SMTP = "" # ENTER SENDER EMAIL SMTP URL



today_tuple = (dt.datetime.today().day, dt.datetime.today().month)

# get birthday information from the birthday data file
people = pandas.read_csv("birthdays.csv").to_dict()

for person_id in people["name"]:

    # check if the birthday day and month match today's
    birthday_tuple = (people["day"][person_id], people["month"][person_id])
    if birthday_tuple == today_tuple:

        # choose a letter template
        file_name = "letter_templates/" + choice(os.listdir(os.getcwd() + "/letter_templates/"))
        with open(file_name, 'r') as file:
            data = file.read()
            data = data.replace("[NAME]", people["name"][person_id])

        # send letter
        with smtplib.SMTP(EMAIL_SMTP) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=people["email"][person_id],
                                msg="Subject:Happy Birthday!\n\n"
                                    + data)
