from ._anvil_designer import ProductInOrderTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ProductInOrder(ProductInOrderTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.product_price_label.text = self.item['from']

  def remove_product_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    c = confirm("Are you sure you want to remove this product from the order?")

    if c:
      # Remove the button
      self.remove_product_button.remove_from_parent()

      # Update the product's status back to "In Production"
      # Remove the product from the order
      # Remove the product from the last
    else:
      return

