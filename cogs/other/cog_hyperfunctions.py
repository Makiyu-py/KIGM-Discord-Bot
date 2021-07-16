"""
This file is part of KIGM-Discord-Bot.

KIGM-Discord-Bot is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

KIGM-Discord-Bot is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with KIGM-Discord-Bot.  If not, see <https://www.gnu.org/licenses/>.
"""

from discord.ext import commands


class Asyncfuncs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_bank_data(self):
        return await self.bot.ecod.get_all()

    async def get_user_data(self, user):
        return await self.bot.ecod.find("BANK ID - " + user.id)

    async def open_account(self, user):

        # if await self.get_user_data(user):
        #   return False

        # else:
        #   await user.send("Making a bank account for you...")
        #   await self.bot.ecod.insert({"_id" : "BANK ID - " + user.id, "Bank" : 0, "Purse" : 0, "Net Worth" : 0})
        #   await user.send("I have **__successfully__** made a bank account for you!\n**Thank you for your service at The Official Bank of the KIGM Bot!** :wave:")

        # return True
        pass

    async def update_eco(self, user, change=0, mode="Purse"):

        mode = [mode, "Net Worth"]
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
