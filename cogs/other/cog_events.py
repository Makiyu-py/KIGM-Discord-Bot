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

from discord.ext import commands
from discord.utils import get
import math
import discord
import json
import traceback
import random
import sys
from the_universe import syntax


botid = 763626077292724264

class Events(commands.Cog):

  def __init__(self, bot):
    self.bot = bot


  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):

    # This prevents any commands with local handlers being handled here in on_command_error.
    if hasattr(ctx.command, 'on_error'):
      return

    # This prevents any cogs with an overwritten cog_command_error being handled here.
    cog = ctx.cog
    if cog:
      if cog._get_overridden_method(cog.cog_command_error) is not None:
        return

    ignored = (commands.CommandNotFound, commands.NotOwner)

    # Allows us to check for original exceptions raised and sent to CommandInvokeError.
    # If nothing is found. We keep the exception passed to on_command_error.
    error = getattr(error, 'original', error)

    # Anything in ignored will return and prevent anything happening.
    if isinstance(error, ignored):
      return

    if isinstance(error, commands.DisabledCommand):
      await ctx.send("**ERROR!**\nThis command has been disabled by the devs!")

    if isinstance(error, commands.ExtensionAlreadyLoaded):
      await ctx.send("Execution stopped. Reason: Cog already loaded.")
      
    if isinstance(error, discord.Forbidden):
      await ctx.send("**ERROR!**\nI am not allowed to do that due to Missing Permissions/Other.")
      return

    if isinstance(error, commands.NoPrivateMessage):
      try:
        await ctx.author.send(f'the `{ctx.command}` can not be used in Private Messages.\nIf you want to use this command without ruining the experience, invite me to your server!')
        return
      except discord.HTTPException:
        pass

    if isinstance(error, commands.MemberNotFound):
      await ctx.send("**ERROR!**\nThe member that you gave/mentioned does not exist.\n(If it does, just... retry in a few seconds)")

    if isinstance(error, commands.MissingPermissions):
      await ctx.send("**ERROR!**\nYou are missing specific permissions to run this command.\n(For more info, look at the description of the command that you are using.)")
      
    if isinstance(error, commands.BadArgument):
      await ctx.send(f"**ERROR!**\nYou have *misued* a required argument on the {ctx.command} command.\nCorrect use: {syntax(ctx.command)}")
      try:
        ctx.command.reset_cooldown(ctx)
      except:
        pass
      return
    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.send(f"**ERROR!**\nYou are *missing* a required argument on the {ctx.command} command.\nCorrect use: {syntax(ctx.command)}")
      try:
        ctx.command.reset_cooldown(ctx)
      except:
        pass
      return

    if isinstance(error, commands.CommandOnCooldown):

      if int(error.retry_after) >= 3600:
        await ctx.send(f"The {ctx.command} command is **currently on cooldown!**\n**Try again in {error.retry_after/3600:,.2f} hours.**")
        return

      elif len(str(int(error.retry_after))) >= 3:
        await ctx.send(f"The {ctx.command} command is **currently on cooldown!**\n**Try again in {error.retry_after/60:,.2f} minutes.**")
        return

      elif int(error.retry_after) <= 99:
        await ctx.send(f"The {ctx.command} command is **currently on cooldown!**\n**Try again in {error.retry_after:,.2f} seconds.**")
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
    if not ctx.command.qualified_name in ['load', 'unload', 'reload', 'blacklist', 'listcogs', 'createtag', 'alltags', 'tag', 'guess_the_number', 'hackerman', 'makeexclusivechannel', 'slowmode', 'delete_textchannel']:

      if await self.bot.cmd_stats.find(ctx.command.qualified_name) is None:
        await self.bot.cmd_stats.upsert({"_id": ctx.command.qualified_name, "usage_count": 1})

      else:
        await self.bot.cmd_stats.increment(
          ctx.command.qualified_name, 1, "usage_count"
        )

    else:
      return

  @commands.Cog.listener()
  async def on_message(self, ctx):
    if not ctx.author.bot:
      if ctx.content == f"<@!{botid}>":
        if ctx.author.id == botid:
          return
        else:
          serverprefix = await self.bot.config.find(ctx.guild.id)
          serverprefix = serverprefix["Bot Prefix"] if serverprefix is not None and not KeyError else "&"
          await ctx.channel.send(f"**Thanks for pinging me!** :mailbox_with_mail:\n\n> :man_astronaut: My prefix in this server is `{serverprefix}`\n\n> :face_with_monocle: Use the `{serverprefix}help [command]` to know more about the commands I have! \n\n> :thumbsup: Liking me so far? You can vote me on:\n> \n> :sailboat: **discord.boats** - **https://discord.boats/bot/763626077292724264**\n> \n> :robot: **top.gg** - **https://top.gg/bot/763626077292724264/vote**")
          
      chance = random.randint(1, 15)
      if chance == 11:
        # auto-reacts

        if ctx.content.startswith('sad '):
          if ctx.author.id == botid:
            return
          else:
            await ctx.add_reaction('<:Sadge:770201772228083712>')
    
        if ctx.content.startswith('Sad '):
          if ctx.author.id == botid:
            return
          else:
            await ctx.add_reaction('<:Sadge:770201772228083712>')
        
        if ctx.content.startswith('Sadge '):
          if ctx.author.id == botid:
            return
          else:
            await ctx.add_reaction('<:Sadge:770201772228083712>')

        if ctx.content.startswith('sadge '):
          if ctx.author.id == botid:
            return
          else:
            await ctx.add_reaction('<:Sadge:770201772228083712>')
            
        if ctx.content.startswith('hm'):
          if ctx.author.id == botid:
            return
          else:
            await ctx.add_reaction('<:LuigiHmm:760444048523395103>')

        if ctx.content.startswith('Hm'):
          if ctx.author.id == botid:
            return
          else:
            await ctx.add_reaction('<:LuigiHmm:760444048523395103>')

        if 'muah' in ctx.content:
          if ctx.author.id == botid:
            return
          else:
            await ctx.add_reaction('<:chefkiss:760770186063118356>')

        if 'Muah' in ctx.content:
          if ctx.author.id == botid:
            return
          else:
            await ctx.add_reaction('<:chefkiss:760770186063118356>')
            
        if 'AYAYA' in ctx.content:
          if ctx.author.id == botid:
            return
          else:
            await ctx.add_reaction('<:AYAYA:767895991218077697>')

        if 'ayaya' in ctx.content:
          if ctx.author.id == botid:
            return
          else:
            await ctx.add_reaction('<:AYAYA:767895991218077697>')

        if '@everyone' in ctx.content:
          await ctx.add_reaction('<:peepoping:760446389917319208>')

        if '@here' in ctx.content:
          await ctx.add_reaction('<:peepoping:760446389917319208>')
          
        #auto-sends

        if ctx.content.startswith('why'):
          if ctx.author.id == botid:
            return
          else:
            await ctx.channel.send('*idk*    ¯\_(ツ)_/¯')

        if ctx.content.startswith('Why'):
          if ctx.author.id == botid:
            return
          else:
            await ctx.channel.send('*idk*    ¯\_(ツ)_/¯')


def setup(bot):
  bot.add_cog(Events(bot))