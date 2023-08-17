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

    Globals.price_confirmed = False
    Globals.comments_changed = False

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

  def confirm_price_confirm(self):
    if Globals.price_changed and not Globals.price_confirmed:
      c = confirm("You've made changes without clicking Confirm Price. Would you like to confirm the price?")
      return c
    return False

  def confirm_price(self):
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
        "Lowest Price": self.lowest_price_text_box.text,
        "Status": "In Production"
      }
      anvil.server.call('update_item', 'products', linked_product_ids[i], update_product)

    # update the main with the notes
    update_main = {
      "Price Confirmation Notes": self.comment_text_field.text
    }

    Globals.price_confirmed = True
    # if this is not the last product, go to the next product. If it is the last product, go back home
    if Globals.currently_selected_price_confirm_product+1 == len(Globals.price_confirmation_mains):
      # Go home
      self.content_panel.clear()
      get_open_form().go_to_home()
    else:
      self.go_to_next_product()
  
  def go_to_next_product(self):
    Globals.currently_selected_price_confirm_product = Globals.currently_selected_price_confirm_product+1
    self.content_panel.clear()
    self.content_panel.add_component(PriceConfirmation())

  def next_product_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.confirm_price_confirm():
      self.confirm_price()
      self.go_to_next_product()
    else:
      self.go_to_next_product()

  def previous_product_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.confirm_price_confirm():
      self.confirm_price()
      Globals.currently_selected_price_confirm_product = Globals.currently_selected_price_confirm_product-1
      self.content_panel.clear()
      self.content_panel.add_component(PriceConfirmation())
    else:
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

    self.confirm_price()

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

  def back_btton_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.confirm_price_confirm():
      self.confirm_price()
      self.content_panel.clear()
      get_open_form().go_to_home()
    else:
      self.content_panel.clear()
      get_open_form().go_to_home()

  def price_text_box_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    Globals.price_changed = True

  def lowest_price_text_box_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    Globals.price_changed = True

  def comment_text_field_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    Globals.price_changed = True
    Globals.comments_changed = True

  def not_approved_for_sale_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass








    
    
      



