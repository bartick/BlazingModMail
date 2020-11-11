import os
from dotenv import load_dotenv
from itertools import cycle
import json
import discord
from discord.ext import commands, tasks

load_dotenv()
def get_prefix(client, message):
    try:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        return prefixes[str(message.guild.id)]
    except Exception:
        return "b."


client = commands.Bot(command_prefix=get_prefix,case_insensitive=True)
client.remove_command('help')

status = cycle(['My Prefix is b.', 'Originally I was developed by Bartick',
                'My developers username with tag is Bartick2003#8063', 'Don\'t try to mess with my code',
                'DM me for help | I am only related to Blazing Warriors Server'])


@client.event
async def on_ready():
    change_status.start()
    print('Bot is ready')


@tasks.loop(seconds=20)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = 'c.'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


def is_owner(ctx):
    return ctx.message.author.id == 707876147324518440

client.load_extension('modmail')
client.load_extension('Fun')

client.run(os.getenv('BOT_TOKEN'))