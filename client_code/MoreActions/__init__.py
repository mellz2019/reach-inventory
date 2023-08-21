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
from ..SingleOrAllProducts import SingleOrAllProducts

class MoreActions(MoreActionsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    user = anvil.users.get_user()
    self.change_price_button.enabled = user['airtable_id'] == 'recLMPfGbsbReIeZD' or user['airtable_id'] == 'rec6PFEn8sQhkdO3J'

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
      self.content_panel.clear()
      self.content_panel.add_component(SingleOrAllProducts())
    else:
      alert('Product must have a status of \'In Production\' in order to change its price.')

  def cancel_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    get_open_form().render_product_details()


    