import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import os

cog = os.path.basename(__file__)

class UserControl(commands.Cog):
    '''These are commands that are used to control users, they require permissions'''
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'cogs.{cog} is online')
   

    @commands.command(name='kick', pass_context=True)
    @has_permissions(administrator=True, manage_roles=True, kick_members=True)
    async def _kick(self, ctx, member: discord.Member, *, reason=None):
        '''kicks member if you have permission'''
        await member.kick(reason=reason)
        await ctx.channel.send(f'{member.mention} was kicked')


    @_kick.error
    async def _kick_error(self, error, ctx):
        if isinstance(error, MissingPermissions):
            owner = ctx.guild.owner
            direct_message = await owner.create_dm()
            await direct_message.send("Missing Permissions")

    @commands.command(name='clear', pass_context=True)
    @has_permissions(administrator=True, manage_messages=True)
    async def _clear(self,ctx, amount=10):
        '''clears set amount of message (default 10) if you have permission'''
        await ctx.channel.purge(limit=amount + 1)
        await ctx.channel.send(f'I cleared {amount} messages')


    @_clear.error
    async def clear_error(self,error, ctx):
        if isinstance(error, MissingPermissions):
            text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
            await commands.send_message(ctx.message.channel, text)            


    @commands.command(name='ban', pass_context=True)
    @has_permissions(administrator=True, manage_roles=True, ban_members=True)
    async def _ban(self,ctx, member: discord.Member, *, reason=None):
        '''bans member if you have permission'''
        await member.ban(reason=reason)
        await ctx.channel.send(f'{member.mention} was banned')


    @_ban.error
    async def ban_error(self,ctx, error):
        if isinstance(error, MissingPermissions):
            await commands.send_message(ctx.message.channel,
                                  "Imagine not having the permision to ban")


    @commands.command(name='unban', pass_context=True)
    @has_permissions(administrator=True, manage_roles=True, ban_members=True)
    async def _unban(self,ctx, *, member):
        '''unbans member if you have permission'''
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name,
                                                  member_discriminator):
                await ctx.guild.unban(user)
                await ctx.channel.send(f'{user.mention} was unbanned')


    @_unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await commands.send_message(ctx.message.channel,
                                  "You don't have the permission to unban")@commands.command(name='unban', pass_context=True)
    
    @commands.command(name='banlist',pass_context=True)
    async def banlist(self, ctx):
      '''lists all banned users'''
      banned_users = await ctx.guild.bans()
      if len(banned_users) > 0:
        for user in range(len(banned_users)):
            num = user
            user = banned_users[user].user
            await ctx.channel.send(f'{num + 1}.\nname: ```{user.mention}```\nname: ```{banned_users[num][1].name}#{banned_users[num][1].discriminator}```\nid: ```{user.id}```')
        else:
          await ctx.channel.send(f'There are no banned users')

    # @commands.command(name='invite',pass_context = True)
    # async def invite(self, ctx,*, member):
    #   member_name, member_discriminator = member.split('#')
    #   guild = self.bot.get_channel(ctx.server.id)
      
    #   link = await guild.create_invite(max_uses = 3 )
    #   await member.send(link)
    #   await ctx.send(f'{member.name} has received an invite.')



def setup(bot):
    bot.add_cog(UserControl(bot))
