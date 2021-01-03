from replit import db
import discord
import random
import json
from typing import Optional
from the_universe import syntax
from the_universe import server_prefix
from discord import Embed, Profile
import math
from aiohttp import request
import dbl
import os
import asyncio
from discord import PublicUserFlags
import re
import platform


from discord.ext.commands import Cog, command
from discord.utils import get
from discord.ext import commands

DBLtoken = os.environ.get("DBL_SECRET")

class Tests(commands.Cog, command_attrs=dict(hidden=True)):

  def __init__(self, bot):
    self.bot = bot
    self.token = DBLtoken
    self.dblpy = dbl.DBLClient(self.bot, self.token)

    
  @commands.command()
  async def vote_test(self, ctx):
    userid = int(ctx.author.id)
    votestatus = await self.dblpy.get_user_vote(763626077292724264, userid)
    if votestatus == True:
      await ctx.send("hi")
    else:
      await ctx.send("ur not voted bruh")

  @commands.command()
  @commands.has_permissions(manage_messages = True)
  @commands.guild_only()
  async def createtag(self, ctx, tag_name):
    await ctx.send("What would be the message when the tag has been used?\nI'll give you **180 seconds.**")

    try:
      tagmsg = await self.bot.wait_for("message", timeout=180, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)

      setupmsg = await ctx.send("Setting things up")
      await asyncio.sleep(.7)
      await setupmsg.edit(content="Setting things up.")
      await asyncio.sleep(.7)
      await setupmsg.edit(content="Setting things up..")

      origKEY = ""
      for k, v in db.keys(), db.values():
        origKEY += {f'{k}' : f'{v},'}
      else:
        origKEY += {f"{tag_name}" : f"{tagmsg.content},"}
        print(origKEY)
        db[str(ctx.guild.id)] = origKEY
        

      await asyncio.sleep(.65)
      await setupmsg.edit(content="Setting things up...")
      await ctx.send("**Set-up Completed!**\nHere's what your tag would look like:")
      await ctx.send(f"**Command:** `{server_prefix(ctx.guild.id)}tag {tag_name}`\n\n{tagmsg.content}")

    except asyncio.TimeoutError:
      await ctx.send("**Times up! :stopwatch:**\nUse this command again when you have your tag message set-up!")

  @commands.command()
  @commands.guild_only()
  async def alltags(self, ctx):
    if str(ctx.guild.id) in db:
      tagmsg = ""
      for key in db[str(ctx.guild.id)]:
        tagmsg += f"`{key}` "

      else:
        embed = discord.Embed(title=f"All Tags in {ctx.guild.name}", description=tagmsg, color=0xf8f8ff)

        embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    else:
      await ctx.send("This Server Hasn't Set-up Any Tags Yet!")

  @commands.command()
  @commands.guild_only()
  async def tag(self, ctx, *, tag_name):
    if str(ctx.guild.id) in db:
      if tag_name in db[str(ctx.guild.id)]:
        await ctx.send(db[str(ctx.guild.id)][tag_name])

      else:
        await ctx.send("**ERROR!**\nTag Name does not exist.")

    else:
      await ctx.send("**ERROR!**\nTag Name does not exist.")

  @commands.command()
  @commands.is_owner()
  async def guess_the_number(self, ctx):
    await ctx.send("**WELCOME TO GUESS THE NUMBER!**\nThe point of this game is to guess a generated number for only a specified amount of messages before you lose.\nModes:   [1/2/3]\n:green_book: (1) *Easy*: Guess between 1 and 15 with 7 chances\n:orange_book: (2) *Intermediate*: Guess between 1 and 35 with 12 chances\n:closed_book: (3) *Hard*: Guess between 1 and 60 with 18 chances")

    try:
      mode = await self.bot.wait_for("message", timeout=10, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)

      global chances

      if mode == '1':
        await ctx.send("**Game started!**\nMode: Easy")
        easy_guess = random.randint(1, 15)
        await ctx.send("**I have now generated a number!**\nWhat is your guess?")
        chances = 7
      elif mode == 2:
        await ctx.send("**Game started!**\nMode: Intermediate")
        easy_guess = random.randint(1, 35)
        await ctx.send("**I have now generated a number!**\nWhat is your guess?")
        chances = 12
      elif mode == 3:
        await ctx.send("**Game started!**\nMode: Hard")
        easy_guess = random.randint(1, 60)
        await ctx.send("**I have now generated a number!**\nWhat is your guess?")
        chances = 18

      for i in range(chances):
        guess = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel)

        guess = int(guess)

        while guess != easy_guess:
          chance_tip = random.randint(1, 2)
          if chance_tip == 2:
            if guess > easy_guess:
              await ctx.send("Wrong guess! Tip: **Go LOWER ;)**")
            if guess < easy_guess:
              await ctx.send("Wrong guess! Tip: **Go HIGHER ;)**")

        if guess == easy_guess:
          await ctx.send("Congrats! You won!")

    except asyncio.TimeoutError:
      await ctx.send("Can't you pick a number?")


  @commands.command(aliases=['hack'])
  @commands.is_owner()
  async def hackerman(self, ctx):
    msg=await ctx.send("Connecting to the hackk server...")
    await asyncio.sleep(1)
    await msg.edit(content="Now in the Server.")
    await asyncio.sleep(1)
    await msg.edit(content="Now.")
    await asyncio.sleep(.8)
    await msg.edit(content="Now..")
    await asyncio.sleep(.8)
    await msg.edit(content="Now...")
    await asyncio.sleep(.8)
    await msg.edit(content="GET RICKROLLEDDDD\nhttps://tenor.com/view/dance-moves-dancing-singer-groovy-gif-17029825")

    for flag in ctx.author.public_flags.all():
      checklist_flags = "User Checklist:\n\n"
      checklist_flags += f":white_check_mark: {str(flag).replace('UserFlags.', '').replace('_', ' ')}\n"
      await ctx.send(checklist_flags)

def setup(bot):
  bot.add_cog(Tests(bot))