from ._anvil_designer import ProductInOrderTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals
from ..EditPrice import EditPrice

class ProductInOrder(ProductInOrderTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    if not Globals.order:
      self.product_title_label.text = "Please add a product."
    else:
      self.product_title_label.text = self.item['fields']['Main Name'][0]
      self.product_image.source = self.item['fields']['Main Image'][0]['thumbnails']['large']['url']
      selected_price = 0
      if self.item['fields']['Has Edited Price'] == 1:
        selected_price = self.item['fields']['Edited Price']
      else:
        selected_price = self.item['fields']['Price']
      self.product_price_label.text = f"${Globals.round_to_decimal_places(selected_price, 2)}"

  def remove_product_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    c = confirm("Are you sure you want to remove this product from the order?")

    if c:
      # Update the product's status back to "In Production"
      update_product = {
        "Status": "In Production",
        "Order": None,
        "Edited Price": None
      }
      anvil.server.call('update_item', 'products', self.item['id'], update_product)

      # Remove the product from Globals.order and the product id from the list of product ids
      Globals.order = Globals.remove_element_by_id(Globals.order, self.item['id'])
    
      # Reset necessary Globals
      Globals.order_total = Globals.calculate_order_total()
      
      # Refresh the UI
      get_open_form().render_start_order()
      self.remove_from_parent()
    else:
      return

  def edit_price_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Make sure that the price can be edited
    if float(self.item['fields']['Price']) < float(self.item['fields']['Lowest Price']) and self.item['fields']['Has Edited Price'] == 0:
      alert(f"${self.item['fields']['Price']} is the lowest price accepted for this item. The price cannot be edited.")
    else:
      Globals.product = Globals.get_single_product_from_order(self.item['id'])
      self.content_panel.clear()
      get_open_form().clear_start_order_content_panel()
      


