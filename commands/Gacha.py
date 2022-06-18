# We can have the framework of the gacha system here. It may end up more
# complex than expected, so we can always add more files to this sub-system.

from discord.ext import commands  # For discord.py commands extension
from discord import File          # For uploading files
import typing                     # For optional typing
import random                     # For RNG
import os                         # To grab images from disk
# import time                       # To keep track of time

class Gacha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """
    Base gacha command, inits the command group
    There was also something about invoking without command?
    Should probably make it just spit out a nice formatted list of all the
    commands in the group.
    """
    @commands.group(pass_context=True, invoke_without_command=True, name='gacha')
    async def gacha(self, ctx):
        await ctx.channel.send('Base gacha command. Subcommands: claim, etc.')

    """
    Claim command, should give the person who claimed it a certain (variable) amount
    of currency. Should only be able to claim if there was a claimable event
    in the past 5 minutes (timing subject to change).
    """
    @gacha.group(pass_context=True, name='claim')
    async def claim(self, ctx):
        await ctx.channel.send('Claim things... hah')

    """
    Summon command, should pull the required amount of currency from a user
    if they don't have enough currency for the number of summons they want to
    make, give them a message. Otherwise, summon as normal.
    """
    @gacha.group(pass_context=True, name='summon')
    async def summon(self, ctx, amt: typing.Optional[int] = 1):
        await ctx.channel.send('Summon {}'.format(amt))

    """
    Random command, spit out a random number from 1-10.
    """
    @gacha.group(pass_context=True, name='random')
    async def random(self, ctx):
        for root, dirs, files in os.walk('.\\commands\\gacha_images'):
            await ctx.channel.send(file=File(os.path.join(root, \
                files[random.randint(0, len(files) - 1)])))

def setup(bot):
    bot.add_cog(Gacha(bot))
