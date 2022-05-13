from typing import List, Dict
from requests import get
from bs4 import BeautifulSoup
from pandas import Timestamp
from re import search, compile

from Service.Label import Label


class Clawer:

  def get_repository_index(self) -> str:
    pass

  def get_page_url(self, page:int) -> str:
    pass

  def get_labels(self) -> List[Label]:
    pass
  
  def get_title(self) -> str:
    pass

  def get_labels_map(self) -> Dict[str, List[Label]]:
    pass

  def get_pages(self) -> int:
    pass

  def get_cover_url(self) -> str:
    pass


class NClawer(Clawer):

  def __init__(self, number):
    r = get(f'https://nhentai.net/g/{number}/')
    soup = BeautifulSoup(r.text, 'html.parser')
    self.labels = []
    self.info_fields = {}
    self._soup = soup
    self._title = soup.select(".title")
    self._tag = [ *soup.find('section', id="tags").children ]
    self._the_cover_img = soup.select_one('div#cover img')
  
  def get_page_url(self, page):
    repository_index = search('\d{6}\d*', self._the_cover_img['data-src']).group(0)
    f"https://i3.nhentai.net/galleries/{repository_index}/{page}.jpg"

  def get_labels(self) -> List[Label]:
    if not self.labels:
      for _tag in self._tag[:-2]:
        self.labels.append([
          Label(
            name = a.select_one("span.name").text,
            amount = a.select_one("span.count").text,
            url = f'https://nhentai.net{a["href"]}'
          ) for a in _tag.select('a')])
  
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
    timestamp = Timestamp(self._tag[-1].find('time')['datetime']).timestamp()
    return  f'<t:{timestamp:.0f}:R>'
  
  def get_pages(self):
    return int(self._tag[-1].find("span").text)

  def get_cover_url(self):
    return self._the_cover_img['data-src']
  
  def get_likes_count(self):
    return self._soup.find("span", text = compile(r'\([0-9]*\)')).text[1:-1]

