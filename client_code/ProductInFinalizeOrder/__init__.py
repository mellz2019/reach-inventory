from ._anvil_designer import ProductInFinalizeOrderTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals

class ProductInFinalizeOrder(ProductInFinalizeOrderTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.product_image.source = self.item['fields']['Main Image'][0]['thumbnails']['large']['url']
    self.barcode_label.text = self.item['fields']['Barcode']['text']
    self.product_status_dropdown.selected_value = self.item['fields']['Status']
    selected_price = 0
    if self.item['fields']['Has Edited Price'] == 1:
      selected_price = self.item['fields']['Edited Price']
    else:
      selected_price = self.item['fields']['Price Lookup'][0]
    self.price_label.text = f"${Globals.round_to_decimal_places(selected_price, 2)}"

  def product_status_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    update_product = {
      "Status": self.product_status_dropdown.selected_value
    }
    anvil.server.call('update_item', 'products', self.item['id'], update_product)
    Globals.order = Globals.edit_product_in_order_by_id(self.item['id'], 'Status', self.product_status_dropdown.selected_value)
    Globals.order = Globals.get_globals_order()
    n = Notification("Product status change successful!")
    n.show()


