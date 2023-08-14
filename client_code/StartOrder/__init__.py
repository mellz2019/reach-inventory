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
from ..EditPrice import EditPrice
from ..FinalizeOrder import FinalizeOrder

class StartOrder(StartOrderTemplate):
  def __init__(self, back, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.products_panel.item_template = ProductInOrder

    self.back = back

    Globals.order = Globals.get_globals_order()

    if not Globals.order:
      self.order_total_label.text = 'Order total: $0.00'
      self.clear_order_button.enabled = False
      self.add_product_button.text = "Add a Product"
      self.finalize_order_button.enabled = False
    else:
      self.new_order_label.text = f"Order - {Globals.order_id}"
      self.clear_order_button.enabled = True
      self.order_total_label.text = f"Order total: ${Globals.round_to_decimal_places(Globals.order_total, 2)}"
      self.add_product_button.text = "Add another Product"
      self.finalize_order_button.enabled = True
      self.products_panel.items = (
        Globals.order
      )
      order_status = anvil.server.call('get_single_item', 'orders', Globals.order_id)
      if order_status == 'Completed' or order_status == "Canceleed":
        self.add_product_button.enabled = False
        self.finalize_order_button.enabled = False
        self.clear_order_button.enabled = False

  def reset_order_details(self):
    Globals.main = {}
    Globals.product = {}
    Globals.order = ()
    Globals.order_id = 0
    Globals.order_total = 0

  def clear_start_order_content_panel(self):
    self.content_panel.clear()
    self.content_panel.add_component(EditPrice())

  def render_start_order(self):
    Globals.order = Globals.get_globals_order()
    self.content_panel.clear()
    self.content_panel.add_component(StartOrder(self.back))

  def update_order_id_label(self):
    self.new_order_label = f"Order - {Globals.order_id}"

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
        "Former Products": Globals.get_item_from_order_list_dictionary('id')
      }
      anvil.server.call('update_item', 'orders', Globals.order_id, update_order)
      
      # Set the products' status back to In Production
      for i in range(len(Globals.order)):
        update_product = {
          "Status": "In Production",
          "Edited Price": None
        }
        anvil.server.call('update_item', 'products', Globals.order[i]['id'], update_product)

      alert("The order was cancelled successfully.")
        
      # Clear the order locally
      self.reset_order_details()
      Globals.reset_order_details()
      self.content_panel.clear()
      self.content_panel.add_component(StartOrder(self.back))

  def back_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.back()

  def finalize_order_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Update the order's status to 'Finalization'
    self.finalize_order_button.text = "Finalizing..."
    self.add_product_button.enabled = False
    self.finalize_order_button.enabled = False
    self.back_button.enabled = False
    self.clear_order_button.enabled = False
    user = anvil.users.get_user()
    airtable_user = anvil.server.call('match_record', 'users', 'Email', user['email'])
    update_order = {
      "Status": "Finalization",
      "Finalization By": airtable_user['id']
    }
    anvil.server.call('update_item', 'orders', Globals.order_id, update_order)
    self.content_panel.clear()
    self.content_panel.add_component(FinalizeOrder())



