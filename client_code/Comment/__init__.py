from ._anvil_designer import CommentTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Globals

class Comment(CommentTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    user = anvil.users.get_user()
    if user['can_delete_others_comments'] or self.item['fields']['By'][0] == user['airtable_id']:
      self.delete_comment_button.enabled = True
      self.edit_comment_button.enabled = True

    # Any code you write here will run before the form opens.
    self.comment_label.text = self.item['fields']['Comment']

  def edit_comment_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.save_comment_button.enabled = Globals.edited_comment_change
    self.comment_text_box.text = self.comment_label.text
    self.comment_text_box.visible = True
    self.comment_text_box.enabled = True
    self.save_comment_button.visible = True
    self.cancel_button.visible = True
    self.cancel_button.enabled = True

  def save_comment(self):
    self.save_comment_button.text = 'Saving...'
    self.comment_label.text = self.comment_text_box.text
    self.save_comment_button.enabled = False
    self.edit_comment_button.enabled = False
    self.delete_comment_button.enabled = False
    self.comment_text_box.enabled = False
    self.cancel_button.enabled = False
    update_comment = {
      'Comment': self.comment_text_box.text
    }
    anvil.server.call('update_item', 'comments', self.item['id'], update_comment)
    n = Notification('Comment saved succesfully!')
    n.show()
    # Get the new value
    self.item = anvil.server.call('get_single_item', 'comments', self.item['id'])
    user = anvil.users.get_user()
    if user['can_delete_others_comments'] or self.item['fields']['By'][0] == user['airtable_id']:
      self.delete_comment_button.enabled = True
      self.edit_comment_button.enabled = True
    self.save_comment_button.text = 'Save'
    self.save_comment_button.enabled = False
    self.comment_text_box.enabled = False
    self.cancel_button.enabled = False
    
    self.cancel_button.visible = False
    self.comment_text_box.visible = False
    self.save_comment_button.visible = False

    Globals.edited_comment_change = False

  def cancel_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if Globals.edited_comment_change:
      c = confirm("You haven't saved your changes. Would you like to save them?")

      if c:
        self.save_comment()
    
    self.comment_text_box.visible = False
    self.save_comment_button.visible = False
    self.cancel_button.visible = False
    self.comment_label.text = self.item['fields']['Comment']

    Globals.edited_comment_change = False

  def comment_text_box_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    Globals.edited_comment_change = True
    if self.comment_text_box.text != '':
      self.comment_label.text = self.comment_text_box.text
      self.save_comment_button.enabled = True
    else:
      self.comment_label.text = self.item['fields']['Comment']
      self.save_comment_button.enabled = False

  def save_comment_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.save_comment()

  def delete_comment_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    c = confirm('Are you sure you want to delete this comment?')

    if c:
      self.delete_comment_button.text = 'Deleting...'
      self.comment_label.text = self.comment_text_box.text
      self.save_comment_button.enabled = False
      self.edit_comment_button.enabled = False
      self.delete_comment_button.enabled = False
      self.comment_text_box.enabled = False
      self.cancel_button.enabled = False
      user = anvil.users.get_user()
      archive_comment = {
        'Archived': True,
        'Archived By': user['airtable_id']
      }
      anvil.server.call('update_item', 'comments', self.item['id'], archive_comment)
      n = Notification('Comment deleted succesfully!')
      self.remove_from_parent()
      n.show()
      if user['can_delete_others_comments'] or self.item['fields']['By'][0] == user['airtable_id']:
        self.delete_comment_button.enabled = True
        self.edit_comment_button.enabled = True
      self.save_comment_button.text = 'Save'
      self.save_comment_button.enabled = False
      self.comment_text_box.enabled = False
      self.cancel_button.enabled = False
      
      self.cancel_button.visible = False
      self.comment_text_box.visible = False
      self.save_comment_button.visible = False
    else:
      return

      




