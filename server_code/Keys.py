import anvil.server
from airtable import Airtable

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

MY_API_KEY = "pattfKbd6Ze5A1yBl.fa4534b500427cde60a4a665d46bd34367ae59917690eb52ebf4fa544f5cfb10"

# Reach Products
REACH_PRODUCTS_BASE_ID = 'appHnxIVSzngT1dCJ'
PRODUCTS_TABLE_NAME = 'Products'
MAIN_TABLE_NAME = 'Main'
SETS_TABLE_NAME = 'Sets'
ORDERS_TABLE_NAME = 'Orders'
REPORTS_TABLE_NAME = 'Reports'
USERS_TABLE_NAME = 'Users'
ATTENDEES_TABLE_NAME = 'Attendees'