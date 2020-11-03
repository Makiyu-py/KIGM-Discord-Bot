import discord
from discord.ext import commands
from discord.utils import get
import math
import random

class HelpCommands(commands.Cog, name=':bookmark_tabs: Help'):

  def __init__(self, bot):
	  self.bot = bot
    
  botid = 763626077292724264


  @commands.command(name='help', description="Shows this message!",aliases=['commands', 'comms'])
  async def help(self, ctx, cog='1'):
    helpEmbed = discord.Embed(title="All Commands!", color = 0xf8f8ff)
    helpEmbed.set_thumbnail(url=ctx.author.avatar_url)

    cogs=[c for c in self.bot.cogs.keys()]
    cogs.remove("Events")

    totalPages = math.ceil(len(cogs) / 2)

    cog = int(cog)
    if cog > totalPages or cog < 1:
      await ctx.send(f"Noneexistent page number (`{cog}`) lol only until {totalPages}")
      return
    
    helpEmbed.set_footer(text=f"Created by Makiyu#4707 | Page {cog} of {totalPages}", icon_url = 'https://cdn.discordapp.com/avatars/526616688091987968/fc88ac5bd50ddabe601fb655e2ba72e0.webp?size=32')
    neededCogs = []

    for i in range(2):
      x = i + (int(cog) - 1) * 2
      try:
        neededCogs.append(cogs[x])
      except IndexError:
        pass

    for cog in neededCogs:
      commandList = ""
      for command in self.bot.get_cog(cog).walk_commands():
        if command.hidden:
          continue
        
        elif command.parent != None:
          continue

        commandList += f"**{command.name}** - *{command.description}*\n"

      commandList += "\n"

      helpEmbed.add_field(name=cog, value=commandList, inline=True)

    await ctx.send(embed=helpEmbed)
      
  @commands.command(description = "Suggest something to improve this bot!",aliases=['bot_suggest'])
  async def suggest(self, ctx, *, your_suggestion):

    suggestion_request_received = discord.Embed(color=0xf8f8ff, title='Thank for the suggestion! Your suggestion has now been sent to the developers!', description='You may find your suggestion in [the official support server](https://discord.gg/jz4WxkB) in the text channel, #suggestions-area!')
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
    await ctx.channel.send("<a:weeeee:771309755427061770>**Invite Me**<a:weeeee:771309755427061770>\nhttps://discord.com/oauth2/authorize?client_id=763626077292724264&permissions=268790854&scope=bot")

    
def setup(bot):
	bot.add_cog(HelpCommands(bot))