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
from the_universe import syntax
import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
from discord.utils import get
import asyncio
from utils.paginate import dpyPaginate
import math
import re
import random



class HelpCommands(commands.Cog, name=':bookmark_tabs: Help'):

  def __init__(self, bot):
    self.bot = bot

    
  botid = 763626077292724264



  async def cmd_help(self, ctx, command):
    prefix = await self.bot.config.find(ctx.guild.id)
    prefix = prefix["Bot Prefix"] or "&"
    embed = discord.Embed(title=f"{str(command).upper()} Help!", description=f"`{prefix}` {syntax(command)}", color = self.bot.main_color)

    '''
    if command.parent in self.bot.get_command(command).walk_commands():
      SCmd = ""
      for subcommmand in command.parent:
        SCmd += f"`{subcommmand}` - {subcommmand.description}\n"

      embed.add_field(name='Subcommands:', value=SCmd)
    '''


    embed.add_field(name=f'Command Description:', value=command.help or command.description)

    embed.set_footer(text=f'{prefix} - Server Prefix | <> - Required | [] - Optional')
    await ctx.send(embed=embed)

  @commands.command(name='help', description="Shows this message!",aliases=['commands', 'comms', 'command'])
  async def help(self, ctx, *, optional_command: Optional[str]=None):

    cogs=[c for c in self.bot.cogs.keys()]

    SB_COGS = ['Events', 'Asyncfuncs', 'Tests', ':desktop: Server Managing', 'SlashCommands', 'TopGG', 'Jishaku']
    
    for hidden_cog in SB_COGS:
      cogs.remove(hidden_cog)
  

    if optional_command == None:
      HelpList = []

      for rl_cog in cogs:
        commandList = ""
        for command in self.bot.get_cog(rl_cog).walk_commands():
          if command.hidden:
            continue
            
          elif command.parent != None:
            continue

          commandList += f"\n`{command.name}` - *{command.description}*\n"

        else:
          prefix = await self.bot.config.find(ctx.guild.id)
          prefix = prefix["Bot Prefix"] or "&"
          helpEmbed = discord.Embed(title="All Commands!", description=':pushpin: My Prefix in this server is **`{}`**'.format(prefix), color = self.bot.main_color)
          helpEmbed.set_footer(
            text=f"Created by Makiyu#4707", 
            icon_url='https://cdn.discordapp.com/avatars/526616688091987968/fc88ac5bd50ddabe601fb655e2ba72e0.webp?size=32'
            )
          helpEmbed.add_field(name=rl_cog, value=commandList, inline=True)
          HelpList.append(helpEmbed)

      else:
        await dpyPaginate(PageList=HelpList, timeout=50).menustart(ctx)

    else:
      if (command := get(self.bot.commands, name=optional_command)):
        for secret_cogs in SB_COGS:
          if command in self.bot.get_cog(secret_cogs).walk_commands() or command.hidden:
            await ctx.send("**ERROR!**\nContent after help must be a command.")
            return
          
          else:
            await self.cmd_help(ctx, command)
            return

      else:
        await ctx.send("**ERROR!**\nContent after help must be a valid command.")
        return

      
  @commands.command(description = "Suggest something to improve this bot!",aliases=['bot_suggest'])
  @cooldown(1, 21600, BucketType.user)
  async def suggest(self, ctx, *, your_suggestion):

    suggestion_request_received = discord.Embed(color=self.bot.main_color, title='Thanks for the suggestion! Your suggestion has now been sent to the developers!', description='You may find your suggestion in [the official support server](https://discord.gg/jz4WxkB) in the text channel, #suggestions-area!')
    await ctx.send(embed=suggestion_request_received)

    embed = discord.Embed(color=0x222222, title='New Suggestion for KIGM: ', description=your_suggestion)


    embed.set_author(name=f'From {ctx.guild.name}', icon_url=ctx.guild.icon_url)
    embed.set_footer(text=f'Suggested by: {ctx.author}', icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    suggestions_channel = self.bot.get_channel(770633934827683923)
    suggestmsg = await suggestions_channel.send(embed=embed)

    await suggestmsg.add_reaction("💁‍♂️")
    await suggestmsg.add_reaction("🤷‍♀️")
    await suggestmsg.add_reaction("🙅")


  @commands.command(description = "Invite this bot to your server!",aliases=['inv'])
  async def invite(self, ctx):
    await ctx.channel.send("<a:weeeee:771309755427061770>**Invite Me**<a:weeeee:771309755427061770>\nhttps://discord.com/api/oauth2/authorize?client_id=763626077292724264&permissions=273115158&scope=bot%20applications.commands")

  @commands.command(description="You have a bug to report? Use this command!", aliases=['bugreport'])
  @cooldown(2, 600, BucketType.user)
  async def reportbug(self, ctx, *, bug: str):
    bug_channel = self.bot.get_channel(777684586003431435)


    embed = discord.Embed(title=f'Bug Report:', description=bug, color=self.bot.main_color)
    
    embed.set_author(name=f'From {ctx.author}', icon_url = ctx.author.avatar_url)


    await bug_channel.send(embed=embed)
    
    bug_received = discord.Embed(color=self.bot.main_color, title='Thanks for the bug-catching! Your bug has now been sent to the developers!', description='You may find your bug in [the official support server](https://discord.gg/jz4WxkB) in the text channel, #bug-report!')
    await ctx.send(embed=bug_received)

def setup(bot):
  bot.add_cog(HelpCommands(bot))