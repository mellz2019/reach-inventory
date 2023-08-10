from ._anvil_designer import AddProductsTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server

class AddProducts(AddProductsTemplate):
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

  def add_item_button_click(self, **event_args):
    """This method is called when the button is clicked"""

    if not all(c.isnumeric() for c in self.barcode_text_box.text):
      alert('Only numbers are allowed in barcode field')
      return
    
    if self.barcode_text_box == '' or self.description_text_box.text == '':
      alert("Please fill in all fields.")
      return

    product_to_insert = {
      "Barcode": self.barcode_text_box.text,
      "Condition": self.condition_drop_down.selected_value,
      "Description": self.description_text_box.text,
      "Added By": 'recLMPfGbsbReIeZD'
    }
    alert(anvil.server.call('add_item', 'products', product_to_insert, False))


 

