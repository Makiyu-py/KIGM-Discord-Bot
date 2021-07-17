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

import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown

from core import KIGMHelp


class HelpCommands(commands.Cog, name=":bookmark_tabs: Help"):
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = KIGMHelp()
        bot.help_command.cog = self
        self.bot = bot

        self.bug_channel_id = 777684586003431435
        self.suggestions_channel_id = 770633934827683923

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

    @discord.utils.cached_property
    def suggestions_channel(self):
        return self.bot.get_channel(self.suggestions_channel_id)

    @discord.utils.cached_property
    def bug_channel(self):
        return self.bot.get_channel(self.bug_channel_id)

    @commands.command(
        description="Suggest something to improve this bot!", aliases=["bot_suggest"]
    )
    @cooldown(1, 21600, BucketType.user)
    async def suggest(self, ctx, *, your_suggestion):

        suggestion_request_received = discord.Embed(
            color=self.bot.main_color,
            title="Thanks for the suggestion! Your suggestion has now been sent to the developers!",
            description="You may find your suggestion in [the official support server](https://discord.gg/jz4WxkB) in the text channel, #suggestions-area!",
        )
        await ctx.send(embed=suggestion_request_received)

        embed = discord.Embed(
            color=0x222222,
            title="New Suggestion for KIGM: ",
            description=your_suggestion,
        )

        embed.set_author(name=f"From {ctx.guild.name}", icon_url=ctx.guild.icon_url)
        embed.set_footer(
            text=f"Suggested by: {ctx.author}", icon_url=ctx.author.avatar_url
        )
        embed.set_thumbnail(url=ctx.author.avatar_url)
        suggestmsg = await self.suggestions_channel.send(embed=embed)

        await suggestmsg.add_reaction("💁‍♂️")
        await suggestmsg.add_reaction("🤷‍♀️")
        await suggestmsg.add_reaction("🙅")

    @commands.command(description="Invite this bot to your server!", aliases=["inv"])
    async def invite(self, ctx):
        await ctx.channel.send(
            "<a:weeeee:771309755427061770>**Invite Me**<a:weeeee:771309755427061770>\nhttps://discord.com/api/oauth2/authorize?client_id=763626077292724264&permissions=273115158&scope=bot%20applications.commands"
        )

    @commands.command(
        description="You have a bug to report? Use this command!", aliases=["bugreport"]
    )
    @cooldown(2, 600, BucketType.user)
    async def reportbug(self, ctx, *, bug: str):

        embed = discord.Embed(
            title=f"Bug Report:", description=bug, color=self.bot.main_color
        )

        embed.set_author(name=f"From {ctx.author}", icon_url=ctx.author.avatar_url)

        await self.bug_channel.send(embed=embed)

        bug_received = discord.Embed(
            color=self.bot.main_color,
            title="Thanks for the bug-catching! Your bug has now been sent to the developers!",
            description="You may find your bug in [the official support server](https://discord.gg/jz4WxkB) in the text channel, #bug-report!",
        )
        await ctx.send(embed=bug_received)


def setup(bot):
    bot.add_cog(HelpCommands(bot))
