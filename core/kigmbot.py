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

from discord.ext import commands
from datetime import datetime
from termcolor import colored
from danbot_api import DanBotClient
import motor.motor_asyncio
import asyncpraw
import random
import os

from utils.mongo import DBShortCuts
from .context import CustomContext


class KIGM(commands.AutoShardedBot):
    
    def __init__(self, *args, **kwargs):
        super(KIGM, self).__init__(*args, **kwargs)
        
        self.replied_to = 0
        self.owner_id = 526616688091987968
        self.version = 'V 1.4.2'
        self.launch_time = datetime.utcnow()  # for stats cmd for getting bot's uptime

        # YouTube is hurting my English soo
        self.main_color = 0xf8f8ff
        self.main_colour = 0xf8f8ff

        self.dbhcli = DanBotClient(self, os.environ.get("DBH_API_SECRET"), True)
        
        
        self.reddit = asyncpraw.Reddit(client_id=os.environ.get("REDDIT_ID"),
                                  client_secret=os.environ.get("REDDIT_ID_SECRET"),
                                  user_agent="KIGM_DISCORD_BOT by u/-Makiyu-")
        self.meme_subs = ("memes", "funny", "dankmemes", "ComedyCemetery", "starterpacks", "terriblefacebookmemes")
        self.av_memes = []
        
        # mongoDB action
        self.mongo = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("MONGODB_SECRET"))

        # Server Configuration Data
        self.db = self.mongo["Guild"]

        self.config = DBShortCuts(self.db, "Config")

        # Main bot's data
        self.botdb = self.mongo["BotData"]

        self.cmd_stats = DBShortCuts(self.botdb, "CommandStats")
        self.bl = DBShortCuts(self.botdb, "Blacklisted")

        # User data
        self.udb = self.mongo["User"]

        self.userconfig = DBShortCuts(self.udb, "Config")
        self.ecod = DBShortCuts(self.udb, "Economy")
        
	
    async def renew_memes(self):
        if len(self.av_memes) <= 5 and self.reddit:
            _meme_subs = random.shuffle(self.meme_subs)
            for i in range(2):
                sub_obj = await self.reddit.subreddit(_meme_subs[i])
                async for submission in sub_obj.top("day"):
                    if len(self.av_memes) >= 60:
                        return
                    if not submission in self.av_memes and not submission.over_18 and not submission.is_self \
                    and not submission.stickied and not submission.spoiler and submission.score > 100:
                        self.av_memes.append(submission)
    

    def load_cogs(self):
        
        # Loads cogs from the cogs/comms directory
        print(colored("Loading all command cogs...", 'grey', 'on_green'))
        for filename in os.listdir('cogs/comms'):
            if filename.endswith('.py'):
                self.load_extension(f'cogs.comms.{filename[:-3]}')
                print(colored("------------------------------------------", 'magenta'))
                print(colored(f"The {filename} cog has now been loaded!", 'magenta'))
        print(colored("------------------------------------------", 'magenta'))

        # Loads cogs from the cogs/other directory
        print(colored("Now Loading all events/shortcut cogs...", 'grey', 'on_green'))
        for filename in os.listdir('cogs/other'):
            if filename.endswith('.py'):
                self.load_extension(f'cogs.other.{filename[:-3]}')
                print(colored("------------------------------------------", 'yellow'))
                print(colored(f"The {filename} cog has now been loaded!", 'yellow'))
        print(colored("------------------------------------------", 'yellow'))
        self.load_extension('jishaku')
        
        
    async def get_context(self, message, *, cls=CustomContext):
        return await super().get_context(message, cls=cls)
