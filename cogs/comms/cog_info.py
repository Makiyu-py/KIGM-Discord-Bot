from typing import Optional
import discord
import platform
from discord import Profile
from utils.paginate import dpyPaginate
from discord.ext import commands

class InfoCommands(commands.Cog, name=':information_source: Informative Commands'):

  def __init__(self, bot):
	  self.bot = bot

  @commands.command(description='Checks the latency of the bot!')
  async def ping(self, ctx):
    await ctx.send(f':regional_indicator_p: :regional_indicator_o: :regional_indicator_n: :regional_indicator_g: :grey_exclamation: `{round(self.bot.latency * 1000)}ms`')
    
  @commands.command(aliases=['cmdstats'], description='Get info about what are the most used commands! (and least too)')
  @commands.guild_only()
  async def command_stats(self, ctx):
        data = await self.bot.cmd_stats.get_all()
        command_map = {item["_id"]: item["usage_count"] for item in data}

        # get total commands run
        total_commands_run = sum(command_map.values())

        # Sort by value
        sorted_list = sorted(command_map.items(), key=lambda x: x[1], reverse=True)

        pages = []
        cmd_per_page = 10

        for i in range(0, len(sorted_list), cmd_per_page):
            message = "Read Structure: `Usage %` **|** `Number of total command runs`\n\n"
            next_commands = sorted_list[i: i + cmd_per_page]

            for item in next_commands:
                use_percent = item[1] / total_commands_run
                message += f"**{item[0]}** - `{use_percent: .2%}` | Ran `{item[1]}` time(s)\n"

            page = discord.Embed(title="Command Usage Statistics!", description=message, color=self.bot.main_color)
            pages.append(page)
        
        breact= dpyPaginate(PageList=pages, timeout=45)
        await breact.menustart(ctx)

  @commands.command(aliases=['stat', 'botinfo'], description="Shows my statistics!")
  async def stats(self, ctx):
    pythonVersion = platform.python_version()
    dpyVersion = discord.__version__
    serverCount = len(self.bot.guilds)
    memberCount=len(set(self.bot.get_all_members()))
    embed = discord.Embed(colour=self.bot.main_color, timestamp=ctx.message.created_at)
    embed.add_field(name='<:python:769448668348416010>Python Version ',   value=pythonVersion)
    embed.add_field(name='<:discord:769449385670737940>Discord.py Version ',value=dpyVersion)
    embed.add_field(name="<:server_boost:769450820076306443>Total Guilds I'm on",      value=serverCount)
    embed.add_field(name="<:members:769449777472471060>Ignorant Friends",      value= memberCount)
    embed.add_field(name='<a:botdev_shine:769445361693491200>Developer', value='<@526616688091987968>')
    embed.add_field(name=':people_hugging:Support Server', value='[Plz join](https://discord.gg/jz4WxkB)')
    embed.add_field(name="<:invite:769450163671400459>Bot Invite", value="[Invite meee](https://discord.com/oauth2/authorize?client_id=763626077292724264&scope=bot&permissions=273115158)", inline=True )
    embed.set_author(name=f"{ctx.bot.user.name} Stats", icon_url=ctx.bot.user.avatar_url)
    embed.set_footer(text=f"As of~~")
    await ctx.send(embed=embed)

  @commands.command(description='Get the id of a user!',aliases=['memid','getmemberidof', 'memberid'])
  async def getuserid(self, ctx, member : Optional[discord.Member]=None):
    if member is None:
      await ctx.send(f"Your user id is `{ctx.author.id}`")
    else:
      await ctx.send(member.name+f"'s user id is  `{str(member.id)}`")

  @commands.command(description="get this server's id!", aliases=['serverid', 'serid'])
  @commands.guild_only()
  async def getserverid(self, ctx):
    await ctx.send(f"This server (which is {ctx.message.guild.name})'s id is `{str(ctx.message.guild.id)}`")

  @commands.command(description="Get the profile picture of a specific member!",aliases=['avatar', 'getpfpof', 'pfp'])
  @commands.guild_only()
  async def getpfp(self, ctx, member : Optional[discord.Member]=None):
    if member is None:
      member=ctx.author

    embed = discord.Embed(colour = member.colour)
    embed.add_field(name='Image link', value=f'[Click mee]({member.avatar_url})')
    embed.set_author(name=f'Avatar of {member}')
    embed.set_image(url=member.avatar_url)
    await ctx.send(embed=embed)
    
  @commands.command(description="Get info about a member!",aliases=['whothefis', 'memberinfo', 'userinfo'])
  @commands.guild_only()
  async def whois(self, ctx, member : Optional[discord.Member]=None):
    if member is None:
      member=ctx.author
      
    embed = discord.Embed(colour = member.colour, timestamp = ctx.message.created_at)

    embed.set_author(name=f'User Info - {member}')
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")

    embed.add_field(name="Discord Name, Nickname", value=member.name +", "+ member.display_name, inline=True)
    embed.add_field(name="Discord ID", value=member.id, inline=True)

    embed.add_field(name="Account Created", value=member.created_at.strftime("%A, %x at %I:%M %p"), inline = False)
    embed.add_field(name="Member Joined", value=member.joined_at.strftime("%A, %x at %I:%M %p"), inline=False)

    await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(InfoCommands(bot))