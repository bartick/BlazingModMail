import datetime

import discord
from discord.ext import commands

from run import client

class Help(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(aliases=['help'])
	def help_command(self, ctx):
		hel = discord.Embed(title=f"Help for {client.user.name}", description="All Commands are listed below", color=ctx.author.color)
		hel.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
		hel.add_field(name="ModMail",value="dm\nclose\nsend\na or add\nremove or rn",inline=True)
		hel.add_field(name="Fun",value="8ball\nguess or gs",inline=True)
		hel.add_field(name="Search",value="anime\npfp or av or avatar\nwiki",inline=True)
		hel.timestamp = datetime.datetime.now()
		await ctx.send(embed=hel)

def setup(client):
	client.add_cog(Help(client))