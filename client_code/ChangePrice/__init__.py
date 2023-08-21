from ._anvil_designer import ChangePriceTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals

class ChangePrice(ChangePriceTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    if Globals.single_product_or_all_products == 'All':
      self.title_label.text = f"Changing price for {len(Globals.change_price_products_ids)} products"
    else:
      self.title_label.text = 'Changing price for 1 product'

  def confirm_price_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.cancel_button.enabled = False
    self.regular_price_text_box.enabled = False
    self.lowest_price_text_box.enabled = False

    self.confirm_price_button.text = 'Confirming Price...'

    if Globals.single_product_or_all_products == 'All':
      # Get the main
      # Get all of the linked product ids
      # Update each product that has a status of 'In Production'
      # Go back to more actions
      pass
    else:
      # Update the product
      pass

  def regular_price_text_box_lost_focus(self, **event_args):
    """This method is called when the TextBox loses focus"""
    pass

  def regular_price_text_box_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    pass

  def lowest_price_text_box_lost_focus(self, **event_args):
    """This method is called when the TextBox loses focus"""
    pass

  def lowest_price_text_box_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    pass




