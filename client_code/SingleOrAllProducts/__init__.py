from ._anvil_designer import SingleOrAllProductsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals
from ..ChangePrice import ChangePrice

class SingleOrAllProducts(SingleOrAllProductsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def go_to_change_price(self):
    self.content_panel.clear()
    self.content_panel.add_component(ChangePrice())

  def render_single_or_all_products(self):
    self.content_panel.clear()
    self.content_panel.add_component(SingleOrAllProducts())

  def all_products_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    Globals.single_product_or_all_products = 'All'
    self.all_products_button.text = 'Loading...'
    self.all_products_button.enabled = False
    self.single_product_button.enabled = False
    self.cancel_button.enabled = False
    main = anvil.server.call('get_single_item', 'main', Globals.product['fields']['Main'][0])
    Globals.total_number_of_change_products = len(main['fields']['Products'])
    for product_id in main['fields']['Products']:
      product = anvil.server.call('get_single_item', 'products', product_id)
      if product['fields']['Status'] == 'In Production':
        Globals.change_price_products = Globals.change_price_products + (product,)
    self.go_to_change_price()

  def single_product_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    Globals.single_product_or_all_products = 'Single'
    self.go_to_change_price()

  def cancel_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    get_open_form().render_more_actions()



