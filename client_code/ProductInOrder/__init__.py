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

class ProductInOrder(ProductInOrderTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    if not Globals.order:
      self.product_title_label.text = "Please add a product."
    else:
      self.product_title_label.text = self.item['fields']['Main Name'][0]
      self.product_image.source = self.item['fields']['Main Image'][0]['thumbnails']['large']['url']
      self.product_price_label.text = f"${self.item['fields']['Price']}"

  def remove_product_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    c = confirm("Are you sure you want to remove this product from the order?")

    if c:
      # Remove the button
      # self.remove_product_button.remove_from_parent()

      # Update the product's status back to "In Production"
      update_product = {
        "Status": "In Production",
        "Order": None
      }
      anvil.server.call('update_item', 'products', self.item['id'], update_product)
    
      # Reset necessary Globals
      Globals.product_ids.remove(self.item['id'])
      Globals.order_total -= self.item['fields']['Price']

      # Remove the product from Globals.order and the product id from the list of product ids
      Globals.order = Globals.remove_element_by_id(Globals.order, self.item['id'])

      # Refresh the UI
      get_open_form().render_start_order()
      self.remove_from_parent()
    else:
      return

