from discord import ButtonStyle
from discord.ui import View, Button

from utils.assets import Repository


class Dashboard:
  def __init__(self, view:View):
    emojis = Repository.emojis
    self.view.add_item(Button(style=ButtonStyle.gray, emoji=emojis["previous_page"]))
    self.view.add_item(Button(style=ButtonStyle.gray, emoji=emojis["visible"]))
    self.view.add_item(Button(style=ButtonStyle.gray, emoji = emojis["next_page"]))