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
    if Globals.single_product_or_all_products == 'All':
      if Globals.total_number_of_change_products == 1:
        self.info_label.visible = False
        self.title_label.text = 'Changing price for 1 product'
      else:
        self.title_label.text = f"Changing price for {len(Globals.change_price_products)} products"
        self.info_label.text = f"There are {Globals.total_number_of_change_products} total products of this type. You can change the price of {len(Globals.change_price_products)} products due to their status being 'In Production'."
    else:
      self.info_label.visible = False
      self.title_label.text = 'Changing price for 1 product'

  def confirm_price_button_click(self, **event_args):
    if self.lowest_price_text_box.text != None and self.regular_price_text_box.text != None:
      if self.lowest_price_text_box.text > self.regular_price_text_box.text:
        alert('Lowest price cannot be more than regular price.')
        self.lowest_price_text_box.text = self.regular_price_text_box.text
        return
    """This method is called when the button is clicked"""
    self.cancel_button.enabled = False
    self.regular_price_text_box.enabled = False
    self.lowest_price_text_box.enabled = False
    self.confirm_price_button.enabled = False

    self.confirm_price_button.text = 'Confirming Price...'

    user = anvil.users.get_user()
    
    if Globals.single_product_or_all_products == 'All':
      # Update each product that has a status of 'In Production'
      for i in range(len(Globals.change_price_products)):
        self.update_status_label.text = f"Updating product {i+1} of {len(Globals.change_price_products)}"
        self.update_status_label.visible = True
        update_product = {
          "Price": self.regular_price_text_box.text,
          "Lowest Price": self.lowest_price_text_box.text,
          "Price Last Edited By": user['airtable_id']
        }
        anvil.server.call('update_item', 'products', Globals.change_price_products[i]['id'], update_product)
      self.update_status_label.text = 'Done!'
    else:
      # Update the product
      update_product = {
        "Price": self.regular_price_text_box.text,
        "Lowest Price": self.lowest_price_text_box.text,
        "Price Last Edited By": user['airtable_id']
      }

      anvil.server.call('update_item', 'products', Globals.product['id'], update_product)
    alert(f'The price has been succesfully updated!')
    self.update_status_label.visible = False
      
  def regular_price_text_box_lost_focus(self, **event_args):
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
    get_open_form().render_single_or_all_products()





