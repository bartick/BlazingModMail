import asyncio
from random import *
from mal import Anime, AnimeSearch

import discord
from discord.ext import commands
import datetime

from run import client

def search_sort(s):
	temp=""
	for i in s:
		if i == " ":
			temp=temp + "+"
		else:
			temp = temp + i
	return temp

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

	@commands.command()
	async def anime(self, ctx, *,name=""):
		if name == "":
			await ctx.send(f"{ctx.author.mention} you need to provide a name to search.")
		else:
			async with ctx.typing():
				search = AnimeSearch(name)
				anime = Anime(search.results[0].mal_id)
				result = discord.Embed(title=anime.title, description=f"Description\n{anime.synopsis}", color=ctx.author.color)
				result.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
				result.add_field(name="Information",value=f"**English Title:** {anime.title_english}\n**Japanese Title:** {anime.title_japanese}\n**Total Episode:** {anime.episodes}\n**Type:** {anime.type}\n**Status:** {anime.status}\n**Genres:** {anime.genres}\n**Duration:** {anime.duration}\n**Rating:** {anime.rating}\n**Rank:** {anime.rank}",inline=False)
				result.set_thumbnail(url=anime.image_url)
				result.timestamp = datetime.datetime.now()
				await ctx.send(embed=result)

	@anime.error
	async def anime_error(self, ctx, error):
		msg = ctx.send(f"{ctx.author.mention} Something went wrong please make sure the anime you are searching is actually the name of an anime.")
		await asyncio.sleep(5)
		await msg.delete()

	@commands.command(aliases=['av','avatar','pfp'])
	async def profile_picture(self, ctx, profile: discord.User=None):
		if profile == None:
			profile = ctx.author
		picture = discord.Embed(color=ctx.author.color)
		picture.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
		picture.set_image(url=profile.avatar_url)
		picture.timestamp = datetime.datetime.now()
		await ctx.send(embed=picture)

def setup(client):
	client.add_cog(Fun(client))