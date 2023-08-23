from ._anvil_designer import ProductInViewAllProductsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ProductInViewAllProducts(ProductInViewAllProductsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.product_name_label.text = self.item['fields']['Name']
    self.product_image.source = self.item['fields']['Image'][0]['thumbnails']['large']['url']
    available_units = self.item['fields']['Available']
    if available_units == 1:
      phrase = 'unit'
    else:
      phrase = 'units'
    self.availability_label.text = f"{available_units} {phrase} available"

  def view_price_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.view_price_button.text = 'Loading...'
    product_ids = self.item['fields']['Products']
    for product_id in product_ids:
      product = anvil.server.call('get_single_item', 'products', product_id)
      if product['fields']['Do Not Use as Price Example Formula'] == 0:
        self.regular_price_label.visible = True
        self.lowest_price_label.visible = True
        self.view_price_button.visible = False
        self.regular_price_label.text = f"Regular Price: ${product['fields']['Price']}"
        self.lowest_price_label.text = f"Lowest Price ${product['fields']['Lowest Price']}"
        return

        
    