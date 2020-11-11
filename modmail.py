import os
import json
import asyncio
from dotenv import load_dotenv
from discord import *
from discord.ext import commands
from run import client

load_dotenv()

def add_mail(member_id, channel_id):
	with open('mail.json', 'r') as f:
		mail = json.load(f)
	mail[channel_id] = member_id
	with open('mail.json', 'w') as f:
		json.dump(mail, f, indent=4)

def del_mail(channel_id):
	with open('mail.json', 'r') as f:
		mail = json.load(f)
		mail.pop(str(channel_id))
	with open('mail.json', 'w') as f:
		json.dump(mail, f, indent=4)

async def create_channel(author):
	await author.send('Please wait our staff will reach to you soon.')
	guild = utils.get(client.guilds, name=os.getenv('GUILD_NAME'))
	role = utils.get(guild.roles,id=int(os.getenv('MOD_ID')))
	overwrites = {
	guild.default_role: PermissionOverwrite(read_messages=False),
	guild.me: PermissionOverwrite(read_messages=True),
	role: PermissionOverwrite(read_messages=True)
	}
	chn = await guild.create_text_channel(name=f"📬〢{author.name}", overwrites=overwrites, category=client.get_channel(int(os.getenv('CATEGORY_ID'))))
	add_mail(author.id, chn.id)
	member = await guild.fetch_member(author.id)
	await chn.send("@here Someone wants help.")
	await chn.send(f"**Username:** {author.name}#{author.discriminator} \n**Account Created:** {author.created_at}\n**Joined on:** {member.joined_at}")
	await chn.send("---------------------------------")
	return chn

class ModMail(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(aliases=['dm'])
	async def direct_message_user(self, ctx, user_id: int, *,message=None):
		user = await ctx.guild.fetch_member(user_id)
		await user.send(f"**You got a dm from {ctx.guild.name} :** {message}")
		embed = Embed(description=f"<:Success:776003968723451914> Successfully sent a dm to {user.mention}", color=ctx.author.color)
		await ctx.send(embed=embed)

	@commands.command()
	@commands.has_permissions(manage_channels=True)
	async def close(self, ctx, channel: TextChannel = None, *, reason=None):
		channel = channel or ctx.channel
		del_mail(channel.id)
		await channel.delete(reason=reason)

	@close.error
	async def close_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			message = await ctx.send(f"{ctx.author.mention} you need `Manage Channels` permission to use this command")

		else:
			message = await ctx.send(f"{ctx.author.mention} Something Went wrong! Make Sure that I have correct permission and you are running this command in the correct channel.")

		await asyncio.sleep(5)
		await message.delete()

	@commands.command(aliases=['r','reply'])
	async def send(self, ctx, *,reply=None):
		guild = ctx.guild
		with open('mail.json','r') as f:
			mail = json.load(f)
		member = await guild.fetch_member(mail[str(ctx.channel.id)])
		await ctx.message.delete()
		await member.send(f"**{ctx.author.name}#{ctx.author.discriminator} :** {reply}")
		await ctx.send(f"**{ctx.author.name} :** {reply}")

	@commands.command(aliases=['a','add'])
	@commands.has_permissions(manage_channels=True)
	async def add_member(self,ctx, member_id: int):
		member = await ctx.guild.fetch_member(member_id)
		overwrites =  PermissionOverwrite()
		overwrites.read_messages = True
		await ctx.channel.set_permissions(member, overwrite=overwrites)
		del_msg = await ctx.send(f"Added {member.name} to this channel")
		await asyncio.sleep(5)
		await msg.delete()

	@add_member.error
	async def add_member_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			msg = await ctx.send(f"{ctx.author.mention} You need to mention a user to add.")
		elif isinstance(error, commands.CheckFailure):
			msg = await ctx.send(f"{ctx.author.mention} You don't have permission to add a member to this channel.")
		else:
			msg = await ctx.send(f"{ctx.author.mention} Something went wrong. Please try again with correct details and permission.")

		await asyncio.sleep(5)
		await msg.delete()

	@commands.command(aliases=['remove','rm'])
	@commands.has_permissions(manage_channels=True)
	async def remove_member(self,ctx, member_id: int):
		member = await ctx.guild.fetch_member(member_id)
		overwrite = PermissionOverwrite()
		overwrite.read_messages = False
		await ctx.channel.set_permissions(member, overwrite=overwrite)
		del_msg = await ctx.send(f"Removed {member.name} to this channel")
		await asyncio.sleep(5)
		await msg.delete()

	@remove_member.error
	async def remove_members_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			msg = await ctx.send(f"{ctx.author.mention} You need to mention someone to remove.")
		elif isinstance(error, commands.CheckFailure):
			msg = await ctx.send(f"{ctx.author.mention} You don't have permission to remove a member from this channel.")
		else:
			msg = await ctx.send(f"{ctx.author.mention} Something went wrong. Please try again with correct details and permission.")

		await asyncio.sleep(5)
		await msg.delete()

	@commands.Cog.listener()
	async def on_message(self, message):
		author = message.author
		if author == client.user:
			return
		if message.author != message.author.bot:
			if not message.guild:
				cnl = utils.get(client.get_all_channels(), guild__name=os.getenv('GUILD_NAME'),name=f"📬〢{author.name.lower()}")
				if cnl == None:
					cnl = await create_channel(author)
					await cnl.send(f"**{author.name}#{author.discriminator} :** {message.content}")
				else:
					await cnl.send(f"**{author.name}#{author.discriminator} :** {message.content}")

def setup(client):
	client.add_cog(ModMail(client))