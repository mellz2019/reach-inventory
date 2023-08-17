from ._anvil_designer import PriceConfirmationTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals

class PriceConfirmation(PriceConfirmationTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    products = Globals.price_confirmation_products
    selected_product_index = Globals.currently_selected_price_confirm_product

    if selected_product_index == 0:
      self.previous_product_button.enabled = False

    if selected_product_index+1 == len(products):
      self.next_product_button.enabled = False

    # Any code you write here will run before the form opens.
    self.title_label.text = f"Product {selected_product_index+1} of {len(products)}"
    self.name_label.text = products[selected_product_index]['fields']['Name']
    self.product_image.source = products[selected_product_index]['fields']['Image'][0]['thumbnails']['large']['url']
