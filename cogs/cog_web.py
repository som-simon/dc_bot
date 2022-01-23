import discord
from discord.ext import commands
import random
import requests
import typing
from bs4 import BeautifulSoup
import os

cog = os.path.basename(__file__)


class WebCommands(commands.Cog, name='Web commands'):
    '''These are the commands that are associated with web'''
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'cogs.{cog} is online')
    
    @commands.command(aliases=['wake'])
    async def wake_up(self, ctx):
        '''random biden's quote'''
        quote = random_quote()
        await ctx.channel.send(
            f'"{quote}"\nJoe Biden {round(self.bot.latency * 1000)}ms')

    @commands.command(aliases=['wiki_search', 'dumbass'])
    async def wiki(self, ctx, key, limit: typing.Optional[int]=3, language='en'):

        PATH = f'https://{language}.wikipedia.org/wiki/{key}'
        LIMIT = limit

        r = requests.get(PATH)
        soup = BeautifulSoup(r.text, features="html.parser")
        title = soup.find(id="firstHeading")
        content = soup.findAll('p', limit=LIMIT + 1)

        message = f'```\n{title.get_text()}\n\n'

        for i in content[1::1]:
            message += f'{i.get_text()}\n'
        if len(message) > 2000:
            message = message[0:1997]
        message += '```'
        await ctx.channel.send(message)
            



def random_quote():
      r = requests.get('https://www.brainyquote.com/authors/joe-biden-quotes')
      content = r.text
      s = BeautifulSoup(content, features="html.parser")
      quotes = ['I forgor 💀']
      for i in s.findAll(
              "div", {"style": "display: flex;justify-content: space-between"}):
          quotes.append(i.contents[0].strip())
      return random.choice(quotes)

def setup(bot):
    bot.add_cog(WebCommands(bot))