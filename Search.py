from mal import Anime, AnimeSearch
import wikipedia
import datetime
import asyncio

import discord
from discord.ext import commands

from run import client

def search_sort(s):
	temp=""
	for i in s:
		if i == " ":
			temp=temp + "+"
		else:
			temp = temp + i
	return temp

class Search(commands.Cog):
	def __init__(self, client):
		self.client = client

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
				result.set_thumbnail(url=client.user.avatar_url)
				result.set_image(url=anime.image_url)
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

	@commands.command(aliases=['wiki'])
	async def wikipedia_search(self, ctx, *,search=""):
		if search == "":
			msg = ctx.send(f"{ctx.author.mention} you need to provide a search query.")
			await asyncio.sleep(5)
			await msg.delete()
		else:
			async with ctx.typing():
				answer = wikipedia.WikipediaPage(question)
				result = discord.Embed(title=answer.title,description=answer.summary,color=ctx.author.color)
				result.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
				result.set_thumbnail(url=client.user.avatar_url)
				result.set_image(url=answer.images[0])
				result.timestamp = datetime.datetime.now()
				await ctx.send(embed=result)
			'''try:
				async with ctx.typing():
					answer = wikipedia.WikipediaPage(question)
					result = discord.Embed(title=answer.title,description=answer.summary,color=ctx.author.color)
					result.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
					result.set_thumbnail(url=client.user.avatar_url)
					result.set_image(url=answer.images[0])
					result.timestamp = datetime.datetime.now()
					await ctx.send(embed=result)
			except Exception:
				msg = await ctx.send(f"{ctx.author.mention} something went wrong please try again later.")
				await asyncio.sleep(5)
				await msg.delete()'''

def setup(client):
	client.add_cog(Search(client))