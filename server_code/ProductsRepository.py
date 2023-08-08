import anvil.server
from airtable import Airtable
from .Keys import MY_API_KEY, PRODUCTS_TABLE_NAME, REACH_PRODUCTS_BASE_ID

products_table = Airtable(REACH_PRODUCTS_BASE_ID, PRODUCTS_TABLE_NAME, MY_API_KEY)

@anvil.server.callable
def add_product(product):
    try:
      inserted_record = products_table.insert(product, True)
    except Exception as e:
        return f'Error inserting product:  + {e}'
    else:
        if return_record:
            return inserted_record

@anvil.server.callable
def delete_product(id):
    try:
      products_table.delete(record_id)
    except Exception as e:
        return f'Error deleting product: {e}'
    else:
        return 'Product deleted successfully'

@anvil.server.callable
def get_all_products():
  return products_table.get_all()

@anvil.server.callable
def get_product(id):
  product = products_table.get(id)
  if not product:
    return 'Product not found'
  else:
    return product

@anvil.server.callable
def update_product(id, fields):
  product = products_table.get(id)
  if not product:
    return f'Error: product not found for id: {id}'
  else:
    try:
      products_table.update(record_id, fields, True)
    except Exception as e:
        return f'Error updating product: {e}'
    else:
        return 'Product updated successfully'