from discord import Embed

from typing import List
from Service.Label import Label


class ViewField:

  def __init__(self):
    self.embed = Embed()

  # def add_page(self, page):
  #   self.embed.set_image(
  #     url = f'https://i3.nhentai.net/galleries/{self.index}/{page}.jpg')
  #   return self
  def add_title(self, title):
    self.embed.title = title
    return self

  def add_subtitle(self, subtitle):
    self.embed.description = subtitle
    return self

  def add_quick_search(self, name:str, labels: List[Label]):
    if labels:
      info = ""
      for label in labels:
        info += f'`•{label.name}` '

      self.embed.add_field(
        name = name,
        value = info)
    return self
  
  def add_footer(self, text, icon_url = None):
    self.embed.set_footer(text = text, icon_url=icon_url)
    return self
  
  def add_image(self, image_url):
    print(image_url)
    self.embed.set_image(url = image_url)
    return self

  def create(self):
    return self.embed