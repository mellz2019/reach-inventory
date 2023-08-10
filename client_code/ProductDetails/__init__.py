from ._anvil_designer import ProductDetailsTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from .. import Globals

class ProductDetails(ProductDetailsTemplate):
  def __init__(self, back_button_callback, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.back_button_callback = back_button_callback

    product = Globals.product
    main = Globals.main

    self.name_label.text = main['fields']['Name']
    self.product_image.source = main['fields']['Image'][0]['thumbnails']['large']['url']
    self.description_label.text = main['fields']['Description']
    self.category_label.text = f"Categories: {Globals.convert_list_to_string(main['fields']['Category'])}"
    msrp_price = product['fields']['Price']
    lowest_price = product['fields']['Lowest Price']
    self.price_label.text = f'MSRP: ${msrp_price}'
    self.lowest_price_label.text = f'Lowest Price: ${lowest_price}'
    self.status_label.text = f'Status: {product["fields"]["Status"]}'
    total_quantity = main['fields']['Quantity']
    self.total_quantity_label.text = f'{total_quantity} total unit(s)'
    available_quantity = main['fields']['Available']
    self.available_label.text = f'{available_quantity} unit(s) available for sale'
    quantity_sold = main['fields']['Sold']
    self.quantity_sold_label.text = f'{quantity_sold} unit(s) sold'
    added_on = Globals.convert_airtable_date_to_friendly_date(product['fields']['Date Added'])
    self.added_on_label.text = f'Added on: {added_on}'
    approved_on = Globals.convert_airtable_date_to_friendly_date(product['fields']['Approved For Sale On'])
    self.approved_for_sale_on_label.text = f'Approved for Sale on: {approved_on}'

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.back_button_callback()
    
    
