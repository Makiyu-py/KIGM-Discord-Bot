import discord
#from PIL import Image
#from io import BytesIO
from discord.utils import get
from discord.ext import commands
from loremipsum import get_sentences
import requests
import asyncio
import random
import os
import the_universe
import praw

botid = 763626077292724264

secret_id = os.environ.get("REDDIT_ID_SECRET")

reddit_id = os.environ.get("REDDIT_ID")

class FunCommands(commands.Cog, name=':smile: Fun Commands'):

  def __init__(self, bot):
    self.bot = bot
    self.reddit = None
    if secret_id and reddit_id:
        self.reddit = praw.Reddit(client_id=reddit_id, client_secret=secret_id, user_agent='KIGM_DISCORD_BOT')

  @commands.command(description="Whenever you feel sad, he'll say hi to you!",aliases=['hi', 'hei'])
  async def hello(self, ctx):
    await ctx.channel.send("Hello there, " + ctx.author.mention + "!")

 
  @commands.command(description="pls dont spam this command")
  async def meme(self, ctx, subreddit : str=""):
    async with ctx.channel.typing():
      all_subreddits = ['memes', 'meme', 'dankmemes', 'Memes_Of_The_Dank', 'PrequelMemes', 'MemeEconomy', 'wholesomememes', 'absolutelynotme_irl', 'me_irl', 'funny', 'aww', 'insanepeoplefacebook', 'WatchPeopleDieInside', 'starterpacks', 'WhitePeopleTwitter', 'ScottishPeopleTwitter']
      random_sub = random.choice(all_subreddits)
      if self.reddit:
        # bot starts working
        chosen_subreddit = random_sub
        if subreddit:
          if subreddit in all_subreddits:
            chosen_subreddit = subreddit

          else:
            await ctx.send("The subreddit you wrote is either not allowed or non-existent.\nAlternatively, you can pick between these subreddits: %s"%', '.join(all_subreddits))
            return

        submissions = self.reddit.subreddit(chosen_subreddit).hot()
        
        post_to_pick = random.randint(1, 16)
        for i in range(0, post_to_pick):
          submission = next(x for x in submissions if not x.stickied)

        if submission.url.endswith('.jpg') or submission.url.endswith('.jpeg') or submission.url.endswith('.gif') or submission.url.endswith('.png'):
          embed = discord.Embed(title=submission.title, colour=0xf8f8ff, url=submission.url)

          embed.set_author(name=f'from r/{chosen_subreddit}')

          embed.set_footer(text=f'⬆️{submission.score}')
          embed.set_image(url=submission.url)
          await ctx.send(embed=embed)
        else:
          await ctx.send(submission.url)
          
      else:
        await ctx.send("Ain't working lol")

  @commands.command(description='Convert text to binary00100001')
  async def binary(self, ctx, *,text):
    res = ''.join(format(i, 'b') for i in bytearray(text, encoding ='utf-8'))
    embed = discord.Embed(title='Text To Binary', color=0xf8f8ff)
    embed.add_field(name='Normal Text:', value=text, inline=False)
    embed.add_field(name='Binary Text:', value=f'`{str(res)}`', inline=False)
    embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)

  @commands.command(description='Generate a specified number of lorem ipsum sentences!',
  aliases=['lig', 'generateli']
  )
  async def loremipsum(self, ctx, number_of_sentences=6):
    sentences_list = get_sentences(number_of_sentences, start_with_lorem=True)
    not_vowel = ['s', 'f', 'r', 'l', 'p', 'w', 'h', 'm', 'v', 'k', 'y', 't']
    random_not_vowel = random.choice(not_vowel)
    lorem_ipsum = the_universe.convert_list_to_string(sentences_list)
    lorem_ipsum = lorem_ipsum.replace("'", "")
    lorem_ipsum=lorem_ipsum.replace("ba", f"{random_not_vowel}a")
    lorem_ipsum=lorem_ipsum.replace("b", "")
    lorem_ipsum=lorem_ipsum.replace("b", "")
    embed = discord.Embed(title="Lorem Ipsum Generator", description=lorem_ipsum, color=0x656565, timestamp = ctx.message.created_at)
    embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

    '''
  @commands.command()
  async def wanted_poster(self, ctx, member : discord.Member=None):
    if member == None:
      member = ctx.author

    wanted = Image.open("poster-wanted.jpeg")

    asset = member.avatar_url_as(size=128)

    data = BytesIO(await asset.read())

    pfp = Image.open(data)
    pfp = pfp.resize((898,991))
    # 898 x 991
    '''
  @commands.group(description="Play games that rely on RNG!",aliases=['goc', 'gameofchance'])
  async def game_of_chance(self, ctx):
    if ctx.invoked_subcommand is None:
      embed=discord.Embed(title=f"Here's a list of games that you can play {ctx.author.name}!", description="Just type `&game_of_chance <game you want to play>`:", color=0xebe5e5)
      embed.add_field(name="1. Dice", value="`&game_of_chance dice`", inline=True)
      embed.add_field(name="2. Coinflip", value="`&game_of_chance coinflip`", inline=True)
      embed.add_field(name="3. RPS (rock, paper, scissors)", value="`&game_of_chance RPS <your move>`", inline=False)
      await ctx.send(embed=embed)

  @game_of_chance.command()
  async def dice(self, ctx):
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    await ctx.send(f"The dice have rolled!:game_die: :game_die: You have rolled... A `{dice1}` and a `{dice2}`!")

  @game_of_chance.command()
  async def coinflip(self, ctx):
    coin = ['Heads', 'Tails']
    coin = random.choice(coin)
    await ctx.send(f"The coin has flipped! You got `{coin}`!")

  @game_of_chance.group()
  async def RPS(self, ctx):
    if ctx.invoked_subcommand is None:
      await ctx.send("If you don't know how to play Rock Paper Scissors, then here's your guide!\nRock Paper Scissors is an old game to kill your boredom (minimum and maximum of 2 players ~~but I'm going to play with you so that you won't get lonely~~)\n\nThese are the only things you need to know about the game:\n\n```rock - draws with itself, loses to paper, and wins against scissors\n\npaper - draws with itself, loses to scissors, and wins against rock\n\nscissors - draws with itself, loses against rock, and wins against paper```\n\nwhat are you waiting for, let's play! | `&game_of_chance RPS <rock, paper or scissors>`")

  @RPS.command()
  async def rock(self, ctx):
    RPS = ["rock", "paper", "scissors"]
    RPSX = random.choice(RPS)
    if RPSX == 'paper':
      embed=discord.Embed(title="Rock Paper Scissors!", description=f"You: `rock`   \n  Me: `{RPSX}`", color=0xf32b2b)
      embed.add_field(name="You lost...", value="Play Again!", inline=True)
      await ctx.send(embed=embed)
    
    elif RPSX == 'rock':
      embed=discord.Embed(title="Rock Paper Scissors!", description=f"You: `rock`  \n   Me: `{RPSX}`", color=0x6c50d3)
      embed.add_field(name="A draw...", value="Play Again!", inline=True)
      await ctx.send(embed=embed)

    elif  RPSX == 'scissors':
      embed=discord.Embed(title="Rock Paper Scissors!", description=f"You: `rock`  \n   Me: `{RPSX}`", color=discord.Colour.green())
      embed.add_field(name="You won! Great job!", value="Play Again!", inline=True)
      await ctx.send(embed=embed)
       
  @RPS.command()
  async def paper(self, ctx):
    RPS = ["rock", "paper", "scissors"]
    RPSX = random.choice(RPS)
    if RPSX == 'scissors':
      embed=discord.Embed(title="Rock Paper Scissors!", description=f"You: `paper`   \n  Me: `{RPSX}`", color=0xf32b2b)
      embed.add_field(name="You lost...", value="Play Again!", inline=True)
      await ctx.send(embed=embed)
    
    elif RPSX == 'paper':
      embed=discord.Embed(title="Rock Paper Scissors!", description=f"You: `paper`  \n   Me: `{RPSX}`", color=0x6c50d3)
      embed.add_field(name="A draw...", value="Play Again!", inline=True)
      await ctx.send(embed=embed)

    elif  RPSX == 'rock':
      embed=discord.Embed(title="Rock Paper Scissors!", description=f"You: `paper`  \n   Me: `{RPSX}`", color=discord.Colour.green())
      embed.add_field(name="You won! Great job!", value="Play Again!", inline=True)
      await ctx.send(embed=embed)

  @RPS.command()
  async def scissors(self, ctx):
    RPS = ["rock", "paper", "scissors"]
    RPSX = random.choice(RPS)
    if RPSX == 'rock':
      embed=discord.Embed(title="Rock Paper Scissors!", description=f"You: `scissors`   \n  Me: `{RPSX}`",color=0xf32b2b)
      embed.add_field(name="You lost...", value="Play Again!", inline=True)
      await ctx.send(embed=embed)
    
    elif RPSX == 'scissors':
      embed=discord.Embed(title="Rock Paper Scissors!", description=f"You: `scissors`  \n   Me: `{RPSX}`",color=0x6c50d3)
      embed.add_field(name="A draw...", value="Play Again!", inline=True)
      await ctx.send(embed=embed)

    elif  RPSX == 'paper':
      embed=discord.Embed(title="Rock Paper Scissors!", description=f"You: `scissors`  \n   Me: `{RPSX}`",color=discord.Colour.green())
      embed.add_field(name="You won! Great job!", value="Play Again!", inline=True)
      await ctx.send(embed=embed)

  @commands.command(description='Returns a (really bad) dad joke to you',aliases=['dadjokes','djoke', 'dadj'])
  async def dadjoke(self, ctx):
    '''
		Returns a (really bad) dad joke to you.
		'''
    joke = requests.get('https://icanhazdadjoke.com', headers={"Accept": "text/plain"}).text

    if 'â' in joke:
      better_joke = joke.replace("â", "'")
      embed = discord.Embed(title='Heard this joke from daddy! :bearded_person:', description=better_joke, colour = discord.Colour.blue())
      embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Requested by: {ctx.author.name}')
      embed.set_author(name="All dad jokes from icanhazdadjoke.com so shoutout to them")
      await ctx.send(embed = embed)
    else:
      embed = discord.Embed(title='Heard this joke from daddy! :bearded_person:', description=joke, colour = discord.Colour.blue())
      embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Requested by {ctx.author.name}')
      embed.set_author(name="All dad jokes from icanhazdadjoke.com so shoutout to them")
      await ctx.send(embed = embed)


  @commands.command(description='lol idk manipulate me to saying something')
  async def say(self, ctx):
    await ctx.message.delete()
    embed=discord.Embed(title='Go. Tell me what you want me to say',description="||If you don't tell me what I'm going to say in less than 20 seconds, the command won't happen anymore.||", color=0xf8f8ff)
    sent = await ctx.send(embed=embed)

    try:

      msg = await self.bot.wait_for("message", timeout=20, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)

      if msg:
        await sent.delete()
        await msg.delete()
        await ctx.send(msg.content)

    except asyncio.TimeoutError:

      await sent.delete()
      await ctx.send("Command cancelled cause u slow lol", delete_after=6)

  @commands.command(description='Converts your text to OwO ^-^',aliases=['0w0'])
  async def owo(self, ctx, *, sentence):
    await ctx.send(the_universe.text_to_owo(sentence))

  @commands.command(description='Converts your text to BriIsh',aliases=['british'])
  async def britishaccent(self, ctx, *, sentence):
    await ctx.send(the_universe.british_accent(sentence))

  @commands.command(description='Converts your text to OwO ^-^',aliases=['texttoemoji', 'tte'])
  async def text_to_emoji(self, ctx, *, sentence):
    await ctx.send(the_universe.ttoemoji(sentence))

  @commands.command(description='V i r t u a l  s l a p p',aliases=['slapp'])
  async def slap(self, ctx, *, User : discord.Member):
    slap_gif = ['https://tenor.com/view/bobs-burgers-louise-louise-slaps-slap-gif-12656044',
    'https://tenor.com/view/dog-slap-gif-3468779', 'https://tenor.com/view/slap-virtual-slap-boglio-laurene-boglio-gif-13857116', 'https://tenor.com/view/amanda-bynes-slap-gif-4079563', 'https://tenor.com/view/baka-slap-huh-angry-gif-15696850']
    slap_gifs = random.choice(slap_gif)

    if User.id == botid:
      await ctx.send("https://tenor.com/view/hell-no-disagree-no-nope-never-gif-14721955")
      
    elif ctx.author.mention == User.mention:
      await ctx.send("weirdo")
      await ctx.send("https://tenor.com/view/sgo48-slap-sgo48nini-slap-your-self-gif-15092286")
    else:
      await ctx.channel.send(ctx.author.mention + f" has slapped "+ User.mention +"! :scream:")
      await ctx.channel.send(slap_gifs)

  @commands.command(description='Disclaimer: Do not try this at home', aliases=['shot'])
  async def shoot(self, ctx, *, User : discord.Member=None):
    shoot_gif = ['https://tenor.com/view/die-gun-shotgun-deus-vult-gif-17767114',
    'https://tenor.com/view/gun-shotgun-shooting-fire-cartoon-gif-14404861', 'https://tenor.com/view/gun-gunshot-gunfire-gif-15642482', 'https://tenor.com/view/water-gun-melissa-mc-carthy-gotcha-attack-childish-gif-7720147', 'https://tenor.com/view/kermit-shoot-lol-gun-frog-gif-16181496', 'https://tenor.com/view/cat-shooting-mouth-open-gif-15017033']
    shoot_gifs = random.choice(shoot_gif)

    if User is None:
      await ctx.send("K I'll shoot u instead lol")
      await ctx.send(shoot_gifs)

    elif ctx.author.mention == User.mention:
      await ctx.send("why r u like this")
      await ctx.send("I hope ur ok")
      await ctx.send("pls don't be that type of person")
      await ctx.send("I hope you're fine :) :heartpulse:")

    elif User.id == botid:
      await ctx.send("not happening lol")

    else:
      await ctx.channel.send(ctx.author.mention + f" has shot "+ User.mention + "! :scream: ")
      await ctx.channel.send(shoot_gifs)

  @commands.command(description='Just type it and see what happens...')
  async def YEET(self, ctx, User : discord.Member=None):
    if User is None:
      await ctx.send(":woman_cartwheeling:\n        :manual_wheelchair: :man_golfing:")
    else:
      await ctx.send(f":woman_cartwheeling:\n   ^"+User.mention+f"\n             :manual_wheelchair: :man_golfing:\n                      ^{ctx.author.mention}")

  @commands.command(description='will give you a random spoiler from a movie!')
  async def spoiler(self, ctx):
    await ctx.send("https://media.discordapp.net/attachments/767572984860508160/770165174891184148/image0.gif")
    
def setup(bot):
	bot.add_cog(FunCommands(bot)) 