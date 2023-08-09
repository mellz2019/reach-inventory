import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from PIL import Image, ImageDraw
from io import BytesIO

import pyzbar.pyzbar

@anvil.server.callable
def decode(img_file):
  img = Image.open(BytesIO(img_file.get_bytes()))
  img = img.convert('RGB')  
  
  decoded = pyzbar.pyzbar.decode(img)
  draw = ImageDraw.Draw(img)
  
  data = []
  
  for barcode in decoded:
    rect = barcode.rect
    print(rect)
    draw.rectangle(
        (
            (rect.left, rect.top),
            (rect.left + rect.width, rect.top + rect.height)
        ),
        outline='#0080ff'
    )

    draw.polygon(barcode.polygon, outline='#e945ff')
    data.append(barcode.data.decode("utf-8"))
  
  
  bs = BytesIO()
  img.save(bs, format="JPEG")
  return data