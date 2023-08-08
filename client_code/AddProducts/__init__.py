from ._anvil_designer import AddProductsTemplate
from anvil import *
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

 

