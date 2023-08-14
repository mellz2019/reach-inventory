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
from ..StartOrder import StartOrder

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
    self.name_label.text = f"{main['fields']['Name']} - ${Globals.round_to_decimal_places(msrp_price, 2)}"
    self.product_image.source = main['fields']['Image'][0]['thumbnails']['large']['url']
    self.barcode_label.text = product['fields']['Barcode']['text']
    self.description_label.text = main['fields']['Description']
    self.condition_label.text = f"Condition: {product['fields']['Condition']}"
    self.category_label.text = f"Categories: {Globals.convert_list_to_string(main['fields']['Category'])}"
    lowest_price = product['fields']['Lowest Price']
    self.price_label.text = f'MSRP: ${Globals.round_to_decimal_places(msrp_price, 2)}'
    self.lowest_price_label.text = f'Lowest Price: ${Globals.round_to_decimal_places(lowest_price, 2)}'
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
    airtable_user = anvil.server.call('match_record', 'users', 'Email', user['email'])
    if not airtable_user:
      alert('Airtable user not found. Please contanct an admin.')
    else:
      self.remove_from_production_button.enabled = False
      self.back_button.enabled = False
      if product['fields']['Is In Order'] == 1:
          self.order_button.text = 'Locating order...'
          # Fetch the order from the database
          airtable_order = anvil.server.call('get_single_item', 'orders', Globals.product['fields']['Order ID'][0])
          if not airtable_order:
            alert('Airtable order not found')
          else:
            # Set the order id
            Globals.order_id = airtable_order['id']
            # Create Globals order object and append all the products
            Globals.order = ()
            product_ids_from_airtable = airtable_order['fields']['Products']
            for p in range(len(product_ids_from_airtable)):
              product_from_airtable = anvil.server.call('match_record', 'products', 'Record ID', product_ids_from_airtable[p])
              Globals.order = Globals.order + (product_from_airtable,)
            # Calculate order total
            Globals.order_total = Globals.calculate_order_total()
            # Render the UI
            self.content_panel.clear()
            self.content_panel.add_component(StartOrder(self.back_button_callback))
      else:
        if user['admin'] or user['can_start_order']:
            self.order_button.text = 'Adding to new order...'
            # This is the first product in the order
            # Create Order in airtable
            order_to_add = {
              "Products": Globals.product['id'],
              "Created By": airtable_user['id']
            }
            new_order = anvil.server.call('add_item', 'orders', order_to_add)
            update_product_status = {
              "Status": "In Pending Order"
            }
            anvil.server.call('update_item', 'products', Globals.product['id'], update_product_status)
            Globals.order = Globals.order + (Globals.product,)
            Globals.order_total = Globals.calculate_order_total()
            Globals.order_id = new_order['id']
            self.content_panel.clear()
            self.content_panel.add_component(StartOrder(self.back_button_callback))
        else:
          alert('You do not have access to this feature. Please contact an administrator.')

  def remove_from_production_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = anvil.users.get_user()
    if user['admin'] or user['can_remove_product_from_production']:
      # TO DO
      pass
    else:
      alert('You do not have access to this feature. Please contact an administrator.')


    
    
