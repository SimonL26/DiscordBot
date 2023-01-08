import discord
from discord.ext import commands
import random
import requests
import json

def parse_random_gif(query:str):
    gifurl = "https://api.giphy.com/v1/gifs/search"
    querystring = {"api_key": "kwz8Oi8yrggYBqp0C05LXtyOlcUw0kLq", "q": query, "limit": 20}
    response = requests.request("GET", gifurl, params=querystring)

    response_gifs_urls = json.loads(response.text)['data']
    random_gif_url = random.choice(response_gifs_urls)

    image_url = random_gif_url['images']['original']['url'].split("?")
    return image_url[0]

class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.__last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("Basic Commands Cog has been added")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        #guild is a server in discord
        #Get channel id such that bot sends message inside the channel
        """Welcomes new members to the server"""
        print(f"{member.name} joined")
        guild = self.bot.get_guild(1059465289743470643)
        channel = discord.utils.get(member.guild.channels, id=1059465290255192146)
        welcome_gif_url = parse_random_gif("welcome")
        embed = discord.Embed()
        embed.set_image(url=welcome_gif_url)

        if guild:
            print("Discord server exist")
        else:
            print("Discord server not found!")
        
        if channel is not None:
            await channel.send(f"Welcome {member.mention}")
            await channel.send(embed=embed)
        else:
            print("Channel not found in the server!")
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Says goodbye to left members"""
        print(f"{member.name} left")
        guild = self.bot.get_guild(1059465289743470643)
        channel = discord.utils.get(member.guild.channels, id=1059465290255192146)
        goodbye_gif_url = parse_random_gif("goodbye sad")
        embed = discord.Embed()
        embed.set_image(url = goodbye_gif_url)

        if channel is not None:
            await channel.send(f"Goodbye {member.name}, we will remember you forever")
            await channel.send(embed=embed)
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

