from ._anvil_designer import EditPriceTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals

class EditPrice(EditPriceTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.custom_price_textfield.enabled = False
    self.custom_price_textfield.placeholder = 'Enter custom price...'

    self.product_image.source = Globals.product['fields']['Main Image'][0]['thumbnails']['large']['url']
    self.regular_price_checkbox.text = f"Regular price: ${Globals.round_to_decimal_places(Globals.product['fields']['Price Lookup'][0], 2)}"
    self.lowest_price_checkbox.text = f"Lowest price: ${Globals.round_to_decimal_places(Globals.product['fields']['Lowest Price Lookup'][0], 2)}"

    if Globals.product['fields']['Has Edited Price'] == 1:
      if Globals.product['fields']['Edited Price'] == Globals.product['fields']['Lowest Price Lookup'][0]:
        self.lowest_price_checkbox.checked = True
      elif Globals.product['fields']['Edited Price'] == Globals.product['fields']['Price Lookup'][0]:
        self.regular_price_checkbox.checked = True
      else:
        self.custom_price_checkbox.checked = True
        self.custom_price_textfield.enabled = True
        self.custom_price_textfield.text = Globals.round_to_decimal_places(Globals.product['fields']['Edited Price'], 2)
    else:
      self.regular_price_checkbox.checked = True

  def regular_price_checkbox_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    if self.regular_price_checkbox.checked:
      self.confirm_price_button.enabled = True
      self.lowest_price_checkbox.checked = False
      self.custom_price_checkbox.checked = False
      self.custom_price_textfield.text = None
      self.custom_price_textfield.placeholder = 'Enter custom price...'
      self.custom_price_textfield.enabled = False

  def lowest_price_checkbox_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    if self.lowest_price_checkbox.checked:
      self.confirm_price_button.enabled = True
      self.regular_price_checkbox.checked = False
      self.custom_price_checkbox.checked = False
      self.custom_price_textfield.text = None
      self.custom_price_textfield.placeholder = 'Enter custom price...'
      self.custom_price_textfield.enabled = False

  def custom_price_checkbox_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    if self.custom_price_checkbox.checked:
      self.confirm_price_button.enabled = False
      self.regular_price_checkbox.checked = False
      self.lowest_price_checkbox.checked = False
      self.custom_price_textfield.enabled = True

  def handle_confirm_price(self):
    user = anvil.users.get_user()
    selected_price = 0
    if self.regular_price_checkbox.checked:
      self.confirm_price_button.text = 'Confirming price...'
      self.confirm_price_button.enabled = False
      self.cancel_button.enabled = False
      Globals.order = Globals.edit_product_in_order_by_id(Globals.product['id'], 'Edited Price', None)
      Globals.order = Globals.edit_product_in_order_by_id(Globals.product['id'], 'Has Edited Price', 0)
      Globals.order = Globals.edit_product_in_order_by_id(Globals.product['id'], 'Price Last Edited By', None)
      update_product = {
      "Edited Price": None,
      "Price Last Edited By": None
      }
      anvil.server.call('update_item', 'products', Globals.product['id'], update_product)
    elif self.lowest_price_checkbox.checked:
      self.confirm_price_button.text = 'Confirming price...'
      self.confirm_price_button.enabled = False
      self.cancel_button.enabled = False
      Globals.order = Globals.edit_product_in_order_by_id(Globals.product['id'], 'Edited Price', Globals.product['fields']['Lowest Price'])
      Globals.order = Globals.edit_product_in_order_by_id(Globals.product['id'], 'Has Edited Price', 1)
      Globals.order = Globals.edit_product_in_order_by_id(Globals.product['id'], 'Price Last Edited By', user['airtable_id'])
      update_product = {
      "Edited Price": Globals.product['fields']['Lowest Price'],
      "Price Last Edited By": user['airtable_id']
      }
      anvil.server.call('update_item', 'products', Globals.product['id'], update_product)
    elif self.custom_price_checkbox.checked:
      self.confirm_price_button.text = 'Confirming price...'
      self.confirm_price_button.enabled = False
      self.cancel_button.enabled = False
      if not Globals.is_valid_currency(self.custom_price_textfield.text):
        alert(f"{self.custom_price_textfield.text} is not a valid currency")
        self.confirm_price_button.enabled = True
        self.cancel_button.enabled = True
        self.confirm_price_button.text = 'Confirm Price'
        return
      if float(self.custom_price_textfield.text) < Globals.product['fields']['Lowest Price']:
        alert(f"Custom price (${Globals.round_to_decimal_places(self.custom_price_textfield.text, 2)}) is lower than the lowest price (${Globals.round_to_decimal_places(Globals.product['fields']['Lowest Price'], 2)}) accepted for this product. Please enter a higher amount.")
        self.confirm_price_button.enabled = True
        self.cancel_button.enabled = True
        self.confirm_price_button.text = 'Confirm Price'
        return

      # Update the price in the Order tuple
      Globals.order = Globals.edit_product_in_order_by_id(Globals.product['id'], 'Edited Price', self.custom_price_textfield.text)
      Globals.order = Globals.edit_product_in_order_by_id(Globals.product['id'], 'Has Edited Price', 1)
      Globals.order = Globals.edit_product_in_order_by_id(Globals.product['id'], 'Price Last Edited By', user['airtable_id'])
      # Update the product's Edited price in airtable
      update_product = {
        "Edited Price": self.custom_price_textfield.text,
        "Price Last Edited By": user['airtable_id']
      }
      anvil.server.call('update_item', 'products', Globals.product['id'], update_product)
    
    # Re-calculate the order total
    Globals.order_total = Globals.calculate_order_total()

    # Go back to start order
    get_open_form().render_start_order()
    self.remove_from_parent()

  def confirm_price_button_click(self, **event_args):
    self.handle_confirm_price()

  def custom_price_textfield_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    if self.custom_price_textfield.text != None:
      if self.custom_price_textfield.text < Globals.product['fields']['Lowest Price']:
        self.confirm_price_button.enabled = False
      else:
        self.confirm_price_button.enabled = True

  def custom_price_textfield_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.handle_confirm_price()

  def cancel_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    get_open_form().render_start_order()

  def custom_price_textfield_lost_focus(self, **event_args):
    """This method is called when the TextBox loses focus"""
    if self.custom_price_textfield.text != None:
      if self.custom_price_textfield.text < Globals.product['fields']['Lowest Price'][0]:
        alert(f"Custom price (${self.custom_price_textfield.text}) cannot be lower than the lowest price (${Globals.product['fields']['Lowest Price Lookup'][0]}) accepted for this product.")
        self.custom_price_textfield.text = Globals.product['fields']['Lowest Price Lookup'][0]
    else:
      self.custom_price_textfield.text = Globals.product['fields']['Price Lookup'][0]






    
