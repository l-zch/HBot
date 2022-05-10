from utils.assets import Repository
from discord.ext import commands
from discord import ButtonStyle, SelectOption, Embed, Interaction
from discord.ui import View, Button, Select
from discord.ext.commands import Context

from requests import get
from bs4 import BeautifulSoup
from pandas import Timestamp
from re import search

from typing import List, Dict
from dataclasses import dataclass

from utils.assets import Repository


def get_page(index, page):
  return f'https://i3.nhentai.net/galleries/{index}/{page}.jpg'


@dataclass
class Label:
  name: str
  amount: str
  url: str

class Clawer:

  def get_repository_index(self) -> str:
    pass

  def get_labels(self) -> List[Label]:
    pass
  
  def get_title(self) -> str:
    pass

  def get_labels_map(self) -> Dict[str, List[Label]]:
    pass

  def get_pages(self) -> int:
    pass

class Dashboard:
  def __init__(self, view:View):
    emojis = Repository.emojis
    self.view.add_item(Button(style=ButtonStyle.gray, emoji=emojis["previous_page"]))
    self.view.add_item(Button(style=ButtonStyle.gray, emoji=emojis["visible"]))
    self.view.add_item(Button(style=ButtonStyle.gray, emoji = emojis["next_page"]))


class ContentManager:

  def __init__(self, pages, repository_url:str, indexes: List[str]):
    self.pages = pages
    self.repository_url = repository_url
    self.indexes = indexes

  def next(self):
    self.page += 1
    return self.refresh()

  def previous(self):
    self.page -= 1
    return self.refresh()

  def refresh(self):
    if(self.page <= 0 or self.page > self.pages):
      return None
    return self.repository_url.format(self.indexes[self.page])


class NClawer(Clawer):

  def __init__(self, number):
    r = get(f'https://nhentai.net/g/{number}/')
    soup = BeautifulSoup(r.text, 'html.parser')
    self.labels = []
    self.info_fields = {}
    self._title = soup.select(".title")
    self._tag = [ *soup.find('section', id="tags").children ]
    self._a_tag = [ i.select('a') for i in self._tag[:-2] ]
    self._the_img = soup.select_one('div#cover img')
    self._the_time = self._tag[-1].find('time')

  def get_repository_index(self):
    return search('\d{6}\d*', self._the_img['data-src']).group(0)

  def get_labels(self) -> List[Label]:
    if not self.labels:
      for _a in self._a_tag:
        self.labels.append([
          Label(
            name = a.select_one("span.name").text,
            amount = a.select_one("span.count").text,
            url = f'https://nhentai.net{a["href"]}'
          ) for a in _a])
  
    return self.labels


  def get_labels_map(self):
    name_list = [
      "parodies", "characters", "tags", "artists",
      "groups", "languages","categories"]
    return dict(zip(name_list, self.get_labels()))

  def get_title(self):
    return self._title[0].text

  def get_subtitle(self):
    return self._title[1].text

  def get_timestamp(self):
    timestamp = Timestamp(self._the_time['datetime']).timestamp()
    return  f'<t:{timestamp:.0f}:R>'
  
  def get_page(self):
    return self._tag[-1].find("span").text


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

  def create(self):
    for i in range(0, len(self.options), 25):
      self.view.add_item(
        Select(
          options = self.options[i:i+25], 
          placeholder = "快速查詢"))
    return self.view


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


def get_cover(soup: BeautifulSoup):
  return soup.select_one('div#cover img')['data-src']


class nCommands(commands.Cog):

  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_interaction(self, interaction: Interaction):
    print(interaction.message.components)

  @commands.command()
  async def n(self, ctx, number:str):
    clawer = NClawer(number)
    emojis = Repository.emojis
    translated = ['改編','角色', '標籤', '繪師','團隊', '語言', '類別']
    name_map = dict(zip(clawer.get_labels_map(), translated))

    quick_search = QuickSearch("")
    comic = Comic("")

    for key, labels in clawer.get_labels_map().items():
      quick_search.add_labels(emojis[key], labels)
      comic.add_labels(f'────  {emojis[key]} {name_map[key]}  ────', labels)

    await ctx.send(
      embed =
        comic
        .add_title(clawer.get_title())
        .add_subtitle(clawer.get_subtitle())
        .add_timestamp(clawer.get_timestamp())
        .create(),
      view = quick_search.create())

  @commands.command()
  async def nsearch(self, ctx, key:str):
    page = 1
    r = get(f'https://nhentai.net/language/translated/?page={page}')
    soup = BeautifulSoup(r.text, 'html.parser')
    covers = soup.select('a.cover')
    for cover in covers:
      print('https://nhentai.net'+cover['href'])
      print(cover.find('img')['data-src'])
      print(cover.find('div').text)


def setup(bot: commands.Bot):
	bot.add_cog(nCommands(bot))