from discord.ext import commands
import glob
from discord import Intents
from utils.assets import Repository

intents = Intents.all()
bot = commands.Bot(command_prefix='?', intents=intents)


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

bot.run("OTc1MDU0NjY4ODQzNjA2MDQ3.Gc0MSY.jHs6EDh7SVm5PUBOrrFcgUhaY9pKCJv2yNg3sA")  # Starts the bot

# OTUwMzgxODc0ODI2NjAwNDQ4.GX20Mx.S5BW8yfUAfl26hYEjPYgciI2Glw8inigTrKFT0