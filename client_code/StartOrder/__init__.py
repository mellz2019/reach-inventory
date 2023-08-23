from ._anvil_designer import StartOrderTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..ProductInOrder import ProductInOrder
from ..SearchProductToAddProductToOrder import SearchProductToAddProductToOrder
from .. import Globals
from ..EditPrice import EditPrice
from ..FinalizeOrder import FinalizeOrder
from ..Comments import Comments

class StartOrder(StartOrderTemplate):
  def __init__(self, back, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.products_panel.item_template = ProductInOrder

    self.back = back

    Globals.comment_text_box_changed = False

    if not Globals.order:
      self.order_total_label.text = 'Order total: $0.00'
      self.clear_order_button.enabled = False
      self.add_product_button.text = "Add a Product"
      self.finalize_order_button.enabled = False
      self.order_status_label.text = "Status: New"
    else:
      self.new_order_label.text = f"Order - {Globals.order_id}"
      self.clear_order_button.enabled = True
      self.order_total_label.text = f"Order total: ${Globals.round_to_decimal_places(Globals.order_total, 2)}"
      self.add_product_button.text = "Add another Product"
      self.finalize_order_button.enabled = True
      self.products_panel.items = (
        Globals.order
      )
      airtable_order = anvil.server.call('get_single_item', 'orders', Globals.order_id)
      order_status = airtable_order['fields']['Status']
      self.order_status_label.text = f"Status: {order_status}"
      if order_status == 'Complete' or order_status == "Cancelled":
        self.add_product_button.visible = False
        self.finalize_order_button.visible = False
        self.clear_order_button.visible = False
      self.view_comments_button.enabled = airtable_order['fields']['Has Active Comments'] == 1
      self.orders_comment_text_box.visible = order_status != 'Complete' and order_status != 'Cancelled'

  def reset_order_details(self):
    Globals.main = {}
    Globals.product = {}
    Globals.order = ()
    Globals.order_id = 0
    Globals.order_total = 0
    Globals.order_paid = False

  def clear_start_order_content_panel(self):
    self.content_panel.clear()
    self.content_panel.add_component(EditPrice())

  def render_start_order(self):
    Globals.order = Globals.get_globals_order()
    self.content_panel.clear()
    self.content_panel.add_component(StartOrder(self.back))

  def update_order_id_label(self):
    self.new_order_label = f"Order - {Globals.order_id}"

  def add_product_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(SearchProductToAddProductToOrder(self.render_start_order))

  def clear_order_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    c = confirm("Are you sure you want to cancel the order?")
    if c:
      # Set the order's status to cancelled, clear the current product ids, and set former products to product ids
      user = anvil.users.get_user()
      update_order = {
        "Status": "Cancelled",
        "Products": None,
        "Cancelled By": user['airtable_id'],
        "Former Products": Globals.get_item_from_order_list_dictionary('id')
      }
      anvil.server.call('update_item', 'orders', Globals.order_id, update_order)
      
      # Set the products' status back to In Production
      for i in range(len(Globals.order)):
        update_product = {
          "Status": "In Production",
          "Edited Price": None
        }
        anvil.server.call('update_item', 'products', Globals.order[i]['id'], update_product)

      alert("The order was cancelled successfully.")
        
      # Clear the order locally
      self.reset_order_details()
      Globals.reset_order_details()
      self.content_panel.clear()
      self.content_panel.add_component(StartOrder(self.back))

  def back_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if Globals.coming_from_product_details:
      get_open_form().render_product_details()
    else:
      self.back()

  def finalize_order_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Update the order's status to 'Finalization'
    self.finalize_order_button.text = "Finalizing..."
    self.add_product_button.enabled = False
    self.finalize_order_button.enabled = False
    self.back_button.enabled = False
    self.clear_order_button.enabled = False
    user = anvil.users.get_user()
    update_order = {
      "Status": "Finalization",
      "Finalization By": user['airtable_id']
    }
    anvil.server.call('update_item', 'orders', Globals.order_id, update_order)
    self.content_panel.clear()
    self.content_panel.add_component(FinalizeOrder())

  def save_commment(self):
    self.save_comment_button.text = "Saving..."
    self.save_comment_button.enabled = False
    self.view_comments_button.enabled = False
    self.add_product_button.enabled = False
    self.finalize_order_button.enabled = False
    self.back_button.enabled = False
    self.clear_order_button.enabled = False
    self.private_comment_check_box.enabled = False
    user = anvil.users.get_user()
    if self.private_comment_check_box.checked:
      public_or_private = 'Private'
    else:
      public_or_private = 'Public'
    new_comment = {
      'Comment': self.orders_comment_text_box.text,
      'Order': Globals.order_id,
      'By': user['airtable_id'],
      'Visibility': public_or_private
    }
    anvil.server.call('add_item', 'comments', new_comment)
    self.save_comment_button.text = 'Save Comment'
    self.orders_comment_text_box.text = ''
    self.save_comment_button.visible = False
    self.private_comment_check_box.visible = False
    self.view_comments_button.enabled = True
    self.save_comment_button.enabled = True
    self.add_product_button.enabled = True
    self.finalize_order_button.enabled = True
    self.back_button.enabled = True
    self.clear_order_button.enabled = True
    n = Notification('Comment saved succesfully')
    n.show()

  def save_comment_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.save_commment()

  def view_comments_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.view_comments_button.text = "Loading..."
    self.save_comment_button.enabled = False
    self.view_comments_button.enabled = False
    self.add_product_button.enabled = False
    self.finalize_order_button.enabled = False
    self.back_button.enabled = False
    self.clear_order_button.enabled = False

    user = anvil.users.get_user()
    all_comments = anvil.server.call('get_all_items', 'comments', '-Created')
    this_orders_comments = list(filter(lambda n: n['fields']['Order ID'][0] == Globals.order_id and n['fields']['Is Archived'] == 0, all_comments))
    if user['can_view_all_private_comments']:
      Globals.comments = this_orders_comments
    else:
      Globals.comments = list(filter(lambda n: n['fields']['Visibility'] == 'Public' or n['fields']['User ID'] == user['airtable_id'], this_orders_comments))
    Globals.comment_label = f"Comments for Order - {Globals.order_id}"
    self.content_panel.clear()
    self.add_component(Comments())

  def orders_comment_text_box_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    if self.orders_comment_text_box.text == '':
      self.save_comment_button.visible = False
      self.private_comment_check_box.visible = False
    else:
      self.save_comment_button.visible = True
      self.private_comment_check_box.visible = True
      self.private_comment_check_box.enabled = True
      self.private_comment_check_box.checked = False

  def orders_comment_text_box_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.save_comment()

  def orders_comment_text_box_lost_focus(self, **event_args):
    """This method is called when the TextBox loses focus"""
    pass








