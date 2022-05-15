from discord import Interaction, Webhook
from discord.ext import commands
from discord.ext.commands import Context
from json import loads

from requests import get
from bs4 import BeautifulSoup
from Service.ButtonData import ButtonData

from Service.ViewCreator import NViewCreator, ViewCreator



class nCommands(commands.Cog):

  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_interaction(self, interaction: Interaction):

    data = ButtonData.from_json(interaction.custom_id)

    creator = {"N": NViewCreator}[data["comic"]]
    is_private = bool(interaction.message.webhook_id)
    if data.type == "main_page":
      embed, view = creator.create_mainpage_view(data["number"], private = is_private)
    elif data.type == "start_to_read":
      embed, view = creator.create_reading_view(data["number"], 1)
    elif data.type == "private_read":
      embed, view = creator.create_reading_view(data["number"], 1)
      await interaction.message.delete()
      await interaction.followup.send(embed = embed, view = view, ephemeral = True)
      return

    elif data.type == "conductor":
      embed, view = creator.create_reading_view(data["number"], data["page"])

    if is_private:
      try:
        await interaction.edit_original_message(embed = embed, view = view)
      except:
        pass
    else:
      await interaction.message.edit(embed = embed, view = view)


  @commands.command()
  async def n(self, ctx: Context, number:str):
    embed, view = NViewCreator.create_mainpage_view(number)
    await ctx.reply(embed = embed, view = view)

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