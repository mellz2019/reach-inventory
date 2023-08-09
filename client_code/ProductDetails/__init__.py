from ._anvil_designer import ProductDetailsTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from .. import Globals

class ProductDetails(ProductDetailsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    product = Globals.product
    
    self.product_image.source = product['fields']['Cover Image'][0]['thumbnails']['full']['url']
