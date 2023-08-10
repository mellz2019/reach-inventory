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

    product_is_in_order = product['fields']['Is In Order']
    if product_is_in_order:
      self.order_button.text = "View Order"
    else:
      self.order_button.text = 'Add to New Order'

    msrp_price = product['fields']['Price']
    self.name_label.text = f"{main['fields']['Name']} - ${msrp_price}"
    self.product_image.source = main['fields']['Image'][0]['thumbnails']['large']['url']
    self.barcode_label.text = product['fields']['Barcode']['text']
    self.description_label.text = main['fields']['Description']
    self.condition_label.text = f"Condition: {product['fields']['Condition']}"
    self.category_label.text = f"Categories: {Globals.convert_list_to_string(main['fields']['Category'])}"
    lowest_price = product['fields']['Lowest Price']
    self.price_label.text = f'MSRP: ${msrp_price}'
    self.lowest_price_label.text = f'Lowest Price: ${lowest_price}'
    self.status_label.text = f'Status: {product["fields"]["Status"]}'
    self.total_quantity_label.text = f"Total Units: {main['fields']['Quantity']}"
    self.available_label.text = f"Available for Sale: {main['fields']['Available']}"
    self.quantity_sold_label.text = f"Units Sold: {main['fields']['Sold']}"
    added_on = Globals.convert_airtable_date_to_friendly_date(product['fields']['Date Added'])
    self.added_on_label.text = f'Added on: {added_on}'
    self.added_by_label.text = f"Added by: {product['fields']['Added By Name'][0]}"
    approved_on = Globals.convert_airtable_date_to_friendly_date(product['fields']['Approved For Sale On'])
    self.approved_for_sale_on_label.text = f'Approved for Sale on: {approved_on}'

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.back_button_callback()

  def order_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    product = Globals.product
    main = Globals.main
    user = anvil.users.get_user()
    if product_is_in_order:
      if user['admin'] or user['can_start_order']:
        # TO DO
        pass
      else:
        alert('You do not have access to this feature. Please contact an administrator.')

  def remove_from_production_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = anvil.users.get_user()
    if user['admin'] or user['can_remove_product_from_production']:
        t = TextBox(placeholder="Example: Sister Fannie is getting this for her house.")
        alert(content=t,
        title="Enter a reason for this action.", 
              buttons=[
                 ("Confirm", "Confirm"),
                 ("Cancel", "Cancel"),
               ])
    else:
      alert('You do not have access to this feature. Please contact an administrator.')


    
    
