from ._anvil_designer import OldHomeTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from ..AddProducts import AddProducts

class OldHome(OldHomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    all_products = anvil.server.call('get_all_items', 'products')
    all_product_count = len(all_products)
    
    sold_products = anvil.server.call('get_items_from_view', 'products', 'Sold')
    sold_products_count = len(sold_products)

    self.total_product_label.text = f'Products: {all_product_count}'
    self.products_sold_label.text = f'Products Sold: {sold_products_count}'

  # def add_items_button_click(self, **event_args):
   # self.content_panel.clear()
   # self.content_panel.add_component(AddProducts())

  def product_info_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('ItemInformation', my_parameter="an_argument")



