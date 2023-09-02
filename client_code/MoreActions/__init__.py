from ._anvil_designer import MoreActionsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals
from ..ChangePrice import ChangePrice

class MoreActions(MoreActionsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    user = anvil.users.get_user()
    self.change_price_button.visible = user['airtable_id'] == 'recLMPfGbsbReIeZD' or user['airtable_id'] == 'rec6PFEn8sQhkdO3J'

    self.barcode_label.text = Globals.product['fields']['Barcode']['text']

    if Globals.product['fields']['Status'] != 'In Production':
      self.change_price_button.enabled = False
      self.move_to_display_button.enabled = False
      self.remove_from_display_button.enabled = False
      self.change_condition_button.enabled = False
      self.status_label_explanation.visible = True
      self.status_label_explanation.text = 'Some options are not available because the product\'s status is not \'In Production\''

    # Any code you write here will run before the form opens.
    product = Globals.product
    main = Globals.main
    
    self.product_name_label.text = f"Editing {main['fields']['Name']}"
    self.product_image.source = main['fields']['Image'][0]['thumbnails']['large']['url']

  def render_more_actions(self):
    self.content_panel.clear()
    self.content_panel.add_component(MoreActions())
  
  def change_price_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if Globals.product['fields']['Status'] == 'In Production':
      Globals.main = anvil.server.call('get_single_item', 'main', Globals.product['fields']['Main'][0])
      self.content_panel.clear()
      self.content_panel.add_component(ChangePrice())
    else:
      alert('Product must have a status of \'In Production\' in order to change its price.')

  def cancel_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    get_open_form().render_product_details()

  def move_to_display_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.change_price_button.enabled = False
    self.move_to_display_button.enabled = False
    self.remove_from_display_button.enabled = False
    self.change_condition_button.enabled = False
    self.cancel_button.enabled = False

    self.move_to_display_button.text = 'Moving to display...'
    update_product = {
      "Is Display Unit": True
    }
    anvil.server.call('update_item', 'products', Globals.product['id'], update_product)
    alert('The product was successfully updated!')
    self.render_more_actions()
    

  def remove_from_display_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.change_price_button.enabled = False
    self.move_to_display_button.enabled = False
    self.remove_from_display_button.enabled = False
    self.change_condition_button.enabled = False
    self.cancel_button.enabled = False

    self.remove_from_display_button.text = 'Removing from display...'
    update_product = {
      "Is Display Unit": False
    }
    anvil.server.call('update_item', 'products', Globals.product['id'], update_product)
    alert('The product was successfully updated!')
    self.render_more_actions()

  def change_condition_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.condition_dropdown.selected_value = Globals.product['fields']['Condition']
    self.condition_dropdown.visible = True
    self.select_condition_label.visible = True
    self.cancel_condition_button.visible = True

  def condition_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    self.change_price_button.enabled = False
    self.move_to_display_button.enabled = False
    self.remove_from_display_button.enabled = False
    self.change_condition_button.enabled = False
    self.cancel_button.enabled = False
    self.cancel_condition_button.enabled = False
    self.condition_dropdown.enabled = False

    self.change_condition_button.text = 'Changing product condtion...'

    update_product = {
      "Condition": self.condition_dropdown.selected_value
    }

    anvil.server.call('update_item', 'products', Globals.product['id'], update_product)
    alert('The product\'s condition was updated successfully!')
    self.render_more_actions()

  def cancel_condition_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.condition_dropdown.visible = False
    self.select_condition_label.visible = False
    self.cancel_condition_button.visible = False







    