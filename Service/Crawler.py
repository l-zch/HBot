from typing import List, Dict
from requests import get
from bs4 import BeautifulSoup
from pandas import Timestamp
from re import search, compile

from Service.Label import Label
from functools import lru_cache

class Crawler:

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


class NCrawler(Crawler):

  @lru_cache
  def __new__(cls, *args, **kwargs):
    return object.__new__(cls)

  @lru_cache
  def __init__(self, number):
    r = get(f'https://nhentai.net/g/{number}/', headers={"Cache-Control": "max-age=60, immutable"})
    soup = BeautifulSoup(r.text, 'html.parser')
    self.labels = []
    self.info_fields = {}
    self._soup = soup
    self._title = soup.select(".title")
    self._tag = [ *soup.find('section', id="tags").children ]
    self.cover_src = soup.select_one('div#cover img')['data-src']

  def get_page_url(self, page):
    repository_index = search('\d{5}\d*', self.cover_src).group(0)
    return f"https://i7.nhentai.net/galleries/{repository_index}/{page}.{self.cover_src[-3:]}"
  
  def get_labels(self) -> List[Label]:
    labels = []
    for _tag in self._tag[:-2]:
      labels.append([
        Label(
          name = a.select_one("span.name").text,
          amount = a.select_one("span.count").text,
          url = f'https://nhentai.net{a["href"]}'
        ) for a in _tag.select('a')])
    return labels

  def get_labels_map(self):
    name_list = [
      "parodies", "characters", "tags", "artists",
      "groups", "languages","categories"]
    return dict(zip(name_list, self.get_labels()))
  
  def get_title(self):
    return self._title[0].text

  def get_subtitle(self):
    try:
      return self._title[1].text
    except:
      return
  
  def get_timestamp(self):
    timestamp = Timestamp(self._tag[-1].find('time')['datetime']).timestamp()
    return  f'<t:{timestamp:.0f}:R>'

  def get_pages(self):
    return int(self._tag[-2].find("span").text)

  def get_cover_url(self):
    return self.cover_src
  
  def get_likes_count(self):
    return self._soup.find("span", text = compile(r'\([0-9]*\)')).text[1:-1]