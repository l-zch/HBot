from discord import ButtonStyle, SelectOption
from discord.ui import View, Button
from typing import List
from Service.Label import Label


class QuickSearch:

  def __init__(self, view: View):
    self.view = view
    self.options = []

  def add_buttons(self, labels: List[Label]):
    if labels:
      for label in labels:
        button = Button(
          label = label.name,
          style = ButtonStyle.success,
          custom_id = label.url)
        self.view.add_item(button)
    return self

  def add_labels(self, emoji:str, labels: List[Label]):
    if labels:
      for label in labels:
        self.options.append(
          SelectOption(
            label=label.name ,
            value = label.url,
            description = label.amount,
            emoji = emoji))
    return self