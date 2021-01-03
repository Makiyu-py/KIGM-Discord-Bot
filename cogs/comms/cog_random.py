from typing import Optional
import discord
import platform
import json
from aiohttp import request
import random
import the_universe
from loremipsum import get_sentences
from discord.ext import commands

class RandomCommands(commands.Cog, name=':grey_question: Randomness'):
  def __init__(self, bot):
	  self.bot = bot

  '''
  @commands.command(aliases=['ytcomment'], description='Make a *fake* YouTube comment!')
  @commands.guild_only()
  async def youtubecomment(self, ctx, *, comment):
    with open("databases/Other/APIS.json", 'r') as f:
      API = json.load(f)

    avatar = str(ctx.author.avatar_url).replace('.webp', '.png')
    comment = comment.replace(' ', '+')
    username=ctx.author.name

    YTAPI = str(API['YTComment']).format(avatar, comment, username)

    async with request("GET", YTAPI, headers={}) as response:
      if response.status == 200:

        embed = discord.Embed(title="Here's your Comment!", description=f'Hope you liked it!\n[Comment Link]({YTAPI})',color=self.bot.main_colour)
        embed.set_footer(text=f'{ctx.author} | Powered by https://some-random-api.ml/', icon_url=ctx.author.avatar_url)

        embed.set_image(url=YTAPI)

        await ctx.send(embed=embed)
        
  '''
  @commands.command(aliases=['pfpbegay'], description='Make your avatar go 🌈 brr 🌈')
  async def rainbowpfp(self, ctx, user: Optional[discord.Member]=None):
    if user is None:
      user= ctx.author

    with open("databases/Other/APIS.json", 'r') as f:
      API = json.load(f)

    avatar = str(user.avatar_url).replace('.webp', '.png')
    Rainbowpfp = str(API['RainbowPFP'] + avatar)

    async with request("GET", Rainbowpfp, headers={}) as response:
      if response.status == 200:

        embed = discord.Embed(title="Here! 🌈", description=f'[avatar link]({Rainbowpfp})',color=self.bot.main_colour)
        embed.set_footer(text=f'{ctx.author} | Powered by https://some-random-api.ml/', icon_url=ctx.author.avatar_url)

        embed.set_image(url=Rainbowpfp)

        await ctx.send(embed=embed)

  @commands.command(aliases=['jail'], description='Lock ur avatar to jail :P')
  async def jailify(self, ctx, user: Optional[discord.Member]=None):
    if user is None:
      user= ctx.author
    with open("databases/Other/APIS.json", 'r') as f:
      API = json.load(f)

    avatar = str(user.avatar_url).replace('.webp', '.png')
    Jailpfp = str(API['JailPFP'] + avatar)

    async with request("GET", Jailpfp, headers={}) as response:
      if response.status == 200:

        embed = discord.Embed(title=f":headstone: Rip cuz *{user}* is in *jail*", description=f"[avatar link]({Jailpfp})", color=self.bot.main_colour)
        embed.set_footer(text=f'{ctx.author} | Powered by https://some-random-api.ml/', icon_url=ctx.author.avatar_url)

        embed.set_image(url=Jailpfp)

        await ctx.send(embed=embed)

  @commands.command(aliases=['quotekanye'], description='Get a real (yes, real. Even I was surprised that they\'re all real lol) random quote from Kanye West himself!')
  @commands.guild_only()
  async def kanyequote(self, ctx):
    with open("databases/Other/APIS.json", 'r') as f:
      API = json.load(f)

    KanyeAPI = API['KanyeQuote']

    kanyeIMGS = [
      'https://www.biography.com/.image/ar_1:1%2Cc_fill%2Ccs_srgb%2Cg_face%2Cq_auto:good%2Cw_300/MTU0OTkwNDUxOTQ5MDUzNDQ3/kanye-west-attends-the-christian-dior-show-as-part-of-the-paris-fashion-week-womenswear-fall-winter-2015-2016-on-march-6-2015-in-paris-france-photo-by-dominique-charriau-wireimage-square.jpg',
      'https://storage.googleapis.com/afs-prod/media/1f764b198a42470189b99b4084be6cf0/800.jpeg',
      'https://www.gannett-cdn.com/presto/2019/03/07/USAT/71d24511-e504-40e1-95eb-180f883eeb81-LL_MW_KanyeWest_010319.JPG?width=600&height=900&fit=crop&format=pjpg&auto=webp',
      'https://pyxis.nymag.com/v1/imgs/014/a62/bc3a72ed5c47e8c0dd5bc52028c5df5005-kanye-west.2x.rsquare.w330.jpg',
      'https://www.aljazeera.com/wp-content/uploads/2020/09/Ye-1.jpg?resize=770%2C513',
      'https://images.businessoffashion.com/profiles/asset/1797/43897e2e4a6d155d72dd9df352017b546ef9e229.jpeg?auto=format%2Ccompress&fit=crop&h=360&w=660',
      'https://i.insider.com/5f624c55323fc4001e0d6a47?width=2000&format=jpeg&auto=webp',
      'https://www.wmagazine.com/wp-content/uploads/2019/10/25/5db30d540e538e000830c68a_GettyImages-1183294345.jpg?w=1352px',
      'https://i.guim.co.uk/img/media/07ad3146c3879e9d3da5e81aa32edf7160b93888/0_195_2326_1396/master/2326.jpg?width=1200&height=1200&quality=85&auto=format&fit=crop&s=8bdf6ca2f739479415c3a3b6d8fe890a'
    ]
    pick_img = random.choice(kanyeIMGS)

    async with request("GET", KanyeAPI, headers={}) as response:
      if response.status == 200:
        data = await response.json()

        embed = discord.Embed(title="From the Words of Kanye West:", description=f'"{data["quote"]}"', color=self.bot.main_color)

        embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=pick_img)

        await ctx.send(embed=embed)

      else:
        print(f"response status gave us {response.status} :(")

  @commands.command(description='Put a wasted overlay (from GTA V) on someone\'s (or yours) profile picture!')
  @commands.guild_only()
  async def wasted(self, ctx, user: Optional[discord.Member]=None):
    if user is None:
      user = ctx.author

    with open("databases/Other/APIS.json", 'r') as f:
      API = json.load(f)

    avatar = str(user.avatar_url).replace('.webp', '.png').replace('.gif', '.png').replace('?size=1024', '?size=512')

    UFAPI = f"{API['Wasted']}{avatar}"

    async with request("GET", UFAPI, headers={}) as response:
      if response.status == 200:

        embed = discord.Embed(title="w a s t e d .", description=f'[T h e  i m a g e  l i n k]({UFAPI})',color=self.bot.main_color)
        embed.set_footer(text=f'{ctx.author} | Powered by https://some-random-api.ml/', icon_url=ctx.author.avatar_url)

        embed.set_image(url=UFAPI)

        await ctx.send(embed=embed)

  @commands.command(description='Generate placeholder (and kinda latin) text!')
  @commands.guild_only()
  async def loremipsum(self, ctx, number_of_sentences: Optional[int]=6):
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

  @commands.command(description='You read the command name :wink:')
  @commands.guild_only()
  async def useless_fact(self, ctx):
    with open("databases/Other/APIS.json", 'r') as f:
      API = json.load(f)

    UFAPI = API['Useless Fact']

    async with request("GET", UFAPI, headers={}) as response:
      if response.status == 200:
        data = await response.json()
        fact = data['text']

        embed = discord.Embed(title="Here's your Dose of a Useless Fact!", description=fact, color=self.bot.main_color)
        embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

  @commands.command(description='I mean, get sometimes right but also random opinions from random people?')
  @commands.guild_only()
  async def random_opinion(self, ctx):
    with open("databases/Other/APIS.json", 'r') as f:
      API = json.load(f)

    OpinionAPI = API['Random Opinion']

    async with request("GET", OpinionAPI, headers={}) as response:
      if response.status == 200:
        data = await response.json()
        opinion = data['quotes'][0]['quote']
        author = data['quotes'][-1]['author']

        embed = discord.Embed(title="Here's your Random Opinion!", description=f'\'{opinion}\'\n\n- {author}', color=self.bot.main_color)
        embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(RandomCommands(bot))