from discord import Embed
from pandas import Timestamp

from typing import List
from Service.Label import Label


class Comic:

  def __init__(self, content_manager):
    self.embed_dict = {"fields":[]}

  def add_page(self, page):
    self.embed.set_image(
      url = f'https://i3.nhentai.net/galleries/{self.index}/{page}.jpg')
    return self

  def add_labels(self, name:str, labels: List[Label]):
    if labels:
      info = ""
      for label in labels:
        info += f'`•{label.name}` '

      self.embed_dict["fields"] += [{
        "name": name,
        "value": info
      }]
    return self

  def add_title(self, title):
    self.embed_dict["title"] = title
    return self

  def add_subtitle(self, subtitle):
    self.embed_dict["description"] = subtitle
    return self
  
  def add_timestamp(self, timestamp: Timestamp):
    # TODO
    return self
  
  def add_hint(self, msg):
    return self
  def create(self):
    return Embed.from_dict(self.embed_dict)