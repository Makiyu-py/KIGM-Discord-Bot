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

from typing import List, Optional, Union

import discord
from discord.ext import commands
from discord.ext.commands import Command, Group

from the_universe import syntax


async def generate_cog_help_embed(
    ctx, *, cog: Optional[commands.Cog], cmds: List[commands.Command]
) -> discord.Embed:
    commandList = "".join(
        f"\n`{command.name}` - *{command.description}*\n" for command in cmds
    )

    prefix = "&"
    if ctx.guild:
        prefix = await ctx.bot.config.find(ctx.guild.id)
        try:
            prefix = prefix["Bot Prefix"]
        except TypeError:
            pass

    helpEmbed = discord.Embed(
        title="All Commands!",
        description=":pushpin: My Prefix in this server is **`{}`**".format(prefix),
        color=ctx.bot.main_color,
    )
    helpEmbed.add_field(
        name=cog.qualified_name if cog else "No Category",
        value=commandList,
        inline=True,
    )

    return helpEmbed


class KIGMHelp(commands.HelpCommand):
    def __init__(self, **options):
        super().__init__(**options)
        self.SB_COGS = [
            "Events",
            "Asyncfuncs",
            "Tests",
            ":desktop: Server Managing",
            "SlashCommands",
            "TopGG",
            "Jishaku",
        ]

    async def cmd_help(self, command: Union[Command, Group]):
        prefix = await self.bot.config.find(self.guild.id)
        prefix = prefix.get("Bot Prefix", "&")
        embed = discord.Embed(
            title=f"{str(command).upper()} Help!",
            description=f"`{prefix}` {syntax(command, False)}",
            color=self.bot.main_color,
        )

        if isinstance(command, Group):
            subcmds_string = "".join(
                "**•  {0.name}**\n".format(subcommmand)
                for subcommmand in command.walk_commands()
                if subcommmand.parents[0] == command
            )

            embed.add_field(name="Subcommands", value=subcmds_string, inline=False)

        if len(command.aliases) > 0:
            embed.add_field(
                name="Command Aliases",
                value=", ".join("**{}**".format(al) for al in command.aliases),
                inline=False,
            )

        embed.add_field(
            name=f"Command Description:",
            value=command.description or "no description ¯\_(ツ)_/¯",
            inline=False,
        )

        embed.set_footer(
            text=f"{prefix} - Server Prefix | <> - Required | [] - Optional"
        )
        return await self.get_destination().send(embed=embed)

    def get_command_signature(self, command):
        return syntax(command)

    async def send_bot_help(self, mapping):
        HelpList = []
        ctx = self.context

        for cog, _commands in mapping.items():
            if not cog or cog.qualified_name in self.SB_COGS:
                continue

            helpEmbed = await generate_cog_help_embed(ctx, cog=cog, cmds=_commands)
            helpEmbed.set_footer(
                text=f"Created by Makiyu#4707 | Page {len(HelpList) + 1} of {len(mapping.items())//2}",
                icon_url="https://cdn.discordapp.com/avatars/526616688091987968/fc88ac5bd50ddabe601fb655e2ba72e0.webp?size=32",
            )
            HelpList.append(helpEmbed)

        await ctx.paginate(HelpList, timeout=50, destination=self.get_destination())

    async def send_cog_help(self, cog):
        ctx = self.context

        if cog.qualified_name in self.SB_COGS:
            return await ctx.error("Content after help must be a command.")

        help_embed = await generate_cog_help_embed(
            ctx, cog=cog, cmds=cog.get_commands()
        )

        help_embed.set_footer(
            text=f"Created by Makiyu#4707",
            icon_url="https://cdn.discordapp.com/avatars/526616688091987968/fc88ac5bd50ddabe601fb655e2ba72e0.webp?size=32",
        )

        dest = self.get_destination()
        await dest.send(embed=help_embed)

    async def send_group_help(self, group):
        ctx = self.context

        if group.cog_name in self.SB_COGS:
            return await ctx.error("Content after help must be a command.")

        await self.cmd_help(group)

    async def send_command_help(self, command):
        ctx = self.context

        if command.cog_name in self.SB_COGS:
            return await ctx.error("Content after help must be a command.")

        await self.cmd_help(command)

    async def send_error_message(self, error):
        dest = self.get_destination()
        await dest.send(error)
