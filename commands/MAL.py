"""
Contains the MAL class.
"""
from mal_py import Mal_Py as Mal
from discord.ext import commands
from time import time
import discord


class MAL(commands.Cog):
    """
    This class contains functions for interacting with the MAL API.
    """
    def __init__(self, bot):
        """
        Initializes a MAL object from a given Discord bot object.
        """
        file_dir = 'json_files/mal_token.json'
        self.bot = bot
        self._mal = Mal(file_dir, 'true')

    @commands.command(name='malsearch')
    async def mal_search(self, ctx, s_type, *, query, offset=0):
        """
        Takes a string command, sends the top MAL anime search result
        to the Discord channel. Users can then use the reacts to scroll
        through the search results.
        """
        color = 144, 208, 238
        embed = await self._get_embed(s_type, query, color, offset=0)
        msg = await ctx.send(embed=embed)

        reactions = ['👈', '🤡', '👉']
        for emoji in reactions:
            await msg.add_reaction(emoji)

        t0 = time()

        def check(reaction, user):
            return str(reaction.emoji) in reactions \
                   and user != self.bot.user \
                   and reaction.message.id == msg.id

        while True:
            msg1 = await self.bot.wait_for('reaction_add',
                                           check=check, timeout=90.0)
            reaction_emoji = str(msg1[0])
            reaction_user = msg1[1]

            if reaction_emoji == reactions[0]:
                if offset > 0:
                    offset -= 1
                    new_embed = await self._get_embed(s_type=s_type,
                                                      query=query,
                                                      color=color,
                                                      offset=offset)
                    await msg.edit(embed=new_embed)
            elif reaction_emoji == reactions[2]:
                offset += 1
                new_embed = await self._get_embed(s_type=s_type,
                                                  query=query,
                                                  color=color,
                                                  offset=offset)
                await msg.edit(embed=new_embed)
            elif reaction_emoji == reactions[1]:
                await ctx.send(f'{str(reaction_user).split("#")[0]},'
                               f' What\'s Updog 🤡')

            if time() - t0 >= 180:
                break

    @commands.command(name='malnsfw')
    async def mal_set_nsfw(self, ctx, *, setting):
        """
        Sets NSFW settings for mal
        """
        if 'true' in setting.lower():
            self._mal.set_nsfw('true')
            await ctx.send('Server NSFW setting for anime/manga search'
                           ' now set to **True**.')
        else:
            self._mal.set_nsfw('false')
            await ctx.send('Server NSFW setting for Anime/Manga search'
                           ' now set to **False**.')

    async def _get_embed(self, s_type, query, color, offset=0):
        """
        Returns a Discord Embed object from the given information.
        """
        mal_id = self._mal.search(s_type, query, 1, offset)[0]
        info = self._mal.details(s_type, mal_id['id'])
        return await self._format_embed(info=info, color=color, s_type=s_type)

    async def _format_embed(self, info, color, s_type):
        """
        Returns a Discord Embed object from a dictionary containing
        Anime information, and a color tuple.
        """
        info = await self._format_dict(info)
        title = f"**{info['title']}**"
        url = info['mal_url']
        img = info['main_picture']['large']

        if s_type == 'anime':
            studios = info['studios'][0]['name']
            for i in range(1, len(info['studios'])):
                studios += f", {info['studios'][i]['name']}"

        cut_off = 400
        synopsis = info['synopsis']
        synopsis = synopsis[: synopsis.rfind('\n')]

        if len(synopsis) > cut_off:
            synopsis = synopsis[: cut_off] + '...'

        genres = info['genres'][0]['name']
        for i in range(1, len(info['genres'])):
            genres += f", {info['genres'][i]['name']}"

        desc = f"**Status**: {await self._format_str(info['status'])}\n\n" \
               f"**Genres**: {genres}\n\n" \
               f"**Synopsis**: {synopsis}\n\n" \
               f"**Score**: {str(info['mean'])}/10\n" \
               f"**Rank**: #{str(info['rank'])}\n" \
               f"**Popularity**: #{str(info['popularity'])}\n\n"

        if s_type == 'anime':
            desc += f"**Studios**: {studios}\n"
            desc += f"**Type**: {await self._format_str(info['media_type'])}"

        r, g, b = color
        embed_d = {'title': title,
                   'url': url,
                   'description': desc}
        embed_var = discord.Embed.from_dict(embed_d)
        embed_var.set_image(url=img)
        if s_type == 'anime':
            footer = f"{await self._format_str(info['start_season']['season'])} " \
                     f"{str(info['start_season']['year'])}  " \
                     f"Episodes: {str(info['num_episodes'])}"
            embed_var.set_footer(text=footer)
        embed_var.color = discord.Color.from_rgb(r, g, b)
        return embed_var

    async def _format_dict(self, dict1):
        """
        Returns a formatted dictionary from a given dictionary
        """
        if 'rank' not in dict1.keys():
            dict1['rank'] = 'N/A'
        if 'mean' not in dict1.keys():
            dict1['mean'] = 'x'
        if 'popularity' not in dict1.keys():
            dict1['popularity'] = 'N/A'
        return dict1

    async def _format_str(self, str1):
        """
        Returns a formatted str from a given str.
        """
        list1 = str1.split('_')
        result = list1[0][0].upper()
        if len(list1[0]) > 1:
            result += list1[0][1:]
        for i in range(1, len(list1)):
            result += f' {list1[i]}'
        return result


def setup(bot):
    bot.add_cog(MAL(bot))
