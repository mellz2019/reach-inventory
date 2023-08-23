from ._anvil_designer import CommentsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals

class Comments(CommentsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.title_label.text = Globals.comment_label

    # Any code you write here will run before the form opens.
    self.comments_panel.items = Globals.comments

  def back_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    Globals.comment_label = 'Comments'
    get_open_form().render_start_order()
