from typing import List, Optional

import discord
from discord.ext import commands

from the_universe import syntax


async def generate_cog_help_embed(
    ctx, *, cog: Optional[commands.Cog], cmds: List[commands.Command]
) -> discord.Embed:
    commandList = ""

    for command in cmds:
        commandList += f"\n`{command.name}` - *{command.description}*\n"

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

    def get_command_signature(self, command):
        return syntax(command)

    async def send_bot_help(self, mapping):
        HelpList = []
        ctx = self.context

        for cog, _commands in mapping.items():
            if cog.qualified_name in self.SB_COGS:
                continue

            helpEmbed = await generate_cog_help_embed(ctx, cog=cog, cmds=_commands)
            helpEmbed.set_footer(
                text=f"Created by Makiyu#4707 | Page {len(HelpList) + 1} of {len(mapping.items())}",
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

        await ctx.cmd_help(group)

    async def send_command_help(self, command):
        ctx = self.context

        if command.cog_name in self.SB_COGS:
            return await ctx.error("Content after help must be a command.")

        await ctx.cmd_help(command)

    async def send_error_message(self, error):
        dest = self.get_destination()
        await dest.send(error)
