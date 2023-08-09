from ._anvil_designer import ProductInformationTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
import anvil.image
from .. import Globals
from ..ProductDetails import ProductDetails

class ProductInformation(ProductInformationTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def file_loader_1_change(self, file, **event_args):
      """This method is called when a new file is loaded into this FileLoader"""
      data = anvil.server.call('decode', anvil.image.generate_thumbnail(file, 640))

      if len(data) < 1:
        alert('No barcode found.')
      else:
        self.barcode_text_box.text = ",".join(data)

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
      self.content_panel.clear()
      self.content_panel.add_component(ProductDetails())
