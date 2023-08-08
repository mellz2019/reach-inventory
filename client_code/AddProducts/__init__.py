from ._anvil_designer import AddProductsTemplate
from anvil import *
import anvil.server

class AddProducts(AddProductsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    anvil.server.call('open_camera')