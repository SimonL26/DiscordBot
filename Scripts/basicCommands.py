import discord
from discord.ext import commands
import random

class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.__last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is None:
            await channel.send(f'Welcome {member.mention}.')

    @commands.command()
    async def greet(self, ctx, *, member:discord.Member = None):
        """Greets a member from the channel"""
        member = member or ctx.author
        if self.__last_member is None or self.__last_member.id != member.id:
            await ctx.send(f'Hello {member.name}!')
        else:
            await ctx.send(f'Hello {member.name}...again')
        self.__last_member = member

    @commands.command()
    async def roll(self, ctx, a:int, b:int):
        """Returns a random number in the range of (a, b)"""
        await ctx.send(str(random.randint(a, b)))

