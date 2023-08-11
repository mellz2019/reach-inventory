from ._anvil_designer import AddProductToOrderTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals
from datetime import date

class AddProductToOrder(AddProductToOrderTemplate):
  def __init__(self, render_start_order, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.render_start_order = render_start_order

    # Any code you write here will run before the form opens.
    self.product_name_label.text = Globals.main['fields']['Name']
    self.product_image.source = Globals.main['fields']['Image'][0]['thumbnails']['large']['url']
    self.price_label.text = f"${Globals.product['fields']['Price']}"
    self.status_label.text = f"Status: {Globals.product['fields']['Status']}"

  def add_product_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # If Globals.order is empty, then create a new Order record in AirTable and set the id in globals
    # just in case the user cancels the order
    if Globals.product['fields']['Status'] != 'In Production':
      alert('Product status must be In Production to add to an order.')
      return
    anvil_user = anvil.users.get_user()
    airtable_user = anvil.server.call('match_record', 'users', 'Email', anvil_user['email'])
    if not airtable_user:
      # TODO
      alert('Airtable user not found. Please contant an administrator.')
    else:
      if not Globals.order:
        # This is the first product in the order
        # Create Order in airtable
        order_to_add = {
          "Products": Globals.product['id'],
          "Created By": airtable_user['id']
        }
        new_order = anvil.server.call('add_item', 'orders', order_to_add)
        update_product_status = {
          "Status": "In Pending Order"
        }
        anvil.server.call('update_item', 'products', Globals.product['id'], update_product_status)
        Globals.order = Globals.order + (Globals.product,)
        Globals.order_total = Globals.product['fields']['Price']
        Globals.product_ids.append(Globals.product['id'])
        Globals.order_id = new_order['id']
        alert('Product added to order successfully!')
        self.render_start_order()
      else:
        update_product_status = {
          "Status": "In Pending Order",
          "Order": Globals.order_id
        }
        anvil.server.call('update_item', 'products', Globals.product['id'], update_product_status)
        Globals.order = Globals.order + (Globals.product,)
        Globals.order_total += Globals.product['fields']['Price']
        Globals.product_ids.append(Globals.product['id'])
        alert('Product added to order successfully!')
        self.render_start_order()

