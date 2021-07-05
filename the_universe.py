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

import random


def ttoemoji(sentence):
    # Don't ask why it's hard-coded ...

    beei = [" 🇧", " 🅱️"]
    ow = [" 🇴", " ⭕", " 🅾️"]
    ehks = [" ❌", " ✖️", " 🇽"]

    sentence = sentence.replace("A", " 🅰️").replace("a", " 🅰️")
    sentence = sentence.replace("B", random.choice(beei)).replace(
        "b", random.choice(beei)
    )
    sentence = sentence.replace("C", " 🇨").replace("c", " 🇨")
    sentence = sentence.replace("D", " 🇩").replace("d", " 🇩")
    sentence = sentence.replace("E", " 🇪").replace("e", " 🇪")
    sentence = sentence.replace("F", " 🇫").replace("f", " 🇫")
    sentence = sentence.replace("G", " 🇬").replace("g", " 🇬")
    sentence = sentence.replace("H", " 🇭").replace("h", " 🇭")
    sentence = sentence.replace("I", " 🇮").replace("i", " ℹ️")
    sentence = sentence.replace("J", " 🇯").replace("j", " 🇯")
    sentence = sentence.replace("K", " 🇰").replace("k", " 🇰")
    sentence = sentence.replace("L", " 🇱").replace("l", " 🇱")
    sentence = sentence.replace("M", " 🇲").replace("m", " 🇲")
    sentence = sentence.replace("N", " 🇳").replace("n", " 🇳")
    sentence = sentence.replace("O", random.choice(ow)).replace("o", random.choice(ow))
    sentence = sentence.replace("P", " 🇵").replace("p", " 🇵")
    sentence = sentence.replace("Q", " 🇶").replace("q", " 🇶")
    sentence = sentence.replace("R", " 🇷").replace("r", " 🇷")
    sentence = sentence.replace("S", " 🇸").replace("s", " 🇸")
    sentence = sentence.replace("T", " 🇹").replace("t", " 🇹")
    sentence = sentence.replace("U", " 🇺").replace("u", " 🇺")
    sentence = sentence.replace("V", " 🇻").replace("v", " 🇻")
    sentence = sentence.replace("W", " 🇼").replace("w", " 🇼")
    sentence = sentence.replace("X", random.choice(ehks)).replace(
        "x", random.choice(ehks)
    )
    sentence = sentence.replace("Y", " 🇾").replace("y", " 🇾")
    sentence = sentence.replace("Z", " 🇿").replace("z", " 🇿")

    sentence = sentence.replace("1", " :one:")
    sentence = sentence.replace("2", " :two:")
    sentence = sentence.replace("3", " :three:")
    sentence = sentence.replace("4", " :four:")
    sentence = sentence.replace("5", " :five:")
    sentence = sentence.replace("6", " :six:")
    sentence = sentence.replace("7", " :seven:")
    sentence = sentence.replace("8", " :eight:")
    sentence = sentence.replace("9", " :nine:")
    sentence = sentence.replace("0", " :zero:")
    sentence = sentence.replace("#", " :hash:")

    question_marks = [" ❓", " ❔"]
    exclamation_marks = [" :exclamation:", " :grey_exclamation:"]

    sentence = sentence.replace("<=>", " ↔️").replace("<==>", " ↔️")
    sentence = sentence.replace("?", random.choice(question_marks))
    sentence = sentence.replace("!", random.choice(exclamation_marks))
    sentence = sentence.replace("*", " *️⃣")
    sentence = sentence.replace(" ", "  ")
    sentence = sentence.replace("=>", " ➡️")
    sentence = sentence.replace("<=", " ➡️")

    return sentence


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
