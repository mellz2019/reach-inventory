from ._anvil_designer import OrderSelectorTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class OrderSelector(OrderSelectorTemplate):
  def __init__(self, cancel_button_callback, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.cancel_button_callback = cancel_button_callback

  def cancel_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.cancel_button_callback()

  def start_order_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = anvil.users.get_user()
    if user['admin'] or user['can_start_order']:
        # TO DO
        pass
    else:
        alert('You do not have access to this feature. Please contact an administrator.')


