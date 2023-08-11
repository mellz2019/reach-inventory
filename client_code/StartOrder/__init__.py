from ._anvil_designer import StartOrderTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..ProductInOrder import ProductInOrder
from ..SearchProductToAddProductToOrder import SearchProductToAddProductToOrder

class StartOrder(StartOrderTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.products_panel.item_template = ProductInOrder

    self.products_panel.items = (
      {'from': 'Joe', 'subject': 'Latest tech report'},
      {'from': 'Sally', 'subject': 'Movie night on Friday?'},
      {'from': 'Ada', 'subject': 'My top 10 cat videos'},
    )

  def render_start_order(self):
    self.content_panel.clear()
    self.content_panel.add_component(StartOrder())

  def add_product_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(SearchProductToAddProductToOrder(self.render_start_order))
