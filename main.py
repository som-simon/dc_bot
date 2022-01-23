import os
import discord
from discord.ext import commands, tasks
# from discord.ext.commands import has_permissions, MissingPermissions
# from bs4 import BeautifulSoup
# import requests
# import random
from itertools import cycle
from no_sleepy_time import jooo_biden_wake_up



if __name__ == '__main__':

  bot = commands.Bot(command_prefix='&')

  for file in os.listdir('./cogs'):
      if file.endswith('.py'):
          bot.load_extension(f'cogs.{file[:-3]}')

  bot.author_id = 578521697532117002


  @bot.event
  async def on_ready():
      change_status.start()
      # await bot.change_presence(status=discord.Status.online, activity=discord.Game(':('))
      print('We have logged in as {0.user}'.format(bot))

  # bot.load_extension('dismusic')

  status = cycle([':(','):','（´＿｀）', ':c', ':^(', '>.<',':/',']:'])

  @tasks.loop(minutes=10)
  async def change_status():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(next(status)))

  @bot.event
  async def on_member_join(member):
      print(f'{member} has joined')


  @bot.event
  async def on_member_remove(member):
      print(f'{member} has left a server')

  # @bot.event
  # async def on_message(message):


  #   if message.content.startswith('this is so sad'):
  #       await message.channel.send('big f : (') 

  # def random_quote():
  #     r = requests.get('https://www.brainyquote.com/authors/joe-biden-quotes')
  #     content = r.text
  #     s = BeautifulSoup(content, features="html.parser")
  #     quotes = ['I forgor 💀']
  #     for i in s.findAll(
  #             "div", {"style": "display: flex;justify-content: space-between"}):
  #         quotes.append(i.contents[0].strip())
  #     return random.choice(quotes)


  # @bot.command(aliases=['wake'])
  # async def wake_up(ctx):
  #     '''random biden's quote'''
  #     quote = random_quote()
  #     await ctx.channel.send(
  #         f'"{quote}"\nJoe Biden {round(bot.latency * 1000)}ms')


  jooo_biden_wake_up()
  bot.run(os.getenv('TOKEN'))
