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

    self.confirm_price_button.enabled = False

    Globals.lowest_price_changed = False

    # Any code you write here will run before the form opens.
    self.title_label.text = f"Changing price for {Globals.main['fields']['Name']}"

    self.regular_price_text_box.text = Globals.alternate_round_to_two_decimal_places(Globals.product['fields']['Price'][0])
    self.lowest_price_text_box.text = Globals.alternate_round_to_two_decimal_places(Globals.product['fields']['Lowest Price'][0])
    

  def confirm_price_button_click(self, **event_args):
    if self.lowest_price_text_box.text != None and self.regular_price_text_box.text != None:
      if self.lowest_price_text_box.text > self.regular_price_text_box.text:
        alert('Lowest price cannot be more than regular price.')
        self.lowest_price_text_box.text = self.regular_price_text_box.text
        return
    self.cancel_button.enabled = False
    self.regular_price_text_box.enabled = False
    self.lowest_price_text_box.enabled = False
    self.confirm_price_button.enabled = False

    self.confirm_price_button.text = 'Confirming New Price...'

    user = anvil.users.get_user()
    update_price = {
      "Price": self.regular_price_text_box.text,
      "Lowest Price": self.lowest_price_text_box.text,
      "Price Last Edited By": user['airtable_id']
    }

    anvil.server.call('update_item', 'main', Globals.main['id'], update_price)

    Globals.product['fields']['Price'][0] = self.regular_price_text_box.text
    Globals.product['fields']['Lowest Price'][0] = self.lowest_price_text_box.text
    
    alert(f'The price has been succesfully updated!')
    self.update_status_label.visible = False
    get_open_form().render_more_actions()
      
  def regular_price_text_box_lost_focus(self, **event_args):
    if self.regular_price_text_box.text is not None and self.lowest_price_text_box.text is not None:
      if self.lowest_price_text_box.text > self.regular_price_text_box.text:
        self.lowest_price_text_box.text = self.regular_price_text_box.text
        n = Notification('Lowest price cannot be more than regular price.')
        n.show()
        self.confirm_price_button.enabled = True

  def regular_price_text_box_change(self, **event_args):
    if not Globals.is_valid_currency(str(self.regular_price_text_box.text)):
      self.confirm_price_button.enabled = False
      return
    else:
      self.confirm_price_button.enabled = True

    if not Globals.lowest_price_changed:
      self.lowest_price_text_box.text = self.regular_price_text_box.text

    if self.regular_price_text_box.text == None or self.lowest_price_text_box.text == None:
      self.confirm_price_button.enabled = False
    else:
      self.confirm_price_button.enabled = True

  def lowest_price_text_box_lost_focus(self, **event_args):
    if self.lowest_price_text_box.text is not None and self.regular_price_text_box.text is not None:
      if self.lowest_price_text_box.text > self.regular_price_text_box.text:
        self.lowest_price_text_box.text = self.regular_price_text_box.text
        n = Notification('Lowest price cannot be more than regular price.')
        n.show()
        self.confirm_price_button.enabled = True

  def lowest_price_text_box_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    Globals.lowest_price_changed = True

    if self.lowest_price_text_box.text != None and self.regular_price_text_box.text != None:
      if self.lowest_price_text_box.text > self.regular_price_text_box.text:
        self.confirm_price_button.enabled = False
        return
      else:
        self.confirm_price_button.enabled = True

    if self.regular_price_text_box.text == None or self.lowest_price_text_box.text == None:
      self.confirm_price_button.enabled = False
    else:
      self.confirm_price_button.enabled = True

  def cancel_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    get_open_form().render_more_actions()





