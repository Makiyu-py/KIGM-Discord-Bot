import random
from discord.ext import commands
import json

def get_prefix(client, message):
  if not message.guild:
    return commands.when_mentioned_or("&")(client, message)

  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)

  if str(message.guild.id) not in prefixes:
    return commands.when_mentioned_or("&")(client, message)

  prefix = prefixes[str(message.guild.id)]

  return commands.when_mentioned_or(prefix)(client, message)

def last_replace(s, old, new):
    li = s.rsplit(old, 1)
    return new.join(li)

def text_to_owo(text):
    smileys = [';;w;;', '^w^', '>w<', 'UwU', '(・`ω\´・)', '(´・ω・\`)']

    text = text.replace("&owo ", "")
    text = text.replace("&0w0 ", "")
    text = text.replace('L', 'W').replace('l', 'w')
    text = text.replace('R', 'W').replace('r', 'w')

    text = last_replace(text, '!', '! {}'.format(random.choice(smileys)))
    text = last_replace(text, '?', '? owo')
    text = last_replace(text, '.', '. {}'.format(random.choice(smileys)))

    vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']

    for v in vowels:
        if 'n{}'.format(v) in text:
            text = text.replace('n{}'.format(v), 'ny{}'.format(v))
        if 'N{}'.format(v) in text:
            text = text.replace('N{}'.format(v), 'N{}{}'.format('Y' if v.isupper() else 'y', v))

    return text

def british_accent(brsentence):

  brsentence=brsentence.replace("it was ", "it was quite")
  brsentence=brsentence.replace("friend", "mate").replace("pal", "mate").replace("buddy", "mate").replace("person", "mate").replace("man", "mate").replace("people", "mates")
  brsentence=brsentence.replace("standing", "stood")
  brsentence=brsentence.replace("sitting", "sat")
  brsentence = brsentence.replace("it was", "it was quite ")
  brsentence=brsentence.replace("o", "oh")
  brsentence=brsentence.replace("ee", "ea")
  brsentence = brsentence.replace("er ", "-a ").replace("er", "-a").replace("or ", "-a ").replace("or", "-a").replace("ar ", "-a ").replace("ar", "-a")
  brsentence = brsentence.replace("a", "ah")

  return brsentence

def convert_list_to_string(org_list, seperator=' '):
    """ Convert list to string, by joining all item in list with given separator.
        Returns the concatenated string """
    return seperator.join(org_list)
