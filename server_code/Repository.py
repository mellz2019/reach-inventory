import anvil.server
from airtable import Airtable
from .Keys import MY_API_KEY, PRODUCTS_TABLE_NAME, REACH_PRODUCTS_BASE_ID

products_table = Airtable(REACH_PRODUCTS_BASE_ID, PRODUCTS_TABLE_NAME, MY_API_KEY)

def get_table(table):
  if table == 'products':
    return products_table

def match_record(table, column_to_match_on, value):
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
def get_all_items(table):
  table = get_table(table)
  return table.get_all()

@anvil.server.callable
def get_single_item(table, id):
  table = get_table(table)
  product = table.get(id)
  if not product:
    return 'Item not found'
  else:
    return product

@anvil.server.callable
def update_item(table, id, fields):
  table = get_table(table)
  if not product:
    return f'Error: Item not found for id: {id}'
  else:
    try:
      table.update(record_id, fields, True)
    except Exception as e:
        return f'Error updating item: {e}'
    else:
        return 'Item updated successfully'