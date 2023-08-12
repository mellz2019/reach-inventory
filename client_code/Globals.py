import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from datetime import datetime

main = {}
product = {}

# Order information
order = ()
order_id = 0
# The product IDs in the order. If the user cancels the order, then the products' statuses need to go back to 'In Production'
product_ids = []
order_total = 0

def reset_order_details():
  main = {}
  product = {}
  order = ()
  order_id = 0
  product_ids = []
  order_total = 0

def get_globals_order():
  return order


def convert_airtable_date_to_date_time(airtable_date):
    year = airtable_date.split("-")[0]
    month = airtable_date.split("-")[1]
    day = airtable_date.split("-")[2]

    first_covered_date_full = year + "-" + month + "-" + day

    return datetime.strptime(first_covered_date_full, "%Y-%m-%d").date()

def convert_airtable_date_to_friendly_date(date):
  date_string = str(convert_airtable_date_to_date_time(date))
  date_object = datetime.strptime(date_string, '%Y-%m-%d')
  return date_object.strftime('%B %d, %Y')

def convert_list_to_string(list):
  return ', '.join(list)

def remove_element_by_id(tup, target_id):
    # Convert tuple to list
    lst = list(tup)
    # Filter out the element with the matching id
    lst = [item for item in lst if item['id'] != target_id]
    # Convert list back to tuple
    return tuple(lst)