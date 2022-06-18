''' A simple Discord bot written with Python

<Longer Description>

'''
import json                       # To read config.json
import pathlib                    # Read information from directories
import os                         # Read information from directories
from discord.ext import commands  # For the commands extension and Discord API

# Variable names for the location of the json files required
config_path = './json_files/config.json'
prefixes_path = './json_files/prefixes.json'

# Opens up config file and loads as a dictionary
with open(config_path, 'r') as read_file:
    config = json.load(read_file)

# Grab token from json file (prefix is not necessary as the JSON used for storing prefixes
# already has a default)
token = config['token']

# Grab prefixes for said servers
def get_prefix(bot, message):
    with open(prefixes_path, 'r') as f:
        prefixes = json.load(f)

    try:
        prefix = prefixes[str(message.guild.id)]
    except KeyError:
        prefix = prefixes['prefix']
    return prefix

client = commands.Bot(command_prefix = get_prefix)


@client.event
# Change status to help command on ready?
# Could also use "Listening to"
async def on_ready():
    print('Updog ready!')

# Provide a default prefix when the bot is added to a server
@client.event
async def on_guild_join(guild):
    with open(prefixes_path, 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '!'

    with open(prefixes_path, 'w') as f:
        json.dump(prefixes, f, indent=4)

# Remove the prefix when the bot is removed from a server
@client.event
async def on_guild_remove(guild):
    with open(prefixes_path, 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open(prefixes_path, 'w') as f:
        json.dump(prefixes, f, indent=4)

if __name__ == '__main__':
    # Read through the directory here so that you only do it once
    # Add them to a list of loaded extensions as you load them
    with os.scandir('.\\commands') as itr:
        for entry in itr:
            if entry.is_file() and pathlib.Path(entry.name).suffix == '.py':
                file = 'commands.' + pathlib.Path(entry.name).stem
                client.load_extension(file)

# Logs Updog into Discord with the bot token in config.json
client.run(token)
