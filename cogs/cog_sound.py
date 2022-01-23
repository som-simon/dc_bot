import discord
from discord.ext import commands
# from discord.ext.commands import has_permissions, MissingPermissions
import wavelink
import os

cog = os.path.basename(__file__)


# players = {}


# class SoundCommands(commands.Cog):
#     '''These are commands that are used for every sound management'''
#     def __init__(self, bot):
#         self.bot = bot

#     @commands.Cog.listener()
#     async def on_ready(self):
#         print(f'cogs.{cog} is online')

#     @commands.command()
#     async def join(self, ctx):
#         if (ctx.author.voice):
#           channel = ctx.message.author.voice.channel
#           await channel.connect()
#         else:
#           await ctx.send("join first :imp:")


#     @commands.command()
#     async def leave(self, ctx):
#         await ctx.voice_client.disconnect()

    # @commands.command()
    # async def play(self, ctx, url):
    #     guild = ctx.message.guild
    #     voice_client = guild.voice_client
    #     player = await voice_client.create_ytdl_player(url)
    #     players[guild.id] = player
    #     player.start()

class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot=self.bot)

        self.bot.loop.create_task(self.start_nodes())

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'cogs.{cog} is online')


    async def start_nodes(self):
        await self.bot.wait_until_ready()

        # Initiate our nodes. For this example we will use one server.
        # Region should be a discord.py guild.region e.g sydney or us_central (Though this is not technically required)
        await self.bot.wavelink.initiate_node(host='lava.link',
                                              port=80,
                                              rest_uri='http://lava.link:80',
                                              password='f',
                                              identifier='JOE',
                                              region='us_central')

    @commands.command(name='connect', aliases=['join', 'con'])
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise discord.DiscordException('No channel to join. Please either specify a valid channel or join one.')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await ctx.send(f'Connecting to **`{channel.name}`**')
        await player.connect(channel.id)

    @commands.command(name='disconnect', aliases=['leave', 'dc'])
    async def disconnect_(self, ctx):
        await self.bot.wavelink.get_player(ctx.guild.id).disconnect()


    @commands.command()
    async def play(self, ctx, *, query: str):
        tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{query}')

        if not tracks:
            return await ctx.send('Could not find any songs with that query.')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect_)

        await ctx.send(f'Added **`{str(tracks[0])}`** to the queue.')
        await player.play(tracks[0])


    @commands.command(name='pause', aliases = ['pau', '||'])
    async def pause_(self, ctx):
      player = self.bot.wavelink.get_player(ctx.guild.id)
      if player.is_playing:
        ctx.channel.send('Paused.')
        await self.bot.wavelink.get_player(ctx.guild.id).set_pause(True)

    @commands.command(name='resume', aliases = ['res', '>'])
    async def resume_(self, ctx):
      player = self.bot.wavelink.get_player(ctx.guild.id)
      if player.is_paused:
        ctx.channel.send('Resumed.')
        await self.bot.wavelink.get_player(ctx.guild.id).set_pause(False)
    
    @commands.command(name='stop', aliases = ['shut'])
    async def stop_(self, ctx):
      player = self.bot.wavelink.get_player(ctx.guild.id)
      if player.is_playing or player.is_paused:
        await ctx.send('Stopped player.')
        await player.stop()
      else:
        await ctx.send(f'There is nothing to stop.')

    @commands.command(name='volume', aliases = ['set_volume', 'vol'])
    async def volume_(self, ctx, vol):
      await self.bot.wavelink.get_player(ctx.guild.id).set_volume(int(vol))
      await ctx.send(f'Set volume **`{str(vol)}`**.')



def setup(bot):
    bot.add_cog(Music(bot))
    # bot.add_cog(SoundCommands(bot))