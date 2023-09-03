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

    self.add_product_button.enabled = True

    # Any code you write here will run before the form opens.
    self.product_name_label.text = Globals.main['fields']['Name']
    self.product_image.source = Globals.main['fields']['Image'][0]['thumbnails']['large']['url']
    self.price_label.text = f"${Globals.product['fields']['Price']}"
    self.status_label.text = f"Status: {Globals.product['fields']['Status']}"

  def add_product_button_click(self, **event_args):
    # We don't want to add the same product twice.
    self.add_product_button.enabled = False
    self.add_product_button.text = 'Adding product'
    self.cancel_button.enabled = False
    """This method is called when the button is clicked"""
    # If Globals.order is empty, then create a new Order record in AirTable and set the id in globals
    # just in case the user cancels the order
    if Globals.product['fields']['Status'] != 'In Production':
      alert('Product status must be In Production to add to an order.')
      self.cancel_button.enabled = True
      self.add_product_button.enabled = True
      self.add_product_button.text = 'Add Product to Order'
      return
    user = anvil.users.get_user()
    if not Globals.order:
      # This is the first product in the order
      # Create Order in airtable
      order_to_add = {
        "Products": Globals.product['id'],
        "Created By": user['airtable_id']
      }
      new_order = anvil.server.call('add_item', 'orders', order_to_add)
      update_product_status = {
        "Status": "In Pending Order",
        "Added to Order By": user['airtable_id']
      }
      anvil.server.call('update_item', 'products', Globals.product['id'], update_product_status)
      Globals.order = Globals.order + (Globals.product,)
      Globals.order_total = Globals.product['fields']['Price'][0]
      Globals.order_id = new_order['id']
      Globals.order_paid = False
      self.content_panel.clear()
      get_open_form().update_start_order_order_id_label()
      self.render_start_order()
    else:
      update_product_status = {
        "Status": "In Pending Order",
        "Order": Globals.order_id,
        "Added to Order By": user['airtable_id']
      }
      anvil.server.call('update_item', 'products', Globals.product['id'], update_product_status)
      Globals.order = Globals.order + (Globals.product,)
      Globals.order_total = Globals.calculate_order_total()
      self.render_start_order()

  def cancel_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    #TODO
    get_open_form().render_start_order()
    pass


