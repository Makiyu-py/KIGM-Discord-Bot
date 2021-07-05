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

import os

import dbl
from discord.ext import commands


# For the thing uh the @ decorator thing u
# put on top of the function, yea yea
def support_server_only():
    async def predicate(ctx):
        if ctx.guild.id == 770558935144726528:
            return True

        await ctx.send(
            "This command is exclusively **for the support server only.**\nSo here's link of the support server then!  **https://discord.gg/jz4WxkB **"
        )
        return False

    return commands.check(predicate)


def cmd_has_blacklist():
    async def get_bl(ctx):
        cmdbl_data = await ctx.bot.bl.find(ctx.command.name)
        if "Blacklisted" in cmdbl_data:
            if ctx.author.id not in cmdbl_data["Blacklisted"]:
                return True

            await ctx.error(
                "You are currently *blacklisted* from using this command."
            )
            return False

    return commands.check(get_bl)


def voters_only():
    async def check_voted(ctx):
        j = dbl.DBLClient(ctx.bot, os.environ.get("DBL_SECRET"))
        usr_vote = await j.get_user_vote(ctx.author.id)

        await j.close()  # idk I get annoyed sometimes with the warnings on the console

        if usr_vote:
            return True

        await ctx.send(
            "oops! It seems like this command is for **__voters only.__**\nIf you want to use this command just **vote me on top.gg!**\nVote link: **https://top.gg/bot/763626077292724264/vote **"
        )
        return False

    return commands.check(check_voted)
