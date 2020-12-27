import os
from dotenv import load_dotenv
from itertools import cycle
import json
import discord
from discord.ext import commands, tasks

load_dotenv()
def get_prefix(client, message):
    prefixes = ['B.','b.']
    return prefixes


intents = discord.Intents.all()

client = commands.AutoShardedBot(command_prefix=get_prefix, intents=intents, case_insensitive=True)
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


def is_owner(ctx):
    return ctx.message.author.id == 707876147324518440

client.load_extension('modmail')
client.load_extension('Fun')
client.load_extension('Search')
client.load_extension('Help')

client.run(os.getenv('BOT_TOKEN'))