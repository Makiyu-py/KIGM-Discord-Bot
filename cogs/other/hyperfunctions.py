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

import discord
from discord.ext import commands


class Asyncfuncs(commands.Cog):
  def __init__(self, bot):
    self.bot = bot


  async def get_bank_data(self):
    return await self.bot.ecod.get_all()

  async def get_user_data(self, user):
    return await self.bot.ecod.get_document("BANK ID - " + user.id)

  async def open_account(self, user):


    # if await self.get_user_data(user):
    #   return False
    
    # else:
    #   await user.send("Making a bank account for you...")
    #   await self.bot.ecod.insert({"_id" : "BANK ID - " + user.id, "Bank" : 0, "Purse" : 0, "Net Worth" : 0})
    #   await user.send("I have **__successfully__** made a bank account for you!\n**Thank you for your service at The Official Bank of the KIGM Bot!** :wave:")

    # return True
    pass

  async def update_eco(self, user,change=0,mode="Purse"):


    mode = [mode]
    mode.append('Net Worth')

    for item in mode:
      await self.bot.ecod.increment("BANK ID - " + user.id, change, item)

    
    return await self.get_user_data(user)


  async def server_prefix(ctx, guild_id):
    datap = ctx.config.find(guild_id)

    try:
      serverpre = datap["Bot Prefix"]

    except KeyError or AttributeError:
      return "&"
      
    else:
      return serverpre

def setup(bot):
  bot.add_cog(Asyncfuncs(bot))