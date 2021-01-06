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
import asyncio
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import BucketType, cooldown
import json

def get_time(time: int):
  if time >= 86400:
    return f"{round(time / 86400)} days"

  elif time >= 3600:
    return f"{round(time / 3600)} hours"

  elif time >= 60:
    return f"{round(time / 60)} minutes"

  else:
    return f"{time} seconds"
class ServerManager(commands.Cog, name=':desktop: Server Managing'):

  def __init__(self, bot):
	  self.bot = bot

  @commands.command(aliases=['exclusivechannel', 'makexclusivechannel', 'mec', 'createexclusivechannel'])
  @commands.is_owner()
  @commands.guild_only()
  @commands.has_permissions(manage_channels = True)
  async def makeexclusivechannel(self, ctx, role: discord.Role, channel_name: str, *, Category_Name: Optional[discord.CategoryChannel]=None):
    overwrites={
      ctx.guild.default_role: discord.PermissionOverwrite(read_messages= False if ctx.guild.default_role != role else True),
      ctx.guild.me: discord.PermissionOverwrite(read_messages = True),
      role: discord.PermissionOverwrite(read_messages=True)
    }
    if Category_Name is None:
      Category_Name = None

    channel = await ctx.guild.create_text_channel(
      name=channel_name, 
      overwrites=overwrites,
      category=Category_Name
      )

    No_Cat = "No Category"
    await ctx.send(f"I have now made {channel.mention} in **{Category_Name if Category_Name != None else No_Cat}!**")

  @commands.command(aliases=['shakey', 'shakechannel'])
  @commands.is_owner()
  @commands.guild_only()
  @commands.has_permissions(manage_channels = True)
  async def slowmode(self, ctx, slow_time_seconds: int, text_channel: Optional[discord.TextChannel]=None):
    await ctx.message.delete()
    if text_channel is None:
      text_channel = ctx.channel
      
    await text_channel.edit(slowmode_delay=slow_time_seconds)

    if slow_time_seconds > 0:
      if text_channel != ctx.channel:
        await ctx.send(f"Slow mode is now **activated** in {text_channel.mention}!")
      await text_channel.send(f"Slowmode is now **turned on** in this channel!\nSlowmode Time: *{get_time(slow_time_seconds)}*")
    elif slow_time_seconds == 0:
      if text_channel != ctx.channel:
        await ctx.send(f"Slow mode is now **deactivated** in {text_channel.mention}!")
      await text_channel.send(f"Slowmode is now **turned off** in this channel!")

  @commands.command()
  @commands.is_owner()
  @commands.guild_only()
  @commands.has_permissions(manage_channels = True)
  async def delete_textchannel(self, ctx, channel: Optional[discord.TextChannel]=None):
    await ctx.message.delete()
    if channel is None:
      channel = ctx.channel
    suremsg = await ctx.send(f"Are you sure that you want to delete {channel.mention}?  [y/n]")
    try:
      msg = msg = await self.bot.wait_for("message", timeout=20, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)

      if msg.content.lower() == 'y' or msg.content.lower() == 'yes':
        await msg.delete()
        editthis = await ctx.send(f"cool. Deleting {channel.mention}.", delete_after=10.0)
        await asyncio.sleep(1)
        await editthis.edit(content=f'cool. Deleting {channel.mention}. .')
        await channel.delete()
        await asyncio.sleep(1)
        await editthis.edit(content=f'cool. Deleting {channel.name}. . .')
        await asyncio.sleep(2)
        await editthis.edit(content=f"#{channel.name} has now been **deleted!**\nNo going back now.")
        await asyncio.sleep(1)
        await editthis.edit(content=f"#{channel.name} has now been **deleted!**\nNo going back now. .")
        await asyncio.sleep(1)
        await editthis.edit(content=f"#{channel.name} has now been **deleted!**\nNo going back now. . .")
        await suremsg.delete()

      elif msg.content.lower() == 'n' or msg.content.lower() == 'no':
        await msg.delete()
        await suremsg.delete()
        await ctx.send("Alrighty then.\nChannel Delete **Cancelled!**", delete_after=5.0)
        return

      else:
        await suremsg.delete()
        await ctx.send("You answer must be a y/n answer!", delete_after=6.0)

    except asyncio.TimeoutError:
      await ctx.send("*Command Cancelled.*", delete_after=5.0)

def setup(bot):
  bot.add_cog(ServerManager(bot))