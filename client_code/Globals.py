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
comment_text_box_changed = False

# Price Confirmation
price_confirmation_mains = []
currently_selected_price_confirm_product = 0
price_changed = False
price_confirmed = False
comments_changed = False
set_aside = 0
main_number_name_list = []

# Order Selector Orders
selected_order_ownership = ''
selected_order_status = ''
pending_orders = ()

# Change Price
change_price_products = ()
single_product_or_all_products = 'All'
total_number_of_change_products = 0
lowest_price_changed = False

# Product Details
coming_from_product_details = False

# View All Products
all_products_main = ()

# Comments
comments = ()
comment_label = 'Comments'
edited_comment_change = False

# Filters for pending orders
filters_manually_shown = True
max_num_of_pending_orders_to_show = 25

# Cancelled Order
product_cancelled = {}
main_cancelled = {}

def clar_selected_order_information():
  selected_order_ownership = ''
  selected_order_status = ''

def clear_price_confirmation_information():
  price_confirmation_mains = []
  currently_selected_price_confirm_product = 0
  price_changed = False
  price_confirmed = False
  comments_changed = False
  set_aside = 0
  main_number_name_list = []

def reset_order_details():
  main = {}
  #product = {}
  order = ()
  order_id = 0
  order_total = 0
  order_paid = False
  comment_text_box_changed = False

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

def convert_airtable_date_to_friendly_date_with_time(date_time):
  date_obj = datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%S.%fZ')
  return date_obj.strftime('%B %d, %Y - %I:%M%p')

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
    return bool(re.match(pattern, str(value)))

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

def alternate_round_to_two_decimal_places(value):
  return "{:.2f}".format(value)

def calculate_order_total():
  total = 0
  for item in order:
      fields = item['fields']
      if fields.get('Has Edited Price', 0) == 1:
          total += float(fields.get('Edited Price', 0))
      else:
          total += float(fields.get('Price Lookup'[0], 0))
        
  return round_to_decimal_places(total, 2)

def ensure_order_can_be_completed():
  for item in order:
      if item['fields']['Status'] not in ['Picked Up', 'Delivered']:
          return False
  return True