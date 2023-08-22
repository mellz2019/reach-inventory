from ._anvil_designer import PendingOrderTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals

class PendingOrder(PendingOrderTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.date_label.text = Globals.convert_airtable_date_to_friendly_date(self.item['fields']['Date'])
    count_word = "products"
    if self.item['fields']['Total Items'] == 1:
      count_word = "product"
    self.num_of_products.text = f"{self.item['fields']['Total Items']} {count_word}"
    self.status_label.text = self.item['fields']['Status']
    airtable_user = anvil.server.call('get_single_item', 'users', self.item['fields']['Created By'][0])
    self.created_by_label.text = airtable_user['fields']['Name']
      
  def view_order_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    order_status = anvil.server.call('get_single_item', 'orders', self.item['id'])['fields']['Status']
    if order_status == 'Complete' or order_status == "Cancelled":
      alert('Cannot view a cancelled order')
      return
    self.view_order_button.enabled = False
    self.view_order_button.text = "Loading order..."
    Globals.order_id = self.item['id']
    Globals.order = ()
    product_ids_from_airtable = self.item['fields']['Products']
    for p in range(len(product_ids_from_airtable)):
      product_from_airtable = anvil.server.call('match_record', 'products', 'Record ID', product_ids_from_airtable[p])
      Globals.order = Globals.order + (product_from_airtable,)
    # Calculate order total
    Globals.order_total = Globals.calculate_order_total()
    # Render the UI
    self.content_panel.clear()
    if self.item['fields']['Status'] == 'Finalization':
      get_open_form().render_finalize_order()
    else:
      get_open_form().render_start_order()

    
