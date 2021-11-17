from zillow_interface import ZillowInterface
from google_form_interface import GoogleFormInterface


zillow_interface = ZillowInterface()
apartment_listings = zillow_interface.get_listings()

google_form_interface = GoogleFormInterface()
google_form_interface.fill_out_form(apartment_listings)
