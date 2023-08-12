from ._anvil_designer import StartOrderTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..ProductInOrder import ProductInOrder
from ..SearchProductToAddProductToOrder import SearchProductToAddProductToOrder
from .. import Globals

class StartOrder(StartOrderTemplate):
  def __init__(self, back, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.products_panel.item_template = ProductInOrder

    self.back = back

    Globals.order = Globals.get_globals_order()

    if not Globals.order:
      self.order_total_label.text = 'Order total: $0'
      self.clear_order_button.enabled = False
      self.add_product_button.text = "Add a Product"
    else:
      self.clear_order_button.enabled = True
      self.order_total_label.text = f"Order total: ${Globals.order_total}"
      self.add_product_button.text = "Add another Product"
      self.products_panel.items = (
        Globals.order
      )

  def reset_order_details(self):
    Globals.main = {}
    Globals.product = {}
    Globals.order = ()
    Globals.order_id = 0
    Globals.product_ids = []
    Globals.order_total = 0

  def render_start_order(self):
    self.content_panel.clear()
    self.content_panel.add_component(StartOrder(self.back))

  def add_product_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(SearchProductToAddProductToOrder(self.render_start_order))

  def clear_order_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    c = confirm("Are you sure you want to cancel the order?")
    if c:
      # Set the order's status to cancelled, clear the current product ids, and set former products to product ids
      user = anvil.users.get_user()
      airtable_user = anvil.server.call('match_record', 'users', 'Email', user['email'])
      update_order = {
        "Status": "Cancelled",
        "Products": None,
        "Cancelled By": airtable_user['id'],
        "Former Products": Globals.product_ids
      }
      anvil.server.call('update_item', 'orders', Globals.order_id, update_order)
      
      # Set the products' status back to In Production
      for i in range(len(Globals.product_ids)):
        update_product = {
          "Status": "In Production"
        }
        anvil.server.call('update_item', 'products', Globals.product_ids[i], update_product)

      alert("The order was cancelled successfully.")
        
      # Clear the order locally
      self.reset_order_details()
      Globals.reset_order_details()
      self.content_panel.clear()
      self.content_panel.add_component(StartOrder(self.back))

  def back_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.back()


