# This will be for bot configurations. Currently being used for prefix change
# for commands, possibly more uses later
import json
from discord.ext import commands

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefixes_path = './json_files/prefixes.json'

    # Command for changing the prefix for calling the bot on a server-to-server
    # basis. Stores the prefixes in a JSON file
    @commands.command(name='config')
    async def changeprefix(self, ctx, prefix):
        with open(self.prefixes_path, 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open(self.prefixes_path, 'w') as f:
            json.dump(prefixes, f, indent=4)


def setup(bot):
    bot.add_cog(Config(bot))
