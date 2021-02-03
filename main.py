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

import os
import sys
import time

# Standard Packages
from datetime import datetime

# Main API / Wrapper
import discord
import motor.motor_asyncio
from discord.ext import commands

# 3rd Party Libraries Used
from termcolor import colored  # colors oo
from dotenv import load_dotenv

# Local Packages
from core import KIGM
from utils.mongo import DBShortCuts  # Shortcuts for mongodb stuff

load_dotenv("./.env")


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


client = KIGM(command_prefix=get_prefix, help_command=None,
              description='The most fun you\'ll ever have with a bot!', case_insensitive=True,
              intents=discord.Intents.all(), owner_id=526616688091987968)

@client.event
async def on_ready():
    print(colored("\n-------------------------------------", 'blue'))
    time.sleep(0.5)
    print(colored("     ~~~IT'S NOW RUNNING!!~~~\n", 'cyan'))

    time.sleep(0.5)
    print(colored(f"Logged as: {client.user}", 'cyan'))
    time.sleep(0.5)
    print(colored("\n-------------------------------------", 'blue'))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                           name=f"&help / @{client.user.name}"))


@client.event
async def on_guild_join(guild):
    await client.config.upsert({"_id": guild.id, "Bot Prefix": "&", "AutoResponse Mode": False})


@client.event
async def on_guild_remove(guild):
    await client.config.delete(guild.id)


@client.command(hidden=True)
async def blacklist(ctx, userid: int, *, list_name):
    await client.bl.upsert({"_id": list_name.lower(), "$addToSet": {"Blacklisted": userid}})

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


client.load_cogs()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)
