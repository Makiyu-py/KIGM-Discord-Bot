import discord
from discord.ext import commands
import json

class ModCommands(commands.Cog, name=':hammer_pick: Moderator Commands'):

  def __init__(self, bot):
	  self.bot = bot

  @commands.command(description='Delete a specified amount of messages! (only members with manage messages can access this command.)',aliases=['c', 'removem', 'removemessage', 'rmms'])
  @commands.has_permissions(manage_messages = True)
  async def clear(self,ctx,amount=1):
    if amount > 40:
      await ctx.send("Oops... You can only delete less than 40 messages at a time :)")
      return
    else:
      await ctx.channel.purge(limit = amount + 1)

  @commands.command(description='Change the prefix of me! (only admins have access to this command.)',aliases=['change_prefix'])
  @commands.has_permissions(administrator = True)
  async def changeprefix(self, ctx, *, pre):
    with open("prefixes.json", "r") as f:
      prefixes= json.load(f)

    prefixes[str(ctx.guild.id)] = pre
    await ctx.send(f"Prefix now updated with '{pre}'!")

    with open("prefixes.json", "w") as f:
      json.dump(prefixes,f)

  @commands.command(description='kick a member! (only members with kick members have access to this command)',aliases=['kickmember', 'k'])
  @commands.has_permissions(kick_members = True)
  async def kick(self,ctx,member : discord.Member,*, reason='for... no reason, hm.'):
    await member.kick(reason=reason)
    await ctx.send(ctx.author.mention + ' has **kicked** '+ member.name +' from this server. Reason: '+ reason)
    await member.send(f"Oof, it seems like you have been kicked from {ctx.guild.name}, that sounds weird. Anyway, reason for kick: "+ reason)
    await ctx.message.delete()

  @commands.command(description='Ban a member! (only members with ban members have access to this command.)',aliases=['banmember', 'b'])
  @commands.has_permissions(ban_members = True)
  async def ban(self, ctx,member : discord.Member,*, reason="for... no reason."):
    await member.ban(reason=reason)
    await ctx.send(ctx.author.mention + ' has **banned** '+ member.name +' from this server. Reason: '+ reason)
    await member.send(f"Oof, it seems like you have been ||banned lol|| from {ctx.guild.name}, that sounds weird. Anyway, reason for ||ban||: "+ reason)
    await ctx.message.delete()

  @commands.command(description='Unban a member! (only members with ban members have access to this command.)',aliases=['unbanmember', 'ub'])
  @commands.has_permissions(ban_members = True)
  async def unban(self, ctx, *, member):
    await ctx.message.delete()
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{ctx.author.mention} has **unbanned** {user.mention}!")
            await user.send(f"You have been officially unbanned from **{ctx.guild.name}**!")

def setup(bot):
	bot.add_cog(ModCommands(bot))