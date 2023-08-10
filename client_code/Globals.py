import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from datetime import datetime

main = {}
product = {}
order = {}


def convert_airtable_date_to_date_time(airtable_date):
    year = airtable_date.split("-")[0]
    month = airtable_date.split("-")[1]
    day = airtable_date.split("-")[2]

    first_covered_date_full = year + "-" + month + "-" + day

    return datetime.strptime(first_covered_date_full, "%Y-%m-%d").date()

def convert_airtable_date_to_friendly_date(date):
  date_string = str(convert_airtable_date_to_date_time(date))
  date_object = datetime.strptime(date_string, '%Y-%m-%d')
  return date_object.strftime('%B %d, %Y')

def convert_list_to_string(list):
  return ', '.join(list)

