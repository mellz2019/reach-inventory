from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
from ..ProductInformation import ProductInformation
from .. import Globals

class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def product_info_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = anvil.users.get_user()
    if user:
      if user['admin'] or user['can_view_product_info']:
        self.content_panel.clear()
        self.content_panel.add_component(ProductInformation())
      else:
        alert('You do not have access to this feature. Please contact an administrator.')
    else:
      alert('You must be signed in to use this feature.')