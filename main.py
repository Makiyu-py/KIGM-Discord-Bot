# Main API / Wrapper
import discord
from discord.ext import commands, tasks

# Standard Packages
import time
import sys
import random
import json
import os

# 3rd Party Libraries Used
from termcolor import colored
import motor.motor_asyncio  # idk what dis is but it's used on a MenuDocs vid so ¯\_(ツ)_/¯
import asyncio

# Local Packages
from keep_alive import keep_alive # Reason why bot is 24/7
from the_universe import get_prefix
from utils.mongo import DBShortCuts  # Shortcuts for mongodb stuff (tnx MenuDocs)


client = commands.Bot(command_prefix=get_prefix, help_command=None,case_insensitive=True, intents=discord.Intents.all(), owner_id=526616688091987968)

client.owner_id = 526616688091987968

# YouTube is hurting my English soo
client.main_color= 0xf8f8ff
client.main_colour= 0xf8f8ff

client.owner = client.get_user(client.owner_id)

@client.event
async def on_ready():
  print(colored("-------------------------------------", 'red'))
  for e in colored("Now Initializing Database. . .", 'grey', 'on_green'):
    sys.stdout.write(e)
    sys.stdout.flush()
    time.sleep(0.08)
  print(colored("\n-------------------------------------", 'blue'))


  client.mongo = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("MONGODB_SECRET"))


  # Server Configuration Data
  client.db = client.mongo["Guild"]

  client.config = DBShortCuts(client.db, "Config")


  # Main bot's data
  client.botdb = client.mongo["BotData"]

  client.cmd_stats = DBShortCuts(client.botdb, "CommandStats")
  client.bl = DBShortCuts(client.botdb, "Blacklisted")
  

  # User data
  client.udb = client.mongo["User"]

  client.userconfig = DBShortCuts(client.udb, "Config")
  client.ecod = DBShortCuts(client.udb, "Economy")

  for e in colored("Initialized Database", 'blue'):
    sys.stdout.write(e)
    sys.stdout.flush()
    time.sleep(0.08)
  print(colored("\n-------------------------------------", 'blue'))
  for x in colored("     ~~~IT'S NOW RUNNING!!~~~\n", 'cyan'):
    sys.stdout.write(x)
    sys.stdout.flush()
    time.sleep(0.1)

  for y in colored(f"Logged as: {client.user}", 'cyan'):
    sys.stdout.write(y)
    sys.stdout.flush()
    time.sleep(0.08)
  print(colored("\n-------------------------------------", 'blue'))
  
  
@client.event
async def on_guild_join(guild):

	with open("databases/Settings/prefixes.json", "r") as f:
		prefixes = json.load(f)

	prefixes[str(guild.id)] = "&"

	with open("databases/Settings/prefixes.json", "w") as f:
		json.dump(prefixes, f, indent=4)


@client.event
async def on_guild_remove(guild):

	with open("databases/Settings/prefixes.json", "r") as f:
		prefixes = json.load(f)

	prefixes.pop(str(guild.id))

@tasks.loop(minutes=5)
async def change_status():

	statuses = [
		    "with your satisfaction... | ping me if ur in help",
		    "with you ;) | ping me if ur in help",
		    f"with my spaghetti code made by {str(client.owner)} | ping me if ur in help",
		    "ping me if ur in help pls i rlly need attention",
		    f"on {str(len(client.guilds))} servers! | ping me if ur in help",
		    "with this good life that i have! | ping me if ur in help",
		    "with these &dadjokes you command me every damn minute | ping me if ur in help",
		    "with the bigger bot boys, they function cool | ping me if ur in help",
		    "jumping in the bed! | ping me if ur in help", "00111010 00101001 | ping me if ur in help",
		    "with over 1800 lines of code! | ping me if ur in help",
		    ".-... .... . .-.. .--. / ---... -.--.- | ping me if ur in help",
        f"with {str(len(client.guilds))} ignorant groups of people | ping me if ur in help",
        "\"I feel calm but energized\" | ping me if ur in help"
		]
	status = random.choice(statuses)
	await client.change_presence(activity=discord.Game(status))

@change_status.before_loop
async def before_change_status():
  await client.wait_until_ready()



@client.command(hidden=True)
async def blacklist(ctx, userid: int, *, list_name):

  await client.bl.upsert({"_id" : list_name.lower()}, {"$addToSet": {"Blacklisted": [userid]}})

  await ctx.send(f"User is now blacklisted in {list_name}")

@client.command(hidden=True)
async def load(ctx, extension):
  '''
  Nothing to be seen...
  '''
  if str(ctx.author.id) == '526616688091987968':
    extension = extension.lower()
    await ctx.send(f"Loading `{extension}`")
    if extension.startswith("cog_") and not extension.endswith(".py"):
      try:
        client.load_extension(f'cogs.comms.{extension}')
      except commands.ExtensionNotFound:
        client.load_extension(f'cogs.other.{extension}')
      except:
        await ctx.send(f"Execution Failed. Reason: Cog `{extension}` could not be loaded.")
        return
      finally:
        await ctx.send(f"`{extension}` has been successfully loaded!")

    elif extension.endswith(".py"):
      try:
        client.load_extension(f'cogs.comms.{extension[:-3]}')
      except commands.ExtensionAlreadyLoaded:
        await ctx.send("Cog already loaded silly!")
      except commands.ExtensionNotFound:
        client.load_extension(f'cogs.other.{extension[:-3]}')
      except:
        await ctx.send(f"Execution Failed. Reason: Cog `{extension}` could not be loaded.")
        return
      finally:
        await ctx.send(f"`{extension}` has been successfully loaded!")
    else:
      await ctx.send('Execution Failed. Reason: Unknown Cog')

  else:
    print(
		    f"{ctx.author.id} attempted to load an extension named {extension}.\n----------------------------------"
		)
    return


