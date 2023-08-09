from ._anvil_designer import ItemDetailsTemplate
from anvil import *
import anvil.server
from .. import Globals

class ItemDetails(ItemDetailsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    product = Globals.product

    self.title_label.text = product['fields']['Barcode']['text']

    is_in_order = product['fields']['In Order']
    if is_in_order == 1:
      self.add_to_order_button.text = 'Item In Order'
      self.add_to_order_button.enabled = False
    else:
      self.add_to_order_button.text = 'Add to New Order'
      self.add_to_order_button.enabled = True
    
    self.cover_image.source = product['fields']['Cover Image'][0]['thumbnails']['full']['url']
    self.descriptioin_label.text = product['fields']['Description']
    self.condition_label.text = product['fields']['Condition']
    price = product['fields']['Price']
    self.price_label.text = f'${price}'
    self.status_label.text = product['fields']['Status']

  def add_to_order_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    new_order = {
      'Products': Globals.product['id']
    }
    anvil.server.call('add_item', 'orders', new_order)

