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
    user = anvil.users.get_user()
    orders_exist = True

    self.filter_button.enabled = False

    # Any code you write here will run before the form opens.
    if not Globals.order:
      existing_orders = anvil.server.call('get_num_of_records_from_any_view', 'orders', 25)
    
      for i in range(len(existing_orders)):
        Globals.order = Globals.order + (existing_orders[i],)
    else:
      existing_orders = Globals.order

    if Globals.selected_order_ownership == '':
      Globals.selected_order_ownership = "My Orders"
      belonging_to = f" belonging to {user['First Name']} {user['Last Name'][0]}."
      Globals.selected_order_status = "All"
      self.order_ownership_dropdown.selected_value = Globals.selected_order_ownership
      existing_orders = [order for order in existing_orders if order['fields']['Created By'][0] == user['airtable_id']]
      if not existing_orders:
        orders_exist = False
      status_phrase = 'with all statuses'
      
    else:
      self.order_ownership_dropdown.selected_value = Globals.selected_order_ownership
      self.order_status_dropdown.selected_value = Globals.selected_order_status

      if Globals.selected_order_ownership == 'My Orders':
        belonging_to = f" belonging to {user['First Name']} {user['Last Name'][0]}."
      elif Globals.selected_order_ownership == 'Everyone\'s Orders':
        belonging_to = ''
      
      if Globals.selected_order_ownership == 'My Orders' and Globals.selected_order_status == 'All':
        existing_orders = [order for order in existing_orders if order['fields']['Created By'][0] == user['airtable_id']]
        if not existing_orders:
          orders_exist = False
        status_phrase = 'with all statuses'
      elif Globals.selected_order_ownership == 'My Orders' and Globals.selected_order_status == 'Pending':
        existing_orders = [order for order in existing_orders if order['fields']['Created By'][0] == user['airtable_id'] and order['fields']['Status'] == 'Pending']
        if not existing_orders:
          orders_exist = False
        status_phrase = f'with a status of {Globals.selected_order_status}'
      elif Globals.selected_order_ownership == 'My Orders' and Globals.selected_order_status == 'Finalization':
        existing_orders = [order for order in existing_orders if order['fields']['Created By'][0] == user['airtable_id'] and order['fields']['Status'] == 'Finalization']
        if not existing_orders:
          orders_exist = False
        status_phrase = f'with a status of {Globals.selected_order_status}'
      elif Globals.selected_order_ownership == 'My Orders' and Globals.selected_order_status == 'Complete':
        existing_orders = [order for order in existing_orders if order['fields']['Created By'][0] == user['airtable_id'] and order['fields']['Status'] == 'Complete']
        if not existing_orders:
          orders_exist = False
        status_phrase = f'with a status of {Globals.selected_order_status}'
      elif Globals.selected_order_ownership == 'Everyone\'s Orders' and Globals.selected_order_status == 'All':
        if not existing_orders:
          orders_exist = False
        status_phrase = 'with all statuses'
      elif Globals.selected_order_ownership == 'Everyone\'s Orders' and Globals.selected_order_status == 'Pending':
        existing_orders = [order for order in existing_orders if order['fields']['Status'] == 'Pending']
        if not existing_orders:
          orders_exist = False
        status_phrase = f'with a status of {Globals.selected_order_status}'
      elif Globals.selected_order_ownership == 'Everyone\'s Orders' and Globals.selected_order_status == 'Finalization':
        existing_orders = [order for order in existing_orders if order['fields']['Status'] == 'Finalization']
        if not existing_orders:
          orders_exist = False
        status_phrase = f'with a status of {Globals.selected_order_status}'
      elif Globals.selected_order_ownership == 'Everyone\'s Orders' and Globals.selected_order_status == 'Complete':
        existing_orders = [order for order in existing_orders if order['fields']['Status'] == 'Complete']
        if not existing_orders:
          orders_exist = False
        status_phrase = f'with a status of {Globals.selected_order_status}'

    quantity_phrase = 'There are'
    quantity_word = 'orders'
    num_of_orders = 0
    if orders_exist:
      num_of_orders = len(existing_orders)
      if num_of_orders == 1:
        quantity_phrase = 'There is'
        quantity_word = 'order'
    self.filter_results_label.text = f"{quantity_phrase} {num_of_orders} {quantity_word}{belonging_to} {status_phrase}."
    if orders_exist:
      self.orders_panel.items = existing_orders
    else:
      self.orders_panel.items = None

  def order_ownership_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    pass

  def filter_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    Globals.selected_order_ownership = self.order_ownership_dropdown.selected_value
    Globals.selected_order_status = self.order_status_dropdown.selected_value
    self.content_panel.clear()
    self.content_panel.add_component(PendingOrders())

