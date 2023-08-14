from ._anvil_designer import OrderSelectorTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..StartOrder import StartOrder
from ..PendingOrders import PendingOrders

class OrderSelector(OrderSelectorTemplate):
  def __init__(self, cancel, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.cancel = cancel

  def back(self):
    self.content_panel.clear()
    self.content_panel.add_component(OrderSelector(self.cancel))

  def cancel_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.cancel()

  def start_order_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = anvil.users.get_user()
    if user['admin'] or user['can_start_order']:
        self.content_panel.clear()
        self.content_panel.add_component(StartOrder(self.back))
        pass
    else:
        alert('You do not have access to this feature. Please contact an administrator.')

  def pending_orders_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.pending_orders_button.text = 'Loading...'
    self.pending_orders_button.enabled = False
    self.start_order_button.enabled = False
    self.completed_orders_button.enabled = False
    self.content_panel.clear()
    self.content_panel.add_component(PendingOrders())
    pass

  def completed_orders_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass




