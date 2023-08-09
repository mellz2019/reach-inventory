from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.server
from ..AddProducts import AddProducts

class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  # def add_items_button_click(self, **event_args):
   # self.content_panel.clear()
   # self.content_panel.add_component(AddProducts())

  def product_info_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('ItemInformation', my_parameter="an_argument")



