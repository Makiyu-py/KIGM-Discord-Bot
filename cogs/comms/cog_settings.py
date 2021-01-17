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

from typing import Optional
import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown


class Settings(commands.Cog, name=':gear: Settings'):

  def __init__(self, bot):
	  self.bot = bot

  @commands.command(description='Set my auto-response/auto-react settings! \n(only admins have access to this command.)',aliases=['set_auto'])
  @commands.guild_only()
  @cooldown(1, 120, BucketType.guild)
  @commands.has_permissions(administrator = True)
  async def set_autoresponse(self, ctx, on_or_off: str):
    if not on_or_off.lower() in ('on', 'off', 'true', 'false'):
      await ctx.send("**ERROR!**\nYou must only input on/off when setting up autoresponse!")
      return

    msg = 'Auto-response mode is now turned {}!'

    if on_or_off.lower() in ('on', 'true'):
      await self.bot.config.upsert({"_id" : ctx.guild.id, "AutoResponse Mode" : True})
      await ctx.send(msg.format('on'))

    
    elif on_or_off.lower() in ('off', 'false'):
      await self.bot.config.upsert({"_id" : ctx.guild.id, "AutoResponse Mode" : False})
      await ctx.send(msg.format('off'))

  @commands.command(description='Set your mute role! \n(only users with manage roles have access to this command.)', aliases=['setmuterole', 'setmute'])
  @commands.guild_only()
  @cooldown(1, 600, BucketType.guild)
  @commands.has_permissions(manage_roles = True)
  async def setmuted(self, ctx, muted_role: discord.Role):
    mutedrole_id = muted_role.id

    await self.bot.config.upsert({"_id" : ctx.guild.id, "MuteRole" : mutedrole_id})

    await ctx.message.reply(f"Muted Role is now updated as {muted_role.mention}!")

  @commands.command(description='Set your Giveaway Maker role! \n(only users with manage roles have access to this command.)', aliases=['setgrrole', 'setgiveaway'])
  @commands.guild_only()
  @cooldown(1, 600, BucketType.guild)
  @commands.has_permissions(manage_roles = True)
  async def setgiveawayrole(self, ctx, giveaway_maker_role: discord.Role):
    giveaway_id = giveaway_maker_role.id
    
    await self.bot.config.upsert({"_id" : ctx.guild.id, "GARole" : giveaway_id})


    await ctx.message.reply(f"Givaway Maker Role is now updated as {giveaway_maker_role.mention}!")

  @commands.command(description='Change the prefix of me! \n(only admins have access to this command.)',aliases=['change_prefix'])
  @commands.guild_only()
  @cooldown(1, 600, BucketType.guild)
  @commands.has_permissions(administrator = True)
  async def changeprefix(self, ctx, *, new_prefix):

    if len(new_prefix) > 5:
      await ctx.send("Your prefix must be shorter than 5 characters!")
      ctx.command.reset_cooldown(ctx)
      return
      
    await self.bot.config.upsert({"_id" : ctx.guild.id, "Bot Prefix" : new_prefix})
    await ctx.message.reply(f"Prefix now updated with `{new_prefix}`!")

def setup(bot):
  bot.add_cog(Settings(bot))