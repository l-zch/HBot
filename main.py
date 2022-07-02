from discord.ext import commands
from discord import Activity
import glob
from discord import Intents
from utils.assets import Repository
from random import choices
from asyncio import sleep
from os import environ

intents = Intents.all()
bot = commands.Bot(command_prefix='?', intents=intents)
activities = (('你', 0), ('本子', 3), ('你澀澀', 3), ('澀澀', 1))

@bot.event 
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier
    filename = slice(5, -3)
    for path in glob.glob('cogs/*.py'):
        bot.load_extension('cogs.' + path[filename])

    emojis = {}
    guild = bot.get_guild(973480971703844904)
    for emoji in guild.emojis:
        emojis[emoji.name] = str(emoji)
    Repository.add_assets("emojis", emojis)

    while not bot.is_closed():
        name, type = choices(activities)[0]
        await bot.change_presence(activity=Activity(name=name, type=type))
        await sleep(10)

token = environ.get("TOKEN") 
bot.run(token)  # Starts the bot

