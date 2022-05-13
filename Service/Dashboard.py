from discord import ButtonStyle, SelectOption
from discord.ui import View, Button, Select
from typing import List
from Service.Label import Label

class Dashboard:

  def __init__(self):
    self.view = View()
    self.options = []

  def add_conductor(self, number, page, pages):
    button = Button(
      label = "<<",
      style = ButtonStyle.success,
      custom_id = 0)
    button = Button(
      label = "<-",
      style = ButtonStyle.success,
      custom_id = page-1)
    button = Button(
      label = "->",
      style = ButtonStyle.success,
      custom_id = page+1)
    button = Button(
      label = ">>",
      style = ButtonStyle.success,
      custom_id = label.url)
    return self

  def add_quick_search(self, emoji:str, labels: List[Label]):
    if labels:
      for label in labels:
        self.options.append(
          SelectOption(
            label=label.name ,
            value = label.url,
            description = label.amount,
            emoji = emoji))
    return self
  
  def create(self):
    for i in range(0, len(self.options), 25):
      self.view.add_item(
        Select(
          options = self.options[i:i+25], 
          placeholder = "快速查詢"))
    return self.view