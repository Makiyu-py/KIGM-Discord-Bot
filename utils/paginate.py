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

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dpymenus import BaseMenu

from discord.abc import GuildChannel
from dpymenus import ButtonsError, PagesError, PaginatedMenu as BasePagination, SessionError


async def call_hook(instance: "BaseMenu", hook: str):
    if fn := getattr(instance, hook, None):
        await fn()


# I modified the `open` method because dpymenus
# auto-removes the user's reaction when the user
# adds a reaction, so my modification is to check
# if the bot has proper permissions before removing
# and clearing the reactions (I also formatted the
# code with the typical black and isort combo)

class PaginatedMenu(BasePagination):
    def __init__(self, ctx):
        super().__init__(ctx)

    async def open(self):
        try:
            self.show_command_message()
            if len(self.buttons_list) == 0:
                self.buttons(["⏮️", "◀️", "⏹️", "▶️", "⏭️"])

            self._validate_buttons()
            await super()._open()

        except (ButtonsError, PagesError, SessionError) as exc:
            print(exc.message)

        else:
            await self._add_buttons()

            # refresh our message content with the reactions added
            self.output = await self.destination.fetch_message(self.output.id)

            await call_hook(self, "_hook_after_open")

            while self.active:
                await call_hook(self, "_hook_before_update")
                self.input = await self._get_input()

                # this will be true when input handles a timeout event
                if (
                    (not self.output)
                    or (not self.active)
                    or (self.output and self.persist and not self.active)
                ):
                    return

                if (
                    self.output
                    and isinstance(self.output.channel, GuildChannel)
                    and self.ctx.me.guild_permissions.manage_messages
                ):
                    await self.output.remove_reaction(self.input, self.ctx.author)

                # this must come after removing reactions to prevent duplicate actions on bot remove
                await self._handle_transition()

            await self._safe_clear_reactions()
	
    async def _safe_clear_reactions(self):
        if self.output and isinstance(self.output.channel, GuildChannel) and self.ctx.me.guild_permissions.manage_messages:
            await self.output.clear_reactions()

class dpyPaginate:
    def __init__(self, **kwargs):
        try:
            self.pl = kwargs["page_list"]
        except KeyError:
            raise KeyError("Expected the page_list kwarg.")

        self.timeout = kwargs.get("timeout", 20)
        self.c_button = kwargs.get("cancel_button", True)
        self.c_page = kwargs.get("cancel_page", None)
        self.destination = kwargs.get("destination", None)

    async def menustart(self, ctx):

        # Checking if list is actually a list or if the length of the of it is only 1
        if not isinstance(self.pl, list):
            await ctx.send(self.pl)
            return

        if len(self.pl) == 1:
            await ctx.send(self.pl[0])
            return

        menu = PaginatedMenu(ctx)
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
        await menu.open()
