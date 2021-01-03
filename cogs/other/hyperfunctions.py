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


    # if await self.get_user_data():
    #   return False
    
    # else:
    #   await user.send("Making a bank account for you...")
    #   await self.bot.ecod.insert({"_id" : "BANK ID - " + user.id, "Bank" : 0, "Purse" : 0, "Net Worth" : 0})
    #   await user.send("I have **__successfully__** made a bank account for you!\n**Thank you for your service at The Official Bank of the KIGM Bot!** :wave:")

    # return True
    pass

  async def update_eco(self, user,change=0,mode="Purse"):


    mode = [mode]
    mode += 'Net Worth'

    for item in mode:
      await self.bot.ecod.increment("BANK ID - " + user.id, change, item)

    # bal = None
    # return True


def setup(bot):
  bot.add_cog(Asyncfuncs(bot))