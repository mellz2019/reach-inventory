from ._anvil_designer import RemoveProductFromProductionTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals

class RemoveProductFromProduction(RemoveProductFromProductionTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    product = Globals.product

    self.title_label.text = f"Remove {product['fields']['Barcode']['text']} from Production"
    self.remove_button.enabled = False

  def reason_textbox_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    if len(self.reason_textbox.text) > 10:
      self.remove_button.enabled = True
    else:
      self.remove_button.enabled = False

  def remove_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass


