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


class Settings(commands.Cog, name=":gear: Settings"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        description="Set my auto-response/auto-react settings! \n(only admins have access to this command.)",
        aliases=["set_auto"],
    )
    @commands.guild_only()
    @cooldown(1, 120, BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def set_autoresponse(self, ctx, on_or_off: str):
        if on_or_off.lower() not in ("on", "off", "true", "false"):
            await ctx.send(
                "**ERROR!**\nYou must only input on/off when setting up autoresponse!"
            )
            return

        msg = "Auto-response mode is now turned {}!"

        if on_or_off.lower() in ("on", "true"):
            await self.bot.config.upsert(
                {"_id": ctx.guild.id, "AutoResponse Mode": True}
            )
            await ctx.send(msg.format("on"))

        elif on_or_off.lower() in ("off", "false"):
            await self.bot.config.upsert(
                {"_id": ctx.guild.id, "AutoResponse Mode": False}
            )
            await ctx.send(msg.format("off"))

    @commands.command(
        description="Set your mute role! \n(only users with manage roles have access to this command.)",
        aliases=["setmuterole", "setmute"],
    )
    @commands.guild_only()
    @cooldown(1, 600, BucketType.guild)
    @commands.has_permissions(manage_roles=True)
    async def setmuted(self, ctx, muted_role: discord.Role):
        mutedrole_id = muted_role.id

        await self.bot.config.upsert({"_id": ctx.guild.id, "MuteRole": mutedrole_id})

        await ctx.message.reply(f"Muted Role is now updated as {muted_role.mention}!")

    @commands.command(
        description="Set your Giveaway Maker role! \n(only users with manage roles have access to this command.)",
        aliases=["setgrrole", "setgiveaway"],
    )
    @commands.guild_only()
    @cooldown(1, 600, BucketType.guild)
    @commands.has_permissions(manage_roles=True)
    async def setgiveawayrole(self, ctx, giveaway_maker_role: discord.Role):
        giveaway_id = giveaway_maker_role.id

        await self.bot.config.upsert({"_id": ctx.guild.id, "GARole": giveaway_id})

        await ctx.message.reply(
            f"Givaway Maker Role is now updated as {giveaway_maker_role.mention}!"
        )

    @commands.command(
        description="Change the prefix of me! \n(only admins have access to this command.)",
        aliases=["change_prefix"],
    )
    @commands.guild_only()
    @cooldown(1, 600, BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def changeprefix(self, ctx, *, new_prefix):

        if len(new_prefix) > 5:
            await ctx.send("Your prefix must be shorter than 5 characters!")
            ctx.command.reset_cooldown(ctx)
            return

        await self.bot.config.upsert({"_id": ctx.guild.id, "Bot Prefix": new_prefix})
        await ctx.message.reply(f"Prefix now updated with `{new_prefix}`!")


def setup(bot):
    bot.add_cog(Settings(bot))
