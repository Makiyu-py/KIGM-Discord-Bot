from typing import Optional
import discord
#from PIL import Image
#from io import BytesIO
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
import requests
import asyncio
import random
import os
import the_universe
import asyncpraw

botid = 763626077292724264

secret_id = os.environ.get("REDDIT_ID_SECRET")

reddit_id = os.environ.get("REDDIT_ID")

class FunCommands(commands.Cog, name='😄 Fun Commands'):

  def __init__(self, bot):
    self.bot = bot
    self.reddit = None
    if secret_id and reddit_id:
        self.reddit = asyncpraw.Reddit(client_id=reddit_id, client_secret=secret_id, user_agent='KIGM_DISCORD_BOT')

 
  @commands.command(description="pls dont spam this command")
  @commands.guild_only()
  @cooldown(1, 2, BucketType.user)
  async def meme(self, ctx, subreddit : Optional[str]=""):
    async with ctx.channel.typing():
      find_app_sub = True
      all_subreddits = ['memes', 'meme', 'dankmemes', 'Memes_Of_The_Dank', 'PrequelMemes', 'MemeEconomy', 'wholesomememes', 'absolutelynotme_irl', 'me_irl', 'funny', 'aww', 'insanepeoplefacebook', 'WatchPeopleDieInside', 'starterpacks', 'WhitePeopleTwitter', 'ScottishPeopleTwitter', 'animemes']
      random_sub = random.choice(all_subreddits)
      if self.reddit:
        # bot starts working
        chosen_subreddit = await self.reddit.subreddit(random_sub)
        if subreddit:
          if subreddit in all_subreddits:
            chosen_subreddit = await self.reddit.subreddit(subreddit)

          else:
            await ctx.send("The subreddit you wrote is either not allowed or non-existent.\nAlternatively, you can pick between these subreddits: %s"%', '.join(all_subreddits))
            return

        all_submissions = []
        async for submission in chosen_subreddit.top("day"):
          all_submissions.append(submission)

          if len(all_submissions) >= 35:
            break

          while find_app_sub is True:
            output_submission = random.choice(all_submissions)
            
            ends = ['jpg', 'jpeg', 'gif', 'mp4', 'png']

            for endsub in ends:
              if output_submission.url.endswith(f'.{endsub}') or output_submission.url.startswith("https://giphy.com/") or output_submission.url.startswith("https://imgur.com/"):
                find_app_sub = False

        embed = discord.Embed(title=output_submission.title, colour=self.bot.main_color, url=output_submission.url)

        embed.set_author(name=f'from r/{chosen_subreddit}')

        embed.set_footer(text=f'⬆️ {output_submission.score}')
        embed.set_image(url=output_submission.url)
        await ctx.send(embed=embed)
        all_submissions = None
          
      else:
        await ctx.send("**ERROR!**\nReddit Not Working wooo *. . .*")
    

  @commands.command(description='Convert text to binary00101001')
  @commands.guild_only()
  async def binary(self, ctx, *,text):
    res = ''.join(format(i, 'b') for i in bytearray(text, encoding ='utf-8'))
    embed = discord.Embed(title='Text To Binary', color=self.bot.main_color)
    embed.add_field(name='Normal Text:', value=text, inline=False)
    embed.add_field(name='Binary Text:', value=f'`{str(res)}`', inline=False)
    embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)

  @commands.command(description='Returns a (really bad) dad joke to you',aliases=['dadjokes','djoke', 'dadj'])
  @commands.guild_only()
  async def dadjoke(self, ctx):
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
  @commands.guild_only()
  @cooldown(1, 5, BucketType.user)
  async def say(self, ctx):
    await ctx.message.delete()
    embed=discord.Embed(title='Go. Tell me what you want me to say',description="||If you don't tell me what I'm going to say in less than 20 seconds, the command won't happen anymore.||", color=self.bot.main_color)
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
      ctx.command.reset_cooldown(ctx)

  @commands.command(description='Converts your text to OwO ^--^',aliases=['0w0'])
  @commands.guild_only()
  async def owo(self, ctx, *, sentence):
    await ctx.send(the_universe.text_to_owo(sentence))

  @commands.command(description='Converts your text to BriIsh',aliases=['british'])
  @commands.guild_only()
  async def britishaccent(self, ctx, *, sentence):
    await ctx.send(the_universe.british_accent(sentence))

  @commands.command(description='Converts your text to emoji! 💩',aliases=['texttoemoji', 'emojithis', 'tte'])
  @commands.guild_only()
  async def text_to_emoji(self, ctx, *, sentence):
    await ctx.send(the_universe.ttoemoji(sentence))

  @commands.command(description="Clap your way with adding the clap :clap: emoji between every letter/word!", aliases=['clapify'])
  async def clap(self, ctx, mode_of_clap_either_letter_or_word, *, phrase):
    output = f"{mode_of_clap_either_letter_or_word},{phrase}"
    await ctx.send(the_universe.clapdacheeks(output))

  @commands.command(description='V i r t u a l  s l a p p',aliases=['slapp'])
  @commands.guild_only()
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