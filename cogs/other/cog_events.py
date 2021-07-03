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

import random

import discord
from discord.ext import commands
from discord.utils import get

from the_universe import syntax

botid = 763626077292724264


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, "on_error"):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, commands.NotOwner, commands.CheckFailure)

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, "original", error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            await ctx.error("\This command has been disabled by the devs!")

        elif isinstance(error, commands.ExtensionAlreadyLoaded):
            await ctx.send("Execution stopped. Reason: Cog already loaded.")

        elif isinstance(error, discord.Forbidden):
            await ctx.error(
                "I am not allowed to do that due to Missing Permissions/Other."
            )
            return

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(
                    f"the `{ctx.command}` can not be used in Private Messages.\nIf you want to use this command without ruining the experience, invite me to your server!"
                )
                return
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.MemberNotFound):
            await ctx.error(
                "The member that you gave/mentioned does not exist.\n(If it does, just... retry in a few seconds)"
            )

        elif isinstance(error, commands.MissingPermissions):
            await ctx.error(
                "You are missing specific permissions to run this command.\n(For more info, look at the description of the command that you are using.)"
            )

        elif isinstance(error, commands.BadArgument):
            await ctx.error(
                f"You have *misued* a required argument on the {ctx.command} command.\nCorrect use: {syntax(ctx.command)}"
            )
            try:
                ctx.command.reset_cooldown(ctx)
            except:
                pass
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.error(
                f"You are *missing* a required argument on the {ctx.command} command.\nCorrect use: {syntax(ctx.command)}"
            )
            try:
                ctx.command.reset_cooldown(ctx)
            except:
                pass
            return

        elif isinstance(error, commands.CommandOnCooldown):

            if int(error.retry_after) >= 3600:
                await ctx.send(
                    f"The {ctx.command} command is **currently on cooldown!**\n**Try again in {error.retry_after / 3600:,.2f} hours.**"
                )
                return

            elif len(str(int(error.retry_after))) >= 3:
                await ctx.send(
                    f"The {ctx.command} command is **currently on cooldown!**\n**Try again in {error.retry_after / 60:,.2f} minutes.**"
                )
                return

            elif int(error.retry_after) <= 99:
                await ctx.send(
                    f"The {ctx.command} command is **currently on cooldown!**\n**Try again in {error.retry_after:,.2f} seconds.**"
                )
                return

        else:
            raise error

    # KIGM Support Exclusives
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 770558935144726528:
            role = get(member.guild.roles, id=770582752067846154)
            await member.add_roles(role)
            return

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        if not ctx.command.qualified_name in [
            "blacklist",
            "listcogs",
            "createtag",
            "alltags",
            "tag",
            "guess_the_number",
            "hackerman",
            "makeexclusivechannel",
            "slowmode",
            "delete_textchannel",
            "jishaku load",
            "vote_test",
            "jishaku shell",
            "jishaku",
            "jishaku python",
        ]:
            if not ctx.command.qualified_name.startswith("jishaku"):

                if await self.bot.cmd_stats.find(ctx.command.qualified_name) is None:
                    await self.bot.cmd_stats.upsert(
                        {"_id": ctx.command.qualified_name, "usage_count": 1}
                    )

                else:
                    await self.bot.cmd_stats.increment(
                        ctx.command.qualified_name, 1, "usage_count"
                    )

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.guild and not ctx.author.bot:
            if ctx.content == f"<@!{botid}>" or ctx.content == f"<@{botid}>":
                serverprefix = await self.bot.config.find(ctx.guild.id)
                try:
                    serverprefix = serverprefix["Bot Prefix"]
                except TypeError:
                    serverprefix = "&"
                finally:
                    await ctx.channel.send(
                        f"**Thanks for pinging me!** :mailbox_with_mail:\n\n> :man_astronaut: My prefix in this server is `{serverprefix}`\n\n> :face_with_monocle: Use the `{serverprefix}help [command]` to know more about the commands I have! \n\n> :thumbsup: Liking me so far? You can vote me on:\n> \n> :sailboat: **discord.boats** - **https://discord.boats/bot/763626077292724264 **\n> \n> :robot: **top.gg** - **https://top.gg/bot/763626077292724264/vote **"
                    )
                return

            chance = random.randint(1, 8)
            g_data = await self.bot.config.find(ctx.guild.id)

            if g_data is not None:
                if "AutoResponse Mode" in g_data:
                    autores = g_data["AutoResponse Mode"]
                else:
                    autores = False

            else:
                autores = False

            if autores and chance == random.randint(1, 8):

                # auto-reacts
                if ctx.content.lower().startswith("sadge "):
                    await ctx.add_reaction("<:Sadge:770201772228083712>")

                elif ctx.content.lower().startswith("hm"):
                    await ctx.add_reaction("<:LuigiHmm:760444048523395103>")

                elif "muah" in ctx.content.lower():
                    await ctx.add_reaction("<:chefkiss:760770186063118356>")

                elif ctx.content.upper() == "AYAYA":
                    await ctx.add_reaction("<:AYAYA:767895991218077697>")

                # auto-sends
                elif ctx.content.lower().startswith("why"):
                    await ctx.channel.send("*idk*    ¯\_(ツ)_/¯")


def setup(bot):
    bot.add_cog(Events(bot))
