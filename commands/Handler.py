# Event Handling for discord.py commands

from discord.ext import commands
from discord.ext.commands.errors import CommandError

class Handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if ctx.command is None:
            print(f'A command was called that does not exist: {ctx.message.content}')
        else:
            print(ctx.command.name + ' failed.')
            print(error)

    # I'm leaving these commands in for the future if we ever need them for
    # troubleshooting. But for the most part, I think that just knowing that a
    # command failed should be enough.
    #
    # @commands.Cog.listener()
    # async def on_command(self, ctx):
    #     print(ctx.command.name + ' was called.')
    #
    # @commands.Cog.listener()
    # async def on_command_completion(self, ctx):
    #     print(ctx.command.name + ' was invoked successfully.')

    # This should theoretically refresh all components of the bot.
    # TODO: Make this command actually work so there's no need to ctrl+c every
    # single time we want to reload modules
    @commands.command(name='refresh', alias=['reset', 'reload'])
    async def shutdown(self, ctx, *, module: str):
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except CommandError as e:
            await ctx.channel.send('{}: {}'.format(type(e).__name__, e))

def setup(bot):
    bot.add_cog(Handler(bot))
