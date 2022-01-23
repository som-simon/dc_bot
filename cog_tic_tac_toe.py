import discord
from discord.ext import commands

class TicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    pass

def setup(bot):
    bot.add_cog(TicTacToe(bot))