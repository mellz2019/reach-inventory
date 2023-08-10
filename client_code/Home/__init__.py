from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
from ..ProductInformation import ProductInformation

class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def product_info_button_click(self, **event_args):
    """This method is called when the button is clicked"""

    self.content_panel.clear()
    self.content_panel.add_component(ProductInformation())