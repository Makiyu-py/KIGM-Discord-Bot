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

import asyncio
from typing import Optional

import discord
from discord.ext import commands


class ModCommands(commands.Cog, name=':hammer_pick: Moderator Commands'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        description='Delete a specified amount of messages! \n(only members with manage messages can access this command.)',
        aliases=['c', 'removem', 'removemessage', 'rmms'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: Optional[int] = 1):
        if amount > 40:
            await ctx.send("Oops... You can only delete less than 40 messages at a time :)")
            return
        else:
            await ctx.channel.purge(limit=amount + 1)

    @commands.command(description='Mute a member! \n(only members with manage roles have access to this command)',
                      aliases=['mutemember', 'muteuser'])
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, user: discord.Member):
        
        print(ctx.command.checks)
        GuildData = await self.bot.config.get_document(ctx.guild.id)

        if GuildData == False:
            await ctx.error(
                "You may have not set your muted role yet!\nYou may by using the `setmuted <muted_role>` command.")
            return

        try:
            role = discord.utils.get(ctx.guild.roles, id=GuildData['MuteRole'])
        except KeyError:
            await ctx.send(
                "**ERROR!**You may have not set your muted role yet!\nYou may by using the `setmuted <muted_role>` command.")
            return

        if role in user.roles:
            await ctx.send("User is **already muted!**")
        else:
            try:
                await user.add_roles(role)
            except discord.Forbidden:
                await ctx.send(f"I am not allowed to mute {user}!")
            else:
                await ctx.send(f"I have now muted {user}!")

    @commands.command(description='Unmute a member! \n(only members with manage roles have access to this command.)')
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, user: discord.Member):
        GuildData = await self.bot.config.get_document(ctx.guild.id)

        if GuildData == False:
            await ctx.error(
                "You may have not set your muted role yet!\nYou may by using the `setmuted <muted_role>` command.")
            return

        try:
            role = discord.utils.get(ctx.guild.roles, id=GuildData["MuteRole"])
        except KeyError:
            await ctx.error(
                "You may have not set your muted role!\nYou may by using the `setmuted <muted_role>` command.")
        else:
            if not role in user.roles:
                return await ctx.error(f"{user} is **already unmuted!**")

            try:
                await user.remove_roles(role)
            except discord.Forbidden:
                await ctx.send(f"I am not allowed to unmute {user}!")
            else:
                await ctx.send(f"I have now unmuted {user}!")


    @commands.command(description='kick a member! \n(only members with kick members have access to this command)',
                      aliases=['kickmember', 'k'])
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason='for... no reason, hm.'):
        await member.kick(reason=reason)
        await ctx.send(ctx.author.mention + ' has **kicked** ' + member.name + ' from this server. Reason: ' + reason)
        await member.send(
            f"Oof, it seems like you have been kicked from {ctx.guild.name}, that sounds weird. Anyway, reason for kick: " + reason)
        await ctx.message.delete()

    @commands.command(description='Ban a member! \n(only members with ban members have access to this command.)',
                      aliases=['banmember', 'b'])
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="for... no reason."):
        await member.ban(reason=reason)
        await ctx.send(ctx.author.mention + ' has **banned** ' + member.name + ' from this server. Reason: ' + reason)
        await member.send(
            f"Oof, it seems like you have been ||banned lol|| from {ctx.guild.name}, that sounds weird. Anyway, reason for ||ban||: " + reason)
        await ctx.message.delete()

    @commands.command(
        description='Softban a user! \n(Basically just kicks and deletes all messages of a user, 5 second ban lmao)',
        aliases=['sb'])
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, user_mention: discord.Member):
        try:
            await ctx.guild.ban(user_mention)
            sbmsg = await ctx.send(f"{user_mention} has now been softbanned!")
            await asyncio.sleep(4.8)
            await ctx.guild.unban(user_mention)
            await sbmsg.edit(content=f"{user_mention} has now been softbanned! `he may now join this server again`")

        except discord.Forbidden:
            await ctx.error(
                f"Cannot softban {user_mention}.\nReason: User is higher than the/as high as the bot to softban.")

    @commands.command(description='Unban a member! \n(only members with ban members have access to this command.)',
                      aliases=['unbanmember', 'ub'])
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        await ctx.message.delete()
        banned_users = await ctx.guild.bans()
        try:
            member_name, member_discriminator = member.split('#')
        except ValueError:
            await ctx.error(
                "The format for undbanning the user must be like this:\n`UserName#UserDiscriminator`")
            return

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{ctx.author.mention} has **unbanned** {user.mention}!")
                await user.send(f"You have been officially unbanned from **{ctx.guild.name}**!")
                return

        else:
            await ctx.error("I cannot find that member!")


def setup(bot):
    bot.add_cog(ModCommands(bot))
