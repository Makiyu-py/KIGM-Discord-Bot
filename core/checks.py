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

import os

import dbl
from discord.ext import commands


# For the thing uh the @ decorator thing u
# put on top of the function, yea yea
def support_server_only():
    async def predicate(ctx):
        if ctx.guild.id == 770558935144726528:
            return True

        await ctx.send(
            "This command is exclusively **for the support server only.**\nSo here's link of the support server then!  **https://discord.gg/jz4WxkB **")
        return False

    return commands.check(predicate)


def cmd_has_blacklist():
    async def get_bl(ctx):
        cmdbl_data = await ctx.bot.bl.find(ctx.command.name)
        if 'Blacklisted' in cmdbl_data:
            if ctx.author.id in cmdbl_data['Blacklisted']:
                await ctx.error("You are currently *blacklisted* from using this command.")
                return False

            else:
                return True

    return commands.check(get_bl)


def voters_only():
    async def check_voted(ctx):
        j = dbl.DBLClient(ctx.bot, os.environ.get("DBL_SECRET"))
        usr_vote = await j.get_user_vote(ctx.author.id)

        await j.close()  # idk I get annoyed sometimes with the warnings on the console

        if usr_vote:
            return True

        await ctx.send(
            "oops! It seems like this command is for **__voters only.__**\nIf you want to use this command just **vote me on top.gg!**\nVote link: **https://top.gg/bot/763626077292724264/vote **")
        return False

    return commands.check(check_voted)
