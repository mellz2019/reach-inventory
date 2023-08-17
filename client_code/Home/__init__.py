from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
from ..ProductInformation import ProductInformation
from .. import Globals
from ..OrderSelector import OrderSelector
from ..PriceConfirmation import PriceConfirmation

class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def cancel(self):
    self.content_panel.clear()
    self.content_panel.add_component(Home())

  def product_info_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = anvil.users.get_user()
    if user:
      if user['admin'] or user['can_view_product_info']:
        self.content_panel.clear()
        self.content_panel.add_component(ProductInformation(self.cancel))
      else:
        alert('You do not have access to this feature. Please contact an administrator.')
    else:
      alert('You must be signed in to use this feature.')

  def orders_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = anvil.users.get_user()
    if user:
      if user['admin'] or user['can_start_order']:
        self.content_panel.clear()
        self.content_panel.add_component(OrderSelector(self.cancel))
      else:
        alert('You do not have access to this feature. Please contact an administrator.')
    else:
      alert('You must be signed in to use this feature.')

  def price_confirmation_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = anvil.users.get_user()
    if user:
      if user['airtable_id'] == 'rec6PFEn8sQhkdO3J' or user['airtable_id'] == 'recLMPfGbsbReIeZD':
        self.price_confirmation_button.text = 'Loading...'
        self.price_confirmation_button.enabled = False
        self.product_info_button.enabled = False
        self.orders_button.enabled = False
        # Load the info
        Globals.price_confirmation_products = anvil.server.call('get_items_from_view', 'main', 'Pending Price Confirmation')
        if Globals.price_confirmation_products:
          Globals.currently_selected_price_confirm_product = 0
          self.content_panel.clear()
          self.content_panel.add_component(PriceConfirmation())
        else:
          alert('There are no products that need price confirmation at this time.')
          self.price_confirmation_button.text = 'Price Confirmation'
          self.price_confirmation_button.enabled = True
          self.product_info_button.enabled = True
          self.orders_button.enabled = True
          return
      else:
        alert('You do not have access to this feature.')
        return
    else:
      alert('You must be signed in to use this feature.')
      return