@client.command(hidden=True)
async def unload(ctx, extension):
  '''
  Nothing to be seen...
  '''
  if str(ctx.author.id) == '526616688091987968':
    extension = extension.lower()
    await ctx.send(f"Unloading `{extension}`")
    if extension.endswith(".py") and extension.startswith("cog_"):
      try:
        client.unload_extension(f'cogs.comms.{extension}')
      except commands.ExtensionNotLoaded:
        client.unload_extension(f'cogs.other.{extension}')
      except:
        await ctx.send(f"Execution Failed. Reason: Cog `{extension}` could not be unloaded.")
        return
      finally:
        await ctx.send(f"`{extension}` has been successfully unloaded!")

    elif extension.startswith("cog_") and not extension.endswith(".py"):
      try:
        client.unload_extension(f'cogs.comms.{extension}')
      except commands.ExtensionNotLoaded:
        client.unload_extension(f'cogs.other.{extension}')
      except:
        await ctx.send(f"Execution Failed. Reason: Cog `{extension}` could not be unloaded.")
        return
      finally:
        await ctx.send(f"`{extension}` has been successfully unloaded!")

    else:
      await ctx.send('Excetuion Failed. Reason: Unknown Cog')

  else:
    print(
        f"{ctx.author.id} attempted to unload an extension named {extension}.\n----------------------------------"
        )
    return


@client.command(aliases=['rl'], hidden=True)
async def reload(ctx, cog):
	'''
	Nothing to be seen...
	'''
	if str(ctx.author.id) == '526616688091987968':
		await ctx.send("Reload starting...")
		cog = cog.lower()

		if cog == 'all':
			await ctx.send("Reloading all cogs...")
			for filename in os.listdir('./cogs/'):
				if filename.endswith('.py'):
					client.unload_extension(f'cogs.comms.{filename[:-3]}')
					client.load_extension(f'cogs.comms.{filename[:-3]}')
					client.unload_extension(f'cogs.other.{filename[:-3]}')
					client.load_extension(f'cogs.other.{filename[:-3]}')
			else:
				await ctx.send('All cogs have been reloaded!')

		elif cog.endswith(".py") and cog.startswith("cog_"):
			await ctx.send(f"Reloading `{cog}`...")
			try:
				client.unload_extension(f'cogs.comms.{cog[:-3]}')
				client.load_extension(f'cogs.comms.{cog[:-3]}')
			except commands.ExtensionNotLoaded:
				client.unload_extension(f'cogs.other.{cog[:-3]}')
				client.load_extension(f'cogs.other.{cog[:-3]}')
			except:
				await ctx.send(f"Excetuion Failed. Reason: Cog `{cog}` could not be loaded.")
				return
			finally:
			  await ctx.send(f'the `{cog}` cog has now been reloaded!')

		elif cog.startswith("cog_") and not cog.endswith(".py"):
			await ctx.send(f"Reloading `{cog}`...")
			try:
				client.unload_extension(f'cogs.comms.{cog}')
				client.load_extension(f'cogs.comms.{cog}')
			except commands.ExtensionNotLoaded:
				client.unload_extension(f'cogs.other.{cog}')
				client.load_extension(f'cogs.other.{cog}')
			except:
				await ctx.send(f"Excetuion Failed. Reason: Cog `{cog}` could not be loaded.")
				raise Exception
				return
			finally:
			  await ctx.send(f'the `{cog}` cog has now been reloaded!')

		else:
			await ctx.send('Excetuion Failed. Reason: Unknown Cog')
	else:
		print(
		    f"{ctx.author.id} attempted to reload an extension named {cog}.\n----------------------------------"
		)
		return


@client.command(name="listcogs", aliases=['lc'], hidden=True)
async def listcogs(ctx):
  '''
	Returns a list of all enabled cogs!
	'''
  if str(ctx.author.id) == '526616688091987968':
    base_string = "**ALL COGS/CATEGORIES!**\n\n"
    for cog in client.extensions:
      base_string += "`" + "".join(str(cog)) + "`"
      base_string += "\n"

    await ctx.send(base_string)

# Loads cogs from the cogs/comms directory
print(colored("Loading all command cogs...", 'grey', 'on_green'))
for filename in os.listdir('./cogs/comms'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.comms.{filename[:-3]}')
    print(colored("------------------------------------------", 'magenta'))
    print(colored(f"The {filename} cog has now been loaded!", 'magenta'))
print(colored("------------------------------------------", 'magenta'))
    
# Loads cogs from the cogs/other directory
print(colored("Now Loading all events/shortcut cogs...", 'grey', 'on_green'))
for filename in os.listdir('./cogs/other'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.other.{filename[:-3]}')
    print(colored("------------------------------------------", 'yellow'))
    print(colored(f"The {filename} cog has now been loaded!", 'yellow'))
print(colored("------------------------------------------", 'yellow'))


change_status.start() 
keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)