from discord import ButtonStyle, SelectOption
from discord.ui import View, Button, Select

from requests import get
from bs4 import BeautifulSoup
from pandas import Timestamp
from re import search

from typing import List

from Service.clawer.Clawer import Clawer
from Service.Label import Label

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