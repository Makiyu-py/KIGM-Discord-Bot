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
from datetime import datetime
from typing import Callable, List

import discord
from discord import utils
from discord import Embed
from discord.ext import commands
from disputils import BotConfirmation

from utils.paginate import dpyPaginate


class CustomContext(commands.Context):
    def uptime(self, **kwargs):

        # Getting the bot's uptime is much 'time-consuming' than I expected... haha...
        bold_it = kwargs.get("boldm", True)

        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        uptime_msg = ""

        if days > 0:
            uptime_msg += f"**{days}d**, "

        if hours > 0:
            uptime_msg += f"**{hours}h**, "

        if minutes > 0:
            uptime_msg += f"**{minutes}m**, "

        uptime_msg += "{0}**{1}s**".format("and " if minutes > 0 else "", seconds)

        if not bold_it:
            uptime_msg = uptime_msg.strip("*")

        return uptime_msg

    async def error(self, errormsg: str, **kwargs):
        return await self.reply(f"**ERROR!**\n{errormsg}", **kwargs)

    async def confirmation(
        self,
        msg: str,
        em_color: hex = 0xF8F8FF,
        confirmed_msg=False,
        failed_msg=False,
        channel_sent: discord.TextChannel = None,
    ):

        _confirm = BotConfirmation(self, em_color)
        await _confirm.confirm(text=msg, channel=channel_sent)

        if _confirm.confirmed:

            if confirmed_msg:
                await _confirm.update(confirmed_msg, color=em_color)

            return True

        else:
            if failed_msg:
                await _confirm.update(failed_msg, color=em_color)

            return False

    async def paginate(self, em_list: List[Embed], **kwargs):

        pag = dpyPaginate(page_list=em_list, **kwargs)

        return await pag.menustart(self)

    async def input(
        self,
        dr: bool = False,
        check: Callable = False,
        tm_msg: str = None,
        delete_after: float = 5.0,
        timeout: float = 20.0,
        escape_mentions: bool = True,
    ):

        if not check:
            check = (
                lambda m: (m.author == self.author and m.channel == self.channel)
                and not m.author.bot
            )

        try:
            inp: discord.Message = await self.bot.wait_for(
                "message", check=check, timeout=timeout
            )

            if dr:
                try:
                    await inp.delete()
                except discord.HTTPException:
                    pass

            return (
                inp.content
                if not escape_mentions
                else utils.escape_mentions(inp.content)
            )

        except asyncio.TimeoutError:
            await self.send(
                tm_msg or "Oops! It seems like you took too long! Try again later.",
                delete_after=delete_after,
            )

            return False
