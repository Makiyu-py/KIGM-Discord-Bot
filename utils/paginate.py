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

import asyncio

import discord
from dpymenus import PaginatedMenu


class dpyPaginate:
  def __init__(self, **kwags):
    try:
      self.pl=kwags['PageList']
    except KeyError:
      raise KeyError('Expected PageList.')

    self.allowms = kwags.get('multi_session', True)
    self.timeout=kwags.get('timeout', 20)
    self.c_button=kwags.get('cancel_button', True)
    self.c_page=kwags.get('cancel_page', None)
    self.destination=kwags.get('destination', None)


  async def menustart(self, ctx):
    
    # Checking if list is actually a list or if the length of the of it is only 1
    if type(self.pl) != list or len(self.pl) == 1:
      # if it passes, just send it :P
      await ctx.send(self.pl) if type(self.pl) != list else await ctx.send(self.pl[0])
      return

    menu = (PaginatedMenu(ctx))
    menu.add_pages(self.pl)
    if self.timeout:
      menu.set_timeout(self.timeout)
    if self.c_page:
      menu.set_cancel_page(self.c_page)
    if len(self.pl) >= 3:
      menu.show_skip_buttons()
    if not self.c_button:
      menu.hide_cancel_button()
    if self.destination:
      menu.set_destination(self.destination)
    if self.allowms:
      menu.allow_multisession()
    await menu.open()
  