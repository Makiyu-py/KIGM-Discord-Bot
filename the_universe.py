import random
from discord.ext import commands
import json

def get_prefix(client, message):
  if not message.guild:
    return commands.when_mentioned_or("&")(client, message)

  with open("databases/Settings/prefixes.json", "r") as f:
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

def ttoemoji(sentence):

  # Don't ask why it's hard-coded ...

  beei = [' 🇧',' 🅱️']
  ow = [' 🇴',' ⭕',' 🅾️']
  ehks = [' ❌', ' ✖️', ' 🇽']

  sentence=sentence.replace("A", " 🅰️").replace("a"," 🅰️")
  sentence=sentence.replace("B", random.choice(beei)).replace("b",random.choice(beei))
  sentence=sentence.replace("C", " 🇨").replace("c"," 🇨")
  sentence=sentence.replace("D", " 🇩").replace("d"," 🇩")
  sentence=sentence.replace("E", " 🇪").replace("e"," 🇪")
  sentence=sentence.replace("F", " 🇫").replace("f"," 🇫")
  sentence=sentence.replace("G", " 🇬").replace("g"," 🇬")
  sentence=sentence.replace("H", " 🇭").replace("h"," 🇭")
  sentence=sentence.replace("I", " 🇮").replace("i"," ℹ️")
  sentence=sentence.replace("J", " 🇯").replace("j"," 🇯")
  sentence=sentence.replace("K", " 🇰").replace("k"," 🇰")
  sentence=sentence.replace("L", " 🇱").replace("l"," 🇱")
  sentence=sentence.replace("M", " 🇲").replace("m"," 🇲")
  sentence=sentence.replace("N", " 🇳").replace("n"," 🇳")
  sentence=sentence.replace("O", random.choice(ow)).replace("o",random.choice(ow))
  sentence=sentence.replace("P", " 🇵").replace("p"," 🇵")
  sentence=sentence.replace("Q", " 🇶").replace("q"," 🇶")
  sentence=sentence.replace("R", " 🇷").replace("r"," 🇷")
  sentence=sentence.replace("S", " 🇸").replace("s"," 🇸")
  sentence=sentence.replace("T", " 🇹").replace("t"," 🇹")
  sentence=sentence.replace("U", " 🇺").replace("u"," 🇺")
  sentence=sentence.replace("V", " 🇻").replace("v"," 🇻")
  sentence=sentence.replace("W", " 🇼").replace("w"," 🇼")
  sentence=sentence.replace("X", random.choice(ehks)).replace("x",random.choice(ehks))
  sentence=sentence.replace("Y", " 🇾").replace("y"," 🇾")
  sentence=sentence.replace("Z", " 🇿").replace("z"," 🇿")
  sentence=sentence.replace("1", " :one:")
  sentence=sentence.replace("2", " :two:")
  sentence=sentence.replace("3", " :three:")
  sentence=sentence.replace("4", " :four:")
  sentence=sentence.replace("5", " :five:")
  sentence=sentence.replace("6", " :six:")
  sentence=sentence.replace("7", " :seven:")
  sentence=sentence.replace("8", " :eight:")
  sentence=sentence.replace("9", " :nine:")
  sentence=sentence.replace("0", " :zero:")
  sentence=sentence.replace("#", " :hash:")

  question_marks=[' ❓', ' ❔']
  exclamation_marks=[' :exclamation:', ' :grey_exclamation:']

  sentence=sentence.replace("<=>", " ↔️").replace("<==>", " ↔️")
  sentence=sentence.replace("?", random.choice(question_marks))
  sentence=sentence.replace("!", random.choice(exclamation_marks))
  sentence=sentence.replace("*", " *️⃣")
  sentence=sentence.replace(" ", "  ")
  sentence=sentence.replace("=>", " ➡️")
  sentence=sentence.replace("<=", " ➡️")
  

  return sentence

def convert_list_to_string(org_list, seperator=' '):
    """ Convert list to string, by joining all item in list with given separator.
        Returns the concatenated string """
    return seperator.join(org_list)

def convert(time):
    pos = ["s","m","h","d","w"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600*24, "w" : 3600*24*7}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2


    return val * time_dict[unit]

def syntax(command):
  cmd_and_aliases = "|".join([str(command), *command.aliases])
  params = []

  for key, value in command.params.items():
    if key not in ("self", "ctx"):
      params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

  params = " ".join(params)

  return f'`{cmd_and_aliases} {params}`'

def server_prefix(guild_id):
  with open("databases/Settings/prefixes.json", 'r') as f:
    datap = json.load(f)

    try:
      serverpre = datap[str(guild_id)]

    except KeyError or AttributeError:
      return "&"
      
    else:
      return serverpre

def clapdacheeks(msg):
  checkmode = msg.split(",")
  if checkmode[0].lower() in ['word', "words", 'per word', 'w']:
    if len(checkmode[1]) > 1500:
      return "**ERROR!**\nThis is message **cannot be clapped** 😱 since it is __too long!__"

    else:
      clapthis = checkmode[1].split(" ")

      if len(clapthis) < 2:
        return "**ERROR!**\nThis is message **cannot be clapped** 😱 since it is __too short!__\n(minimum words to be clapped is 2 words btw)"

      finalProduct = ""
      wordcount = 0
      for word in clapthis:
        wordcount += 1
        if word == " ":
          continue

        if wordcount == len(clapthis):
          finalProduct += word
        else:
          finalProduct += f"{word} :clap: "


      return finalProduct

  elif checkmode[0].lower() in ['letter', "letters", 'per letter', 'l']:
    if len(checkmode[1]) > len("PneumonoultramicroscopicsilicovolcanoconiosissupercalifragilisticexpialidociousPseudopseudohypoparathyroidism"):
      return "**ERROR!**\nThis is message **cannot be clapped** 😱 since it is __too long!__\n(Longer than the three of the longest words in English Dictionaries combined xD)"

    if len(checkmode[1]) <= 2:
      return "**ERROR!**\nThis is message **cannot be clapped** 😱 since it is __too short!__\n(minimum letters to be clapped is 3 letters btw)"

    finalLetterClapped = ""
    lettercount = 0
    for letter in checkmode[1]:
      lettercount += 1
      if letter == " ":
        continue

      if lettercount == len(checkmode[1]):
        finalLetterClapped += letter
      else:
        finalLetterClapped += f"{letter} :clap: "

    return finalLetterClapped


  else:
    return "**ERROR!**\nInvalid Clap Mode."