import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from airtable import Airtable

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
COMMENTS_TABLE_NAME = 'Comments'

main_table = Airtable(REACH_PRODUCTS_BASE_ID, MAIN_TABLE_NAME, MY_API_KEY)
products_table = Airtable(REACH_PRODUCTS_BASE_ID, PRODUCTS_TABLE_NAME, MY_API_KEY)
orders_table = Airtable(REACH_PRODUCTS_BASE_ID, ORDERS_TABLE_NAME, MY_API_KEY)
users_table = Airtable(REACH_PRODUCTS_BASE_ID, USERS_TABLE_NAME, MY_API_KEY)
comments_table = Airtable(REACH_PRODUCTS_BASE_ID, COMMENTS_TABLE_NAME, MY_API_KEY)

def get_table(table):
  if table == 'products':
    return products_table
  elif table == 'orders':
    return orders_table
  elif table == 'users':
    return users_table
  elif table == 'main':
    return main_table
  elif table == 'comments':
    return comments_table

@anvil.server.callable
def match_record(table, column_to_match_on, value):
    table = get_table(table)
    return table.match(column_to_match_on, value)

@anvil.server.callable
def add_item(table, item, return_record=True):
    table = get_table(table)
    try:
      inserted_record = table.insert(item, True)
    except Exception as e:
      return f'Error inserting item:  + {e}'
    else:
      if return_record:
        return inserted_record
      else:
        return 'Item inserted successfully.'

@anvil.server.callable
def delete_item(table, id):
    table = get_table(table)
    try:
      table.delete(record_id)
    except Exception as e:
        return f'Error deleting item: {e}'
    else:
        return 'Item deleted successfully'

@anvil.server.callable
def get_all_items(table, column_to_sort=None):
  table = get_table(table)
  if column_to_sort is not None:
    items = table.get_all(sort=column_to_sort)
  else:
    items = table.get_all()
  return items

@anvil.server.callable
def search_for_items(table, column_to_search, search_value):
    table = get_table(table)
    return table.search(column_to_search, search_value)

@anvil.server.callable
def get_single_item(table, id):
  table = get_table(table)
  item = table.get(id)
  if not item:
    return 'Item not found'
  else:
    return item

@anvil.server.callable
def get_items_from_view(table, view, column_to_sort=None):
  table = get_table(table)
  if column_to_sort is not None:
    items = table.get_all(view=view, sort=column_to_sort)
  else:
    items = table.get_all(view=view)
  return items

@anvil.server.callable
def get_num_of_records_from_any_view(table, num_records, column_to_sort=None):
  table = get_table(table)
  if column_to_sort is not None:
    items = table.get_all(maxRecords=num_records, sort=column_to_sort)
  else:
    items = table.get_all(maxRecords=num_records)
  return items

@anvil.server.callable
def get_num_of_records_from_specific_view(table, view, num_records, column_to_sort=None):
  table = get_table(table)
  if column_to_sort is not None:
    items = table.get_all(view=view, maxRecords=num_records, sort=column_to_sort)
  else:
    items = table.get_all(view=view, maxRecords=num_records)
  return items
  

@anvil.server.callable
def update_item(table, id, fields):
  table = get_table(table)
  item = table.get(id)
  if not item:
    return f'Error: Item not found for id: {id}'
  else:
    try:
      table.update(id, fields, True)
    except Exception as e:
        return f'Error updating item: {e}'
    else:
        return 'Item updated successfully'