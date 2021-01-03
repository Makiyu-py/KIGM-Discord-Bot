from typing import Optional
import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
import json

class Settings(commands.Cog, name=':gear: Settings'):

  def __init__(self, bot):
	  self.bot = bot

  @commands.command(description='Set your mute role! \n(only users with manage roles have access to this command.)', aliases=['setmuterole', 'setmute'])
  @commands.guild_only()
  @cooldown(1, 600, BucketType.guild)
  @commands.has_permissions(manage_roles = True)
  async def setmuted(self, ctx, muted_role: discord.Role):
    mutedrole_id = muted_role.id

    await self.bot.config.upsert({"_id" : ctx.guild.id, "MuteRole" : mutedrole_id})

    await ctx.send(f"Muted Role is now updated as {muted_role.mention}!")

  @commands.command(description='Set your Giveaway Maker role! \n(only users with manage roles have access to this command.)', aliases=['setgrrole', 'setgiveaway'])
  @commands.guild_only()
  @cooldown(1, 600, BucketType.guild)
  @commands.has_permissions(manage_roles = True)
  async def setgiveawayrole(self, ctx, giveaway_maker_role: discord.Role):
    giveaway_id = giveaway_maker_role.id
    
    await self.bot.config.upsert({"_id" : ctx.guild.id, "GARole" : giveaway_id})


    await ctx.send(f"Givaway Maker Role is now updated as {giveaway_maker_role.mention}!")

  @commands.command(description='Change the prefix of me! \n(only admins have access to this command.)',aliases=['change_prefix'])
  @commands.guild_only()
  @cooldown(1, 600, BucketType.guild)
  @commands.has_permissions(administrator = True)
  async def changeprefix(self, ctx, *, new_prefix):

    if len(new_prefix) > 5:
      await ctx.send("Your prefix must be shorter than 5 characters!")
      ctx.command.reset_cooldown(ctx)
      return
      
    with open("databases/Settings/prefixes.json", "r") as f:
      prefixes= json.load(f)

    prefixes[str(ctx.guild.id)] = new_prefix
    with open("databases/Settings/prefixes.json", "w") as f:
      json.dump(prefixes,f)
    
    await ctx.send(f"Prefix now updated with `{new_prefix}`!")

def setup(bot):
  bot.add_cog(Settings(bot))