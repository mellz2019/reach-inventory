from ._anvil_designer import ViewAllProductsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals
class ViewAllProducts(ViewAllProductsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    if Globals.all_or_only_available == 'All':
      self.hide_unavailable_product_button.text = 'Hide Sold Out Products'
      self.products_panel.items = Globals.all_products_main
    else:
      self.hide_unavailable_product_button.text = 'Show Sold Out Products'
      self.products_panel.items = [main for main in Globals.all_products_main if main['fields']['Available']>0]

    self.num_of_products_label.text = f"{len(self.products_panel.items)} total products sorted from newest to oldest"

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    get_open_form().go_to_home()

  def hide_unavailable_product_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if Globals.all_or_only_available == 'All':
      Globals.all_or_only_available = 'Only Available'
    else:
      Globals.all_or_only_available = 'All'
    self.content_panel.clear()
    self.add_component(ViewAllProducts())

