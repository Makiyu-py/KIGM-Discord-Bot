"""
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
"""

import random

from discord.ext import commands
from discord_slash import SlashCommand, SlashCommandOptionType, cog_ext
from discord_slash.utils import manage_commands


class SlashCommands(commands.Cog):
    def __init__(self, bot):
        if not hasattr(bot, "slash"):
            bot.slash = SlashCommand(bot, override_type=True, auto_register=True)
            self.bot = bot
            self.cmdschannel = self.bot.get_channel(770560162812657715)
            self.bot.slash.get_cog_commands(self)

    def cog_unload(self):
        self.bot.slash.get_cog_commands(self)

    @cog_ext.cog_slash(
        name="8ball",
        description="Let's talk about our fortune... through an 8ball!",
        options=[
            manage_commands.create_option(
                "question",
                "Your question for the magic 8ball!",
                SlashCommandOptionType.STRING,
                True,
            )
        ],
    )
    async def fortune8ball(self, ctx, question: str):

        question = question.lower()
        starts = ["is", "will", "does", "do", "did", "can", "are", "am"]
        Falseness = 0
        for startofquestion in starts:
            if not question.startswith(startofquestion):
                Falseness += 1

        if Falseness == len(starts):
            await ctx.send(
                3,
                content="Hm, it seems like your question is **not a yes/no-type of question**, pls try again. :)",
                hidden=True,
            )
            return

        answers = [
            # 6 yes
            # 6 no
            # 3 maybe
            # that's fair, right?
            "Oh that's a hard one.... probably?",
            "no. just, no",
            "obviously no lol",
            "uhhh yea?",
            "yes!!",
            "probably not tbh",
            "YEP",
            "Heck yea!",
            "honestly... *no*",
            "maybe? but i don't really know u decide on that",
            "ez **yes**",
            "maybe? yea, maybe",
            "lol no",
            f'well that\'s an obvious *{random.choice(["yes", "no"])}* right there',
        ]
        da_answer = random.choice(answers)

        await ctx.send(content=":8ball: " + da_answer)


def setup(bot):
    bot.add_cog(SlashCommands(bot))
