from ._anvil_designer import PendingOrdersTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals

class PendingOrders(PendingOrdersTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    if not Globals.order:
      existing_orders = anvil.server.call('get_items_from_view', 'orders', 'Past Week')

    for i in range(len(existing_orders)):
      Globals.orders = Globals.order + (existing_orders[i],)
    
    self.orders_panel.items =  existing_orders