from ._anvil_designer import BaseTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from ..Home import Home
from ..StartOrder import StartOrder
from ..OrderSelector import OrderSelector

class Base(BaseTemplate):
  def __init__(self, **properties):
    self.change_sign_in_text()
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.go_to_home()

  def go_to_home(self):
    self.content_panel.clear()
    self.content_panel.add_component(Home())
    self.change_sign_in_text()

  def render_start_order(self):
    StartOrder.render_start_order(self)

  def clear_start_order_content_panel(self):
    StartOrder.clear_start_order_content_panel(self)

  def back(self):
    OrderSelector.back(self)

  def cancel(self):
    Home.cancel(self)

  def change_sign_in_text(self):
    user = anvil.users.get_user()
    if user:
      email = user['email']
      self.sign_in_link.text = 'Sign Out'
    else:
      self.sign_in_link.text = 'Sign In'

  def home_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.go_to_home()

  def sign_in_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    user = anvil.users.get_user()
    if user:
      logout = confirm("Would you like to logout?")
      if logout:
        anvil.users.logout()
        self.sign_in_link.text = 'Sign In'
        self.go_to_home()
    else:
      anvil.users.login_with_form()
      n = Notification("Sign in successful!")
      n.show()
      self.change_sign_in_text()


