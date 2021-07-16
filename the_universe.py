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


def convert_list_to_string(org_list, seperator=" "):
    """Convert list to string, by joining all item in list with given separator.
    Returns the concatenated string"""
    return seperator.join(org_list)


def convert(time):
    pos = ["s", "m", "h", "d", "w"]

    time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24, "w": 3600 * 24 * 7}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2

    return val * time_dict[unit]


def syntax(command, show_aliases_on_syntax: bool = True):
    cmd_and_aliases = (
        "|".join([str(command), *command.aliases])
        if show_aliases_on_syntax
        else str(command)
    )
    params = []

    for key, value in command.params.items():
        if key not in ("self", "ctx"):
            key = key.replace("_", " ")
            params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

    params = " ".join(params) if params else ""

    return f"`{cmd_and_aliases} {params}`"
