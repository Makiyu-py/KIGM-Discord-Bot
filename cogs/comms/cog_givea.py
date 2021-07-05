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
import random

import discord
from discord.ext import commands

from the_universe import convert


class Giveaway(commands.Cog, name=":tada: Giveaway Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        description=f"Start a giveaway! \n(only users with the specified role from the `setgiveawayrole` command can only start.)",
        aliases=["g_start"],
    )
    @commands.guild_only()
    async def giveaway_start(self, ctx):
        GuildData = await self.bot.config.get_document(ctx.guild.id)

        if GuildData == False:
            await ctx.send(
                "**ERROR!**You may have not set your Giveaway Maker role yet!\nYou may by using the `setgiveawayrole <giveaway_role>` command."
            )
            return

        try:
            role = discord.utils.get(ctx.guild.roles, id=GuildData["GARole"])
        except KeyError:
            await ctx.send(
                "You may have not set your Giveaway Maker role!\nYou may by using the `setgiveawayrole <giveaway_role>` command."
            )
        else:
            if role in ctx.author.roles:
                await ctx.send(
                    "**Let's start with this giveaway!** Answer these questions within 20 seconds!"
                )

                questions = [
                    "1. **Which channel should this giveaway be hosted in?**",
                    "2. What should be the duration of the giveaway? (s|m|h|d|w) \nexample: `5d`",
                    "3. What is the prize when someone wins the giveaway?",
                ]

                answers = []

                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel

                for i in questions:
                    await ctx.send(i)

                    try:
                        msg = await self.bot.wait_for(
                            "message", timeout=20.0, check=check
                        )
                    except asyncio.TimeoutError:
                        await ctx.send(
                            "You didn't answer in time, please be quicker next time!"
                        )
                        return
                    else:
                        answers.append(msg.content)
                try:
                    c_id = int(answers[0][2:-1])
                except:
                    await ctx.send(
                        f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time."
                    )
                    return

                channel = self.bot.get_channel(c_id)

                time = convert(answers[1])

                if time == -1:
                    await ctx.send(
                        f"You didn't answer the time with a proper unit. Use (s|m|h|d|w) next time!"
                    )
                    return
                elif time == -2:
                    await ctx.send(
                        f"The time must be an integer. Please enter an integer next time"
                    )
                    return

                prize = answers[2]

                await ctx.send(
                    f"The __Giveaway will be in {channel.mention}__ and will last **{answers[1]}!** And prize... **{prize}!**\nI recommend you to not react to the giveaway so you also won't be entered. *(Unless you really....)*"
                )

                embed = discord.Embed(
                    title="Giveaway!", description=f"{prize}", color=0xB19CD9
                )
                embed.set_author(
                    name=f"Giveaway Created by {ctx.author}!",
                    icon_url=ctx.author.avatar_url,
                )
                embed.set_footer(
                    text=f"React with 🎉 to enter! | Ends {answers[1]} from now!"
                )

                my_msg = await channel.send(embed=embed)

                await my_msg.add_reaction("🎉")

                # if time < 600:
                await asyncio.sleep(time)

                new_msg = await channel.fetch_message(my_msg.id)

                users = await new_msg.reactions[0].users().flatten()
                users.pop(users.index(self.bot.user))

                try:
                    winner = random.choice(users)
                except IndexError:
                    await ctx.author.send(
                        f"The giveaway that you started {answers[1]} ago from {ctx.guild.name} has now reached its death and got __a winner!__ \nAbout that...\nNo winner."
                    )
                    await channel.send("Congrats!")
                    await asyncio.sleep(1.5)
                    await channel.send("*No one....*")

                await ctx.author.send(
                    f"The giveaway that you started {answers[1]} ago from {ctx.guild.name} has now reached its death and got __a winner!__\n\nWinner: {winner} | ID: `{winner.id}` "
                )
                await channel.send(
                    f"Congratulations! {winner.mention} has won the **{prize}** Giveaway!"
                )

            else:
                await ctx.send(
                    "**ERROR!**\nYou do not have the Giveaway Maker role set by the admins!\n(Please contact the admins for more info about the Giveaway Maker role.)"
                )
                return

    @commands.command(description="Got an undeserving winner? Re-roll the dice!")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def reroll(self, ctx, id_of_giveaway: int):
        await ctx.message.delete()

        try:
            new_msg = await ctx.channel.fetch_message(id_of_giveaway)
        except:
            await ctx.error("Invalid message id")
            return

        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))

        winner = random.choice(users)

        await ctx.channel.send(
            f"Oh! I have read my papers wrong. The **ACTUAL** winner is {winner.mention}! Congrats!"
        )

    @commands.Cog.listener()
    async def on_giveaway_end(self, time_left, data):
        if time_left > 0:
            await asyncio.sleep(time_left)

        chan = self.bot.get_channel(data["chan_id"])
        giv_usr = self.bot.get_user(data["user_id"])
        em_msg = await chan.fetch_message(int(data["msg_id"]))
        ctx = self.bot.get_context(em_msg)

        embed = discord.Embed(
            title="Giveaway Ended!", description=str(data["prize"]), color=0xB19CD9
        )
        embed.set_author(
            name=f"Giveaway Created by {ctx.author}!", icon_url=ctx.author.avatar_url
        )
        embed.set_footer(text=f"Ended at {em_msg.ended_at} UTC")

        users = await em_msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))

        winners = []
        for _ in range(int(data["how many winners"])):
            winner = random.choice(users)
            users.pop(users.index(winner))
            winners.append(winner.mention)

        embed.add_field(name="Winners", value="\n".join(*winners))

        await em_msg.edit(embed=embed)
        await chan.send(
            f"Congratulations! {', '.join(*winners)} has won the **{data['prize']}** Giveaway!"
        )


def setup(bot):
    bot.add_cog(Giveaway(bot))
