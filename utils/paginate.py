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

from dpymenus import PaginatedMenu


class dpyPaginate:
    def __init__(self, **kwags):
        try:
            self.pl = kwags["PageList"]
        except KeyError:
            raise KeyError("Expected PageList.")

        self.timeout = kwags.get("timeout", 20)
        self.c_button = kwags.get("cancel_button", True)
        self.c_page = kwags.get("cancel_page", None)
        self.destination = kwags.get("destination", None)

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
