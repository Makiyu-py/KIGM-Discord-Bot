'''
Copyright 2021 Makiyu-py

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

# Main API / Wrapper
import discord
from discord.ext import commands, tasks

# Standard Packages
from datetime import datetime
import time
import sys
import random
import json
import os

# 3rd Party Libraries Used
from termcolor import colored  # colors oo
import motor.motor_asyncio
import asyncio

# Local Packages
from keep_alive import keep_alive  # Reason why bot is 24/7 thru flask *(remove if forked from GitHub)*
from utils.mongo import DBShortCuts  # Shortcuts for mongodb stuff


async def get_prefix(bot, message):
    
    # If dm's
    if not message.guild:
        return commands.when_mentioned_or("&")(bot, message)

    try:
        data = await bot.config.find(message.guild.id)

        # Make sure we have a useable prefix
        if not data or "Bot Prefix" not in data:
            return commands.when_mentioned_or("&")(bot, message)

        return commands.when_mentioned_or(data["Bot Prefix"])(bot, message)

    except:
        return commands.when_mentioned_or("&")(bot, message)


client = commands.AutoShardedBot(command_prefix=get_prefix, help_command=None, description='The most fun you\'ll ever have with a bot!', case_insensitive=True, intents=discord.Intents.all(), owner_id=526616688091987968)


client.owner_id = 526616688091987968
client.launch_time = datetime.utcnow()  # for stats cmd for getting bot's uptime

# YouTube is hurting my English soo
client.main_color= 0xf8f8ff
client.main_colour= 0xf8f8ff


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
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"&help / @{client.user.name} (for more info!)"))
  

@client.event
async def on_guild_join(guild):

	await client.config.upsert({"_id" : guild.id, "Bot Prefix" : "&"})


@client.event
async def on_guild_remove(guild):

	await client.config.delete(guild.id)


@client.command(hidden=True)
async def blacklist(ctx, userid: int, *, list_name):

  await client.bl.upsert({"_id" : list_name.lower(), "$addToSet": {"Blacklisted": userid}})

  await ctx.send(f"User is now blacklisted in {list_name}")


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



keep_alive()  # again, pls remove this line if u forked this from GitHub.
client.load_extension('jishaku')
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)