"""
This file is part of KIGM-Discord-Bot.

KIGM-Discord-Bot is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

KIGM-Discord-Bot is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with KIGM-Discord-Bot.  If not, see <https://www.gnu.org/licenses/>.
"""

import asyncio
import os
import sys
import time

# Standard Packages
from datetime import datetime

# Main API / Wrapper
import discord
from discord.ext import commands
from dotenv import load_dotenv

# 3rd Party Libraries Used
from termcolor import colored  # colors oo

# Local Packages
from core import KIGM
from utils.mongo import DBShortCuts  # Shortcuts for mongodb stuff

load_dotenv("./.env")


async def get_prefix(bot, message):
    # If dm's
    if not message.guild:
        return commands.when_mentioned_or("&")(bot, message)

    data = await bot.config.find(message.guild.id)

    # Make sure we have a useable prefix
    if not data or "Bot Prefix" not in data:
        await bot.config.upsert({"_id": message.guild.id, "Bot Prefix": "&"})
        return commands.when_mentioned_or("&")(bot, message)

    return commands.when_mentioned_or(data["Bot Prefix"])(bot, message)


client = KIGM(
    command_prefix=get_prefix,
    help_command=None,
    description="The most fun you'll ever have with a bot!",
    case_insensitive=True,
    intents=discord.Intents.all(),
    owner_id=526616688091987968,
)


@client.event
async def on_ready():
    print(colored("\n-------------------------------------", "blue"))
    time.sleep(0.5)
    print(colored("     ~~~IT'S NOW RUNNING!!~~~\n", "cyan"))

    time.sleep(0.5)
    print(colored(f"Logged as: {client.user}", "cyan"))
    time.sleep(0.5)
    print(colored("\n-------------------------------------", "blue"))
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name=f"&help / @{client.user.name}"
        )
    )
    await client.renew_memes()


@client.event
async def on_dbh_post(data):
    print("IT WORKSSSS")


@client.event
async def on_guild_join(guild):
    await client.config.upsert(
        {"_id": guild.id, "Bot Prefix": "&", "AutoResponse Mode": False}
    )


@client.event
async def on_guild_remove(guild):
    await client.config.delete(guild.id)


@client.command(hidden=True)
async def blacklist(ctx, userid: int, *, list_name):
    await client.bl.upsert(
        {"_id": list_name.lower(), "$addToSet": {"Blacklisted": userid}}
    )

    await ctx.send(f"User is now blacklisted in {list_name}")


@client.command(name="listcogs", aliases=["lc"], hidden=True)
@commands.is_owner()
async def listcogs(ctx):
    """
    Returns a list of all enabled cogs!
    """
    base_string = "**ALL COGS/CATEGORIES!**\n\n"
    for cog in client.extensions:
        base_string += "`" + "".join(str(cog)) + "`"
        base_string += "\n"

    await ctx.send(base_string)


client.load_cogs()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)
