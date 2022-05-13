from dataclasses import dataclass
from typing import List, Tuple
from discord import Embed
from discord.ui import View

from Service.Crawler import NCrawler
from Service.ButtonData import ButtonData
from Service.Dashboard import Dashboard
from Service.ViewField import ViewField
from utils.assets import Repository


class ViewCreator:
  
  @staticmethod
  def create_mainpage_view(number:str) -> Tuple[Embed, View]:
    pass

  @staticmethod
  def create_reading_view(number:str, page:int) -> Tuple[Embed, View]:
    pass


@dataclass
class ComicButton:
  comic: str
  type: str
  data: list
  
class NViewCreator:

  @staticmethod
  def create_mainpage_view(number:str):
    Crawler = NCrawler(number)
    emojis = Repository.emojis
    translated = ['改編','角色', '標籤', '繪師','團隊', '語言', '類別']
    name_map = dict(zip(Crawler.get_labels_map(), translated))

    dashboard = Dashboard()
    view_field = ViewField()

    button_data = ButtonData("開始閱讀", "start_to_read")
    button_data["number"] = number
    button_data["comic"] = "N"
    dashboard.add_start_button(button_data)
  
    for key, labels in Crawler.get_labels_map().items():
      dashboard.add_quick_search(emojis[key], labels)
      view_field.add_quick_search(f'────  {emojis[key]} {name_map[key]}  ────', labels)

    return (
      view_field
        .add_title(Crawler.get_title())
        .add_subtitle(Crawler.get_subtitle())
        .add_image(Crawler.get_cover_url())
        .add_footer(Crawler.get_likes_count(), "https://cdn-icons-png.flaticon.com/512/3237/3237429.png")
        .create(),
      dashboard.create())
  

  @staticmethod
  def create_reading_view(number:str, page:int):
    Crawler = NCrawler(number)
    pages = Crawler.get_pages()
    labels = ["<<", "<-", "->", ">>"]
    button_data = [ButtonData(label, "conductor") for label in labels]
  
    for i,data in enumerate(button_data):
      data["a"] = i

    def set_page(data, page):
      data["page"] = page
      data["number"] = number
      data["comic"] = "N"
      data.disabled = False

    if page > 1:
      set_page(button_data[0], 1)
      set_page(button_data[1], page-1)

    if page < pages:
      set_page(button_data[2], page+1)
      set_page(button_data[3], pages)

    dashboard = Dashboard().add_conductor(button_data)

    return ViewField().add_image(
      Crawler.get_page_url(page)
    ).add_footer(f"{page}/{Crawler.get_pages()}", "https://cdn-icons-png.flaticon.com/512/1057/1057565.png").create(), dashboard.create()