from discord.ext import commands


class DevCommands(commands.Cog):
    '''These are the developer commands'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(  # Decorator to declare where a command is.
        name='reload',  # Name of the command, defaults to function name.
        aliases=['rl']  # Aliases for the command.
    )
    async def reload(self, ctx):
        '''
        Reloads a cog.
        '''
        extensions = self.bot.extensions  # A list of the bot's cogs/extensions.

        for extension in list(extensions):
            self.bot.unload_extension(extension)
            self.bot.load_extension(extension)
        await ctx.send('Done')

    @commands.command(name="unload", aliases=['ul'])
    async def unload(self, ctx, cog):
        '''
        Unload a cog.
        '''
        extensions = self.bot.extensions
        if cog not in extensions:
            await ctx.send("Cog is not loaded!")
            return
        self.bot.unload_extension(cog)
        await ctx.send(f"`{cog}` has successfully been unloaded.")

    @commands.command(name="load")
    async def load(self, ctx, cog):
        '''
        Loads a cog.
        '''
        try:

            self.bot.load_extension(cog)
            await ctx.send(f"`{cog}` has successfully been loaded.")

        except commands.errors.ExtensionNotFound:
            await ctx.send(f"`{cog}` does not exist!")

    @commands.command(name="listcogs", aliases=['lc'])
    async def listcogs(self, ctx):
        '''
        Returns a list of all enabled commands.
        '''
        base_string = "```css\n"  # Gives some styling to the list (on pc side)
        base_string += "\n".join([str(cog) for cog in self.bot.extensions])
        base_string += "\n```"
        await ctx.send(base_string)


def setup(bot):
    bot.add_cog(DevCommands(bot))
