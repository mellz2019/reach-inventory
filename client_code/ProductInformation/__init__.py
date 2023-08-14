from ._anvil_designer import ProductInformationTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
import anvil.image
from .. import Globals
from ..ProductDetails import ProductDetails

class ProductInformation(ProductInformationTemplate):
  def __init__(self, cancel, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.cancel = cancel

    # Any code you write here will run before the form opens.

  def back(self):
    self.content_panel.clear()
    self.content_panel.add_component(ProductInformation(self.cancel))

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

  def search(self):
    if not self.barcode_text_box.text:
      alert("Please scan or enter a barcode.")
      return

    self.search_button.text = "Searching..."
    self.search_button.enabled = False
    self.file_loader_1.enabled = False
    self.button_1.enabled = False
    self.barcode_text_box.enabled = False
    
    product = anvil.server.call('match_record', 'products', 'Barcode', self.barcode_text_box.text)
    
    if not product:
      alert('Product not found.')
      self.search_button.text = "Search"
      self.search_button.enabled = True
      self.file_loader_1.enabled = True
      self.button_1.enabled = True
      self.barcode_text_box.enabled = True
    else:
      has_main = product['fields']['Has Main']
      if has_main != 1:
        alert('Product is not connected to main.')
        self.search_button.text = "Search"
        self.search_button.enabled = True
        self.file_loader_1.enabled = True
        self.button_1.enabled = True
        self.barcode_text_box.enabled = True
      else:
        Globals.main = anvil.server.call('get_single_item', 'main', product['fields']['Main ID'][0])
        Globals.product = product
        self.content_panel.clear()
        self.content_panel.add_component(ProductDetails(self.back))

  def search_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.search()
    
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.cancel()

  def barcode_text_box_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.search()


