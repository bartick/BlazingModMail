import asyncio
from random import *

import discord
from discord.ext import commands

from run import client

class Fun(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command()
	async def ping(self, ctx):
		message = await ctx.send('\uD83C\uDFD3' + ' Pong!')
		await asyncio.sleep(0.3)
		ws = str(round(client.latency * 1000))
		await message.edit(content='\uD83C\uDFD3' + ' WS: `' + ws + 'ms`')

	@commands.command(aliases=['8ball'])
	async def _8ball(self, ctx, *,question):
		responses = ['As I see it, yes.',
                     'Ask again later.',
                     'Better not tell you now.',
                     'Cannot predict now.',
                     'Concentrate and ask again.',
                     'Don’t count on it.',
                     'It is certain.',
                     'It is decidedly so.',
                     'Most likely.',
                     'My reply is no.',
                     'My sources say no.',
                     'Outlook not so good.',
                     'Outlook good.',
                     'Reply hazy, try again.',
                     'Signs point to yes.',
                     'Very doubtful.',
                     'Without a doubt.',
                     'Yes.',
                     'Yes – definitely.',
                     'You may rely on it.']
		await ctx.send(f'Question: {question}\nAnswer: {choice(responses)}')

def setup(client):
	client.add_cog(Fun(client))