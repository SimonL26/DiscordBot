import discord
from discord.ext import commands
import random

class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.__last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online!")
        print("-----------------")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        #guild is a server in discord
        #Get channel id such that bot sends message inside the channel
        """Welcomes new members to the server"""
        print(f"{member.name} joined")
        guild = self.bot.get_guild(1059465289743470643)
        channel = discord.utils.get(member.guild.channels, id=1059465290255192146)

        if guild:
            print("Discord server exist")
        else:
            print("Discord server not found!")
        
        if channel is not None:
            await channel.send(f"Welcome {member.mention}")
        else:
            print("Channel not found in the server!")
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Says goodbye to left members"""
        print(f"{member.name} left")
        channel = discord.utils.get(member.guild.channels, id=1059465290255192146)
        if channel is not None:
            await channel.send(f"Goodbye {member.name}, we will remember you forever")
        else:
            print("Channel not found.")

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

    @commands.command()
    async def choose(self, ctx, *choices: str):
        """Choose one thing from the list provided by the channel member"""
        await ctx.send(random.choice(choices))

async def setup(bot):
    await bot.add_cog(BasicCommands(bot))

