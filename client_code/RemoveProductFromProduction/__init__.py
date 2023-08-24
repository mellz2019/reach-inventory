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
    if len(self.reason_textbox.text) >= 10:
      self.remove_button.enabled = True
    else:
      self.remove_button.enabled = False

  def remove_from_production(self):
    self.remove_button.text = "Removing from Production..."
    self.remove_button.enabled = False
    self.cancel_button.enabled = False
    self.reason_textbox.enabled = False
    user = anvil.users.get_user()
    update_product = {
      "Status": "Removed from Production",
      "Removed from Production Reason": self.reason_textbox.text,
      "Removed from Production By": user['airtable_id']
    }
    anvil.server.call('update_item', 'products', Globals.product['id'], update_product)

    # Get the updated product
    Globals.product['fields']['Status'] = 'Removed from Production'
    
    # Go back
    get_open_form().back_button_callback()

  def remove_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.remove_from_production()

  def reason_textbox_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.remove_from_production()

  def cancel_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    get_open_form().back_button_callback()




