from ._anvil_designer import BaseTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from ..Home import Home

class Base(BaseTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.content_panel.add_component(Home())

  def home_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.add_component(Home())

