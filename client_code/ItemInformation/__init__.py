from ._anvil_designer import ItemInformationTemplate
from anvil import *
import anvil.server
from .. import Globals

class ItemInformation(ItemInformationTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.


  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    self.raise_event("change", file=file)

  def form_show(self, **event_args):
    """This method is called when the HTML panel is shown on the screen"""

    # Use some custom JS to hint the FileLoader to open the phone camera by default
    self.call_js("initFileLoader")

  def search_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    product = anvil.server.call('match_record', 'products', 'Barcode', self.barcode_text_box.text)
    if not product:
      alert('Item not found.')
    else:
      Globals.product = product
      open_form('ItemDetails', my_parameter="an_argument")

