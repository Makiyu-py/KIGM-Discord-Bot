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

from typing import Optional

import discord
from discord.ext import commands
from discord.ext.commands import cooldown


class Economy(commands.Cog, name=":euro: Economy System"):
    def __init__(self, bot):
        self.bot = bot
        self.ecofunc = self.bot.get_cog("Asyncfuncs")

    # ------------------------------------Doing Stuff to the Balance--------------------------------------------

    @commands.command(description="Check your balance!", aliases=["bal"])
    async def balance(self, ctx, user: Optional[discord.Member] = None):
        """
        if user == None:
          user = ctx.author

        await self.ecofunc.open_account(user)

        users = await self.ecofunc.get_user_data(user)
        purse_amt = users["Purse"]
        bank_amt = users["Bank"]

        embed = discord.Embed(
        title=":european_post_office: The Official Bank of the KIGM Bot :european_post_office:",
        description=f"Balance of {user}:",
        color=0xf8f8ff
        )

        embed.add_field(name=":purse: Purse Bal: ", value=f'{str(purse_amt)} Nitro Shards <a:boost_evolve:769448461824163870>')
        embed.add_field(name=":Bank: Bank Bal: ", value=f'{str(bank_amt)} Nitro Shards <a:boost_evolve:769448461824163870>')

        await ctx.send(embed=embed)
        """
        await ctx.send(
            "**The Devs Are Currently Improving The Economy!**\nSorry for the inconvinience!"
        )

    @commands.command(aliases=["wdrw"], description="Withdraw your shards to the Bank!")
    async def withdraw(self, ctx, amount=None):
        """

        await self.ecofunc.get_user_data(ctx.author)

        if amount == None:
          await ctx.send("**ERROR!**\npls give the specified amount next time pls (like this: `withdraw <amount>`)")
          return

        if amount == 'all':
          users = await self.ecofunc.get_bank_data()
          amount = int(users["Bank"])

        if amount == 'half':
          users = await self.ecofunc.get_bank_data()
          amount = int(users["Bank"]) / 2

        amount=int(amount)
        bal = await self.ecofunc.update_eco(ctx.author)


        if amount > bal[1]:
          await ctx.send("**YOU DON'T HAVE THAT MUCH MONEY XD POOOOOOORRRR <:kekw:773125072637788160>**")
          return

        if amount < 0:
          await ctx.send("<a:weeeee:771309755427061770> Number must be positive kiddo <a:weeeee:771309755427061770>")
          return

        await self.ecofunc.update_eco(ctx.author, amount)
        await self.ecofunc.update_eco(ctx.author, -1*amount, "Bank")

        await ctx.send(f"**You have successfully withdrew {amount} Nitro Shards <a:boost_evolve:769448461824163870> from the Official Bank of the KIGM Bot to your purse! :Bank:**")
        """
        await ctx.send(
            "**The Devs Are Currently Improving The Economy!**\nSorry for the inconvinience!"
        )

    @commands.command(aliases=["dep"], description="Deposit your shards to the Bank!")
    async def deposit(self, ctx, amount=None):
        # await self.ecofunc.open_account(ctx.author)

        # if amount == None:
        #   await ctx.send("**ERROR!**\npls give the specified amount next time pls (like this: `withdraw <amount>`)")
        #   return

        # bal = await self.ecofunc.update_eco(ctx.author)

        # if amount == 'all':
        #   users = await self.ecofunc.get_bank_data()
        #   amount = int(users["Purse"])

        # if amount == 'half':
        #   users = await self.ecofunc.get_bank_data()
        #   amount = int(users["Purse"]) / 2

        # amount=int(amount)

        # if amount > bal[0]:
        #   await ctx.send("**YOU DON'T HAVE THAT MUCH MONEY XD POOOOOOORRRR <:kekw:773125072637788160>**")
        #   return

        # if amount < 0:
        #   await ctx.send("<a:weeeee:771309755427061770> Number must be positive kiddo <a:weeeee:771309755427061770>")
        #   return

        # await self.ecofunc.update_eco(ctx.author, -1*amount)
        # await self.ecofunc.update_eco(ctx.author, amount, "Bank")

        # await ctx.send(f"**You have successfully deposited {amount} Nitro Shards <a:boost_evolve:769448461824163870> to the Official Bank of the KIGM Bot! :bank:**")
        await ctx.send(
            "**The Devs Are Currently Improving The Economy!**\nSorry for the inconvinience!"
        )

        # -----------------------------------Earning/Losing Shards--------------------------------------------------

    @commands.command(aliases=["give"], description="Give someone your money!")
    @commands.guild_only()
    async def send_money(self, ctx, member: discord.Member = None, amount=None):
        # await self.ecofunc.open_account(ctx.author)

        # if member == None:
        #   await ctx.send("**ERROR** \nNo member provided")
        #   return

        # await self.ecofunc.open_account(member)

        # if amount == None:
        #   await ctx.send("**ERROR!**\npls give the specified amount next time pls (like this: `withdraw <amount>`)")
        #   return

        # amount=int(amount)

        # if amount <= 24:
        #   await ctx.send("**ERROR!**\n**To avoid spam, I made the minimum Nitro Shard donation to __25__.**\nI hope u understand :)")
        #   return

        # bal = await self.ecofunc.update_eco(ctx.author)

        # if amount > bal[0]:
        #   await ctx.send("**YOU DON'T HAVE THAT MUCH MONEY XD POOOOOOORRRR <:kekw:773125072637788160>**")
        #   return

        # if amount < 0:
        #   await ctx.send("<a:weeeee:771309755427061770> Number must be positive kiddo <a:weeeee:771309755427061770>")
        #   return

        # await self.ecofunc.update_eco(ctx.author, -1*amount)
        # await self.ecofunc.update_eco(member, amount)

        # await ctx.send(f"**You have successfully gave {amount} Nitro Shards to {member.mention}! <a:boost_evolve:769448461824163870>**")

        # await member.send(f"**{ctx.author}** | `ID: {ctx.author.id}` has given you **{amount} Nitro Shards! <a:boost_evolve:769448461824163870>**")
        await ctx.send(
            "**The Devs Are Currently Improving The Economy!**\nSorry for the inconvinience!"
        )

    @commands.command(
        description=":detective: *theif boi* :detective:", aliases=["steal", "loot"]
    )
    @commands.guild_only()
    @cooldown(1, 3600, commands.BucketType.user)
    async def rob(self, ctx, member: discord.Member = None):
        # await self.ecofunc.open_account(ctx.author)

        # if member == None:
        #   await ctx.send("**ERROR** \nNo member provided to rob lmao")
        #   ctx.command.reset_cooldown(ctx)
        #   return

        # await self.ecofunc.open_account(member)

        # bal = await self.ecofunc.update_eco(member)

        # if bal[0] < 40:
        #   await ctx.send("**Member doesn't have that much money to get robbed!** Poor guy...\n(person must have at least 40 Nitro Shards <a:boost_evolve:769448461824163870> in order to be robbable.)")
        #   ctx.command.reset_cooldown(ctx)
        #   return

        # if bal[0] < 1500:
        #   eorl = random.randint(10, bal[0]) * 0.8
        # else:
        #   eorl = random.randint(10, bal[0]) / 6

        # eorl = int(eorl)
        # chance = random.randint(1, 9)

        # if chance == 8 or chance == 9:
        #   await self.ecofunc.update_eco(ctx.author, -1*eorl)

        #   earnings_of_member = eorl / 2
        #   earnings_of_member= int(earnings_of_member)

        #   await self.ecofunc.update_eco(member, earnings_of_member)

        #   embed = discord.Embed(title="**ROB FAILED!**", description=f"You attempted to pickpocket {member.mention} but instead, stole {earnings_of_member} Nitro Shards <a:boost_evolve:769448461824163870> from you!",color = discord.Color.red())

        #   embed.set_footer(text=f"Dumb Thief: {ctx.author} | Plot Twister: {member}", icon_url=ctx.author.avatar_url)

        #   await ctx.send(embed=embed)

        # else:
        #   await self.ecofunc.update_eco(ctx.author, eorl)
        #   await self.ecofunc.update_eco(member, -1*eorl)

        #   embed = discord.Embed(title="**ROB SUCCESSFUL!**", description=f"You pickpocketed {member.mention} and stole {eorl} Nitro Shards! <a:boost_evolve:769448461824163870>",color = discord.Color.green())

        #   embed.set_footer(text=f"Thief: {ctx.author} | Poor Victim: {member}", icon_url=ctx.author.avatar_url)

        #   await ctx.send(embed=embed)
        await ctx.send(
            "**The Devs Are Currently Improving The Economy!**\nSorry for the inconvinience!"
        )

    @commands.command(description="Get your daily shards!")
    @cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        # await self.ecofunc.open_account(ctx.author)

        # await self.ecofunc.update_eco(ctx.author, 200)

        # embed = discord.Embed(title="Here's your daily shards!", description='**200 Nitro Shards <a:boost_evolve:769448461824163870>** have been now placed into your purse!', color=0xfcb2c5)
        # embed.set_footer(text="You may get your daily again in 24 HOURS!")

        # await ctx.send(embed=embed)
        await ctx.send(
            "**The Devs Are Currently Improving The Economy!**\nSorry for the inconvinience!"
        )

    @commands.group(
        name="gamble",
        description="Bet/Gamble your shards for more satisfaction!",
        aliases=["bet"],
    )
    @commands.guild_only()
    async def game_eco(self, ctx):
        # if ctx.invoked_subcommand is None:
        #   embed = discord.Embed(
        #     title='**Games where you can gamble your shards on!**',
        #     color=discord.Color.red()
        #     )

        #   embed.add_field(name="**Flip the Coin!**", value='`gamble coinflip <bet_size>`')
        #   embed.add_field(name="**Roll the Dice!**", value='`gamble dice <bet_size>`')

        #   await ctx.send(embed=embed)
        await ctx.send(
            "**The Devs Are Currently Improving The Economy!**\nSorry for the inconvinience!"
        )

    @game_eco.command(
        description="Gamble yourself 50/50 with a coin!",
        aliases=["flipcoin", "flipthecoin"],
    )
    @commands.guild_only()
    @cooldown(1, 600, commands.BucketType.user)
    async def coinflip(self, ctx, bet: int = None):
        # await self.ecofunc.open_account(ctx.author)

        # if bet is None:
        #   await ctx.send("Where's your bet? lol")
        #   ctx.command.reset_cooldown(ctx)
        #   return

        # bal = await self.ecofunc.update_eco(ctx.author)

        # if bet > bal[0]:
        #   await ctx.send("You don't have that much Nitro Shards on your Bank like that lol")
        #   ctx.command.reset_cooldown(ctx)
        #   return

        # if bet < 30:
        #   await ctx.send("Your bet must be higher than **30 Shards!**")
        #   ctx.command.reset_cooldown(ctx)
        #   return

        # await ctx.send("**The coin has flipped!**\nPick a side! Heads or tails?")

        # coin = ('head', 'tail')

        # flip = random.choice(coin)
        # try:

        #   msg = await self.bot.wait_for("message", timeout=8, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)

        #   msg = str(msg.content.lower())

        #   if len(msg) < 3:
        #     await ctx.send("Your guess must be heads/tails!")
        #     ctx.command.reset_cooldown(ctx)
        #     return

        #   msgSplit = []

        #   for letter in msg:
        #     msgSplit.append(letter)

        #   msgWord = f"{msgSplit[0]}{msgSplit[1]}{msgSplit[2]}{msgSplit[3]}"

        #   if msgWord in coin:
        #     if msgWord == flip:
        #       await ctx.send("You won! You get 150% of your Nitro Shards <a:boost_evolve:769448461824163870> back!")

        #       await self.ecofunc.update_eco(ctx.author, int(bet * 1.5))

        #     elif msgWord != flip:
        #       await ctx.send(f"You lost! It was actually the **{flip}s side!**\nRip ur {bet} Nitro Shards")

        #       await self.ecofunc.update_eco(ctx.author, -1*int(bet))

        #   else:
        #     await ctx.send("**ERROR!**\n'Side' not found. Please try again.")
        #     ctx.command.reset_cooldown(ctx)

        # except asyncio.TimeoutError:
        #   await ctx.send("*Command cancelled cuz u sloww*")
        await ctx.send(
            "**The Devs Are Currently Improving The Economy!**\nSorry for the inconvinience!"
        )

    @game_eco.command(
        description="Guess the dice! (dev running out of ideas so just use the suggest command when u have a cool one)",
        aliases=["guessthedice"],
    )
    @commands.guild_only()
    @cooldown(1, 600, commands.BucketType.user)
    async def dice(self, ctx, bet: int = None):
        # await self.ecofunc.open_account(ctx.author)

        # die1 = random.randint(1, 6)
        # die2 = random.randint(1, 6)

        # if bet is None:
        #   await ctx.send("**You don't have a bet!**\nCome back when u do have ;)")
        #   ctx.command.reset_cooldown(ctx)
        #   return

        # bal = await self.ecofunc.update_eco(ctx.author)

        # if bet > bal[0]:
        #   await ctx.send("You don't have that much Nitro Shards on your Bank like that lol")
        #   ctx.command.reset_cooldown(ctx)
        #   return

        # if bet < 30:
        #   await ctx.send("Your bet must be higher than **30 Shards!**")
        #   ctx.command.reset_cooldown(ctx)
        #   return

        # await ctx.send("What do you want to guess?\n\n*1. Guess both of the numbers of each die (gives 200% of your shards back if guessed correctly)*\n*2. Is it a double, or not? (only gives 120% of your money back if guessed correctly)*")

        # try:

        #   msg = await self.bot.wait_for("message", timeout=10, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)

        #   msg = msg.content

        #   if msg == "1" or msg == "1.":
        #     await ctx.send("The dice is about to be rolled! What is your guess? (separate with spaces plss)")
        #     try:

        #       guess_msg = await self.bot.wait_for("message", timeout=20, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)

        #       guess_list = guess_msg.content.split(" ")

        #       if guess_list[0] not in "123456" or guess_list[1] not in "123456":
        #         await ctx.send("Your guess must be a number lower than 7!")
        #         ctx.command.reset_cooldown(ctx)
        #         return

        #       if die1 == int(guess_list[0]) and die2 == int(guess_list[1]) or die1 == int(guess_list[1]) and die2 == int(guess_list[0]):
        #         dice_guess_profit = bet * 2
        #         await ctx.send("You are...")
        #         await asyncio.sleep(.5)
        #         await ctx.send(f"**Correct!** \nThe dice numbers are `{die1}` and `{die2}`!\n**Here's your prize money of :tada: {dice_guess_profit} Nitro Shards! <a:boost_evolve:769448461824163870> :tada:**")

        #         await self.ecofunc.update_eco(ctx.author, int(dice_guess_profit))

        #       elif die1 != int(guess_list[0]) and die2 != int(guess_list[1]) or die1 != int(guess_list[1]) and die2 != int(guess_list[0]):
        #         await ctx.send("You are...")
        #         await asyncio.sleep(.5)
        #         await ctx.send(f"Incorrect! \n**The numbers were {die1} and {die2}!**\nWelp, all of your shards have to go somewhere, Am I right?")

        #         await self.ecofunc.update_eco(ctx.author, -1*int(bet))

        #     except asyncio.TimeoutError:
        #       await ctx.send("Slow. Just... cmon")
        #       ctx.command.reset_cooldown(ctx)

        #   elif msg == "2" or msg == "2.":
        #     await ctx.send("**The dice has rolled!** What do you think it is... double or no? [d/n]")

        #     try:

        #       msg = await self.bot.wait_for("message", timeout=15, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)

        #       if msg.content.lower() in ['double', 'd', 'yes', 'a double'] and die1 == die2 or msg.content.lower() in ['not double', 'not a double', 'no', 'n', 'false'] and die1 != die2:
        #         await self.ecofunc.update_eco(ctx.author, -1*int(bet))

        #         bet_double_profit = bet * 1.2
        #         await ctx.send("Guess what...")
        #         await asyncio.sleep(.5)
        #         await ctx.send(f"You won! \n{die1} and {die2}!\nHere's the shards that I promised you to keep.")

        #         await self.ecofunc.update_eco(ctx.author, int(bet_double_profit))

        #       elif msg.content.lower() in ['not double', 'not a double', 'no', 'n', 'false'] and die1 == die2 or msg.content.lower() in ['double', 'd', 'yes', 'a double'] and die1 != die2:
        #         await ctx.send("Guess what...")
        #         await asyncio.sleep(.5)
        #         await ctx.send(f"You lost! \n**:skull: RIP YOUR {bet} HARD-EARNED SHARDS :skull:**\nDice was `{die1}` and `{die2}`!")

        #         await self.ecofunc.update_eco(ctx.author, -1*int(bet))

        #     except asyncio.TimeoutError:
        #       await ctx.send("slow. cancelled lol")
        #       ctx.command.reset_cooldown(ctx)

        #   else:
        #     await ctx.send("DON'T YOU KNOW THE DIFFERENCE BETWEEN A LETTER AND A NUMBER BRUHHH")
        #     ctx.command.reset_cooldown(ctx)

        # except asyncio.TimeoutError:
        #   await ctx.send("Bruhh just pick a numberrrr cancelled.")
        #   ctx.command.reset_cooldown(ctx)
        await ctx.send(
            "**The Devs Are Currently Improving The Economy!**\nSorry for the inconvinience!"
        )

    @commands.command(
        description="Work hard to get that juicy shards! <a:boost_evolve:769448461824163870>"
    )
    @commands.guild_only()
    @cooldown(1, 1800, commands.BucketType.user)
    async def work(self, ctx):
        # give_money = random.randint(15, 30)
        # work_list = [
        #   f"You made a discord bot and made **{str(give_money)} Nitro Shards!** <a:boost_evolve:769448461824163870>",
        #   f"You played :person_bouncing_ball: basketball :person_bouncing_ball: for a team and won! They gave you **{str(give_money)} Nitro Shards!** <a:boost_evolve:769448461824163870>",
        #   f"You worked for a nursing home :couch: for a day and made **{str(give_money)} Nitro Shards!** <a:boost_evolve:769448461824163870>",
        #   f"You worked as a car washer :blue_car: for a few hours and made **{str(give_money)} Nitro Shards!** <a:boost_evolve:769448461824163870>"
        # ]

        # work_msg = random.choice(work_list)

        # await self.ecofunc.open_account(ctx.author)

        # await self.ecofunc.update_eco(ctx.author, -int(give_money))

        # embed = discord.Embed(description=work_msg, color=0xffa500)

        # embed.set_author(name=f"Hardwork Done by {ctx.author}", icon_url=ctx.author.avatar_url)

        # await ctx.send(embed=embed)
        await ctx.send(
            "**The Devs Are Currently Improving The Economy!**\nSorry for the inconvinience!"
        )


def setup(bot):
    bot.add_cog(Economy(bot))
