from keep_alive import keep_alive
from the_universe import get_prefix
from discord.ext import commands
import discord
import os
import random
import asyncio
import json


client = commands.Bot(command_prefix=get_prefix, help_command=None,case_insensitive=True, intents=discord.Intents.all())

client.author_id = 526616688091987968


@client.event
async def on_ready():
	print("IT WORKS!")
	print(client.user)
	print("----------------------------------")


@client.event
async def on_guild_join(guild):

	with open("prefixes.json", "r") as f:
		prefixes = json.load(f)

	prefixes[str(guild.id)] = "&"

	with open("prefixes.json", "w") as f:
		json.dump(prefixes, f, indent=4)


@client.event
async def on_guild_remove(guild):

	with open("prefixes.json", "r") as f:
		prefixes = json.load(f)

	prefixes.pop(str(guild.id))


async def change_status():
	await client.wait_until_ready()

	while not client.is_closed():
		statuses = [
		    "with your satisfaction... | &help if ur in danger",
		    "with you ;) | &help if ur in danger",
		    "with my horrible code made by Makiyu^#4707",
		    "&help if ur in danger",
		    f"on {str(len(client.guilds))} servers! | &help if ur in danger",
		    "with this good life that i have! | &help if ur in danger",
		    "with these &dadjokes you command me every damn minute | &help if ur in danger",
		    "with the bigger bot boys, they function cool | &help if ur in danger",
		    "jumping in the bed! | &help if ur in danger", "00111010 00101001 | &help if ur in danger",
		    "with over 850 lines of code! | &help if ur in danger",
		    ".-... .... . .-.. .--. / ---... -.--.- | &help if ur in danger",
        f"with {str(len(client.guilds))} ignorant groups of people... Sadge | &help if ur in danger"
		]
		status = random.choice(statuses)
		await client.change_presence(activity=discord.Game(status))
		await asyncio.sleep(300)


client.loop.create_task(change_status())


@client.command()
async def load(ctx, extension):
  '''
  Loads a cog!
  '''
  if str(ctx.author.id) == '526616688091987968':
    await ctx.send(f"Loading `{extension}`")
    if extension.startswith("cog_") and not extension.endswith(".py"):
      client.load_extension(f'cogs.{extension}')
      await ctx.send(f"`{extension}` has been successfully loaded!")
    elif extension.endswith(".py") and extension.startswith("cog_"):
      client.load_extension(f'cogs.{extension[:-3]}')
      await ctx.send(f"`{extension}` has been successfully loaded!")
    else:
      await ctx.send('Excetuion Failed. Reason: Unknown Cog')

  else:
    print(
		    f"{ctx.author.id} attempted to load an extension named {extension}.\n----------------------------------"
		)
    return


@client.command()
async def unload(ctx, extension):
	'''
	Unloads a cog!
	'''
	if str(ctx.author.id) == '526616688091987968':
		await ctx.send(f"Unloading `{extension}`")
		if extension.endswith(".py") and extension.startswith("cog_"):
			client.unload_extension(f'cogs.{extension[:-3]}')
			await ctx.send(f"`{extension}` has been successfully unloaded!")

		elif extension.startswith("cog_") and not extension.endswith(".py"):
			client.unload_extension(f'cogs.{extension}')
			await ctx.send(f"`{extension}` has been successfully unloaded!")

		else:
			await ctx.send('Excetuion Failed. Reason: Unknown Cog')

	else:
		print(
		    f"{ctx.author.id} attempted to unload an extension named {extension}.\n----------------------------------"
		)
		return


@client.command(aliases=['rl'])
async def reload(ctx, cog):
	'''
	Reloads a cog!
	'''
	if str(ctx.author.id) == '526616688091987968':
		await ctx.send("Reload starting...")
		if cog == 'all':
			await ctx.send("Reloading all cogs...")
			for filename in os.listdir('./cogs/'):
				if filename.endswith('.py'):
					client.unload_extension(f'cogs.{filename[:-3]}')
					client.load_extension(f'cogs.{filename[:-3]}')
			else:
				await ctx.send('All cogs have been reloaded!')

		elif cog.endswith(".py") and cog.startswith("cog_"):
			await ctx.send(f"Reloading `{cog}`...")
			client.unload_extension(f'cogs.{cog[:-3]}')
			client.load_extension(f'cogs.{cog[:-3]}')
			await ctx.send(f'the `{cog}` cog has now been reloaded!')

		elif cog.startswith("cog_") and not cog.endswith(".py"):
			await ctx.send(f"Reloading `{cog}`...")
			client.unload_extension(f'cogs.{cog}')
			client.load_extension(f'cogs.{cog}')
			await ctx.send(f'the `{cog}` cog has now been reloaded!')

		else:
			await ctx.send('Excetuion Failed. Reason: Unknown Cog')
	else:
		print(
		    f"{ctx.author.id} attempted to reload an extension named {cog}.\n----------------------------------"
		)
		return


@client.command(name="listcogs", aliases=['lc'])
async def listcogs(ctx):
  '''
	Returns a list of all enabled cogs!
	'''
  if str(ctx.author.id) == '526616688091987968':
    base_string = "```css\n"  # Gives some styling to the list (on pc side)
    base_string += "\n".join([str(cog) for cog in client.extensions])
    base_string += "\n```"
    await ctx.send(base_string)


for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')

keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)
