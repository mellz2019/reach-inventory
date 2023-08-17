import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from datetime import datetime
import re

main = {}
# For when you need to get information on a single product
product = {}

# Order information
order = ()
order_id = 0
order_total = 0
order_paid = False

# Price Confirmation
price_confirmation_products = ()

def reset_order_details():
  main = {}
  product = {}
  order = ()
  order_id = 0
  order_total = 0
  order_paid = False

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

def get_item_from_order_list_dictionary(item):
  return [d[item] for d in order]

def get_single_product_from_order(id):
  for item in order:
      if item['id'] == id:
          return item
  else:
    return None

def is_valid_currency(value):
    pattern = r'^\d{1,3}(,\d{3})*(\.\d{2})?$'
    return bool(re.match(pattern, value))

def edit_product_in_order_by_id(id, value_to_update, update_value):
    items_list = list(order)
    for item in items_list:
        if item['id'] == id:
            item['fields'][value_to_update] = update_value
    return tuple(items_list)

def add_trailing_zero_if_needed(value):
    if len(str(value).split(".", 1)[1]) < 2:
        string_value = str(value)
        string_value += "0"
        return string_value
    else:
        return str(value)

def round_to_decimal_places(value, number_of_decimal_places):
    if "." in str(value):
        rounded_value = round(float(value), number_of_decimal_places)
        rounded_value = add_trailing_zero_if_needed(rounded_value)
        return rounded_value
    else:
        rounded_value = str(value)
        rounded_value += ".00"
        return rounded_value

def calculate_order_total():
  total = 0
  for item in order:
      fields = item['fields']
      if fields.get('Has Edited Price', 0) == 1:
          total += float(fields.get('Edited Price', 0))
      else:
          total += float(fields.get('Price', 0))
        
  return round_to_decimal_places(total, 2)

def ensure_order_can_be_completed():
  for item in order:
      if item['fields']['Status'] not in ['Picked Up', 'Delivered']:
          return False
  return True