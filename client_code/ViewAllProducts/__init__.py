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
    self.products_panel.items = Globals.all_products_main

    self.num_of_products_label.text = f"{len(Globals.all_products_main)} total products"

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    get_open_form().go_to_home()
