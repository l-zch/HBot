from typing import List, Tuple
from discord import Embed
from discord.ui import View

from Service.Clawer import NClawer
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


class NViewCreator:

  @staticmethod
  def create_mainpage_view(number:str):
    clawer = NClawer(number)
    emojis = Repository.emojis
    translated = ['改編','角色', '標籤', '繪師','團隊', '語言', '類別']
    name_map = dict(zip(clawer.get_labels_map(), translated))

    dashboard = Dashboard()
    view_field = ViewField()

    for key, labels in clawer.get_labels_map().items():
      dashboard.add_quick_search(emojis[key], labels)
      view_field.add_quick_search(f'────  {emojis[key]} {name_map[key]}  ────', labels)

    return (view_field
      .add_title(clawer.get_title())
      .add_subtitle(clawer.get_subtitle())
      .add_image(clawer.get_cover_url())
      .add_footer(clawer.get_likes_count(), "https://cdn-icons-png.flaticon.com/512/3237/3237429.png")
      .create()), dashboard.create()

  @staticmethod
  def create_reading_view(number:str, page:int):
    clawer = NClawer(number)
    pages = clawer.get_pages()

    image_urls = [None]*4
    if page > 1:
      image_urls[0] = clawer.get_page_url(1)
      image_urls[1] = clawer.get_page_url(page-1)

    if page < pages:
      image_urls[2] = clawer.get_page_url(page+1)
      image_urls[3] = clawer.get_page_url(pages)

    dashboard = Dashboard().add_conductor(
      *image_urls
    )

    return ViewField().add_image(
      clawer.get_page_url(page)
    ).add_footer(f"{page}/{clawer.get_pages()}").create(), dashboard.add_conductor()