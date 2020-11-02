from discord.ext import commands
from discord.utils import get
import discord

botid = 763626077292724264

class Events(commands.Cog):

  def __init__(self, bot):
	  self.bot = bot


  @commands.Cog.listener()
  async def on_member_join(self, member):
    role = get(member.guild.roles, id=770582752067846154)
    await member.add_roles(role)


  @commands.Cog.listener()
  async def on_message(self, ctx):
      # auto-reacts

      if ':weeeee:' in ctx.content:
        if ctx.author.id == botid:
          return
        else:
          await ctx.channel.purge(limit=1)
          await ctx.channel.send('<a:weeeee:771309755427061770>')

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