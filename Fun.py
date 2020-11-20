import asyncio
from random import *
import sqlite3

import discord
from discord.ext import commands
import datetime

from run import client

def get_data_database_exp(a,b):
	conn = sqlite3.connect('Main_Database.db')
	cursor = conn.cursor()
	sum=0
	cursor.execute('SELECT Exp FROM Expcards WHERE Level Between ? AND ?',(a,b))
	for i in cursor.fetchall():
		sum = sum+i[0]
	cursor.close()
	conn.close()
	return sum

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

	@commands.command(aliases=['guess','gs'])
	@commands.has_permissions(manage_messages=True)
	async def random(self, ctx, *, num: int):
		number = randint(1, num)
		await ctx.message.delete()
		await ctx.author.send(f"The the correct number is {number}.\nDo not share this information with others.")
		await ctx.send(f"**Guess The Number Game has been Started**\nGuess the number between 1 and {num}")
		guess = 0
		while guess != number:
			try:
				msg = await client.wait_for(
					"message",
					timeout=100,
					check=lambda message: message.author != ctx.author
											and message.channel == ctx.channel
				)
				try:
					guess = int(msg.content)
				except ValueError:
					continue
				if guess == number:
					await ctx.send(f"{msg.author.mention} You have have guessed correctly.\nAnd you have won the match.\nThank you for playing.")
					await ctx.author.send(f"The Winner of your **Guess The Number** is {msg.author.mention}.")
					break
			except asyncio.TimeoutError:
				continue

	@random.error
	async def random_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			msg = await ctx.send(f"{ctx.author.mention} You don't have `Manage Messages` permission to use this command.")
		else:
			msg = await ctx.send(f"{ctx.author.mention} Something went wrong please try again later.")
		await asyncio.sleep(5)
		await msg.delete()

	@commands.command(aliases=['exp'])
	async def experience(self, ctx, l1: int=0, l2: int=0):
		if l1 >= l2 or l1 >= 60 or l1 < 1 or l2 > 60 or l2 < 2:
			await ctx.send(f"{ctx.author.mention} Please provide a valid level.")
		else:
			req=get_data_database_exp(l1+1,l2)
			expreq = discord.Embed()
			expreq.set_author(name="ENHANCEMENT",icon_url=client.user.avatar_url)
			expreq.add_field(name="The amount of exp you need to enhance the cards from:",value=f"Level **{l1}** to Level **{l2}**: **{req}** Exp",inline=False)
			expreq.set_footer(text=f"Total Exp: {req} Exp")
			await ctx.send(embed=expreq)

def setup(client):
	client.add_cog(Fun(client))