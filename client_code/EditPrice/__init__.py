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
    self.regular_price_checkbox.text = f"Regular price: ${Globals.product['fields']['Price']}"
    self.lowest_price_checkbox.text = f"Lowest price: ${Globals.product['fields']['Lowest Price']}"

    if Globals.product['fields']['Has Edited Price'] == 1:
      if Globals.product['fields']['Edited Price'] == Globals.product['fields']['Lowest Price']:
        self.lowest_price_checkbox.checked = True
      elif Globals.product['fields']['Edited Price'] == Globals.product['fields']['Price']:
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
      self.lowest_price_checkbox.checked = False
      self.custom_price_checkbox.checked = False
      self.custom_price_textfield.text = None
      self.custom_price_textfield.placeholder = 'Enter custom price...'
      self.custom_price_textfield.enabled = False

  def lowest_price_checkbox_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    if self.lowest_price_checkbox.checked:
      self.regular_price_checkbox.checked = False
      self.custom_price_checkbox.checked = False
      self.custom_price_textfield.text = None
      self.custom_price_textfield.placeholder = 'Enter custom price...'
      self.custom_price_textfield.enabled = False

  def custom_price_checkbox_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    if self.custom_price_checkbox.checked:
      self.regular_price_checkbox.checked = False
      self.lowest_price_checkbox.checked = False
      self.custom_price_textfield.enabled = True

  def confirm_price_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    selected_price = 0
    if self.regular_price_checkbox.checked:
      selected_price = Globals.product['fields']['Price']
    elif self.lowest_price_checkbox.checked:
      selected_price = Globals.product['fields']['Lowest Price']
    elif self.custom_price_checkbox.checked:
      selected_price = self.custom_price_textfield.text

      if not Globals.is_valid_currency(self.custom_price_textfield.text):
        alert(f"{self.custom_price_textfield.text} is not a valid currency")
        return
      if float(self.custom_price_textfield.text) < Globals.product['fields']['Lowest Price']:
        alert(f"Custom price (${self.custom_price_textfield.text}) is lower than the lowest price (${Globals.product['fields']['Lowest Price']}) accepted for this product. Please enter a higher amount.")
        return

    self.confirm_price_button.text = 'Confirming price...'
    self.confirm_price_button.enabled = False
    self.cancel_button.enabled = False

     # Update the price in the Order tuple
    Globals.order = Globals.edit_product_in_order_by_id(Globals.product['id'], 'Edited Price', selected_price)
    # Update the product's Edited price in airtable
    user = anvil.users.get_user()
    airtable_user = anvil.server.call('match_record', 'users', 'Email', user['email'])
    update_product = {
      "Edited Price": selected_price,
      "Price Last Edited By": airtable_user['id']
    }
    anvil.server.call('update_item', 'products', Globals.product['id'], update_product)
    # Re-calculate the order total
    Globals.order_total = Globals.calculate_order_total()

    # Go back to start order
    get_open_form().render_start_order()
    self.remove_from_parent()



    
