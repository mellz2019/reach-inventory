from ._anvil_designer import PriceConfirmationTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals

class PriceConfirmation(PriceConfirmationTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    mains = Globals.price_confirmation_mains
    selected_product_index = Globals.currently_selected_price_confirm_product

    linked_product = anvil.server.call('get_single_item', 'products', mains[selected_product_index]['fields']['Products'][0])

    if selected_product_index == 0:
      self.previous_product_button.enabled = False

    if selected_product_index+1 == len(mains):
      self.next_product_button.enabled = False

    calculated_price = linked_product['fields']['Price'] * mains[selected_product_index]['fields']['Pending Price Confirmation']
    self.price_calculation_label.text = f"${Globals.round_to_decimal_places(calculated_price, 2)} value"

    # Any code you write here will run before the form opens.
    self.title_label.text = f"Product {selected_product_index+1} of {len(mains)}"
    self.name_label.text = mains[selected_product_index]['fields']['Name']
    pending_units = mains[selected_product_index]['fields']['Pending Price Confirmation']
    word = 'units'
    if pending_units == 1:
      word = 'unit'
    self.unit_count.text = f"{pending_units} {word}"
    self.product_image.source = mains[selected_product_index]['fields']['Image'][0]['thumbnails']['large']['url']
    self.price_text_box.text = Globals.round_to_decimal_places(linked_product['fields']['Price'], 2)
    self.lowest_price_text_box.text = Globals.round_to_decimal_places(linked_product['fields']['Lowest Price'], 2)

  def next_product_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    Globals.currently_selected_price_confirm_product = Globals.currently_selected_price_confirm_product+1
    self.content_panel.clear()
    self.content_panel.add_component(PriceConfirmation())

  def previous_product_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    Globals.currently_selected_price_confirm_product = Globals.currently_selected_price_confirm_product-1
    self.content_panel.clear()
    self.content_panel.add_component(PriceConfirmation())

  def confirm_price_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if not Globals.is_valid_currency(self.price_text_box.text):
      alert(f"{self.price_text_box.text} is not a valid currency")
      return
    if not Globals.is_valid_currency(self.lowest_price_text_box.text):
      alert(f"{self.lowest_price_text_box.text} is not a valid currency")
      return
    if float(self.price_text_box.text) < float(self.lowest_price_text_box.text):
      alert(f"Lowest price (${self.lowest_price_text_box.text}) can not be higher than regular price (${self.price_text_box.text})")
      return

    self.confirm_price_button.enabled = False
    self.back_btton.enabled = False
    self.previous_product_button.enabled = False
    self.next_product_button.enabled = False
    self.confirm_price_button.text = 'Confirming Price...'
    self.price_text_box.enabled = False
    self.lowest_price_text_box.enabled = False
    self.comment_text_field.enabled = False
    
    # Loop through all of the product_ids conntected to the currently selected main
    # Update each product's price
    linked_product_ids = Globals.price_confirmation_mains[Globals.currently_selected_price_confirm_product]['fields']['Products']
    for i in range(len(linked_product_ids)):
      update_product = {
        "Price": self.price_text_box.text,
        "Lowest Price": self.lowest_price_text_box.text
      }
      anvil.server.call('update_item', 'products', linked_product_ids[i], update_product)

    # update the main with the notes
    # if this is not the last product, go to the next product. If it is the last product, go back home

  def price_text_box_lost_focus(self, **event_args):
    """This method is called when the TextBox loses focus"""
    if not Globals.is_valid_currency(self.price_text_box.text):
      alert(f"{self.price_text_box.text} is not a valid currency")
      return
    if "." not in self.price_text_box.text:
      self.price_text_box.text = self.price_text_box.text + ".00"

    calculated_price = float(self.price_text_box.text) * Globals.price_confirmation_mains[Globals.currently_selected_price_confirm_product]['fields']['Pending Price Confirmation']
    self.price_calculation_label.text = f"${Globals.round_to_decimal_places(calculated_price, 2)} value"

  def lowest_price_text_box_lost_focus(self, **event_args):
    """This method is called when the TextBox loses focus"""
    if not Globals.is_valid_currency(self.lowest_price_text_box.text):
      alert(f"{self.lowest_price_text_box.text} is not a valid currency")
      return
    if "." not in self.lowest_price_text_box.text:
      self.lowest_price_text_box.text = self.lowest_price_text_box.text + ".00"



    
    
      



