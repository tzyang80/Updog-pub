# We can have the framework of the gacha system here. It may end up more
# complex than expected, so we can always add more files to this sub-system.

from asyncio.windows_events import NULL
from discord.ext import commands  # For discord.py commands and Cogs
import discord  # For discord types
import typing  # For optional typing
import random  # For RNG


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        random.seed()

    @commands.command(name='roll')
    async def roll(self, ctx, count: typing.Optional[int] = 100):
        if count <= 0:
            count = 100
        num = random.randint(0, count)
        await ctx.channel.send('{} rolled {}!'.format(ctx.author.mention, num))

    # An 8 ball command that returns a random response
    @commands.command(aliases=['8b', '8ball', '8balls', 'eightball', 'eightballs'])
    async def ball(self, ctx, question: typing.Optional[str] = NULL):
        if question == NULL:
            await ctx.channel.send('Please enter a question.')
            return

        responses = ['It is certain.',
                     'It is decidedly so.',
                     'Without a doubt.',
                     'Yes definitely.',
                     'You may rely on it.',
                     'As I see it, yes.',
                     'Most likely.',
                     'Outlook good.',
                     'Yes.',
                     'Signs point to yes.',
                     'Reply hazy, try again.',
                     'Ask again later.',
                     'Better not tell you now.',
                     'Cannot predict now.',
                     'Concentrate and ask again.',
                     'Don\'t count on it.',
                     'My reply is no.',
                     'My sources say no.',
                     'Outlook not so good.',
                     'Very doubtful.']

        await ctx.channel.send(f'{random.choice(responses)}')

    # TODO: If tagging multiple, is it possible to just get the one that was
    #       mentioned first?
    @commands.command(name='eject')
    async def eject(self, ctx, name: typing.Optional[str] = NULL):
        mentions = ctx.message.mentions
        if name == NULL:
            name = ctx.author.display_name
        elif mentions:
            name = mentions[0].display_name
        await ctx.channel.send('```. 　　　。　　　　•　 　ﾟ　　。 　　.\n　　\
            　.　　　 　　.　　　　　。　　 。　. 　\n.　　 。　　　　　 ඞ 。 . 　\
                　 • 　　　　•\n　　ﾟ　　 {} was ejected.　 。\
                    　.\n　　\'　　　                    　 　　。\n　　ﾟ　　　.　　　\
                        . ,　　　　.　 .```'.format(name))


def setup(bot):
    bot.add_cog(Misc(bot))
