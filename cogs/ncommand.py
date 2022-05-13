from dataclasses import dataclass
from discord.ext import commands
from discord import Interaction
from discord.ext.commands import Context
from json import loads

from requests import get
from bs4 import BeautifulSoup

from Service.ViewCreator import NViewCreator, ViewCreator


def get_page(index, page):
  return f'https://i3.nhentai.net/galleries/{index}/{page}.jpg'


@dataclass
class ComicButton:
  comic: str
  type: str
  data: list

class nCommands(commands.Cog):

  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_interaction(self, interaction: Interaction):
    print(interaction.data)
    data = loads(interaction.custom_id)
    if data["type"] == "comic_button":
      button = ComicButton(**data)
      Creator: ViewCreator = { "N": NViewCreator }[button.comic]
      number, page = button.data

      if button.type == "mainpage":
        embed, view = Creator.create_mainpage_view(number)
      else:
        embed, view = Creator.create_reading_view(number, page)
      await interaction.message.edit(embed = embed, view = view)

  @commands.command()
  async def n(self, ctx, number:str):
    embed, view = NViewCreator.create_mainpage_view(number)
    await ctx.send(embed = embed, view = view)

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