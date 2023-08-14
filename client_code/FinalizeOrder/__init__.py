from ._anvil_designer import FinalizeOrderTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..ProductInFinalizeOrder import ProductInFinalizeOrder
from .. import Globals

class FinalizeOrder(FinalizeOrderTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.products_panel.item_template = ProductInFinalizeOrder

    Globals.order = Globals.get_globals_order()

    self.products_panel.items = (Globals.order)

  def render_finalize_order(self):
    self.content_panel.clear()
    self.content_panel.add_component(FinalizeOrder())

  def complete_order_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # All products in the order must have a status of Picked Up or Delivered
    if Globals.ensure_order_can_be_completed():
      self.complete_order_button.enabled = False
      self.complete_order_button.text = 'Completing Order...'
      self.edit_order_button.enabled = False
      # Update each product's Final Price
      selected_price = 0
      for product in Globals.order:
        if product['fields'].get('Has Edited Price', False):
            selected_price = product['fields']['Edited Price']
        else:
            selected_price = product['fields']['Price']
        update_product = {
          "Final Price": selected_price
        }
        anvil.server.call('update_item', 'products', product['id'], update_product)
      user = anvil.users.get_user()
      airtable_user = anvil.server.call('match_record', 'users', 'Email', user['email'])
      update_order = {
        "Status": "Complete",
        "Completed By": airtable_user['id']
      }
      anvil.server.call('update_item', 'orders', Globals.order_id, update_order)
      alert('The order has been completed successfully!')
      Globals.reset_order_details()
      Globals.order = Globals.get_globals_order()
      self.content_panel.clear()
      get_open_form().go_to_home()
    else:
      alert('All items must have a status of either \"Picked Up" or \"Delivered" in order for the order to be completed')

  def edit_order_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    get_open_form().render_start_order()


