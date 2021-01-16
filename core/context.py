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


class CustomContext(commands.Context):

  async def error(self, errormsg: str, **kwargs):
    return await self.reply(f'**ERROR!**\n{errormsg}', **kwargs)

  async def reply(self, message: str, **kwargs):
    try:
      return await commands.Context.reply(self, message, **kwargs)
    except commands.MessageNotFound:
      return await commands.Context.send(message, **kwargs)
