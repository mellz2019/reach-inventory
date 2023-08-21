from ._anvil_designer import SearchProductToAddProductToOrderTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals
from ..AddProductToOrder import AddProductToOrder

class SearchProductToAddProductToOrder(SearchProductToAddProductToOrderTemplate):
  def __init__(self, render_start_order, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.search_button.enabled = False

    # Any code you write here will run before the form opens.
    self.render_start_order = render_start_order

  def render_search_product_to_add_to_order(self):
    self.content_panel.clear()
    self.content_panel.add_component(SearchProductToAddProductToOrder(self.render_start_order))
    

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    data = anvil.server.call('decode', anvil.image.generate_thumbnail(file, 640))

    if len(data) < 1:
      alert('No barcode found.')
    else:
      self.barcode_textbox.text = ",".join(data)
      self.search_button.enabled = True

  def form_show(self, **event_args):
    """This method is called when the HTML panel is shown on the screen"""
    # Use some custom JS to hint the FileLoader to open the phone camera by default
    self.call_js("initFileLoader")

  def handle_search(self):
    self.search_button.text = 'Searching...'
    self.search_button.enabled = False
    self.file_loader_1.enabled = False
    self.barcode_textbox.enabled = False

    if self.barcode_textbox.text == None:
      alert('Please scan or enter a barcode.')
      self.search_button.text = 'Search'
      self.file_loader_1.enabled = True
      return
    
    product = anvil.server.call('match_record', 'products', 'Barcode', self.barcode_textbox.text)

    has_main = 0
    
    if not product:
      alert('Product not found.')
      self.search_button.text = 'Search'
      self.search_button.enabled = True
      self.file_loader_1.enabled = True
      self.barcode_textbox.enabled = True
      return
    else:
      has_main = product['fields']['Has Main']
    if has_main != 1:
      alert('Product is not connected to main.')
      self.search_button.text = 'Search'
      self.search_button.enabled = True
      self.file_loader_1.enabled = True
      self.barcode_textbox.enabled = True
      return
    else:
      Globals.main = anvil.server.call('get_single_item', 'main', product['fields']['Main ID'][0])
      Globals.product = product
      self.content_panel.clear()
      self.content_panel.add_component(AddProductToOrder(self.render_start_order))

  def search_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.handle_search()
    
  def barcode_textbox_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    if self.barcode_textbox.text != None and self.barcode_textbox.text > 0:
      self.search_button.enabled = True
    else:
      self.search_button.enabled = False

  def barcode_textbox_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.handle_search()




